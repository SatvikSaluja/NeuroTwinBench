# NeuroTwinBench: experiment and command guide

Run from this repository root. Commands are explicit and are NOT an instruction to rerun completed work. Read [RESULTS_REPORT.md](RESULTS_REPORT.md) first. Repository: https://github.com/SatvikSaluja/hnn_neuro_bridge

## Environment and operational rules

The validated local interpreter is `/home/satvik/miniconda3/envs/neurotwin/bin/python` (Python 3.11). Locally:

```bash
conda activate neurotwin
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -m pip install -e '.[hnn]'
command -v nrniv
python -c 'from mpi4py import MPI; import hnn_core, nemos; print(hnn_core.__version__, nemos.__version__)'
```

On another machine install NEURON with MPI support and mpi4py linked to the same MPI implementation. Package lower bounds are not an exact environment lock; use the version records accompanying old results for historical reproduction. HNN 0.6.1 / NEURON 8.2.7 were the measured original environment.

Never run two HNN MPI simulations concurrently. Keep the machine powered and awake. `tmux` survives terminal closure, not shutdown. Before launching, inspect host processes (`pgrep -af 'phase2_studies|nrniv'`) and `df -h .`. Large GLM feature caches use substantial disk space. A stale status file alone is not proof of progress.

## Main completed and active topology studies

Executable: [experiments/phase2_studies.py](experiments/phase2_studies.py).

| Circuit | Wiring seed | First event seed | Chunks × seconds | Output directory | State at report snapshot |
|---|---:|---:|---|---|---|
| C11 | 11 | 1000000 | 8 × 320 | results/phase2/topology_c11_e1000000 | Complete |
| C12 | 12 | 1010000 | 8 × 320 | results/phase2_full/topology_c12_e1010000 | Complete |
| C13 | 13 | 1020000 | 8 × 320 | results/phase2_full/topology_c13_e1020000 | Complete |
| C15 | 15 | 1040000 | 40 × 320 | results/phase2_full/topology_c15_e1040000 | Complete |
| C16 | 16 | 1050000 | 40 × 320 | results/phase2_full/topology_c16_e1050000 | Incomplete; resume existing output |

For C16, the exact resume command is:

```bash
python -u experiments/phase2_studies.py --kind topology --conn-seed 16 --event-seed 1050000 --chunks 40 --chunk-s 320 --out results/phase2_full/topology_c16_e1050000
```

Use the corresponding table values for other circuits ONLY if reproducing missing data. `recording.npz` is reused if its configuration signature agrees; otherwise the runner loads completed content-addressed chunks in `cache/simulations`. An interrupted chunk must repeat from its beginning. A fit is skipped only when both its NPZ and JSON exist. Outputs are `original`, `jitter101`, `jitter202`, `jitter303` (each NPZ/JSON) and `report.json`. The historical `status.json` can still say SIMULATING after completion; the report and diagnostics are authoritative. Back up recordings and chunks before deleting any caches.

## Calibration, shared drive and location

```bash
# Repeat for seeds 0, 1, 2. Existing summaries are bundled in results_page/sources.
python experiments/calibrate.py --duration 300 --neurons 20 --n-basis 5 --seed 0 --out results/calibration5/seed0
# Latency control: no adjacent tested lag separation reliably resolved.
python experiments/latency_calibration.py --duration 300 --neurons 20 --n-basis 5 --no-float32 --seed 0 --out results/latency_f64/seed0
# Completed corrected common-input study: two recordings, three fits.
python experiments/phase2_studies.py --kind shared --conn-seed 11 --event-seed 1000000 --chunks 8 --chunk-s 320 --out results/phase2_full/shared_c11_2560s
```

Shared mode compares private-only input with private5+shared5 Hz input; one fit observes the shared train and one hides it. Original aggregate-private-drive experiments are historical and do not test shared input.

For location mode use `--kind location`; it runs original and swapped location circuits, compares matching pairs and reports paired area differences. The existing 1280-second result is in `results/phase2_long/location_s3_1280s`. Recover its exact event/configuration values from each saved recording signature before attempting historical reproduction. A new independent replication recipe is supplied below; do not relabel it as the old study.

## New experiments supplied as executable recipes

[experiments/pending_runs.py](experiments/pending_runs.py) prints its command by default; `--run` executes it. None of these recipes is claimed complete. They reuse existing implementations and write to fresh directories.

```bash
python experiments/pending_runs.py mesh270-pilot --run
python experiments/pending_runs.py mesh270-production          # review after pilot, not an automatic next run
python experiments/pending_runs.py location-replication --run
python experiments/pending_runs.py shared-replication --run
```

The 270-neuron pilot is sparse and simulation-only. Measure runtime, firing rates, active fraction, storage and potential-delay coverage before choosing a production duration. Production recipe duration is a starting configuration, not a power guarantee. At 10×10 only ~53% of connections were inside the original 25 ms window. Scoring all versus in-window pairs are different claims.

Shared replication uses the same corrected drive construction; it is not a new correlated/state-dependent-input model. An L5 mechanism sweep, longer-history validation, validation-based penalty selection, and a low-rank-plus-sparse model remain design/implementation work, not experiments with existing results. Do not change several biological variables at once or select settings by the final anatomical test score.

## Historical experiments and tools

| Entry point | Purpose / existing outputs |
|---|---|
| experiments/production.py | Chunked recording; dense production_spikes.npz and sparse pilots; use --simulate-only to separate simulation from fitting |
| experiments/fit_production.py | Original production fit; inspect --help for cache path and solver |
| experiments/grid.py | Hidden neurons/drive grid; results/seed100, seed200, seed300; original private-drive interpretation caveat |
| experiments/production_baselines.py | Pairwise, CCG and jitter comparisons for cached production grids |
| experiments/topology.py | Original sparse C3/C4 studies; accepts --from-cache, --conn-seeds, --event-seeds, --solver DISK_LBFGS --no-float32 |
| experiments/location.py | Historical location experiment; superseded for replication by Phase 2 location mode |
| experiments/design_pilots.py | Structural design checks before expensive location/shared runs |
| experiments/phase2_uncertainty.py | Historical C3/C4 conditional analysis and old results/phase2 glob; does NOT aggregate phase2_full automatically |
| experiments/run_handoff.py, run_phase2.py, finish_pending.py | Historical broad orchestration; inspect queues before use; prefer explicit commands above |
| scripts/ground_truth_audit.py | Structural ground-truth checks |
| scripts/build_results_page.py | Read saved reports and rebuild static HTML; requires sibling StreamGLM path or --stream-root |

Use each script's `--help` for its exact interface. Smoke outputs (2–20 seconds) and the short C14 recording are engineering checks, not substitutes for full-duration evidence. Duration learning curves and independent-circuit aggregation can use cached data; they do not require new HNN simulation.

## Publication size

Only compact report JSON/Markdown/CSV and source code should be staged. Do not add `cache/`, raw NPZ/NPY, NWB downloads, optimizer checkpoints, whole artifacts directories, or export ZIP archives. The page's bundled source files are sufficient to inspect its numbers. A fresh Git clone cannot resume unshipped numerical checkpoints; retain them locally or transfer separately.
