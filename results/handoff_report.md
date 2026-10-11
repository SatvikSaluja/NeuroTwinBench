## Primary grid — first result

Generated from durable per-class checkpoints; no pooled E/I correlations.

Completed grids: **3 independent base-seed recordings** (100, 200, 300 as available).
Across-seed SD is unavailable for a single seed, rather than reported as zero.

The old grid stopped after one console-only pooled result and wrote no JSON; that number is not used.
New fits use LBFGS/float32, five basis functions, ridge 1e-3, and exclude history across independent chunks.
The 16.1 synthetic spikes/predictor observation is a budget reference, not a sufficiency threshold for HNN.

Each receptor/location class is retained. Shared pairs have one total inferred influence, so these are not independent receptor/location recoveries.
Autapses are excluded; inhibitory weight ranks are unavailable because their spread is degenerate (§2F).
Production baselines cover the full-population/true-drive condition. Other grid cells are exploratory contrasts until matched controls are available.

**L2_pyramidal->L2_basket|ampa|soma**

| Observed population | True drive | Proxy | Hidden |
|---|---:|---:|---:|
| full | +0.726 ± 0.003 | +0.726 ± 0.002 | +0.726 ± 0.003 |
| interneurons_hidden | -- | -- | -- |
| random_subsample | +0.763 ± 0.025 | +0.762 ± 0.026 | +0.764 ± 0.025 |

**L2_pyramidal->L2_pyramidal|ampa|proximal**

| Observed population | True drive | Proxy | Hidden |
|---|---:|---:|---:|
| full | +0.311 ± 0.002 | +0.311 ± 0.002 | +0.311 ± 0.002 |
| interneurons_hidden | +0.277 ± 0.004 | +0.278 ± 0.003 | +0.277 ± 0.004 |
| random_subsample | +0.229 ± 0.033 | +0.230 ± 0.033 | +0.229 ± 0.033 |

**L2_pyramidal->L2_pyramidal|nmda|proximal**

| Observed population | True drive | Proxy | Hidden |
|---|---:|---:|---:|
| full | +0.311 ± 0.002 | +0.311 ± 0.002 | +0.311 ± 0.002 |
| interneurons_hidden | +0.277 ± 0.004 | +0.278 ± 0.003 | +0.277 ± 0.004 |
| random_subsample | +0.229 ± 0.033 | +0.230 ± 0.033 | +0.229 ± 0.033 |

**L2_pyramidal->L5_basket|ampa|soma**

| Observed population | True drive | Proxy | Hidden |
|---|---:|---:|---:|
| full | +0.704 ± 0.006 | +0.704 ± 0.005 | +0.704 ± 0.005 |
| interneurons_hidden | -- | -- | -- |
| random_subsample | +0.750 ± 0.022 | +0.749 ± 0.022 | +0.750 ± 0.022 |

**L2_pyramidal->L5_pyramidal|ampa|distal**

| Observed population | True drive | Proxy | Hidden |
|---|---:|---:|---:|
| full | +0.110 ± 0.010 | +0.110 ± 0.010 | +0.110 ± 0.010 |
| interneurons_hidden | -0.076 ± 0.008 | -0.076 ± 0.007 | -0.076 ± 0.008 |
| random_subsample | +0.144 ± 0.020 | +0.143 ± 0.020 | +0.144 ± 0.020 |

**L2_pyramidal->L5_pyramidal|ampa|proximal**

| Observed population | True drive | Proxy | Hidden |
|---|---:|---:|---:|
| full | +0.110 ± 0.010 | +0.110 ± 0.010 | +0.110 ± 0.010 |
| interneurons_hidden | -0.076 ± 0.008 | -0.076 ± 0.007 | -0.076 ± 0.008 |
| random_subsample | +0.144 ± 0.020 | +0.143 ± 0.020 | +0.144 ± 0.020 |

**L5_pyramidal->L5_basket|ampa|soma**

| Observed population | True drive | Proxy | Hidden |
|---|---:|---:|---:|
| full | +0.388 ± 0.003 | +0.389 ± 0.004 | +0.388 ± 0.003 |
| interneurons_hidden | -- | -- | -- |
| random_subsample | +0.358 ± 0.035 | +0.358 ± 0.034 | +0.358 ± 0.036 |

**L5_pyramidal->L5_pyramidal|ampa|proximal**

| Observed population | True drive | Proxy | Hidden |
|---|---:|---:|---:|
| full | +0.492 ± 0.003 | +0.492 ± 0.004 | +0.492 ± 0.003 |
| interneurons_hidden | +0.503 ± 0.004 | +0.503 ± 0.004 | +0.503 ± 0.004 |
| random_subsample | +0.483 ± 0.046 | +0.483 ± 0.045 | +0.483 ± 0.046 |

**L5_pyramidal->L5_pyramidal|nmda|proximal**

| Observed population | True drive | Proxy | Hidden |
|---|---:|---:|---:|
| full | +0.492 ± 0.003 | +0.492 ± 0.004 | +0.492 ± 0.003 |
| interneurons_hidden | +0.503 ± 0.004 | +0.503 ± 0.004 | +0.503 ± 0.004 |
| random_subsample | +0.483 ± 0.046 | +0.483 ± 0.045 | +0.483 ± 0.046 |

True→proxy→hidden recovery decreases monotonically in 0/24 scoreable class/population combinations.
This is descriptive; class overlap and seed count preclude a significance claim.

Interneuron-hidden minus random-subsample recovery ranges from -0.220 to +0.048 across common scoreable classes/drive conditions.
These masks retain different pairs; this contrast also changes the evaluation set.

Fits not satisfying the recorded solver stopping criterion: 9/27. Their scores are provisional, not validated scientific findings.

**Seed 100 baselines** (complete=True)

| Connection class | Population | Pairwise + drive | CCG | Jitter + drive |
|---|---:|---:|---:|---:|
| L2_pyramidal->L2_basket|ampa|soma | +0.725 | +0.687 | +0.488 | +0.594 |
| L2_pyramidal->L2_pyramidal|ampa|proximal | +0.309 | +0.047 | +0.461 | +0.494 |
| L2_pyramidal->L2_pyramidal|nmda|proximal | +0.309 | +0.047 | +0.461 | +0.494 |
| L2_pyramidal->L5_basket|ampa|soma | +0.705 | +0.584 | +0.343 | +0.557 |
| L2_pyramidal->L5_pyramidal|ampa|distal | +0.118 | +0.318 | +0.509 | +0.533 |
| L2_pyramidal->L5_pyramidal|ampa|proximal | +0.118 | +0.318 | +0.509 | +0.533 |
| L5_pyramidal->L5_basket|ampa|soma | +0.391 | +0.390 | +0.578 | +0.540 |
| L5_pyramidal->L5_pyramidal|ampa|proximal | +0.494 | +0.468 | +0.638 | +0.633 |
| L5_pyramidal->L5_pyramidal|nmda|proximal | +0.494 | +0.468 | +0.638 | +0.633 |

No advantage for joint estimation is assumed; compare each population score directly with its pairwise and null scores.

**Seed 200 baselines** (complete=True)

| Connection class | Population | Pairwise + drive | CCG | Jitter + drive |
|---|---:|---:|---:|---:|
| L2_pyramidal->L2_basket|ampa|soma | +0.724 | +0.684 | +0.485 | +0.592 |
| L2_pyramidal->L2_pyramidal|ampa|proximal | +0.313 | +0.051 | +0.465 | +0.457 |
| L2_pyramidal->L2_pyramidal|nmda|proximal | +0.313 | +0.051 | +0.465 | +0.457 |
| L2_pyramidal->L5_basket|ampa|soma | +0.698 | +0.584 | +0.341 | +0.581 |
| L2_pyramidal->L5_pyramidal|ampa|distal | +0.099 | +0.319 | +0.507 | +0.531 |
| L2_pyramidal->L5_pyramidal|ampa|proximal | +0.099 | +0.319 | +0.507 | +0.531 |
| L5_pyramidal->L5_basket|ampa|soma | +0.384 | +0.375 | +0.576 | +0.530 |
| L5_pyramidal->L5_pyramidal|ampa|proximal | +0.493 | +0.469 | +0.637 | +0.642 |
| L5_pyramidal->L5_pyramidal|nmda|proximal | +0.493 | +0.469 | +0.637 | +0.642 |

No advantage for joint estimation is assumed; compare each population score directly with its pairwise and null scores.

**Seed 300 baselines** (complete=True)

| Connection class | Population | Pairwise + drive | CCG | Jitter + drive |
|---|---:|---:|---:|---:|
| L2_pyramidal->L2_basket|ampa|soma | +0.729 | +0.686 | +0.495 | +0.609 |
| L2_pyramidal->L2_pyramidal|ampa|proximal | +0.311 | +0.050 | +0.470 | +0.441 |
| L2_pyramidal->L2_pyramidal|nmda|proximal | +0.311 | +0.050 | +0.470 | +0.441 |
| L2_pyramidal->L5_basket|ampa|soma | +0.709 | +0.585 | +0.335 | +0.511 |
| L2_pyramidal->L5_pyramidal|ampa|distal | +0.113 | +0.319 | +0.507 | +0.521 |
| L2_pyramidal->L5_pyramidal|ampa|proximal | +0.113 | +0.319 | +0.507 | +0.521 |
| L5_pyramidal->L5_basket|ampa|soma | +0.389 | +0.375 | +0.584 | +0.534 |
| L5_pyramidal->L5_pyramidal|ampa|proximal | +0.488 | +0.466 | +0.635 | +0.644 |
| L5_pyramidal->L5_pyramidal|nmda|proximal | +0.488 | +0.466 | +0.635 | +0.644 |

No advantage for joint estimation is assumed; compare each population score directly with its pairwise and null scores.

**Latency calibration (§6)**

No adjacent lag separation was resolved.
This is a one-seed, across-edge dispersion criterion on basis-aligned lags, not a universal timing resolution.

