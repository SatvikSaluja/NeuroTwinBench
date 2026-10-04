"""PROJECT.md section 18: can real edges be ranked above non-edges?

Only answerable in a sparse network. The default model connects nearly every
eligible pair, so there are no designed non-edges and "edge detection" is not a
detection task at all -- `edge_detection` returns nan there rather than a
flattering number computed against an empty negative class.

Thinning also switches on the second uncertainty axis of section 20: with
`probability < 1` the `conn_seed` finally does something, so circuit
realisations become a source of variation distinct from drive events. This
script varies both, and reports them separately because pooling them would
present anatomical variability and trial variability as one error bar.

    python experiments/topology.py --probability 0.3 --conn-seeds 3 4 --n-procs 4
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import replace
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from neurotwinbench import fit as fitmod
from neurotwinbench import metrics as met
from neurotwinbench import simulate as simmod
from neurotwinbench.ground_truth import extract_ground_truth
from neurotwinbench.reporting import load_recording, write_json
from types import SimpleNamespace

#: Thin only the excitatory recurrent projections. Inhibitory classes have
#: almost no weight spread (section F) and thinning them would remove the
#: inhibition that keeps the network firing at all (section 3's drive sweep).
THINNED = ("L2_pyramidal->L2_pyramidal", "L5_pyramidal->L5_pyramidal")


def candidate_mask(gt, gids: np.ndarray, thinned: tuple[str, ...]) -> np.ndarray:
    """Pairs some thinned class could have produced, connected or not.

    Without this the negative class is dominated by pairs the model never
    proposed -- L5->L2, cross-type combinations that no connection spec covers --
    and the estimator would be credited for rejecting connections that were
    never on the table.
    """
    index = {int(g): i for i, g in enumerate(gids)}
    types = np.empty(len(gids), dtype=object)
    types[:] = ""
    # Resolve from BOTH source and target rows. Using source rows alone leaves a
    # target-only cell typed "", dropping its columns from the candidate set and
    # silently shrinking the negative class -- which would inflate every
    # detection score. No cell is target-only in the default model, so this is
    # latent there, but purpose-built networks can and do have them.
    for gid_array, type_array in ((gt.src_gid, gt.src_type),
                                  (gt.target_gid, gt.target_type)):
        for gid, cell_type in zip(gid_array, type_array):
            i = index.get(int(gid))
            if i is not None and not types[i]:
                types[i] = cell_type
    if any(t == "" for t in types):
        raise ValueError(
            f"{sum(1 for t in types if not t)} observed cells appear in no "
            f"connection; their type cannot be resolved and the candidate mask "
            f"would be wrong"
        )

    mask = np.zeros((len(gids), len(gids)), dtype=bool)
    for spec in thinned:
        src_type, target_type = spec.split("->")
        rows = np.array([t == src_type for t in types])
        cols = np.array([t == target_type for t in types])
        mask |= rows[:, None] & cols[None, :]
    np.fill_diagonal(mask, False)
    return mask


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tstop", type=float, default=300000.0, help="ms")
    p.add_argument("--mesh", nargs=2, type=int, default=(5, 5))
    p.add_argument("--probability", type=float, default=0.3)
    p.add_argument("--conn-seeds", nargs="+", type=int, default=[3, 4],
                   help="circuit realisations (section 20)")
    p.add_argument("--event-seeds", nargs="+", type=int, default=[2],
                   help="drive-event realisations on each circuit")
    p.add_argument("--history-ms", type=float, default=25.0)
    p.add_argument("--n-basis", type=int, default=5)
    p.add_argument("--n-procs", type=int, default=4)
    p.add_argument("--regularizer", type=float, default=1e-3)
    p.add_argument("--max-iter", type=int, default=500)
    p.add_argument("--out", type=Path, default=Path("results"))
    p.add_argument("--float32", action=argparse.BooleanOptionalAction, default=True)
    p.add_argument("--solver", choices=["LBFGS", "DISK_LBFGS"], default="LBFGS")
    p.add_argument("--jitter-seed", type=int)
    p.add_argument("--from-cache", type=Path)
    args = p.parse_args()

    records = []
    for conn_seed in args.conn_seeds:
        for event_seed in args.event_seeds:
            config = simmod.SimulationConfig(
                mesh_shape=tuple(args.mesh), tstop_ms=args.tstop,
                event_seed=event_seed, conn_seed=conn_seed,
                connection_probability={s: args.probability for s in THINNED},
            )
            print(f"\n=== circuit {conn_seed}, events {event_seed} ===", flush=True)
            t0 = time.time()
            if args.from_cache:
                data = load_recording(args.from_cache)
                stored = simmod.SimulationConfig(**json.loads(str(data['simulation_config'])))
                if tuple(stored.mesh_shape) != tuple(config.mesh_shape) or stored.network != config.network or stored.conn_seed != config.conn_seed or stored.connection_probability != config.connection_probability:
                    raise ValueError("cache anatomy differs from requested experiment")
                if int(data['base_seed']) != config.event_seed:
                    raise ValueError("cache event seed differs from requested experiment")
                sim = SimpleNamespace(spikes=data['spikes'], drive_spikes=data['drives'],
                    gids=data['gids'], bin_s=float(data['bin_s']),
                    rates_hz=data['spikes'].mean(axis=0) / float(data['bin_s']))
                lengths = data['segment_lengths']
            else:
                sim = simmod.run(config, n_procs=args.n_procs)
                lengths = None
            rates = sim.rates_hz
            power = fitmod.power_check(sim.spikes, args.n_basis, n_exog=1,
                                       bin_s=sim.bin_s)
            ratio = power["spikes_per_predictor"]
            print(f"simulated in {time.time()-t0:.0f}s | {sim.spikes.sum()} spikes | "
                  f"{rates.mean():.1f} Hz | {int((rates==0).sum())}/{len(rates)} silent "
                  f"| {ratio:.1f} spikes/predictor", flush=True)
            if ratio < 16:
                print(f"  WARNING: {ratio:.1f} spikes/predictor vs 16.1 for the "
                      f"synthetic run that reached rho +0.80", flush=True)

            gt = extract_ground_truth(simmod.build_network(config))
            _, _, connected = gt.to_matrices(sim.gids)
            # Eligibility must not depend on whether thinning retained an edge.
            # Resolve hypothetical delays from the unthinned circuit so distant
            # negatives and positives are excluded by the identical rule.
            potential = extract_ground_truth(simmod.build_network(
                replace(config, connection_probability={})))
            _, potential_delays, potential_edges = potential.to_matrices(sim.gids)
            candidates = candidate_mask(potential, sim.gids, THINNED)
            in_window = potential_edges & np.isfinite(potential_delays) & (potential_delays <= args.history_ms)

            fit_spikes = sim.spikes
            if args.jitter_seed is not None:
                if lengths is None: lengths = [len(sim.spikes)]
                fit_spikes = np.empty_like(sim.spikes)
                boundaries = np.r_[0, np.cumsum(lengths)]
                for index,(lo,hi) in enumerate(zip(boundaries[:-1],boundaries[1:])):
                    fit_spikes[lo:hi] = met.jitter(sim.spikes[lo:hi],
                        width_bins=2*int(round(args.history_ms/(sim.bin_s*1000))),
                        seed=args.jitter_seed+index)
            result = fitmod.fit_population_glm(
                fit_spikes, bin_s=sim.bin_s, history_ms=args.history_ms,
                n_basis=args.n_basis, exogenous=sim.drive_spikes,
                regularizer_strength=args.regularizer, max_iter=args.max_iter,
                float32=args.float32, solver=args.solver, segment_lengths=lengths,
            )
            scored = candidates & result.evaluable & in_window
            detection = met.edge_detection(connected, result.areas, candidate=scored)
            per_projection = {name: met.edge_detection(connected, result.areas,
                candidate=scored & candidate_mask(potential, sim.gids, (name,))) for name in THINNED}
            distance_control = met.edge_detection(connected, 1.0 / np.maximum(potential_delays,1e-12), candidate=scored)
            strata = {}
            for name in THINNED:
                mask = scored & candidate_mask(potential, sim.gids, (name,))
                edges = np.unique(np.quantile(potential_delays[mask], np.linspace(0,1,6)))
                bins = []
                for i,(lo,hi) in enumerate(zip(edges[:-1],edges[1:])):
                    same_distance_range = mask & (potential_delays>=lo) & ((potential_delays<=hi) if i==len(edges)-2 else (potential_delays<hi))
                    bins.append({'delay_range_ms':[float(lo),float(hi)], **met.edge_detection(connected,result.areas,candidate=same_distance_range)})
                strata[name] = bins
            args.out.mkdir(parents=True,exist_ok=True)
            np.savez_compressed(args.out / f'filters_c{conn_seed}_e{event_seed}.npz',
                filters=result.filters, baseline=result.baseline, gids=sim.gids,
                connected=connected, eligible=scored, potential_delays=potential_delays)
            records.append({"conn_seed": conn_seed, "event_seed": event_seed,
                            "jitter_seed": args.jitter_seed,
                            "distance_only_control": distance_control,
                            "delay_distance_strata": strata,
                            "spikes_per_predictor": ratio, "diagnostics": result.diagnostics,
                            "per_projection": per_projection,
                            "eligibility": "unthinned counterfactual delays; identical rule for edges and non-edges",
                            "interpretation": "Exploratory detection; distance-matched and jitter controls still required for a synaptic-recovery claim.",
                            **detection})
            print(f"  ROC-AUC {detection['roc_auc']:.3f} | PR-AUC "
                  f"{detection['pr_auc']:.3f} (chance = prevalence "
                  f"{detection['prevalence']:.3f}) | {detection['n_edges']} edges, "
                  f"{detection['n_non_edges']} non-edges", flush=True)

    if args.from_cache:
        args.tstop = len(sim.spikes) * sim.bin_s * 1000
    _report(records)
    args.out.mkdir(parents=True, exist_ok=True)
    out = args.out / f"topology_p{args.probability:g}_t{args.tstop:g}.json"
    write_json(out,
        {"config": vars(args) | {"out": str(args.out), "mesh": list(args.mesh), "from_cache": str(args.from_cache)},
         "thinned": list(THINNED), "records": records})
    print(f"\nwrote {out}")


def _report(records: list[dict]) -> None:
    if not records:
        return
    roc = [r["roc_auc"] for r in records if not np.isnan(r["roc_auc"])]
    if not roc:
        print("\nNo scoreable records: the network was not sparse enough.")
        return

    print("\n" + "=" * 62)
    spread = f"± {np.std(roc, ddof=1):.3f}" if len(roc) > 1 else "(one realization; SD unavailable)"
    print(f"ROC-AUC  {np.mean(roc):.3f} {spread}   (chance 0.5)")
    prevalence = np.mean([r["prevalence"] for r in records])
    pr = [r["pr_auc"] for r in records if not np.isnan(r["pr_auc"])]
    spread = f"± {np.std(pr, ddof=1):.3f}" if len(pr) > 1 else "(one realization; SD unavailable)"
    print(f"PR-AUC   {np.mean(pr):.3f} {spread}   "
          f"(chance = prevalence {prevalence:.3f})")

    # Variance decomposition only means something with several circuits.
    circuits = {r["conn_seed"] for r in records}
    if len(circuits) > 1:
        between = np.std([np.mean([r["roc_auc"] for r in records
                                   if r["conn_seed"] == c]) for c in circuits])
        print(f"\nbetween-circuit sd {between:.3f} -- anatomical variability, "
              f"distinct from drive variability (section 20)")


if __name__ == "__main__":
    main()
