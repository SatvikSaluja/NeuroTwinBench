"""The production HNN run: enough spikes per predictor to be interpretable.

PROJECT.md section 5 established the target. At 70 neurons with 8 basis
functions there are 568 predictors, and HNN fires at ~3.8 Hz, so reaching the
16.1 spikes per predictor that gave rho +0.80 on synthetic data needs roughly
2500 simulated seconds. A 300 s run gives 2.0 -- eight times too few, and
indistinguishable from model mismatch, which is the one confound this project
exists to rule out.

Run in CHUNKS, each cached separately by `simulate.run`'s content hash. A single
2500 s call would lose everything if it died at hour six, and long HNN runs do
die: hnn-core kills nrniv machine-wide on backend exit, and background jobs are
killed when their parent session tears down. Chunks make that recoverable --
rerun and completed chunks are served from cache.

Chunks are independent drive-event realisations on fixed anatomy, which is the
event_seed axis of section 20, and they are concatenated for fitting. The only
cost is `window` bins of lost history per chunk boundary, negligible against
hundreds of thousands of bins.

    setsid python experiments/production.py --chunks 8 --chunk-s 320 &
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from neurotwinbench import fit as fitmod
from neurotwinbench import metrics as met
from neurotwinbench import simulate as simmod
from neurotwinbench.ground_truth import extract_ground_truth
from neurotwinbench.reporting import per_class, write_json


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--chunks", type=int, default=8)
    p.add_argument("--chunk-s", type=float, default=320.0, help="simulated s per chunk")
    p.add_argument("--mesh", nargs=2, type=int, default=(5, 5))
    p.add_argument("--n-procs", type=int, default=4)
    p.add_argument("--history-ms", type=float, default=25.0)
    p.add_argument("--n-basis", type=int, default=5)
    p.add_argument("--regularizer", type=float, default=1e-3)
    p.add_argument("--max-iter", type=int, default=500)
    p.add_argument("--float32", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--base-seed", type=int, default=100)
    p.add_argument("--network", choices=["default", "location"], default="default")
    p.add_argument("--probability", type=float, default=1.0)
    p.add_argument("--conn-seed", type=int, default=3)
    p.add_argument("--simulate-only", action="store_true",
                   help="stop after simulation; the fit can be run separately "
                        "against the cache if it needs different memory settings")
    p.add_argument("--out", type=Path, default=Path("results"))
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if args.chunks < 1 or args.chunk_s <= 0:
        p.error("chunks and chunk-s must be positive")

    total_s = args.chunks * args.chunk_s
    print(f"target: {args.chunks} x {args.chunk_s:g}s = {total_s:g}s simulated", flush=True)

    spikes, drives, gids, cell_types = [], [], None, None
    started = time.time()
    for i in range(args.chunks):
        config = simmod.SimulationConfig(
            mesh_shape=tuple(args.mesh), tstop_ms=args.chunk_s * 1000.0,
            event_seed=args.base_seed + i,
            network=args.network, conn_seed=args.conn_seed,
            connection_probability={} if args.probability == 1.0 else {
                "L2_pyramidal->L2_pyramidal": args.probability,
                "L5_pyramidal->L5_pyramidal": args.probability},
        )
        t0 = time.time()
        sim = simmod.run(config, n_procs=args.n_procs)
        spikes.append(sim.spikes)
        drives.append(sim.drive_spikes)
        gids, cell_types, bin_s = sim.gids, sim.cell_types, sim.bin_s
        done = (i + 1) * args.chunk_s
        rate = (time.time() - started) / max(done, 1e-9)
        print(f"  chunk {i+1}/{args.chunks}: {time.time()-t0:.0f}s wall | "
              f"{sim.spikes.sum()} spikes | {sim.rates_hz.mean():.1f} Hz | "
              f"ETA {(total_s - done) * rate / 60:.0f} min", flush=True)

    segment_lengths = np.array([len(s) for s in spikes])
    spikes = np.concatenate(spikes)
    drives = np.concatenate(drives)
    power = fitmod.power_check(spikes, args.n_basis, n_exog=drives.shape[1])
    print(f"\nPOWER: {power['spikes_per_predictor']:.1f} spikes/predictor "
          f"({power['n_predictors']} predictors, {power['spikes_per_neuron']:.0f} "
          f"spikes/neuron, {power['mean_rate_hz']:.1f} Hz)", flush=True)
    print("       synthetic reached rho +0.80 at 16.1, +0.89 at 32.1", flush=True)
    if power["spikes_per_predictor"] < 16:
        print("       below the synthetic reference budget; HNN sufficiency is not established", flush=True)

    temporary = args.out / "production_spikes.tmp.npz"
    np.savez_compressed(
        temporary, spikes=spikes, drives=drives,
        gids=gids, cell_types=cell_types, bin_s=bin_s,
        segment_lengths=segment_lengths, base_seed=args.base_seed,
        simulation_config=json.dumps(sim.config.__dict__),
    )
    temporary.replace(args.out / "production_spikes.npz")
    print(f"cached concatenated spikes -> {args.out}/production_spikes.npz", flush=True)
    if args.simulate_only:
        return

    print("\nfitting (true drive, condition A) ...", flush=True)
    t0 = time.time()
    result = fitmod.fit_population_glm(
        spikes, bin_s=bin_s, history_ms=args.history_ms, n_basis=args.n_basis,
        exogenous=drives, regularizer_strength=args.regularizer,
        max_iter=args.max_iter, float32=args.float32, solver="LBFGS",
        segment_lengths=segment_lengths,
    )
    print(f"  fit in {time.time()-t0:.0f}s", flush=True)

    gt = extract_ground_truth(simmod.build_network(sim.config))
    rows = per_class(gt, gids, result.areas, result.evaluable, args.history_ms)
    out = args.out / f"production_{total_s:g}s.json"
    write_json(out, {"config": vars(args), "power": power, "per_class": rows,
                     "diagnostics": result.diagnostics})
    print(f"DONE wrote {out}", flush=True)


if __name__ == "__main__":
    main()
