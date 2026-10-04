"""Primary 3x3 experiment; isolated fits, per-class scores, resumable cells.

Run --from-cache on production data. Every completed cell is saved before the
next starts. No pooled E/I correlation or uncalibrated latency is reported.
Baselines are produced separately by production_baselines.py.
"""
from __future__ import annotations
import argparse
import json
import resource
import subprocess
import sys
import time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from neurotwinbench import fit as fitmod, simulate as simmod
from neurotwinbench.ground_truth import extract_ground_truth
from neurotwinbench.reporting import load_recording, per_class, segment_transform, write_json

INTERNEURONS = ('L2_basket', 'L5_basket')
OBSERVATIONS = ('full', 'interneurons_hidden', 'random_subsample')
DRIVES = ('true', 'proxy', 'hidden')


def observation_masks(sim, rng):
    full = np.ones(len(sim.gids), dtype=bool)
    no_inter = sim.observed(exclude_types=INTERNEURONS)
    subsample = np.zeros_like(full)
    subsample[rng.choice(len(full), int(no_inter.sum()), replace=False)] = True
    return dict(zip(OBSERVATIONS, (full, no_inter, subsample)))


def drive_conditions(sim):
    return {'true': sim.drive_spikes,
            'proxy': fitmod.drive_proxy(sim.drive_spikes, bin_s=sim.bin_s), 'hidden': None}


def configuration(args):
    stat = args.from_cache.stat()
    return {'cache': str(args.from_cache.resolve()), 'cache_size': stat.st_size,
            'cache_mtime_ns': stat.st_mtime_ns, 'seed': args.seeds[0],
            'mesh': list(args.mesh), 'n_basis': args.n_basis,
            'history_ms': args.history_ms, 'regularizer': args.regularizer,
            'max_iter': args.max_iter, 'float32': args.float32, 'solver': getattr(args, 'solver', 'LBFGS'),
            'schema': 2}


def run_cell(args, observation, drive):
    data = load_recording(args.from_cache)
    spikes, drives, gids = data['spikes'], data['drives'], data['gids']
    bin_s, lengths = float(data['bin_s']), data['segment_lengths']
    mask = np.ones(len(gids), dtype=bool)
    keep = ~np.isin(data['cell_types'].astype(str), INTERNEURONS)
    if observation == 'interneurons_hidden':
        mask = keep
    elif observation == 'random_subsample':
        mask[:] = False
        rng = np.random.default_rng(args.seeds[0])
        mask[rng.choice(len(mask), int(keep.sum()), replace=False)] = True
    exog = drives if drive == 'true' else None
    if drive == 'proxy':
        exog = segment_transform(drives, lengths, lambda x: fitmod.drive_proxy(x, bin_s=bin_s))
    config = simmod.SimulationConfig(mesh_shape=tuple(args.mesh))
    gt = extract_ground_truth(simmod.build_network(config))
    observed = spikes[:, mask]
    t0 = time.time()
    result = fitmod.fit_population_glm(
        observed, bin_s=bin_s, n_basis=args.n_basis, history_ms=args.history_ms,
        exogenous=exog, regularizer_strength=args.regularizer,
        max_iter=args.max_iter, float32=args.float32, solver=args.solver,
        segment_lengths=lengths)
    record = {'seed': args.seeds[0], 'observation': observation, 'drive': drive,
              'n_observed': int(mask.sum()), 'gids': gids[mask].tolist(),
              'power': fitmod.power_check(observed, args.n_basis,
                       n_exog=0 if exog is None else exog.shape[1], bin_s=bin_s),
              'per_class': per_class(gt, gids[mask], result.areas, result.evaluable, args.history_ms),
              'diagnostics': result.diagnostics, 'fit_seconds': time.time() - t0,
              'peak_rss_gib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20}
    path = args.out / 'cells' / f'{observation}_{drive}.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(path.with_suffix('.npz'), filters=result.filters,
                        baseline=result.baseline, active=result.active,
                        exog_filters=np.array([]) if result.exog_filters is None else result.exog_filters)
    write_json(path, {'config': configuration(args), 'record': record})
    print(f'DONE {observation}/{drive}: {record["fit_seconds"]:.0f}s, '
          f'{record["peak_rss_gib"]:.2f} GiB; converged={result.diagnostics["converged"]}', flush=True)


def _report(records):
    names = sorted({n for r in records for n, v in r['per_class'].items() if v['rank_informative']})
    for name in names:
        print('\n' + name, flush=True)
        print(f'{"observation":24} {"true":>10} {"proxy":>10} {"hidden":>10}')
        for obs in OBSERVATIONS:
            values = []
            for drive in DRIVES:
                vals = [r['per_class'][name]['weight_spearman'] for r in records
                        if r['observation'] == obs and r['drive'] == drive and name in r['per_class']]
                vals = [v for v in vals if v is not None]
                values.append(f'{np.mean(vals):+.3f}' if vals else '--')
            print(f'{obs:24} ' + ' '.join(f'{v:>10}' for v in values), flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--from-cache', type=Path)
    p.add_argument('--seeds', type=int, nargs='+', default=[100])
    p.add_argument('--mesh', type=int, nargs=2, default=[5, 5])
    p.add_argument('--tstop', type=float, default=300000)
    p.add_argument('--n-procs', type=int, default=4)
    p.add_argument('--n-basis', type=int, default=5)
    p.add_argument('--history-ms', type=float, default=25)
    p.add_argument('--regularizer', type=float, default=1e-3)
    p.add_argument('--max-iter', type=int, default=500)
    p.add_argument('--float32', action=argparse.BooleanOptionalAction, default=True)
    p.add_argument('--out', type=Path, default=Path('results/seed100'))
    p.add_argument('--solver', choices=['LBFGS','DISK_LBFGS'], default='LBFGS')
    p.add_argument('--cell', nargs=2, metavar=('OBSERVATION', 'DRIVE'), help=argparse.SUPPRESS)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.from_cache is None:
        if len(args.seeds) != 1:
            p.error('run one seed per invocation, with a separate output directory')
        config = simmod.SimulationConfig(mesh_shape=tuple(args.mesh), tstop_ms=args.tstop,
                                         event_seed=args.seeds[0])
        sim = simmod.run(config, n_procs=args.n_procs)
        args.from_cache = args.out / 'grid_spikes.npz'
        np.savez_compressed(args.from_cache, spikes=sim.spikes, drives=sim.drive_spikes,
                            gids=sim.gids, cell_types=sim.cell_types, bin_s=sim.bin_s,
                            segment_lengths=[len(sim.spikes)])
    if len(args.seeds) != 1:
        p.error('a cache represents one base seed; give exactly one --seeds value')
    if args.cell:
        if args.cell[0] not in OBSERVATIONS or args.cell[1] not in DRIVES:
            p.error('invalid cell')
        run_cell(args, *args.cell)
        return
    config = configuration(args)
    records = []
    for obs in OBSERVATIONS:
        for drive in DRIVES:
            path = args.out / 'cells' / f'{obs}_{drive}.json'
            if path.exists() and json.loads(path.read_text())['config'] != config:
                raise ValueError(f'{path}: different configuration; choose a new output directory')
            if not path.exists():
                command = [sys.executable, __file__, '--from-cache', str(args.from_cache),
                           '--seeds', str(args.seeds[0]), '--mesh', *map(str, args.mesh),
                           '--n-basis', str(args.n_basis), '--history-ms', str(args.history_ms),
                           '--regularizer', str(args.regularizer), '--max-iter', str(args.max_iter),
                           '--float32' if args.float32 else '--no-float32', '--out', str(args.out),
                           '--solver', args.solver, '--cell', obs, drive]
                subprocess.run(command, check=True)
            records.append(json.loads(path.read_text())['record'])
            write_json(args.out / 'grid.json', {'config': config, 'complete': len(records) == 9,
                                              'records': records})
    _report(records)
    print(f'DONE wrote {args.out / "grid.json"}', flush=True)

if __name__ == '__main__':
    main()
