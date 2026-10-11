# Consolidated evidence record — 2026-09-29

This is a dated snapshot of completed work, not a claim that all proposed research is finished. The 26-task HNN queue and StreamGLM v6/v7 suites finished. No new experiment was launched for this report. Historical files are preserved; older reports may contain superseded status or convergence claims.

## Metric definitions

Spearman rho measures ranking agreement, not percent correct. ROC-AUC ranks existing against absent edges (chance .5); PR-AUC depends on edge prevalence. Bits/spike is predictive log-likelihood gain per spike relative to the stated baseline, not accuracy. Gradient gates measure stationarity, not biological truth or a global optimum for low-rank models. Peak RSS is process memory, not parameter storage.

## NeuroTwinBench scope

70-neuron HNN circuits; spike bins 1 ms; 25 ms history; five temporal basis functions in production. Dense primary grids: seeds100/200/300, 2560 s each. Dense scores are distance-confounded; inhibitory ranks have insufficient weight spread; shared receptor/location pairs are not independent recoveries. Original drive uses cell-specific external inputs and an aggregate predictor, not a target-specific oracle.

## Five-basis matched synthetic calibration

| Seed | Population rho | Pairwise rho | CCG rho | Jitter rho | Population sign accuracy |
|---|---:|---:|---:|---:|---:|
| 0 | 0.823649 | 0.820334 | 0.550130 | 0.220012 | 1.000000 |
| 1 | 0.797481 | 0.788523 | 0.640686 | 0.139389 | 0.991870 |
| 2 | 0.841419 | 0.838976 | 0.519969 | 0.171080 | 0.983193 |

Mean population rho .820849; pairwise .815944; CCG .570261; jitter .176827. This supports calibration under a correctly specified generator, not HNN synaptic identification.

## Historical eight-basis calibration

| Duration s | Population mean rho | CCG mean rho | Jitter mean rho |
|---|---:|---:|---:|
| 120 | 0.670768 | 0.347176 | 0.047545 |
| 300 | 0.801943 | 0.462052 | 0.198834 |
| 600 | 0.871046 | 0.575604 | 0.317251 |

## Converged proxy refits

All nine refits passed their recorded gradient criterion. Means across three seeds below; original full/hidden-drive results and baselines are in the primary report appended later.

| Class | Full | Interneurons hidden | Random subsample |
|---|---:|---:|---:|
| L2_pyramidal->L2_basket / ampa / soma | 0.725715 | -- | 0.762206 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.311243 | 0.278138 | 0.229967 |
| L2_pyramidal->L5_basket / ampa / soma | 0.703777 | -- | 0.749291 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.110257 | -0.076519 | 0.143464 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.110257 | -0.076519 | 0.143464 |
| L5_pyramidal->L5_basket / ampa / soma | 0.388758 | -- | 0.358348 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.491593 | 0.503330 | 0.482716 |

## Sparse topology and all jitter controls

| Circuit | Condition | ROC-AUC | PR-AUC | L2 ROC-AUC | L5 ROC-AUC | Converged |
|---|---|---:|---:|---:|---:|---|
| 3 | disk_fit | 0.649960 | 0.529093 | 0.734733 | 0.565848 | True |
| 3 | jitter101 | 0.555129 | 0.367542 | 0.605787 | 0.543694 | True |
| 3 | jitter202 | 0.553514 | 0.367281 | 0.599436 | 0.545124 | True |
| 3 | jitter303 | 0.551761 | 0.368818 | 0.593355 | 0.546647 | True |
| 4 | disk_fit | 0.622302 | 0.513273 | 0.711351 | 0.530622 | True |
| 4 | jitter101 | 0.548301 | 0.351197 | 0.598811 | 0.524880 | True |
| 4 | jitter202 | 0.543256 | 0.344416 | 0.586659 | 0.525267 | True |
| 4 | jitter303 | 0.547549 | 0.350060 | 0.592722 | 0.530409 | True |

Circuit3: 3200s,354 edges/838 nonedges,prevalence .296980,distance-only AUC .512729. Circuit4:3520s,360/832,prevalence .302013,distance-only AUC .455823. Only L2/L5 recurrent pyramidal projections are thinned. L2 recovery exceeds all tested jitter controls; L5 improvement is small. Two circuits use the same base event-seed schedule; edges sharing neurons are not independent replications. Coarse distance strata do not remove all confounding.

## Location and latency

Location converged float64 fit: basal rho .008895, sign .963087, median effective lag5ms,298 evaluated pairs; tuft rho .597011, sign .978328,lag6ms,323 pairs. Both median anatomical delays1.742909ms. Original source-group assignment confounds the placement comparison; excitatory-only sign accuracy has a trivial positive-sign baseline.

Latency: true lags1/2/4/7ms -> recovered medians3.5/4/4/6(seed0),3/3/4/6(seed1),3/3/4/6(seed2). All12 fits converge; no adjacent separation resolved by the recorded descriptive criterion. No reliable timing claim.

Design pilots:20s shared-drive simulation,1 source targeting70neurons,911spikes,no silent cells. Paired placement pilot625pairs swap location with identical weights/delays,4643vs4499spikes. These establish manipulation feasibility, not powered recovery or rate matching.

## Numerical engineering

Disk-backed float64 HNN fitter with chunked exact objective/gradient, atomically saved parameters and completed-job ledger. L-BFGS history is not checkpointed. Matched small-case max filter difference1.745836e-6; objective gap3.29e-13. Historical OOM failures preserved. Matched float32/float64 L-BFGS agreed; the earlier precision-caused-sign-flip claim was confounded. SVRG is not globally discredited by earlier settings that failed.

## StreamGLM implementation

Independent JAX dense/factorized Poisson engine, exact chunked gradients, low-rank projection/convolution, epochs and memmaps, optional separate self-history, Adam and SciPy L-BFGS, parameter persistence, validation-based rank selection, import/evaluation/prediction CLI, NWB/Pynapple/HNN adapters and NeMoS interoperability. Low rank W=UV^T compresses independent patterns; it is not synonymous with sparsity. Streaming itself already exists in current NeMoS. Local package0.3 wheel built and installation checked;25 tests passed in the recorded upstream environment. No package publication, remote CI or upstream acceptance claimed.

## Tuned model comparison, two-seed means

| N | Truth | Model | Test bits/spike over intercept | Filter correlation |
|---|---|---|---:|---:|
| 64 | lowrank | dense | 0.000906 | 0.293899 |
| 64 | lowrank | lowrank | 0.006618 | 0.764262 |
| 64 | lowrank | nemos | 0.000906 | 0.293852 |
| 64 | permutation_fullrank | dense | 0.031283 | 0.788817 |
| 64 | permutation_fullrank | lowrank | 0.022109 | 0.646431 |
| 64 | permutation_fullrank | nemos | 0.031283 | 0.788826 |
| 128 | lowrank | dense | 0.000008 | 0.151978 |
| 128 | lowrank | lowrank | 0.002470 | 0.593215 |
| 128 | lowrank | nemos | 0.000005 | 0.151415 |
| 128 | permutation_fullrank | dense | 0.014152 | 0.646256 |
| 128 | permutation_fullrank | lowrank | 0.004911 | 0.377006 |
| 128 | permutation_fullrank | nemos | 0.014151 | 0.646256 |

Low-rank structure improves synthetic low-rank recovery but loses full-rank structure. Dense StreamGLM matches tuned unrestricted NeMoS. Small gains are not classification accuracy; no biological connectivity claim follows.

## Outstanding work

Corrected full shared-drive and paired-location studies; dependence-aware uncertainty and more independent circuit/drive realizations; unified final primary-grid report incorporating replacement fits; NeMoS streaming-versus-streaming performance scaling; BFGS/Newton/sparse baselines where appropriate; multiple real sessions and covariates; meaningful coupled1000-neuron recovery; clean release/CI/documentation review; literature-based novelty assessment. Completing the queue does not complete these extensions.

## Detailed source reports (historical context retained)

## Dense primary report: original proxy results are superseded
Source: /home/satvik/hnn_neuro_bridge/results/handoff_report.md

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



## StreamGLM matched small-model validation
Source: /home/satvik/side_project/artifacts/v3/matched_dense/report.md

# Matched dense fits

Fresh processes, float64, unregularized, identical initialization and splits. Each row is a synthetic dataset; seeds are data replicates, not timing repeats. The HNN simulation shared this host. NeMoS native uses a different solver.

| Bins | Seed | Backend | Seconds* | Peak GiB | Gradient norm | Accuracy gate |
|---:|---:|---|---:|---:|---:|:---:|
| 4000 | 7 | streamed | 2.762 | 0.282 | 9.7e-08 | True |
| 4000 | 7 | nemos_common | 3.339 | 0.502 | 7e-08 | True |
| 4000 | 7 | nemos_native | 8.378 | 0.635 | 1.4e-09 | True |
| 4000 | 11 | streamed | 2.681 | 0.284 | 7e-08 | True |
| 4000 | 11 | nemos_common | 3.395 | 0.516 | 9.3e-08 | True |
| 4000 | 11 | nemos_native | 9.510 | 0.624 | 2.2e-09 | True |
| 4000 | 19 | streamed | 3.473 | 0.289 | 9.7e-08 | True |
| 4000 | 19 | nemos_common | 3.977 | 0.514 | 6.2e-08 | True |
| 4000 | 19 | nemos_native | 11.332 | 0.636 | 1.4e-09 | True |
| 16000 | 7 | streamed | 8.105 | 0.292 | 7.1e-08 | True |
| 16000 | 7 | nemos_common | 6.264 | 0.587 | 8.9e-08 | True |
| 16000 | 7 | nemos_native | 13.213 | 0.695 | 8.1e-10 | True |
| 16000 | 11 | streamed | 7.053 | 0.294 | 9.4e-08 | True |
| 16000 | 11 | nemos_common | 5.962 | 0.586 | 5.8e-08 | True |
| 16000 | 11 | nemos_native | 12.951 | 0.699 | 2.6e-10 | True |
| 16000 | 19 | streamed | 7.742 | 0.286 | 9.4e-08 | True |
| 16000 | 19 | nemos_common | 5.792 | 0.580 | 7.2e-08 | True |
| 16000 | 19 | nemos_native | 13.058 | 0.685 | 9.9e-10 | True |
| 64000 | 7 | streamed | 25.147 | 0.296 | 5e-08 | True |
| 64000 | 7 | nemos_common | 14.695 | 0.866 | 7.1e-08 | True |
| 64000 | 7 | nemos_native | 26.664 | 0.955 | 5.4e-10 | True |
| 64000 | 11 | streamed | 24.294 | 0.299 | 9.8e-08 | True |
| 64000 | 11 | nemos_common | 14.973 | 0.867 | 9e-08 | True |
| 64000 | 11 | nemos_native | 26.098 | 0.955 | 9.4e-10 | True |
| 64000 | 19 | streamed | 28.752 | 0.299 | 8.2e-08 | True |
| 64000 | 19 | nemos_common | 17.402 | 0.879 | 7.7e-08 | True |
| 64000 | 19 | nemos_native | 31.467 | 0.954 | 1.4e-09 | True |

*Includes feature construction, initial objective evaluation, compilation and optimization. Peak RSS covers the whole worker, including held-out scoring. Common-driver fits use SciPy L-BFGS-B (ftol=1e-14, gtol=1e-7, maxcor=10). Native NeMoS uses LBFGS tol=1e-7. All have a 1,000-iteration budget. The separate accuracy gate requires gradient infinity norm <=1e-5. No low-rank, real-data, large-scale speedup or current upstream batching claim.

Native timing also includes the independent objective-audit compilation; use the common-driver arms for the primary implementation comparison.

## Agreement with StreamGLM

| Bins | Seed | Reference | Objective difference | Held-out LL difference | Max prediction difference | All gates pass |
|---:|---:|---|---:|---:|---:|:---:|
| 4000 | 7 | nemos_common | 3.93e-11 | 3.64e-07 | 6.81e-06 | True |
| 4000 | 7 | nemos_native | 5.2e-11 | 3.55e-07 | 9.96e-06 | True |
| 4000 | 11 | nemos_common | 3.29e-11 | 1.16e-06 | 8.01e-06 | False |
| 4000 | 11 | nemos_native | 4.6e-11 | 1.27e-06 | 7.79e-06 | False |
| 4000 | 19 | nemos_common | 1.01e-11 | 2.81e-07 | 7.87e-06 | True |
| 4000 | 19 | nemos_native | 9.54e-12 | 8.67e-08 | 4.23e-06 | True |
| 16000 | 7 | nemos_common | 2.99e-11 | 2.85e-07 | 4.8e-06 | True |
| 16000 | 7 | nemos_native | 2.31e-11 | 5.34e-08 | 8.14e-06 | True |
| 16000 | 11 | nemos_common | 1.58e-11 | 4.62e-07 | 9.01e-06 | True |
| 16000 | 11 | nemos_native | 4.88e-11 | 7.67e-07 | 1.08e-05 | True |
| 16000 | 19 | nemos_common | 6.7e-12 | 1.31e-07 | 6.95e-06 | True |
| 16000 | 19 | nemos_native | 2.56e-11 | 2.64e-07 | 9.72e-06 | True |
| 64000 | 7 | nemos_common | 1.61e-11 | 8.81e-08 | 9.33e-06 | True |
| 64000 | 7 | nemos_native | 1.03e-11 | 1.53e-07 | 4.35e-06 | True |
| 64000 | 11 | nemos_common | 1.33e-11 | 1.44e-07 | 3.05e-06 | True |
| 64000 | 11 | nemos_native | 2.84e-11 | 1e-07 | 5.12e-06 | True |
| 64000 | 19 | nemos_common | 9.31e-13 | 7.65e-09 | 6.19e-06 | True |
| 64000 | 19 | nemos_native | 1.97e-11 | 1.03e-07 | 5.23e-06 | True |

Agreement requires gradient norms <=1e-5, initial objective/gradient differences <=1e-10, final objective and held-out LL differences <=1e-6, and maximum prediction difference <=1e-3. No failed gate is omitted.


## StreamGLM real data and scale tests
Source: /home/satvik/side_project/artifacts/v4/report.md

# StreamGLM 0.3 measured validation

Real Neuropixels predictive tests, an explicitly synthetic scale test, and interoperability with pinned current NeMoS. These establish software capabilities under the recorded conditions; they do not establish anatomical recovery.

## Allen Visual Coding Neuropixels

300 seconds at 5 ms bins; provider quality==good and VISp; ascending unit IDs. Chronological 60/20/20 split, training-only activity filtering, ranks 0/2/5 and two starts for nonzero ranks. Selection uses validation data.

| Retained / requested | Rank | Gain over self-history (nats/bin) | Gain (bits/spike) | Peak GiB | Workflow seconds |
|---:|---:|---:|---:|---:|---:|
| 98/100 | 5 | 0.0879799 | 0.0456145 | 0.433 | 214.5 |
| 185/195 | 5 | 0.196361 | 0.0766088 | 0.492 | 754.0 |

## Synthetic scale test

1000 independent Poisson units, 3600 seconds, 10 ms bins. Peak process RSS 1.241 GiB; workflow 1623.0 seconds. Hypothetical full-recording design: 8.05 GiB. The design size is arithmetic, not an OOM measurement.

Rank-5 test gain over self-history: -0.000381805 nats/bin. No coupling exists in this generator; do not treat this as recovery validation.

## Current NeMoS interoperability

Pinned commit `81c7200a0e66686e98fd1907e7fa11e111a0e66a`. `NeMoSRecordingLoader` retains epoch boundaries and short tails; fixed features are tested against independent whole-epoch NeMoS convolutions. Current upstream already supports this kind of streaming.

SVRG reached gradient norm 9.97e-06; objective difference from unrestricted StreamGLM L-BFGS: 9.25e-07. The initial 300-pass run did not meet the gradient threshold; it is retained. The longer run used the same settings and stopped at the threshold.

## Limitations

- The two real-data subsets overlap within one VISp recording, not independent biological replications.
- Quality labels come from the supplied workshop extract; no waveform-level quality reanalysis.
- Real-data coupling has no stimulus/behavior adjustment and does not establish synaptic or causal connectivity.
- The 1,000-unit hour-long case is independent synthetic Poisson at 10 ms bins, not real Neuropixels at 1 ms.
- Optimizer relative-objective stopping does not certify a global optimum or a small gradient; diagnostics retained.
- The current-NeMoS exercise validates loader interoperability and accuracy, not a performance advantage over upstream streaming.
- CPU timing was measured on a shared host while HNN and other validation jobs ran.
- No remote CI, upstream acceptance, package publication, or 1,000-unit hour-long real-data fit is claimed.


## StreamGLM tuned comparison
Source: /home/satvik/side_project/artifacts/v6/tuned/report.md

# Tuned StreamGLM / NeMoS comparison

Fixed protocol: 60/20/20 chronological splits, fresh seeds, validation-only selection among gradient-gate-passing candidates. Failed settings remain in candidates.json. Two seeds are exploratory, not a significance certification.

| Dataset | Model | Rank | Ridge | Step | Test bits/spike | Filter correlation | Relative filter error | Selected fit seconds | Tuning seconds | Peak GiB |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| lowrank_n64_s31 | dense | None | 0.1 | None | 0.000854251 | 0.2928 | 0.9599 | 2.8 | 48.7 | 0.306 |
| lowrank_n64_s31 | lowrank | 2 | 0.01 | None | 0.00654007 | 0.7587 | 0.7124 | 16.1 | 789.4 | 0.296 |
| lowrank_n64_s31 | nemos | None | 0.1 | 1.0 | 0.000853999 | 0.2928 | 0.9599 | 13.6 | 1696.8 | 0.488 |
| permutation_fullrank_n64_s31 | dense | None | 0.01 | None | 0.0312326 | 0.7866 | 0.6167 | 9.0 | 60.4 | 0.305 |
| permutation_fullrank_n64_s31 | lowrank | 16 | 0.01 | None | 0.0220035 | 0.6426 | 0.7618 | 49.1 | 836.5 | 0.294 |
| permutation_fullrank_n64_s31 | nemos | None | 0.01 | 0.1 | 0.0312312 | 0.7866 | 0.6167 | 215.1 | 1307.8 | 0.494 |
| lowrank_n64_s47 | dense | None | 0.1 | None | 0.000958415 | 0.2950 | 0.9606 | 3.2 | 57.3 | 0.306 |
| lowrank_n64_s47 | lowrank | 2 | 0.01 | None | 0.00669658 | 0.7698 | 0.7128 | 15.7 | 803.6 | 0.296 |
| lowrank_n64_s47 | nemos | None | 0.1 | 1.0 | 0.000958225 | 0.2950 | 0.9606 | 13.7 | 1693.5 | 0.482 |
| permutation_fullrank_n64_s47 | dense | None | 0.01 | None | 0.0313343 | 0.7911 | 0.6121 | 13.0 | 63.4 | 0.304 |
| permutation_fullrank_n64_s47 | lowrank | 16 | 0.01 | None | 0.0222147 | 0.6502 | 0.7568 | 65.7 | 752.1 | 0.296 |
| permutation_fullrank_n64_s47 | nemos | None | 0.01 | 0.5 | 0.0313339 | 0.7911 | 0.6122 | 50.3 | 1307.1 | 0.490 |
| lowrank_n128_s31 | dense | None | 0.1 | None | 2.72649e-06 | 0.1545 | 0.9766 | 6.8 | 129.3 | 0.328 |
| lowrank_n128_s31 | lowrank | 2 | 0.01 | None | 0.00240575 | 0.6027 | 0.7728 | 31.2 | 1141.3 | 0.302 |
| lowrank_n128_s31 | nemos | None | 0.1 | 1.0 | 3.13195e-08 | 0.1538 | 0.9768 | 19.1 | 3761.1 | 0.519 |
| permutation_fullrank_n128_s31 | dense | None | 0.1 | None | 0.0140076 | 0.6445 | 0.8423 | 10.0 | 162.0 | 0.328 |
| permutation_fullrank_n128_s31 | lowrank | 16 | 0.1 | None | 0.00478865 | 0.3736 | 0.9510 | 37.5 | 1216.0 | 0.307 |
| permutation_fullrank_n128_s31 | nemos | None | 0.1 | 0.1 | 0.0140068 | 0.6445 | 0.8423 | 191.8 | 3256.3 | 0.517 |
| lowrank_n128_s47 | dense | None | 0.1 | None | 1.22765e-05 | 0.1495 | 0.9787 | 6.5 | 149.1 | 0.336 |
| lowrank_n128_s47 | lowrank | 2 | 0.01 | None | 0.00253489 | 0.5837 | 0.7937 | 43.4 | 2208.4 | 0.304 |
| lowrank_n128_s47 | nemos | None | 0.1 | 1.0 | 9.81227e-06 | 0.1490 | 0.9789 | 14.3 | 3426.8 | 0.489 |
| permutation_fullrank_n128_s47 | dense | None | 0.1 | None | 0.0142954 | 0.6480 | 0.8421 | 12.5 | 186.0 | 0.328 |
| permutation_fullrank_n128_s47 | lowrank | 16 | 0.1 | None | 0.00503344 | 0.3804 | 0.9502 | 49.2 | 1509.5 | 0.308 |
| permutation_fullrank_n128_s47 | nemos | None | 0.1 | 0.1 | 0.0142946 | 0.6480 | 0.8421 | 168.1 | 2850.2 | 0.512 |

Candidate outcomes: 256; execution failures: 22; gradient passes: 188.

Bits/spike are gains over training constant-rate predictions. Correlations are Pearson correlations of reconstructed filters, including diagonals. Low-rank gradient gates use factor coordinates. Timing includes compilation and differs across solver/search configurations; shared host. Do not interpret failures as generic library inferiority. Rank/penalty winners at search boundaries require new confirmation data before further tuning.

## Failure and convergence accounting

Of 256 candidates, 188 passed the convergence gate, 46 finished without passing it, 21 failed with nonfinite objective/gradient, and one timed out. All 24 model selections were available. See [the detailed audit](../failure_audit/README.md). The identical-settings timeout retry is supplementary; original outcomes remain unchanged.

## Identical-settings retry outcome

The timeout candidate finished in 126.7 seconds on retry, using 0.311 GiB peak RSS. It reached the 1500-iteration limit, with gradient infinity norm 9.87083e-05, above the 1e-5 gate. It remains ineligible. Validation log likelihood was -51.508607, compared with -50.513115 for the original selected rank-2, ridge-0.01 model (higher is better). No held-out test evaluation was performed for the retry, and no selected model or original candidate record changed.

Accounting with the supplementary retry: 188 converged, 47 completed without convergence, 21 numerical failures. Historical original accounting remains 188/46/21/1. This retry resolves the missing outcome without changing the comparison conclusions.


## StreamGLM failure audit
Source: /home/satvik/side_project/artifacts/v6/failure_audit/README.md

# Completed-grid failure audit

All 256 original candidate outcomes and all selected results are preserved.
Classification is based on per-candidate JSON, traceback logs and convergence gates.

| Backend | Converged | Finished, gate failed | Nonfinite objective/gradient | Timeout |
|---|---:|---:|---:|---:|
| dense | 32 | 0 | 0 | 0 |
| lowrank | 110 | 17 | 0 | 1 |
| nemos | 46 | 29 | 21 | 0 |

## Numerical failures

All 21 exceptions are NeMoS SVRG on the permutation-full-rank synthetic family. Sixteen use stepsize 1.0; five use 0.5. Every traceback ends in the independent full-objective check detecting a nonfinite objective/gradient. This supports instability at these tested settings, not a general failure of NeMoS. Smaller stepsizes were already included in the original grid; all eight NeMoS dataset groups selected a converged model. Do not silently replace divergent candidates with changed configurations.

## Timeout

The single timeout is lowrank_n128_s47/candidate04: rank 16, ridge 0, budget 1500. Supervisor wall duration was 1206.7 s against a 900 s limit, while the last saved progress reported 120.1 s and gradient infinity norm 6.969e-5 (above the 1e-5 gate). A system pause or clock discontinuity is possible; the available logs do not establish the cause. An identical-settings, fresh-initialization diagnostic retry is recorded separately in timeout_retry.json. It does not overwrite the original grid or change its selected models.

## Interpretation

188/256 original candidates passed the convergence gate. Another 46 finished but failed that gate; 22 failed execution. These categories must be reported separately. All 24 backend/dataset selections exist, so no dataset/backend comparison was lost. The comparison is conditional on the tested settings, budgets, implementation and two seeds, not a general solver ranking.

## Per-failure evidence

| Dataset | Candidate | Classification | Ridge | Step |
|---|---|---|---:|---:|
| lowrank_n128_s47 | candidate04 | timeout | 0.0 | None |
| permutation_fullrank_n128_s31 | candidate06 | nonfinite_objective_gradient | 0.0 | 0.5 |
| permutation_fullrank_n128_s31 | candidate07 | nonfinite_objective_gradient | 0.0 | 1.0 |
| permutation_fullrank_n128_s31 | candidate14 | nonfinite_objective_gradient | 0.001 | 0.5 |
| permutation_fullrank_n128_s31 | candidate15 | nonfinite_objective_gradient | 0.001 | 1.0 |
| permutation_fullrank_n128_s31 | candidate23 | nonfinite_objective_gradient | 0.01 | 1.0 |
| permutation_fullrank_n128_s31 | candidate31 | nonfinite_objective_gradient | 0.1 | 1.0 |
| permutation_fullrank_n128_s47 | candidate06 | nonfinite_objective_gradient | 0.0 | 0.5 |
| permutation_fullrank_n128_s47 | candidate07 | nonfinite_objective_gradient | 0.0 | 1.0 |
| permutation_fullrank_n128_s47 | candidate14 | nonfinite_objective_gradient | 0.001 | 0.5 |
| permutation_fullrank_n128_s47 | candidate15 | nonfinite_objective_gradient | 0.001 | 1.0 |
| permutation_fullrank_n128_s47 | candidate22 | nonfinite_objective_gradient | 0.01 | 0.5 |
| permutation_fullrank_n128_s47 | candidate23 | nonfinite_objective_gradient | 0.01 | 1.0 |
| permutation_fullrank_n128_s47 | candidate31 | nonfinite_objective_gradient | 0.1 | 1.0 |
| permutation_fullrank_n64_s31 | candidate07 | nonfinite_objective_gradient | 0.0 | 1.0 |
| permutation_fullrank_n64_s31 | candidate15 | nonfinite_objective_gradient | 0.001 | 1.0 |
| permutation_fullrank_n64_s31 | candidate23 | nonfinite_objective_gradient | 0.01 | 1.0 |
| permutation_fullrank_n64_s31 | candidate31 | nonfinite_objective_gradient | 0.1 | 1.0 |
| permutation_fullrank_n64_s47 | candidate07 | nonfinite_objective_gradient | 0.0 | 1.0 |
| permutation_fullrank_n64_s47 | candidate15 | nonfinite_objective_gradient | 0.001 | 1.0 |
| permutation_fullrank_n64_s47 | candidate23 | nonfinite_objective_gradient | 0.01 | 1.0 |
| permutation_fullrank_n64_s47 | candidate31 | nonfinite_objective_gradient | 0.1 | 1.0 |

## Identical-settings retry outcome

The timeout candidate finished in 126.7 seconds on retry, using 0.311 GiB peak RSS. It reached the 1500-iteration limit, with gradient infinity norm 9.87083e-05, above the 1e-5 gate. It remains ineligible. Validation log likelihood was -51.508607, compared with -50.513115 for the original selected rank-2, ridge-0.01 model (higher is better). No held-out test evaluation was performed for the retry, and no selected model or original candidate record changed.

Accounting with the supplementary retry: 188 converged, 47 completed without convergence, 21 numerical failures. Historical original accounting remains 188/46/21/1. This retry resolves the missing outcome without changing the comparison conclusions.


## Deterministic solver comparison
Source: /home/satvik/side_project/artifacts/v7/extended_dense/report.md

# Extended deterministic solver comparison

Fixed configuration; two seeds and two executions per worker. All measurements include the timing limitations in protocol.json.

| Neurons | Seed | Family | Backend | First s | Repeat s | Both pass gradient gate | Peak GiB |
|---|---|---|---|---:|---:|---|---:|
| 64 | 31 | lowrank | streamglm | 1.747 | 0.903 | True | 0.303 |
| 64 | 31 | lowrank | nemos | 7.901 | 2.176 | True | 0.639 |
| 64 | 31 | permutation_fullrank | streamglm | 4.251 | 3.716 | True | 0.306 |
| 64 | 31 | permutation_fullrank | nemos | 8.509 | 3.968 | True | 0.643 |
| 64 | 47 | lowrank | streamglm | 1.533 | 0.957 | True | 0.309 |
| 64 | 47 | lowrank | nemos | 6.653 | 2.093 | True | 0.647 |
| 64 | 47 | permutation_fullrank | streamglm | 4.877 | 4.146 | True | 0.312 |
| 64 | 47 | permutation_fullrank | nemos | 8.255 | 3.683 | True | 0.642 |
| 128 | 31 | lowrank | streamglm | 3.018 | 2.373 | True | 0.335 |
| 128 | 31 | lowrank | nemos | 8.764 | 3.989 | True | 0.710 |
| 128 | 31 | permutation_fullrank | streamglm | 10.554 | 10.057 | True | 0.340 |
| 128 | 31 | permutation_fullrank | nemos | 19.117 | 14.515 | True | 0.743 |
| 128 | 47 | lowrank | streamglm | 2.409 | 1.853 | True | 0.323 |
| 128 | 47 | lowrank | nemos | 8.723 | 4.031 | True | 0.724 |
| 128 | 47 | permutation_fullrank | streamglm | 13.017 | 12.498 | True | 0.338 |
| 128 | 47 | permutation_fullrank | nemos | 18.139 | 13.381 | True | 0.739 |


## Recording-length scaling
Source: /home/satvik/side_project/artifacts/v7/length_scaling/report.md

# Recording-length scaling pilot

Fixed configuration; one seed and two executions per worker. All measurements include the timing limitations in protocol.json.

| Bins | Seed | Family | Backend | First s | Repeat s | Both pass gradient gate | Peak GiB |
|---|---|---|---|---:|---:|---|---:|
| 24000 | 31 | lowrank | streamglm | 2.379 | 1.606 | True | 0.311 |
| 24000 | 31 | lowrank | nemos | 7.863 | 2.781 | True | 0.730 |
| 24000 | 31 | permutation_fullrank | streamglm | 7.446 | 6.436 | True | 0.315 |
| 24000 | 31 | permutation_fullrank | nemos | 11.489 | 6.545 | True | 0.723 |
| 48000 | 31 | lowrank | streamglm | 3.960 | 3.274 | True | 0.316 |
| 48000 | 31 | lowrank | nemos | 8.413 | 3.627 | True | 0.814 |
| 48000 | 31 | permutation_fullrank | streamglm | 13.007 | 12.867 | True | 0.309 |
| 48000 | 31 | permutation_fullrank | nemos | 14.459 | 9.781 | True | 0.879 |
| 96000 | 31 | lowrank | streamglm | 5.605 | 4.802 | True | 0.335 |
| 96000 | 31 | lowrank | nemos | 9.809 | 5.034 | True | 1.018 |
| 96000 | 31 | permutation_fullrank | streamglm | 22.125 | 21.315 | True | 0.332 |
| 96000 | 31 | permutation_fullrank | nemos | 21.120 | 16.682 | True | 1.020 |


1000-neuron null_1000_1h: 1623.017s,1.240784GiB,gain over self-history -0.000381805nats/bin. Rank5 gradient norm 3.3825254e-05; optimizer stopping is not a strict1e-5 certificate.

1000-neuron null_1000_1h_seed733: 1191.239s,1.268688GiB,gain over self-history -0.000180223nats/bin. Rank5 gradient norm 0.00015780236; optimizer stopping is not a strict1e-5 certificate.
