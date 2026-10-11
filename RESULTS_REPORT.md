# NeuroTwinBench results

Snapshot: 2026-10-05. Completed reports are the evidence; a saved RUNNING flag does not establish that a job is alive.

## Main result: sparse topology

70-neuron circuits, recurrent excitatory connection probability 0.3, 1 ms bins, 25 ms history, five basis functions, float64 disk-backed fitting, ridge 0.001. Each circuit has an original fit and three independently jittered fits.

| Circuit | Seconds | L2 ROC-AUC | All jitter AUCs (range) | L2 average precision | L5 ROC-AUC |
|---|---:|---:|---:|---:|---:|
| C11 | 2560 | 0.700 | 0.600–0.611 | 0.577 | 0.494 |
| C12 | 2560 | 0.807 | 0.635–0.653 | 0.730 | 0.581 |
| C13 | 2560 | 0.784 | 0.616–0.625 | 0.709 | 0.555 |
| C15 | 12800 | 0.731 | 0.578–0.580 | 0.666 | 0.568 |

All reported original/control fits converged. L2 exceeds all three jitter controls in every circuit. L5's conditional AUC-difference intervals include zero. Distance-only AUCs are 0.447, 0.529, 0.524 and 0.492 respectively. This supports selective recovery in this simulation design, not complete reconstruction or causal identification in real recordings.

ROC-AUC measures ranking of true edges above absent candidate edges, not reconstruction accuracy. Average precision (stored as `pr_auc`) has an approximate random baseline of edge prevalence (~0.30). Jitter independently displaces spikes by ±50 ms, clipped within each segment. Bootstrap intervals resample neurons with fits held fixed; they exclude refitting and independent-circuit uncertainty. Longer C15 cannot isolate a duration effect because its wiring differs.

## Supporting and negative findings

- Five-basis synthetic calibration: mean Spearman strength recovery 0.821 (population GLM), 0.816 (pairwise), 0.570 (CCG), 0.177 (jitter). Sign recovery ranges from 98.3% to 100%, rather than the previously quoted 99.2%–100% range. Matched GLM assumptions are a control, not validation of biological recovery.
- Location: paired area contrast +0.555, conditional interval [0.364, 0.745], 621 pairs. This is a circuit-wide dendritic location swap, not a single-synapse causal effect.
- Corrected shared drive: observed-minus-hidden L2 AUC −0.000484; no benefit in this particular construction.
- Dense weight rank is confounded with distance. It is not independent evidence of synaptic identification.
- No reliable fine-latency claim or 270-neuron recovery result is established.
- C16 was incomplete at the last verified checkpoint. It is excluded from the result table.

## Evidence

The [HTML page](results_page/index.html) includes the tables and all controls. Small source reports are in [results_page/sources](results_page/sources); the [manifest](results_page/sources/manifest.json) records their provenance. Large spike arrays, feature caches and optimizer checkpoints are intentionally not included in this publication bundle.

See [SIMULATIONS.md](SIMULATIONS.md) for execution, resumption and proposed experiments.
