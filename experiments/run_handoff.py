"""Sequential, restartable handoff runner. Launch detached with setsid.

Exactly one subprocess group is active at a time. Every step has its own log;
status.json is refreshed every 30 seconds and always ends DONE or FAILED.
Completed experiment checkpoints are reused by their owning scripts.
"""
import argparse
import fcntl
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import psutil
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from neurotwinbench.reporting import write_json, load_recording
from neurotwinbench import fit, simulate

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'results/handoff'


def run_step(name, arguments, min_available_gib=3):
    command = [sys.executable, *arguments]
    print(f'START {name}: {" ".join(command)}', flush=True)
    started = time.time()
    with (RUN / f'{name}.log').open('a', buffering=1) as log:
        log.write(f'\nSTART {time.ctime()} {command!r}\n')
        child = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                 stdin=subprocess.DEVNULL, start_new_session=True)
        try:
            while child.poll() is None:
                available = psutil.virtual_memory().available / 2**30
                processes = [psutil.Process(child.pid)]
                try:
                    processes += processes[0].children(recursive=True)
                    rss = sum(p.memory_info().rss for p in processes if p.is_running()) / 2**30
                except psutil.Error:
                    rss = None
                write_json(RUN / 'status.json', {'status': 'RUNNING', 'step': name,
                    'runner_pid': os.getpid(), 'child_pid': child.pid, 'updated_unix': time.time(),
                    'elapsed_s': time.time() - started, 'rss_gib': rss, 'available_gib': available,
                    'log': str(RUN / f'{name}.log')})
                if available < min_available_gib:
                    raise RuntimeError(f'memory guard: only {available:.2f} GiB available')
                try:
                    child.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    pass
            if child.returncode:
                raise RuntimeError(f'{name} exited {child.returncode}; see {RUN / (name + ".log")}')
        except BaseException:
            if child.poll() is None:
                # Terminate only this runner's job and descendants, never by name.
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    child.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
            raise
    print(f'DONE {name}: {time.time()-started:.0f}s', flush=True)


def report():
    run_step('report', ['experiments/report_handoff.py'])
    run_step('figures', ['figures/make_figures.py'])


def production(seed, out, extra=(), chunks=8):
    path = Path(out) / 'production_spikes.npz'
    if path.exists():
        data = load_recording(path)
        if int(data.get('base_seed', seed)) != seed or len(data['spikes']) != chunks * 320000:
            raise ValueError(f'{path}: existing cache does not match requested seed/duration')
        print(f'REUSE {path}', flush=True)
        return path
    simulate._require_no_concurrent_nrniv()
    run_step(f'simulate_{Path(out).name}', ['experiments/production.py', '--chunks', str(chunks),
        '--chunk-s', '320', '--base-seed', str(seed), '--n-basis', '5', '--simulate-only',
        '--out', str(out), *extra])
    return path


def grid_and_baselines(seed, cache):
    out = f'results/seed{seed}'
    run_step(f'grid_seed{seed}', ['experiments/grid.py', '--from-cache', str(cache),
        '--seeds', str(seed), '--n-basis', '5', '--regularizer', '0.001',
        '--max-iter', '500', '--float32', '--out', out])
    report()
    run_step(f'baselines_seed{seed}', ['experiments/production_baselines.py',
        '--from-cache', str(cache), '--seed', str(seed), '--out', out])
    report()


def variant(kind, conn_seed=3):
    name = kind if kind == 'location' else f'topology_c{conn_seed}'
    out = Path('results') / name
    pilot = out / 'pilot.json'
    if not pilot.exists():
        simulate._require_no_concurrent_nrniv()
        run_step(f'pilot_{name}', ['experiments/run_handoff.py', '--pilot', kind,
                                 '--conn-seed', str(conn_seed)])
    record = json.loads(pilot.read_text())
    chunks = record['planned_chunks']
    extra = ['--network', 'location'] if kind == 'location' else ['--probability', '.3', '--conn-seed', str(conn_seed)]
    cache = production(2, out, extra, chunks=chunks)
    if kind == 'location':
        command = ['experiments/location.py', '--seeds', '2']
    else:
        command = ['experiments/topology.py', '--probability', '.3', '--conn-seeds', str(conn_seed), '--event-seeds', '2']
    fit_out = out / 'disk_fit'
    run_step(f'fit_{name}', [*command, '--from-cache', str(cache), '--out', str(fit_out),
                            '--no-float32', '--solver', 'DISK_LBFGS', '--n-basis', '5', '--max-iter', '1500'])


def pilot(kind, conn_seed):
    import resource
    config = simulate.SimulationConfig(tstop_ms=20000, event_seed=2, conn_seed=conn_seed,
        network='location' if kind == 'location' else 'default',
        connection_probability={} if kind == 'location' else {
            'L2_pyramidal->L2_pyramidal': .3, 'L5_pyramidal->L5_pyramidal': .3})
    started = time.time()
    sim = simulate.run(config, n_procs=4)
    power = fit.power_check(sim.spikes, 5, n_exog=sim.drive_spikes.shape[1], bin_s=sim.bin_s)
    if power['spikes_per_predictor'] <= 0:
        raise RuntimeError('pilot has no spike information')
    # Reference budget plus 25% margin. This is not a guarantee of HNN power.
    planned_seconds = 20 * 16.1 / power['spikes_per_predictor'] * 1.25
    chunks = max(1, math.ceil(planned_seconds / 320))
    fitted = fit.fit_population_glm(sim.spikes, exogenous=sim.drive_spikes,
        n_basis=5, float32=True, solver='LBFGS', regularizer_strength=.001, max_iter=500)
    name = kind if kind == 'location' else f'topology_c{conn_seed}'
    write_json(Path('results') / name / 'pilot.json', {'config': config.__dict__,
        'power': power, 'planned_chunks': chunks, 'planned_seconds': chunks * 320,
        'seconds': time.time()-started, 'diagnostics': fitted.diagnostics,
        'peak_rss_gib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20,
        'note': 'duration extrapolated from a measured 20s pilot; 16.1 is a synthetic reference, not HNN sufficiency'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--pilot', choices=['location', 'topology'])
    parser.add_argument('--conn-seed', type=int, default=3)
    scope.add_argument('--primary-only', action='store_true')
    scope.add_argument('--location-only', action='store_true',
                       help='resume only the location simulation and fit, then report and stop')
    scope.add_argument('--variants-only', action='store_true',
                       help='resume location and topology circuits 3 and 4 without primary analyses')
    scope.add_argument('--topology-only', action='store_true',
                       help='resume only topology circuits 3 and 4, then reports')
    args = parser.parse_args()
    os.chdir(ROOT)
    if args.pilot:
        pilot(args.pilot, args.conn_seed)
        return
    RUN.mkdir(parents=True, exist_ok=True)
    lock = (RUN / 'runner.lock').open('w')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit('another handoff runner is active')
    def terminate(signum, frame):
        raise RuntimeError(f'runner received signal {signum}')
    signal.signal(signal.SIGTERM, terminate)
    try:
        if args.location_only or args.variants_only or args.topology_only:
            if not args.topology_only:
                variant('location')
            if args.variants_only or args.topology_only:
                variant('topology', 3)
                variant('topology', 4)
            report()
            write_json(RUN / 'status.json', {'status': 'DONE', 'updated_unix': time.time(),
                        'scope': 'topology only; completed location and primary analyses retained' if args.topology_only
                                 else 'location and topology; primary analyses reused' if args.variants_only
                                 else 'location only; primary analyses reused; topology not scheduled'})
            print('DONE requested variant simulations, fits and reports', flush=True)
            return
        # Complete the saved-data analysis before spending on new simulations.
        grid_and_baselines(100, 'results/production_spikes.npz')
        latency = Path('results/latency/latency_calibration_n20_t300.json')
        if not latency.exists():
            run_step('latency', ['experiments/latency_calibration.py', '--duration', '300',
                '--n-basis', '5', '--float32', '--out', 'results/latency'])
        report()
        for seed in (200, 300):
            cache = production(seed, f'results/seed{seed}')
            grid_and_baselines(seed, cache)
        if not args.primary_only:
            variant('location')
            variant('topology', 3)
            variant('topology', 4)
        report()
        write_json(RUN / 'status.json', {'status': 'DONE', 'updated_unix': time.time(),
                    'scope': 'research computations; upstream PRs remain separate'})
        print('DONE all queued research computations', flush=True)
    except BaseException as exc:
        previous = json.loads((RUN / 'status.json').read_text()) if (RUN / 'status.json').exists() else {}
        write_json(RUN / 'status.json', previous | {'status': 'FAILED', 'error': str(exc),
                                                   'updated_unix': time.time()})
        print(f'FAILED {exc}', flush=True)
        raise

if __name__ == '__main__':
    main()
