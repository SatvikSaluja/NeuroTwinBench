"""CCG, drive-conditioned pairwise GLM, and jitter null on cached HNN data.

Each estimator runs in a fresh process and writes its result immediately.
Jitter width is frozen at twice the 25 ms coupling window, independently per
neuron and simulation segment. Drive covariates are retained for the null.
"""
import argparse
import json
import resource
import subprocess
import sys
import time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from neurotwinbench import fit as fitmod, metrics as met, simulate as simmod
from neurotwinbench.ground_truth import extract_ground_truth
from neurotwinbench.reporting import load_recording, per_class, write_json
from experiments.grid import configuration


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--from-cache', type=Path, default=Path('results/production_spikes.npz'))
    p.add_argument('--out', type=Path, default=Path('results/seed100'))
    p.add_argument('--seed', type=int, default=100)
    p.add_argument('--mesh', type=int, nargs=2, default=[5, 5])
    p.add_argument('--n-basis', type=int, default=5)
    p.add_argument('--history-ms', type=float, default=25)
    p.add_argument('--regularizer', type=float, default=1e-3)
    p.add_argument('--max-iter', type=int, default=500)
    p.add_argument('--float32', action=argparse.BooleanOptionalAction, default=True)
    p.add_argument('--estimator', choices=['ccg', 'pairwise', 'jitter'], help=argparse.SUPPRESS)
    args = p.parse_args()
    args.seeds = [args.seed]
    config = configuration(args) | {'jitter_width_history_multiple': 2, 'jitter_seed': args.seed + 1,
                                    'pairwise_drive': 'true'}
    if args.estimator is None:
        results = {}
        for estimator in ('ccg', 'pairwise', 'jitter'):
            path = args.out / 'baselines' / f'{estimator}.json'
            if path.exists() and json.loads(path.read_text())['config'] != config:
                raise ValueError(f'{path}: different configuration; use a new output directory')
            if not path.exists():
                subprocess.run([sys.executable, __file__, '--from-cache', str(args.from_cache),
                    '--out', str(args.out), '--seed', str(args.seed), '--mesh', *map(str, args.mesh),
                    '--n-basis', str(args.n_basis), '--history-ms', str(args.history_ms),
                    '--regularizer', str(args.regularizer), '--max-iter', str(args.max_iter),
                    '--float32' if args.float32 else '--no-float32', '--estimator', estimator], check=True)
            results[estimator] = json.loads(path.read_text())['result']
            write_json(args.out / 'baselines.json', {'config': config,
                       'complete': len(results) == 3, 'results': results})
        return
    data = load_recording(args.from_cache)
    spikes, drives, gids = data['spikes'], data['drives'], data['gids']
    lengths, bin_s = data['segment_lengths'], float(data['bin_s'])
    window = int(round(args.history_ms / (bin_s * 1000)))
    offsets = np.r_[0, np.cumsum(lengths)]
    gt = extract_ground_truth(simmod.build_network(simmod.SimulationConfig(mesh_shape=tuple(args.mesh))))
    kw = dict(bin_s=bin_s, history_ms=args.history_ms, n_basis=args.n_basis,
              regularizer_strength=args.regularizer, max_iter=args.max_iter,
              float32=args.float32, exogenous=drives, segment_lengths=lengths)
    t0 = time.time()
    diagnostics = None
    if args.estimator == 'ccg':
        # Accumulate lag covariances across segments before selecting the peak.
        # Do not correlate across independent trial boundaries.
        areas = np.zeros((len(gids), len(gids)))
        for lag in range(1, window + 1):
            cov = np.zeros_like(areas)
            count = 0
            for lo, hi in zip(offsets[:-1], offsets[1:]):
                x = spikes[lo:hi].astype(np.float64)
                x -= x.mean(axis=0)
                cov += x[:-lag].T @ x[lag:]
                count += len(x) - lag
            cov /= count
            areas = np.where(np.abs(cov) > np.abs(areas), cov, areas)
        active = spikes.sum(axis=0) > 0
        evaluable = active[:, None] & active[None, :]
    else:
        if args.estimator == 'pairwise':
            fitted = fitmod.fit_pairwise_glm(spikes, **kw)
        else:
            jittered = np.empty_like(spikes)
            for index, (lo, hi) in enumerate(zip(offsets[:-1], offsets[1:])):
                jittered[lo:hi] = met.jitter(spikes[lo:hi], width_bins=2 * window,
                                            seed=args.seed + 1 + index)
            fitted = fitmod.fit_population_glm(jittered, solver='LBFGS', **kw)
        areas, evaluable = fitted.areas, fitted.evaluable
        diagnostics = fitted.diagnostics
    result = {'per_class': per_class(gt, gids, areas, evaluable, args.history_ms),
              'seconds': time.time() - t0, 'diagnostics': diagnostics,
              'peak_rss_gib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20}
    path = args.out / 'baselines' / f'{args.estimator}.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(path.with_suffix('.npy'), areas)
    write_json(path, {'config': config, 'result': result})
    print(f'DONE {args.estimator}: {result["seconds"]:.0f}s, '
          f'{result["peak_rss_gib"]:.2f} GiB, {len(result["per_class"])} classes', flush=True)

if __name__ == '__main__':
    main()
