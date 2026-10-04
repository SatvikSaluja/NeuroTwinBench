"""Regenerate the handoff findings from complete, per-class checkpoints."""
import json
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from neurotwinbench.reporting import write_json
from experiments.grid import DRIVES, OBSERVATIONS
ROOT = Path(__file__).resolve().parents[1]


def summarize(records):
    output = {}
    for observation in OBSERVATIONS:
        for drive in DRIVES:
            selected = [r for r in records if r['observation'] == observation and r['drive'] == drive]
            names = sorted({name for r in selected for name in r['per_class']})
            cell = {}
            for name in names:
                values = {}
                for metric in ('weight_spearman', 'sign_accuracy'):
                    by_seed = {r['seed']: r['per_class'][name][metric] for r in selected if name in r['per_class']}
                    vals = [v for v in by_seed.values() if v is not None and np.isfinite(v)]
                    values[metric] = {'n_seeds': len(vals),
                        'mean': float(np.mean(vals)) if vals else None,
                        'sd': float(np.std(vals, ddof=1)) if len(vals) > 1 else None}
                cell[name] = values
            output[f'{observation}/{drive}'] = cell
    return output


def main():
    grids = []
    for seed in (100, 200, 300):
        path = ROOT / f'results/seed{seed}/grid.json'
        if path.exists():
            payload = json.loads(path.read_text())
            if payload.get('complete'):
                grids.append(payload)
    records = [r for g in grids for r in g['records']]
    summary = summarize(records)
    write_json(ROOT / 'results/grid_summary.json', {'n_seeds': len(grids), 'summary': summary})
    lines = ['## Primary grid — first result', '',
        'Generated from durable per-class checkpoints; no pooled E/I correlations.', '',
        f'Completed grids: **{len(grids)} independent base-seed recordings** (100, 200, 300 as available).',
        'Across-seed SD is unavailable for a single seed, rather than reported as zero.', '',
        'The old grid stopped after one console-only pooled result and wrote no JSON; that number is not used.',
        'New fits use LBFGS/float32, five basis functions, ridge 1e-3, and exclude history across independent chunks.',
        'The 16.1 synthetic spikes/predictor observation is a budget reference, not a sufficiency threshold for HNN.', '',
        'Each receptor/location class is retained. Shared pairs have one total inferred influence, so these are not independent receptor/location recoveries.',
        'Autapses are excluded; inhibitory weight ranks are unavailable because their spread is degenerate (§2F).',
        'Production baselines cover the full-population/true-drive condition. Other grid cells are exploratory contrasts until matched controls are available.', '']
    names = sorted({n for r in records for n, v in r['per_class'].items() if v['rank_informative']})
    for name in names:
        lines += [f'**{name}**', '', '| Observed population | True drive | Proxy | Hidden |',
                  '|---|---:|---:|---:|']
        for obs in OBSERVATIONS:
            cells = []
            for drive in DRIVES:
                stats = summary[f'{obs}/{drive}'].get(name, {}).get('weight_spearman', {})
                mean, sd = stats.get('mean'), stats.get('sd')
                cells.append('--' if mean is None else f'{mean:+.3f}' + (f' ± {sd:.3f}' if sd is not None else ' (one seed)'))
            lines.append(f'| {obs} | ' + ' | '.join(cells) + ' |')
        lines.append('')
    if records:
        tested = monotone = 0
        differences = []
        for name in names:
            for obs in OBSERVATIONS:
                vals = [summary[f'{obs}/{d}'].get(name, {}).get('weight_spearman', {}).get('mean') for d in DRIVES]
                if all(v is not None for v in vals):
                    tested += 1; monotone += vals[0] >= vals[1] >= vals[2]
            for d in DRIVES:
                a = summary[f'interneurons_hidden/{d}'].get(name, {}).get('weight_spearman', {}).get('mean')
                b = summary[f'random_subsample/{d}'].get(name, {}).get('weight_spearman', {}).get('mean')
                if a is not None and b is not None:
                    differences.append((name, d, a-b))
        lines += [f'True→proxy→hidden recovery decreases monotonically in {monotone}/{tested} scoreable class/population combinations.',
                  'This is descriptive; class overlap and seed count preclude a significance claim.', '']
        if differences:
            lo, hi = min(v for _, _, v in differences), max(v for _, _, v in differences)
            lines += [f'Interneuron-hidden minus random-subsample recovery ranges from {lo:+.3f} to {hi:+.3f} across common scoreable classes/drive conditions.',
                      'These masks retain different pairs; this contrast also changes the evaluation set.', '']
        unconverged = sum(not r.get('diagnostics', {}).get('converged', False) for r in records)
        lines += [f'Fits not satisfying the recorded solver stopping criterion: {unconverged}/{len(records)}. '
                  'Their scores are provisional, not validated scientific findings.', '']
    else:
        lines += ['**Grid results pending. No degradation or dropout conclusion is available.**', '']
    for seed in (100, 200, 300):
        path = ROOT / f'results/seed{seed}/baselines.json'
        if not path.exists():
            continue
        baseline = json.loads(path.read_text())
        lines += [f'**Seed {seed} baselines** (complete={baseline.get("complete", False)})', '',
                  '| Connection class | Population | Pairwise + drive | CCG | Jitter + drive |', '|---|---:|---:|---:|---:|']
        population = next((r['per_class'] for r in records if r['seed'] == seed and r['observation'] == 'full' and r['drive'] == 'true'), {})
        all_names = sorted(set(population).union(*(set(v['per_class']) for v in baseline['results'].values())))
        for name in all_names:
            metrics = [population.get(name, {})] + [baseline['results'].get(e, {}).get('per_class', {}).get(name, {}) for e in ('pairwise', 'ccg', 'jitter')]
            vals = [m.get('weight_spearman') for m in metrics]
            if not any(v is not None for v in vals):
                continue
            lines.append('| ' + name + ' | ' + ' | '.join('--' if v is None else f'{v:+.3f}' for v in vals) + ' |')
        lines += ['', 'No advantage for joint estimation is assumed; compare each population score directly with its pairwise and null scores.', '']
    latency_paths = sorted((ROOT / 'results/latency').glob('latency_calibration_*.json'))
    lines += ['**Latency calibration (§6)**', '']
    if latency_paths:
        latency = json.loads(latency_paths[-1].read_text())
        gap = latency['smallest_resolved_separation_ms']
        lines += [f'Smallest resolved adjacent separation: {gap} ms.' if gap is not None else 'No adjacent lag separation was resolved.',
                  'This is a one-seed, across-edge dispersion criterion on basis-aligned lags, not a universal timing resolution.', '']
    else:
        lines += ['Pending. No HNN latency claim is licensed.', '']
    text = '\n'.join(lines) + '\n'
    (ROOT / 'results/handoff_report.md').write_text(text)
    project = ROOT / 'PROJECT.md'
    start, end = '<!-- handoff-results:start -->', '<!-- handoff-results:end -->'
    old = project.read_text()
    section = start + '\n\n' + text + '\n' + end
    if start in old:
        old = old[:old.index(start)] + section + old[old.index(end) + len(end):]
    else:
        old += '\n---\n\n' + section + '\n'
    project.write_text(old)
    print(f'wrote report: {len(grids)} completed seed grids', flush=True)

if __name__ == '__main__':
    main()
