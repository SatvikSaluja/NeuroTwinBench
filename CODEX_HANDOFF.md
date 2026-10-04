## Active restart — 2026-09-28

User authorized all pending runs. HNN runner PID 6742, topology c3 fit child
6788; StreamGLM runner PID 5533, report watcher 7607. Verify command lines and
heartbeat before acting; PIDs here are snapshots.

HNN now uses float64 DISK_LBFGS: disk feature maps and chunked analytic gradients.
Validation matched NeMoS loss/gradient and fitted filters (max difference
1.746e-6). Optimization RSS approximately 0.86 GiB. Validation evidence:
results/handoff/disk_fit_validation.json. The 26-task pending_manifest.json
queues topology c3/c4, location refit, two design pilots, six topology jitter
fits, nine proxy refits, three five-basis calibrations and three latency runs.
Existing simulations are reused. Completed commands do not prove convergence.
Shared-drive and swapped-location runs are 20-second feasibility pilots;
full corrected-design scientific experiments remain follow-up work.
Status: results/handoff/status.json. Log: results/handoff/pending_runner.log.
Never start a second HNN runner or MPI simulation concurrently.

StreamGLM resumed the v6 comparison, preserving existing candidate outcomes.
133/256 were recorded at this snapshot, including failures. Status:
/home/satvik/side_project/artifacts/v6/tuned/status.json. Report watcher writes
report.md on completion. Upstream-env suite: 25 tests passed. Wheel rebuilt
locally. No publication or remote CI performed.

Earlier process snapshots below are historical and superseded.

# NeuroTwinBench — handoff for Codex

Read `PROJECT.md` first for the full scientific spec, governing principles,
and the history of findings/retractions. This file is operational: what's
running, what commands to run next, and what's genuinely left.

## Environment

```bash
cd /home/satvik/hnn_neuro_bridge
export PATH="/home/satvik/miniconda3/envs/neurotwin/bin:$PATH"
```

All Python commands below assume this. The conda env `neurotwin` has
hnn-core, nemos, jax, scipy, psutil, mpi4py already installed.

**Critical gotcha**: `MPIBackend` kills *every* `nrniv` process on the
machine by name (not by PID) when it exits — see `upstream/README.md` §3.
**Never run two HNN simulations concurrently.** `simulate.py`'s
`_require_no_concurrent_nrniv()` guards against this but only inside one
process; don't launch a second `setsid` job that touches NEURON while
another is alive. Check first:

```bash
pgrep -fa nrniv || echo "clear to simulate"
```

**Long jobs must be launched with `setsid ... &` and `< /dev/null`**, not
plain `nohup ... &`, or they die when the parent shell session ends (this
killed a run earlier in the project). Pattern:

```bash
setsid nohup python experiments/whatever.py --args > /tmp/whatever.log 2>&1 < /dev/null &
disown
```

**Never `pkill -f <pattern>` with a short/generic pattern** — it has
self-matched this session's own shell wrapper multiple times and killed the
wrong process. Use `ps -eo pid,args` and kill by exact PID.

## Current state (as of this handoff)

- 24+ commits in, all passing `tests/test_pipeline.py`.
- `results/production_spikes.npz` exists: **2,560,000 bins × 70 neurons**,
  the full production HNN simulation (8 chunks × 320s, base_seed=100),
  concatenated. **Do not re-simulate this** — it took ~4.9 hours. Every
  downstream analysis should load it directly.
- Validated fitting config: **LBFGS, float32, n_basis=5, regularizer=1e-3**.
  Proven numerically identical to float64 (`results/solver/`), ~2x faster,
  ~half the memory. This is the config to use for everything from here.
- First full-power per-class result exists at
  `results/solver/production_full.json` — single seed, true-drive-only
  condition. **This is not yet a result**, just a proof the pipeline works
  end to end at full power (24.5 spikes/predictor vs the 16.1 synthetic
  benchmark that gave rho +0.80).
- **The primary grid experiment is running right now** (or may have just
  finished — check first):

```bash
ps -eo pid,args --no-headers | grep "grid.py" | grep -v grep
tail -50 grid_full.log
```

It was launched as:
```bash
python experiments/grid.py --from-cache results/production_spikes.npz \
    --seeds 100 --n-basis 5 --regularizer 1e-3 --max-iter 500
```
This runs all 9 cells (3 drive conditions × 3 observation conditions) on the
cached spikes with **no new simulation** — it's pure GLM fitting, ~5-15 min
per cell depending on observation subset size. Output goes to
`results/grid_*.json` (check `grid_full.log` for the exact filename it
prints at the end) and stdout has the full 3x3 summary table.

**If it's still running**, just wait for it — do not kill it, do not start
a second one. **If it finished**, read the result and move to "Next steps"
below.

## What's actually left (in priority order)

### 1. Read and record the grid result (5 min, no compute)

```bash
cat grid_full.log | tail -80
ls results/grid*.json
```

Add the 3x3 table (drive observability × observed population) to
`PROJECT.md` under a new "Primary grid — first result" section, same style
as the existing findings. State plainly whether the true→proxy→hidden
degradation predicted in §12 actually appears, and whether
interneuron-hidden vs random-subsample differ. This is one seed — say so.

### 2. Baselines on the real HNN data (30 min compute, ~30 lines of code)

The synthetic calibration has CCG + pairwise + jitter-null baselines
(`experiments/calibrate.py`). The HNN production fit does not. Write
`experiments/production_baselines.py` (or extend `fit_production.py`) that
loads `results/production_spikes.npz` and runs:

```python
from neurotwinbench import fit as fitmod, metrics as met

result_ccg = met.cross_correlogram(spikes, ...)       # exists in metrics.py
result_pairwise = fitmod.fit_pairwise_glm(spikes, ..., float32=True, n_basis=5)
result_null = fitmod.fit_population_glm(met.jitter(spikes, ...), ...)
```

Report per-class, same table format as `production_full.json`. Without this
the +0.7/+0.3/-0.03 per-class numbers have no baseline to be compared
against, and PROJECT.md principle 4 says no primary metric without one.

### 3. Seeds for error bars (biggest compute item: ~15h, run overnight)

Everything HNN so far is **one seed** (base_seed=100). Run 2 more full
production simulations at different `event_seed` values:

```bash
# each ~4.9h, run SEQUENTIALLY (NEURON constraint above), check nrniv is clear first
python experiments/production.py --chunks 8 --chunk-s 320 --base-seed 200 \
    --out results/seed200
python experiments/production.py --chunks 8 --chunk-s 320 --base-seed 300 \
    --out results/seed300
```

Then rerun the grid + per-class fit against each, using the validated
config (`--float32`, `n_basis=5`, `regularizer=1e-3`, LBFGS). Report mean ±
sd per connection class, matching the synthetic calibration's format
(`results/calibration_n20_t*_s*.json` already does this — same pattern).

**This is the long pole.** Everything else is minutes; this is ~10 hours of
unattended NEURON time. Start it early if there's a fixed deadline.

### 4. §6 latency calibration — never successfully run

```bash
python experiments/latency_calibration.py --duration 300
```

This exists (`experiments/latency_calibration.py`) but has not been
confirmed to complete and produce a resolvable-lag table. Run it, check it
finishes without error, and record the smallest resolvable lag separation
in `PROJECT.md` §6. **No latency claim anywhere in the project is licensed
until this runs successfully** — the per-class effective-latency numbers in
`production_full.json` should not be reported as findings yet for this
reason.

### 5. Location + topology experiments (each ~5-10h compute, independent of each other and of #3)

These use purpose-built networks (`network="location"` /
`connection_probability` thinning in `simulate.py`) and need their own
fresh simulations — they cannot reuse `production_spikes.npz`.

```bash
python experiments/location.py --tstop 2560000 --n-procs 4 \
    --regularizer 1e-3 --n-basis 5
python experiments/topology.py --probability 0.3 --conn-seeds 3 4 \
    --n-procs 4 --regularizer 1e-3 --n-basis 5
```

Use `--tstop` scaled to hit ~16+ spikes/predictor for whatever `n_basis`
you pick — check with `fitmod.power_check()` on a short pilot run first
rather than assuming. Remember: **run one at a time**, and not concurrently
with anything else touching NEURON.

### 6. Regenerate figures once grid + baselines exist

```bash
python figures/make_figures.py
```

Currently only `data_budget.png` and `hnn_per_class.png` exist (from
synthetic calibration + the single-seed production fit). Once the grid JSON
exists, `figures/make_figures.py` should be extended with a
drive-observability × observed-population heatmap or grouped bar chart —
check the file, it may already stub this out.

### 7. Upstream PRs

`upstream/README.md` documents 3 proposed hnn-core contributions with
reference implementations already written in this repo. Nobody has
actually opened the PRs against `jonescompneurolab/hnn-core`. Lowest
priority — do this last, it's writeup work, not research.

## Things that are DONE — do not redo

- Ground-truth resolver, validated against real hnn-core (`ground_truth.py`)
- Synthetic calibration across 3 durations × 3 seeds
  (`results/calibration_n20_t*_s*.json`) — instrument is proven, rho +0.80
  ± 0.004 at 300s
- Solver/precision validation (`results/solver/`) — float32+LBFGS is safe,
  don't re-litigate this
- The production spike cache (`results/production_spikes.npz`) — 4.9h of
  compute, reuse it
- MPI benchmarking, drive-strength sweep, memory scaling — all in
  `PROJECT.md` with numbers

## Known risks / things to watch for

- Every memory estimate made in this project so far has been wrong at
  least once (extrapolation from small subsets is optimistic ~20-30%).
  Before running location/topology at scale, do a small pilot and measure,
  don't calculate from the scaling formula alone.
- The pairwise GLM baseline nearly tied the population GLM on synthetic
  data (+0.788 vs +0.802 at 300s). If that holds on HNN baselines (#2
  above), the "joint estimation is worth it" premise is not supported —
  that's a legitimate finding, report it honestly rather than downplaying it.
- `tests/test_pipeline.py` should still pass after any change to
  `neurotwinbench/fit.py` — it's fast (no NEURON) and catches regressions
  in the metrics/synthetic path.

## Implementation update — 2026-09-23

The old grid was no longer running and had not saved a grid JSON. Its one
console-only pooled correlation is not a scientific result. The production
cache and saved solver-validation artifacts have been preserved.

Implemented continuation:

```bash
export PATH="/home/satvik/miniconda3/envs/neurotwin/bin:$PATH"
export NEURON_MODULE_OPTIONS=-nogui
export MPLCONFIGDIR=/tmp/neurotwin-mpl
setsid nohup python -u experiments/run_handoff.py > results/handoff/runner.log 2>&1 < /dev/null &
```

Create `results/handoff` before redirecting on a fresh checkout. The runner
holds a file lock and executes one job at a time. It refreshes
`results/handoff/status.json` every 30 seconds, guards a 3 GiB available-RAM
reserve, saves per-step logs, and records `DONE` or `FAILED`. A failed run can
be restarted with the same command; completed grid cells, baselines and cached
simulation chunks are reused. Do not launch a second external HNN simulation.

Order: seed-100 grid and baselines; matched latency calibration; seed-200
simulation/grid/baselines; seed-300 simulation/grid/baselines; measured pilots
and chunked location/topology recordings and fits; reports and figures. These
are substantial computations, not completed scientific results at launch.
Upstream PRs remain last, after the research computations; no upstream changes
have been published by this runner.

Corrections incorporated:

- Fits use the validated LBFGS/float32/5-basis/ridge-1e-3 configuration.
- Each grid condition runs in a separate process and writes JSON and fitted
  filters immediately. `fit_production.py` uses that same worker.
- Every receptor/location class is retained, including classes sharing a pair;
  the old single-label matrix silently overwrote some of them. Comparisons are
  against total inferred pair influence, not receptor-specific estimates.
- Inter-neuron recovery excludes autapses. Inhibitory ranks are not interpreted;
  sign scores and support counts remain available.
- Independent simulation chunks never supply history to each other. Original
  production boundaries come from this handoff (eight 320-second chunks);
  new caches contain explicit segment lengths and simulation configuration.
- Pairwise baselines accept float32, silent neurons, segment boundaries and
  the same true-drive covariates. CCG and jitter respect chunk boundaries.
- The 16.1 synthetic observation is a budget reference, not a validated HNN
  sufficiency threshold. Variant durations use measured pilots with that caveat.
- Reports give a separate 3×3 table for each informative class, sample SD only
  with multiple seeds, and no uncalibrated HNN latency claim.

Outputs: `results/seed{100,200,300}/grid.json`, `baselines.json`, individual
`cells/` and `baselines/` checkpoints, `results/grid_summary.json`, and
`results/handoff_report.md`. The report generator refreshes a marked section
of `PROJECT.md`; figures regenerate from saved JSON. Production input files
are never truncated to fit memory.
