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

# Claude handoff — NeuroTwinBench and StreamGLM

Updated 2026-09-27 UTC. Read this before the older CODEX_HANDOFF.md: that file
contains superseded queue instructions. Never infer a live process from a
`RUNNING` JSON field alone; check PID command lines and heartbeat age.

## Latest status, 2026-09-28

Topology_c3 simulation finished, then fit_topology_c3 failed the memory guard:
21.26 GiB RSS, only 1.27 GiB available. Runner 70933 stopped. Circuit 4 remains
pending. Preserve the completed topology simulation and do not retry the same
memory-heavy fit unchanged. Location remains complete.

StreamGLM v5 three-way comparison finished all 54 workers; strict convergence
passed for 41. User authorized the follow-up tuned experiment, now launched
in the side worktree as PID 265412: artifacts/v6/tuned/status.json. It selects
ridge/rank/NeMoS stepsize on validation data with fresh seeds. Read the side
worktree's HANDOFF_STREAMGLM.md and docs/TUNED_COMPARISON.md. Verify live PID.

Earlier process snapshots below are historical.

## User's current request

The latest user request explicitly authorizes restarting location AND topology,
and completing StreamGLM validation. Location simulation and fitting completed:
results/location/production_spikes.npz and location_5x5_t2.24e+06.json exist.
Topology circuit 3 was interrupted later; PID 1146144 was absent and its RUNNING
heartbeat stale. The cause of that interruption is unknown.

Restarted with --topology-only: PID 70933, child 70955, verified live around
19:48 UTC on 2026-09-27. Circuit 4 follows circuit 3. Cached chunks are reused;
location, primary grids and baselines are not repeated. Verify PIDs and heartbeat
again before future actions.

Previous attempt reached the final time
step but HNN-Core terminated MPI after 60 seconds without output while returning
results. `simulate._mpi_output_timeout` now raises that process-local silence
timeout to 600 seconds, restores the original function in `finally`, and leaves
the separate 3 GiB memory guard enabled. Two timeout regression tests passed.
The earlier memory-guard stop was a different failure.

Topology scoring now obtains eligibility from the unthinned counterfactual
network, applying the same delay/window filter to both labels, and reports
per-projection scores. Checked real circuits 3 and 4: 1,192 eligible pairs each,
354/360 edges respectively. Jitter/distance controls are still needed for strong
anatomical claims. This corrects the scoring issue described further below.

StreamGLM v0.3 work is in the separate worktree; artifacts/v4 includes Allen
Neuropixels VISp validation, current-upstream NeMoS loader tests/fits, and the
explicitly synthetic 1,000-neuron stress fit. Consult its current handoff/results.
The remaining historical notes below describe the initial resume, not live state.

The user authorized local implementation and execution without repeat permission
prompts. No external messages, PRs or publication have been requested.

## Workspaces

- Original: `/home/satvik/hnn_neuro_bridge`, branch `master`, a dirty worktree.
  Preserve all existing edits and results; do not reset/clean it.
- Side project: `/home/satvik/side_project`, branch `side-project/streaming-glm`.
  StreamGLM 0.2 is committed through `e5cd0a3` (main implementation `9bab12d`).
  Read its README.md and HANDOFF_STREAMGLM.md. Its original PROJECT.md and
  CODEX_HANDOFF.md are inherited NeuroTwinBench documents, not its current spec.
- Python for HNN: `/home/satvik/miniconda3/envs/neurotwin/bin/python`.
  Add `/home/satvik/miniconda3/envs/neurotwin/bin` to PATH for mpiexec/nrniv.

## Primary analysis is finished

Seeds 100, 200, 300 each have readable `grid.json` and `baselines.json` under
`results/seed100`, `results/seed200`, `results/seed300`. Seed100's original spikes
are `results/production_spikes.npz`; other seeds have their own spike caches.
Latency calibration and the aggregate handoff report also exist.

The old full runner, PID 10193, was interrupted during `simulate_location`.
Its last heartbeat was 2026-09-25 04:29:53 UTC. The environment booted again at
13:18:58 UTC. Both old runner and child PIDs were absent on inspection. The
precise cause of interruption is not established. Do not call its stale status
evidence of progress. Location's final concatenated cache was not yet written;
topology_c3 and topology_c4 had not started.

## Location resume

`experiments/run_handoff.py` now supports `--location-only`. It uses the existing
lock, memory guard, subprocess-group cleanup, heartbeat and final DONE/FAILED
status, but goes directly to `variant('location')`, then reports and exits.

The cached pilot is `results/location/pilot.json` and plans seven 320-second
chunks, totaling 2,240 simulated seconds. Its 20-second fit did NOT converge;
the production fit must be judged on its own diagnostics. The duration is an
extrapolation from a synthetic reference, not a statistical power guarantee.

The location run uses network='location', mesh 5x5, conn_seed=3, and event seeds
2 through 8. As of the resume audit, these chunk caches passed ZIP CRC checks:

| Chunk | Event seed | File under cache/simulations |
|---|---:|---|
| 1 | 2 | 67628a3c6418daea.npz |
| 2 | 3 | 68152099cafd8d4b.npz |
| 3 | 4 | d465aa14e9986300.npz |
| 4 | 5 | 4a33943f96b5e399.npz |

Remaining chunk keys are f746220ef3e28e2a, e4bed2cad4be9386, 17f16ca76a4f9ec6.
The resumed production script automatically loads completed chunks and simulates
missing ones. The interrupted unfinished chunk must start again. No need to
repeat the primary analyses or the location pilot.

The resume uses the unchanged scientific configuration, including its known
limitations; changing seeds or network design would create a different experiment
and intentionally miss the existing cache.

Operational files:

```text
results/handoff/status.json
results/handoff/location_only_runner.log
results/handoff/simulate_location.log
results/handoff/fit_location.log
results/location/production_spikes.npz  # appears once all chunks finish
results/location/location_5x5_t2240000.json  # expected fit output
```

Check status plus process command lines. Cached chunks can make the production
script's early ETA artificially optimistic; base estimates on newly computed
chunk timings. Approximately a few hours of simulation/fit remain, not a measured
deadline. A stale heartbeat after a machine shutdown does not write FAILED.

If restart is needed after confirming no other HNN job is alive, use:

```bash
cd /home/satvik/hnn_neuro_bridge
export PATH=/home/satvik/miniconda3/envs/neurotwin/bin:$PATH
export NEURON_MODULE_OPTIONS=-nogui
export MPLCONFIGDIR=/tmp/neurotwin-mpl
setsid nohup /home/satvik/miniconda3/envs/neurotwin/bin/python -u \
  experiments/run_handoff.py --variants-only \
  >> results/handoff/location_only_runner.log 2>&1 < /dev/null &
```

Never run two HNN simulations concurrently: HNN's MPI backend can kill nrniv
processes globally when it exits. Do not `pkill` generic name patterns. Stop only
an identified runner PID if explicitly requested. The runner handles its own
child process group. Keep the host powered and ventilated; display-off is fine,
but sleep, shutdown, battery depletion and WSL termination interrupt work.

## Scientific interpretation — be candid

Location asks whether basal versus apical-tuft placement alters the GLM's inferred
influence or effective timing. It can add a biophysical stress case and demonstrate
the pipeline, but the CURRENT design does not isolate a causal placement effect:

1. L2 source neurons are split into two fixed groups which also differ in position
   and potentially firing/network context. The same source-target pairs are not
   compared under a placement swap. A matched/swapped or randomized controlled
   experiment would be needed for a stronger location claim.
2. Within class, weight magnitude is a deterministic monotone function of distance.
   A weight-rank score cannot separate geometry from anatomical recovery. Partial
   Spearman controlling distance is undefined when those ranks are collinear.
3. The five-basis latency calibration resolved no tested adjacent separation.
   Location timing outputs remain exploratory, not calibrated latency recovery.
4. The external drive is cell-specific; the pooled drive covariate is not an oracle
   shared-input control. Recurrent common inputs can still exist. A deliberately
   shared source needs both `cell_specific=False` and `n_drive_cells=1`.
5. Adjacent chunk seeds overlap HNN's `event_seed + cell_offset` random streams.
   In an event-only check, 69/70 trains repeated at shifted neuron assignments
   between adjacent seeds. Network outputs are not thereby identical, but these
   chunks must not be treated as independent replications.
6. The queued topology scoring rule excludes long-delay positives while retaining
   analogous negatives. Fix label-independent support eligibility before treating
   sparse topology as a decisive experiment. It is not part of this resumed queue.

`experiments/location.py`'s introductory docstring still overstates group
equivalence; its final printed report correctly says the contrast is exploratory
and position-confounded. Judge its final convergence flag before interpreting it.

Benefit assessment: finishing cached location data is optional exploratory work,
not a requirement for the first primary study or the NeuroRSE application. Its
benefit is limited without a redesigned control. The user requested resumption;
finish it without presenting its outcome as definitive location reconstruction.

## StreamGLM side project — already built, no background job needed

StreamGLM 0.2 includes disk-backed data, dense/factorized JAX GLMs, self-history,
NWB/Pynapple/HNN adapters, L-BFGS and exact epoch-boundary Adam resume, model
selection on validation data, CLI, tests, wheel and saved scientific artifacts.

- 19 tests passed across the final suite plus targeted NeMoS export checks.
- The installed wheel was exercised outside the source directory.
- Small unrestricted NeMoS fit: objective difference ~3.11e-11, maximum
  predicted-count difference ~1.12e-5.
- Corrected public Mouse32 run: 44 neurons, rank 2, test gain over self-history
  0.06400 nats/bin. It is head-direction data, NOT Neuropixels.
- Cached HNN predictive subset: 70 neurons, rank 2, gain 0.03079 nats/bin.
- 1,000-neuron benchmark: ~0.411 GiB peak RSS for objective/gradient PASSES,
  not an hour-long fitted recording.
- No anatomical recovery claim, full 1,000-neuron hours-long fit or comparison
  with newer upstream NeMoS streaming APIs has been completed.

See `side_project/artifacts/v2/`, particularly provenance.json, real_mouse32,
validation and upstream_comparison.json. The initial-binning result is retained
as historical; use real_mouse32 for the corrected current result. Raw datasets
and converted recordings are in ignored cache directories.

No changes have been pushed or sent to collaborators. Preserve local work.

## Phase 2 started 2026-09-29 (supersedes earlier process snapshots)

HNN runner82671: results/phase2/status.json plus results/handoff/status.json heartbeat.14 tasks include conditional uncertainty,6 new topology circuit/drive recordings,3 corrected shared-input contrasts,3 paired location contrasts,and final aggregation. No concurrent HNN MPI. StreamGLM runner93641: artifacts/v8/queue_status.json; coupled1000 seeds941/942 then streamed-vs-streamed benchmark,which waits for HNN to exit for timing isolation. Source protocols in results/phase2/PROTOCOL.md and side_project/artifacts/v8/PROTOCOL.md. Verify PIDs and heartbeat; snapshots can stale.26 StreamGLM tests passed and3 new HNN tests passed. New scientific runs are not yet complete.
