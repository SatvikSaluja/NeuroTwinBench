# NeuroTwinBench — complete results snapshot

Captured: 2026-09-24T12:51:43.830428+00:00

All values below come from saved artifacts. In-progress fits have no inferred results until checkpointed. Correlations are ranks of absolute anatomical weights versus absolute inferred filter areas, not percentages of recovered wiring.

## Scope and limitations

- Two completed grids, seeds 100 and 200; seed-100 baselines complete; seed-200 baselines partial at capture.
- Base seeds label groups of eight independently initialized 320 s simulations on fixed anatomy. Uncertainty is across input realizations, not circuit anatomies.
- Default dense-circuit results evaluate strength and sign of existing connections; they do not establish edge detection.
- AMPA/NMDA and proximal/distal classes can share the same pairs and the same total inferred influence; repeated numerical rows are not independent confirmations or receptor/location-specific recovery.
- Autapses excluded. Inhibitory weight ranks suppressed due to degenerate within-class anatomical spread; inhibitory sign scores retained.
- All proxy-drive fits reached the 500-iteration cap. Those comparisons are provisional. CPU/GPU or solver completion does not imply convergence.
- Full-population/true-drive baselines are available; other observation/drive conditions lack matched baselines.
- Only one jitter realization per completed baseline seed. No significance test or universal recovery threshold follows from these point estimates.
- Interneuron removal preserves the pyramidal-to-pyramidal candidate pairs, but changes conditioning. Random subsampling changes which pairs are evaluated; direct comparison needs a common pair set.
- Synthetic weight calibration used eight basis functions; current production uses five. That earlier calibration is not an exact configuration-matched certification of the reduced basis.

## Execution status

```json
{
  "status": "RUNNING",
  "step": "baselines_seed200",
  "runner_pid": 10193,
  "child_pid": 404162,
  "updated_unix": 1790254287.5467184,
  "elapsed_s": 10893.47752046585,
  "rss_gib": 7.67352294921875,
  "available_gib": 17.556686401367188,
  "log": "/home/satvik/hnn_neuro_bridge/results/handoff/baselines_seed200.log"
}
```

Elapsed since successful restart: 15 h 55 min. Excludes the interrupted earlier attempt.

| Completed stage | Wall time (seconds) |
| --- | --- |
| grid_seed100 | 8874 |
| report | 1 |
| figures | 2 |
| baselines_seed100 | 14617 |
| report | 1 |
| figures | 2 |
| latency | 37 |
| report | 1 |
| figures | 2 |
| simulate_seed200 | 15963 |
| grid_seed200 | 6892 |
| report | 1 |
| figures | 2 |

## Recording and fitting configuration

LBFGS, float32, five basis functions, 25 ms history, 1 ms bins, ridge strength 0.001, tolerance 1e-6, maximum 500 iterations. History never crosses an independent segment boundary.

| Seed | Neurons | Spikes | Predictors | Spikes/predictor | Mean Hz |
| --- | --- | --- | --- | --- | --- |
| 100 | 70 | 609567 | 355 | 24.5299 | 3.4016 |
| 200 | 70 | 610661 | 355 | 24.5739 | 3.4077 |

The synthetic 16.1 spikes/predictor observation is a reference budget, not a proven HNN sufficiency threshold.

## Every grid fit and convergence diagnostic

| Seed | Observed | Drive | Converged | Iterations | Penalized objective | Seconds | Peak GiB | Spikes/predictor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | full | true | True | 446 | 1.0386 | 1998 | 18.2738 | 24.5299 |
| 100 | full | proxy | False | 500 | 1.0380 | 2362 | 18.2842 | 24.5299 |
| 100 | full | hidden | True | 115 | 1.0387 | 520 | 18.0716 | 24.8803 |
| 100 | interneurons_hidden | true | True | 439 | 0.8140 | 848 | 13.4269 | 35.1259 |
| 100 | interneurons_hidden | proxy | False | 500 | 0.8136 | 939 | 13.4085 | 35.1259 |
| 100 | interneurons_hidden | hidden | True | 97 | 0.8142 | 193 | 13.1750 | 35.8284 |
| 100 | random_subsample | true | True | 435 | 0.7852 | 836 | 13.3577 | 34.2976 |
| 100 | random_subsample | proxy | False | 500 | 0.7846 | 955 | 13.3715 | 34.2976 |
| 100 | random_subsample | hidden | True | 92 | 0.7853 | 185 | 13.1692 | 34.9836 |
| 200 | full | true | True | 442 | 1.0385 | 1551 | 18.2960 | 24.5739 |
| 200 | full | proxy | False | 500 | 1.0382 | 1750 | 18.2856 | 24.5739 |
| 200 | full | hidden | True | 113 | 1.0387 | 412 | 18.0647 | 24.9249 |
| 200 | interneurons_hidden | true | True | 370 | 0.8146 | 579 | 13.4043 | 35.1995 |
| 200 | interneurons_hidden | proxy | False | 500 | 0.8143 | 802 | 13.3989 | 35.1995 |
| 200 | interneurons_hidden | hidden | True | 105 | 0.8148 | 172 | 13.1968 | 35.9035 |
| 200 | random_subsample | true | True | 415 | 0.7667 | 649 | 13.3797 | 33.1754 |
| 200 | random_subsample | proxy | False | 500 | 0.7664 | 783 | 13.4876 | 33.1754 |
| 200 | random_subsample | hidden | True | 94 | 0.7669 | 160 | 13.1753 | 33.8389 |

Objective values are not directly comparable across different observed populations.

## All grid results: every seed, condition and anatomical class

### Seed 100: full, drive=true

Converged: True. Observed gids: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.9200 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.9200 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.4760 | 250 | 0 | 0 | 0.0027 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7251 | 0.7702 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.3091 | 0.9815 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.3091 | 0.9815 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7050 | 0.8185 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1181 | 0.9984 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1181 | 0.9984 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3907 | 0.8589 | 248 | 2 | 0 | 0.5692 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4944 | 0.8557 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4944 | 0.8557 | 596 | 4 | 0 | 0.5354 |

### Seed 100: full, drive=proxy

Converged: False. Observed gids: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.9200 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.9200 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.4760 | 250 | 0 | 0 | 0.0027 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7246 | 0.7702 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.3096 | 0.9799 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.3096 | 0.9799 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7048 | 0.8185 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1179 | 0.9984 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1179 | 0.9984 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3920 | 0.8589 | 248 | 2 | 0 | 0.5692 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4944 | 0.8557 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4944 | 0.8557 | 596 | 4 | 0 | 0.5354 |

### Seed 100: full, drive=hidden

Converged: True. Observed gids: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.9200 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.9200 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.4760 | 250 | 0 | 0 | 0.0027 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7249 | 0.7702 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.3090 | 0.9815 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.3090 | 0.9815 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7050 | 0.8185 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1180 | 0.9984 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1180 | 0.9984 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3908 | 0.8589 | 248 | 2 | 0 | 0.5692 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4944 | 0.8557 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4944 | 0.8557 | 596 | 4 | 0 | 0.5354 |

### Seed 100: interneurons_hidden, drive=true

Converged: True. Observed gids: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2728 | 0.9161 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2728 | 0.9161 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L5_pyramidal / ampa / distal | -0.0705 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | -0.0705 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5069 | 0.8003 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5069 | 0.8003 | 596 | 4 | 0 | 0.5354 |

### Seed 100: interneurons_hidden, drive=proxy

Converged: False. Observed gids: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2745 | 0.9144 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2745 | 0.9144 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L5_pyramidal / ampa / distal | -0.0708 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | -0.0708 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5072 | 0.8003 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5072 | 0.8003 | 596 | 4 | 0 | 0.5354 |

### Seed 100: interneurons_hidden, drive=hidden

Converged: True. Observed gids: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2730 | 0.9161 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2730 | 0.9161 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L5_pyramidal / ampa / distal | -0.0704 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | -0.0704 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5068 | 0.8003 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5068 | 0.8003 | 596 | 4 | 0 | 0.5354 |

### Seed 100: random_subsample, drive=true

Converged: True. Observed gids: [0, 1, 2, 6, 7, 8, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30, 32, 35, 37, 38, 39, 41, 42, 44, 45, 48, 49, 50, 51, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 66, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 30 | 0 | 0 | 0.0172 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.9352 | 108 | 0 | 0 | 0.0027 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.9352 | 108 | 0 | 0 | 0.0027 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.5088 | 114 | 0 | 0 | 0.0029 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7667 | 0.8131 | 107 | 1 | 0 | 0.5761 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.1933 | 0.9901 | 304 | 2 | 0 | 0.5123 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.1933 | 0.9901 | 304 | 2 | 0 | 0.5123 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7247 | 0.8651 | 126 | 0 | 0 | 0.5590 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1214 | 1.0000 | 341 | 1 | 0 | 0.5368 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1214 | 1.0000 | 341 | 1 | 0 | 0.5368 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 42 | 0 | 0 | 0.0174 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.3459 | 133 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.3459 | 133 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3302 | 0.8788 | 132 | 1 | 0 | 0.5587 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5107 | 0.8676 | 340 | 2 | 0 | 0.5517 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5107 | 0.8676 | 340 | 2 | 0 | 0.5517 |

### Seed 100: random_subsample, drive=proxy

Converged: False. Observed gids: [0, 1, 2, 6, 7, 8, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30, 32, 35, 37, 38, 39, 41, 42, 44, 45, 48, 49, 50, 51, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 66, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 30 | 0 | 0 | 0.0172 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.9352 | 108 | 0 | 0 | 0.0027 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.9352 | 108 | 0 | 0 | 0.0027 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.5088 | 114 | 0 | 0 | 0.0029 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7649 | 0.8131 | 107 | 1 | 0 | 0.5761 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.1943 | 0.9901 | 304 | 2 | 0 | 0.5123 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.1943 | 0.9901 | 304 | 2 | 0 | 0.5123 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7241 | 0.8651 | 126 | 0 | 0 | 0.5590 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1207 | 1.0000 | 341 | 1 | 0 | 0.5368 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1207 | 1.0000 | 341 | 1 | 0 | 0.5368 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 42 | 0 | 0 | 0.0174 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.3459 | 133 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.3459 | 133 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3309 | 0.8788 | 132 | 1 | 0 | 0.5587 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5103 | 0.8706 | 340 | 2 | 0 | 0.5517 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5103 | 0.8706 | 340 | 2 | 0 | 0.5517 |

### Seed 100: random_subsample, drive=hidden

Converged: True. Observed gids: [0, 1, 2, 6, 7, 8, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 29, 30, 32, 35, 37, 38, 39, 41, 42, 44, 45, 48, 49, 50, 51, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 66, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 30 | 0 | 0 | 0.0172 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.9352 | 108 | 0 | 0 | 0.0027 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.9352 | 108 | 0 | 0 | 0.0027 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.5088 | 114 | 0 | 0 | 0.0029 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7668 | 0.8131 | 107 | 1 | 0 | 0.5761 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.1935 | 0.9901 | 304 | 2 | 0 | 0.5123 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.1935 | 0.9901 | 304 | 2 | 0 | 0.5123 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7250 | 0.8651 | 126 | 0 | 0 | 0.5590 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1212 | 1.0000 | 341 | 1 | 0 | 0.5368 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1212 | 1.0000 | 341 | 1 | 0 | 0.5368 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 42 | 0 | 0 | 0.0174 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.3459 | 133 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.3459 | 133 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3294 | 0.8788 | 132 | 1 | 0 | 0.5587 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5105 | 0.8676 | 340 | 2 | 0 | 0.5517 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5105 | 0.8676 | 340 | 2 | 0 | 0.5517 |

### Seed 200: full, drive=true

Converged: True. Observed gids: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.9240 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.9240 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.4800 | 250 | 0 | 0 | 0.0027 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7244 | 0.7621 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.3126 | 0.9748 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.3126 | 0.9748 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | 0.6984 | 0.8065 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.0989 | 0.9968 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.0989 | 0.9968 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3842 | 0.8468 | 248 | 2 | 0 | 0.5692 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4929 | 0.8523 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4929 | 0.8523 | 596 | 4 | 0 | 0.5354 |

### Seed 200: full, drive=proxy

Converged: False. Observed gids: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.9240 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.9240 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.4800 | 250 | 0 | 0 | 0.0027 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7240 | 0.7621 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.3130 | 0.9748 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.3130 | 0.9748 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | 0.6980 | 0.8024 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.0991 | 0.9968 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.0991 | 0.9968 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3840 | 0.8468 | 248 | 2 | 0 | 0.5692 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4928 | 0.8507 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4928 | 0.8507 | 596 | 4 | 0 | 0.5354 |

### Seed 200: full, drive=hidden

Converged: True. Observed gids: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.9240 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.9240 | 250 | 0 | 0 | 0.0027 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.4800 | 250 | 0 | 0 | 0.0027 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7244 | 0.7621 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.3127 | 0.9748 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.3127 | 0.9748 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | 0.6986 | 0.8065 | 248 | 2 | 0 | 0.5692 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.0990 | 0.9968 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.0990 | 0.9968 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 90 | 0 | 0 | 0.0169 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.4080 | 250 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3843 | 0.8468 | 248 | 2 | 0 | 0.5692 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4930 | 0.8523 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4930 | 0.8523 | 596 | 4 | 0 | 0.5354 |

### Seed 200: interneurons_hidden, drive=true

Converged: True. Observed gids: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2802 | 0.9144 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2802 | 0.9144 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L5_pyramidal / ampa / distal | -0.0849 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | -0.0849 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4988 | 0.7903 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4988 | 0.7903 | 596 | 4 | 0 | 0.5354 |

### Seed 200: interneurons_hidden, drive=proxy

Converged: False. Observed gids: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2813 | 0.9128 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2813 | 0.9128 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L5_pyramidal / ampa / distal | -0.0850 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | -0.0850 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4991 | 0.7903 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4991 | 0.7903 | 596 | 4 | 0 | 0.5354 |

### Seed 200: interneurons_hidden, drive=hidden

Converged: True. Observed gids: [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2801 | 0.9144 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2801 | 0.9144 | 596 | 4 | 0 | 0.5354 |
| L2_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L2_pyramidal->L5_pyramidal / ampa / distal | -0.0848 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | -0.0848 | 1.0000 | 621 | 4 | 0 | 0.5403 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0 | 0 | — |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_basket / ampa / soma | — | — | 0 | 0 | 0 | — |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4989 | 0.7903 | 596 | 4 | 0 | 0.5354 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4989 | 0.7903 | 596 | 4 | 0 | 0.5354 |

### Seed 200: random_subsample, drive=true

Converged: True. Observed gids: [0, 2, 4, 5, 7, 8, 10, 13, 14, 15, 16, 17, 18, 25, 26, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 30 | 0 | 0 | 0.0167 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.8778 | 90 | 0 | 0 | 0.0030 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.8778 | 90 | 0 | 0 | 0.0030 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.4083 | 120 | 0 | 0 | 0.0029 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7870 | 0.8427 | 89 | 1 | 0 | 0.6209 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2367 | 0.9760 | 208 | 2 | 0 | 0.5934 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2367 | 0.9760 | 208 | 2 | 0 | 0.5934 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7630 | 0.8657 | 134 | 1 | 0 | 0.6368 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1585 | 1.0000 | 297 | 3 | 0 | 0.5674 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1585 | 1.0000 | 297 | 3 | 0 | 0.5674 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 72 | 0 | 0 | 0.0175 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.4000 | 180 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.4000 | 180 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3981 | 0.8876 | 178 | 2 | 0 | 0.5941 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5071 | 0.8830 | 376 | 4 | 0 | 0.5497 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5071 | 0.8830 | 376 | 4 | 0 | 0.5497 |

### Seed 200: random_subsample, drive=proxy

Converged: False. Observed gids: [0, 2, 4, 5, 7, 8, 10, 13, 14, 15, 16, 17, 18, 25, 26, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 30 | 0 | 0 | 0.0167 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.8778 | 90 | 0 | 0 | 0.0030 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.8778 | 90 | 0 | 0 | 0.0030 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.4083 | 120 | 0 | 0 | 0.0029 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7863 | 0.8427 | 89 | 1 | 0 | 0.6209 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2370 | 0.9760 | 208 | 2 | 0 | 0.5934 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2370 | 0.9760 | 208 | 2 | 0 | 0.5934 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7623 | 0.8657 | 134 | 1 | 0 | 0.6368 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1584 | 1.0000 | 297 | 3 | 0 | 0.5674 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1584 | 1.0000 | 297 | 3 | 0 | 0.5674 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 72 | 0 | 0 | 0.0175 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.4000 | 180 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.4000 | 180 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3970 | 0.8876 | 178 | 2 | 0 | 0.5941 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5073 | 0.8803 | 376 | 4 | 0 | 0.5497 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5073 | 0.8803 | 376 | 4 | 0 | 0.5497 |

### Seed 200: random_subsample, drive=hidden

Converged: True. Observed gids: [0, 2, 4, 5, 7, 8, 10, 13, 14, 15, 16, 17, 18, 25, 26, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 52, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 69]

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable | Anatomical weight CV |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 1.0000 | 30 | 0 | 0 | 0.0167 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.8778 | 90 | 0 | 0 | 0.0030 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.8778 | 90 | 0 | 0 | 0.0030 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.4083 | 120 | 0 | 0 | 0.0029 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7870 | 0.8427 | 89 | 1 | 0 | 0.6209 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2367 | 0.9760 | 208 | 2 | 0 | 0.5934 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2367 | 0.9760 | 208 | 2 | 0 | 0.5934 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7623 | 0.8657 | 134 | 1 | 0 | 0.6368 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1587 | 1.0000 | 297 | 3 | 0 | 0.5674 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1587 | 1.0000 | 297 | 3 | 0 | 0.5674 |
| L5_basket->L5_basket / gabaa / soma | — | 1.0000 | 72 | 0 | 0 | 0.0175 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.4000 | 180 | 0 | 0 | 0.0014 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.4000 | 180 | 0 | 0 | 0.0014 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3981 | 0.8876 | 178 | 2 | 0 | 0.5941 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5071 | 0.8830 | 376 | 4 | 0 | 0.5497 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5071 | 0.8830 | 376 | 4 | 0 | 0.5497 |

## Across-seed grid summaries

Sample SD uses ddof=1. Two seeds give descriptive variability only; they do not establish precise confidence bounds.

### full/true

| Class | Mean rho | SD rho | Rank seeds | Mean sign accuracy | SD sign | Sign seeds |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0.9220 | 0.0028 | 2 |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0.9220 | 0.0028 | 2 |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0.4780 | 0.0028 | 2 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7247 | 0.0005 | 2 | 0.7661 | 0.0057 | 2 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.3108 | 0.0025 | 2 | 0.9782 | 0.0047 | 2 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.3108 | 0.0025 | 2 | 0.9782 | 0.0047 | 2 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7017 | 0.0047 | 2 | 0.8125 | 0.0086 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1085 | 0.0136 | 2 | 0.9976 | 0.0011 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1085 | 0.0136 | 2 | 0.9976 | 0.0011 | 2 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0.4080 | 0.0000 | 2 |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0.4080 | 0.0000 | 2 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3875 | 0.0046 | 2 | 0.8528 | 0.0086 | 2 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4936 | 0.0011 | 2 | 0.8540 | 0.0024 | 2 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4936 | 0.0011 | 2 | 0.8540 | 0.0024 | 2 |

### full/proxy

| Class | Mean rho | SD rho | Rank seeds | Mean sign accuracy | SD sign | Sign seeds |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0.9220 | 0.0028 | 2 |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0.9220 | 0.0028 | 2 |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0.4780 | 0.0028 | 2 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7243 | 0.0004 | 2 | 0.7661 | 0.0057 | 2 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.3113 | 0.0024 | 2 | 0.9773 | 0.0036 | 2 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.3113 | 0.0024 | 2 | 0.9773 | 0.0036 | 2 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7014 | 0.0048 | 2 | 0.8105 | 0.0114 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1085 | 0.0133 | 2 | 0.9976 | 0.0011 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1085 | 0.0133 | 2 | 0.9976 | 0.0011 | 2 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0.4080 | 0.0000 | 2 |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0.4080 | 0.0000 | 2 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3880 | 0.0057 | 2 | 0.8528 | 0.0086 | 2 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4936 | 0.0012 | 2 | 0.8532 | 0.0036 | 2 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4936 | 0.0012 | 2 | 0.8532 | 0.0036 | 2 |

### full/hidden

| Class | Mean rho | SD rho | Rank seeds | Mean sign accuracy | SD sign | Sign seeds |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0.9220 | 0.0028 | 2 |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0.9220 | 0.0028 | 2 |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0.4780 | 0.0028 | 2 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7246 | 0.0003 | 2 | 0.7661 | 0.0057 | 2 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.3109 | 0.0026 | 2 | 0.9782 | 0.0047 | 2 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.3109 | 0.0026 | 2 | 0.9782 | 0.0047 | 2 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7018 | 0.0046 | 2 | 0.8125 | 0.0086 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1085 | 0.0134 | 2 | 0.9976 | 0.0011 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1085 | 0.0134 | 2 | 0.9976 | 0.0011 | 2 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0.4080 | 0.0000 | 2 |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0.4080 | 0.0000 | 2 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3875 | 0.0046 | 2 | 0.8528 | 0.0086 | 2 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4937 | 0.0010 | 2 | 0.8540 | 0.0024 | 2 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4937 | 0.0010 | 2 | 0.8540 | 0.0024 | 2 |

### interneurons_hidden/true

| Class | Mean rho | SD rho | Rank seeds | Mean sign accuracy | SD sign | Sign seeds |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | — | — | 0 |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | — | — | 0 |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | — | — | 0 |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | — | — | 0 |
| L2_pyramidal->L2_basket / ampa / soma | — | — | 0 | — | — | 0 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2765 | 0.0052 | 2 | 0.9153 | 0.0012 | 2 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2765 | 0.0052 | 2 | 0.9153 | 0.0012 | 2 |
| L2_pyramidal->L5_basket / ampa / soma | — | — | 0 | — | — | 0 |
| L2_pyramidal->L5_pyramidal / ampa / distal | -0.0777 | 0.0102 | 2 | 1.0000 | 0.0000 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | -0.0777 | 0.0102 | 2 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | — | — | 0 |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | — | — | 0 |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | — | — | 0 |
| L5_pyramidal->L5_basket / ampa / soma | — | — | 0 | — | — | 0 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5029 | 0.0057 | 2 | 0.7953 | 0.0071 | 2 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5029 | 0.0057 | 2 | 0.7953 | 0.0071 | 2 |

### interneurons_hidden/proxy

| Class | Mean rho | SD rho | Rank seeds | Mean sign accuracy | SD sign | Sign seeds |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | — | — | 0 |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | — | — | 0 |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | — | — | 0 |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | — | — | 0 |
| L2_pyramidal->L2_basket / ampa / soma | — | — | 0 | — | — | 0 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2779 | 0.0048 | 2 | 0.9136 | 0.0012 | 2 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2779 | 0.0048 | 2 | 0.9136 | 0.0012 | 2 |
| L2_pyramidal->L5_basket / ampa / soma | — | — | 0 | — | — | 0 |
| L2_pyramidal->L5_pyramidal / ampa / distal | -0.0779 | 0.0100 | 2 | 1.0000 | 0.0000 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | -0.0779 | 0.0100 | 2 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | — | — | 0 |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | — | — | 0 |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | — | — | 0 |
| L5_pyramidal->L5_basket / ampa / soma | — | — | 0 | — | — | 0 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5032 | 0.0058 | 2 | 0.7953 | 0.0071 | 2 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5032 | 0.0058 | 2 | 0.7953 | 0.0071 | 2 |

### interneurons_hidden/hidden

| Class | Mean rho | SD rho | Rank seeds | Mean sign accuracy | SD sign | Sign seeds |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | — | — | 0 |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | — | — | 0 |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | — | — | 0 |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | — | — | 0 |
| L2_pyramidal->L2_basket / ampa / soma | — | — | 0 | — | — | 0 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2765 | 0.0051 | 2 | 0.9153 | 0.0012 | 2 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2765 | 0.0051 | 2 | 0.9153 | 0.0012 | 2 |
| L2_pyramidal->L5_basket / ampa / soma | — | — | 0 | — | — | 0 |
| L2_pyramidal->L5_pyramidal / ampa / distal | -0.0776 | 0.0102 | 2 | 1.0000 | 0.0000 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | -0.0776 | 0.0102 | 2 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | — | — | 0 |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | — | — | 0 |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | — | — | 0 |
| L5_pyramidal->L5_basket / ampa / soma | — | — | 0 | — | — | 0 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5029 | 0.0056 | 2 | 0.7953 | 0.0071 | 2 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5029 | 0.0056 | 2 | 0.7953 | 0.0071 | 2 |

### random_subsample/true

| Class | Mean rho | SD rho | Rank seeds | Mean sign accuracy | SD sign | Sign seeds |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0.9065 | 0.0406 | 2 |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0.9065 | 0.0406 | 2 |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0.4586 | 0.0710 | 2 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7768 | 0.0143 | 2 | 0.8279 | 0.0209 | 2 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2150 | 0.0307 | 2 | 0.9830 | 0.0100 | 2 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2150 | 0.0307 | 2 | 0.9830 | 0.0100 | 2 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7438 | 0.0271 | 2 | 0.8654 | 0.0004 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1399 | 0.0262 | 2 | 1.0000 | 0.0000 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1399 | 0.0262 | 2 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0.3729 | 0.0383 | 2 |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0.3729 | 0.0383 | 2 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3641 | 0.0480 | 2 | 0.8832 | 0.0063 | 2 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5089 | 0.0025 | 2 | 0.8753 | 0.0108 | 2 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5089 | 0.0025 | 2 | 0.8753 | 0.0108 | 2 |

### random_subsample/proxy

| Class | Mean rho | SD rho | Rank seeds | Mean sign accuracy | SD sign | Sign seeds |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0.9065 | 0.0406 | 2 |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0.9065 | 0.0406 | 2 |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0.4586 | 0.0710 | 2 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7756 | 0.0151 | 2 | 0.8279 | 0.0209 | 2 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2156 | 0.0302 | 2 | 0.9830 | 0.0100 | 2 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2156 | 0.0302 | 2 | 0.9830 | 0.0100 | 2 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7432 | 0.0270 | 2 | 0.8654 | 0.0004 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1395 | 0.0266 | 2 | 1.0000 | 0.0000 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1395 | 0.0266 | 2 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0.3729 | 0.0383 | 2 |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0.3729 | 0.0383 | 2 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3639 | 0.0468 | 2 | 0.8832 | 0.0063 | 2 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5088 | 0.0021 | 2 | 0.8755 | 0.0069 | 2 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5088 | 0.0021 | 2 | 0.8755 | 0.0069 | 2 |

### random_subsample/hidden

| Class | Mean rho | SD rho | Rank seeds | Mean sign accuracy | SD sign | Sign seeds |
| --- | --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L2_basket->L2_pyramidal / gabaa / soma | — | — | 0 | 0.9065 | 0.0406 | 2 |
| L2_basket->L2_pyramidal / gabab / soma | — | — | 0 | 0.9065 | 0.0406 | 2 |
| L2_basket->L5_pyramidal / gabaa / distal | — | — | 0 | 0.4586 | 0.0710 | 2 |
| L2_pyramidal->L2_basket / ampa / soma | 0.7769 | 0.0143 | 2 | 0.8279 | 0.0209 | 2 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.2151 | 0.0306 | 2 | 0.9830 | 0.0100 | 2 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.2151 | 0.0306 | 2 | 0.9830 | 0.0100 | 2 |
| L2_pyramidal->L5_basket / ampa / soma | 0.7437 | 0.0264 | 2 | 0.8654 | 0.0004 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.1399 | 0.0265 | 2 | 1.0000 | 0.0000 | 2 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.1399 | 0.0265 | 2 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_basket / gabaa / soma | — | — | 0 | 1.0000 | 0.0000 | 2 |
| L5_basket->L5_pyramidal / gabaa / soma | — | — | 0 | 0.3729 | 0.0383 | 2 |
| L5_basket->L5_pyramidal / gabab / soma | — | — | 0 | 0.3729 | 0.0383 | 2 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3638 | 0.0486 | 2 | 0.8832 | 0.0063 | 2 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.5088 | 0.0024 | 2 | 0.8753 | 0.0108 | 2 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.5088 | 0.0024 | 2 | 0.8753 | 0.0108 | 2 |

## All completed baselines

Pairwise and jitter GLMs include true-drive covariates. Pairwise uses the source history; it does not condition on all other neurons. CCG is a lagged-covariance peak baseline, not a fitted GLM. Jitter displaces spikes by up to ±50 ms within each segment, with counts conserved.

### Seed 100: ccg

Wall time: 24.9s; peak RSS: 0.811 GiB; converged: None.

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable |
| --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 0.0000 | 90 | 0 | 0 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.0000 | 250 | 0 | 0 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.0000 | 250 | 0 | 0 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.0000 | 250 | 0 | 0 |
| L2_pyramidal->L2_basket / ampa / soma | 0.4879 | 1.0000 | 248 | 2 | 0 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.4613 | 1.0000 | 596 | 4 | 0 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.4613 | 1.0000 | 596 | 4 | 0 |
| L2_pyramidal->L5_basket / ampa / soma | 0.3430 | 1.0000 | 248 | 2 | 0 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.5092 | 1.0000 | 621 | 4 | 0 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.5092 | 1.0000 | 621 | 4 | 0 |
| L5_basket->L5_basket / gabaa / soma | — | 0.0000 | 90 | 0 | 0 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.0000 | 250 | 0 | 0 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.0000 | 250 | 0 | 0 |
| L5_pyramidal->L5_basket / ampa / soma | 0.5776 | 1.0000 | 248 | 2 | 0 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.6385 | 1.0000 | 596 | 4 | 0 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.6385 | 1.0000 | 596 | 4 | 0 |

### Seed 100: pairwise

Wall time: 13092.0s; peak RSS: 7.649 GiB; converged: True.

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable |
| --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 0.1111 | 90 | 0 | 0 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.0160 | 250 | 0 | 0 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.0160 | 250 | 0 | 0 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.0000 | 250 | 0 | 0 |
| L2_pyramidal->L2_basket / ampa / soma | 0.6871 | 1.0000 | 248 | 2 | 0 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.0471 | 1.0000 | 596 | 4 | 0 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.0471 | 1.0000 | 596 | 4 | 0 |
| L2_pyramidal->L5_basket / ampa / soma | 0.5845 | 1.0000 | 248 | 2 | 0 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.3176 | 1.0000 | 621 | 4 | 0 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.3176 | 1.0000 | 621 | 4 | 0 |
| L5_basket->L5_basket / gabaa / soma | — | 0.1333 | 90 | 0 | 0 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.0000 | 250 | 0 | 0 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.0000 | 250 | 0 | 0 |
| L5_pyramidal->L5_basket / ampa / soma | 0.3896 | 1.0000 | 248 | 2 | 0 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.4680 | 1.0000 | 596 | 4 | 0 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.4680 | 1.0000 | 596 | 4 | 0 |

Diagnostics:
```json
{
  "per_source": {
    "0": {
      "function_val": 1.5701295137405396,
      "num_steps": 283,
      "converged": true,
      "reached_max_steps": false
    },
    "1": {
      "function_val": 1.558927297592163,
      "num_steps": 287,
      "converged": true,
      "reached_max_steps": false
    },
    "2": {
      "function_val": 1.5373183488845825,
      "num_steps": 297,
      "converged": true,
      "reached_max_steps": false
    },
    "3": {
      "function_val": 1.5584946870803833,
      "num_steps": 340,
      "converged": true,
      "reached_max_steps": false
    },
    "4": {
      "function_val": 1.5521043539047241,
      "num_steps": 318,
      "converged": true,
      "reached_max_steps": false
    },
    "5": {
      "function_val": 1.5266879796981812,
      "num_steps": 300,
      "converged": true,
      "reached_max_steps": false
    },
    "6": {
      "function_val": 1.537366271018982,
      "num_steps": 287,
      "converged": true,
      "reached_max_steps": false
    },
    "7": {
      "function_val": 1.5584787130355835,
      "num_steps": 314,
      "converged": true,
      "reached_max_steps": false
    },
    "8": {
      "function_val": 1.569940447807312,
      "num_steps": 312,
      "converged": true,
      "reached_max_steps": false
    },
    "9": {
      "function_val": 1.5584547519683838,
      "num_steps": 311,
      "converged": true,
      "reached_max_steps": false
    },
    "10": {
      "function_val": 1.542673945426941,
      "num_steps": 300,
      "converged": true,
      "reached_max_steps": false
    },
    "11": {
      "function_val": 1.5240246057510376,
      "num_steps": 315,
      "converged": true,
      "reached_max_steps": false
    },
    "12": {
      "function_val": 1.5112764835357666,
      "num_steps": 282,
      "converged": true,
      "reached_max_steps": false
    },
    "13": {
      "function_val": 1.5235410928726196,
      "num_steps": 306,
      "converged": true,
      "reached_max_steps": false
    },
    "14": {
      "function_val": 1.5429874658584595,
      "num_steps": 312,
      "converged": true,
      "reached_max_steps": false
    },
    "15": {
      "function_val": 1.5236873626708984,
      "num_steps": 335,
      "converged": true,
      "reached_max_steps": false
    },
    "16": {
      "function_val": 1.4786268472671509,
      "num_steps": 313,
      "converged": true,
      "reached_max_steps": false
    },
    "17": {
      "function_val": 1.457667589187622,
      "num_steps": 307,
      "converged": true,
      "reached_max_steps": false
    },
    "18": {
      "function_val": 1.479514241218567,
      "num_steps": 318,
      "converged": true,
      "reached_max_steps": false
    },
    "19": {
      "function_val": 1.5233817100524902,
      "num_steps": 309,
      "converged": true,
      "reached_max_steps": false
    },
    "20": {
      "function_val": 1.5119080543518066,
      "num_steps": 312,
      "converged": true,
      "reached_max_steps": false
    },
    "21": {
      "function_val": 1.4586759805679321,
      "num_steps": 327,
      "converged": true,
      "reached_max_steps": false
    },
    "22": {
      "function_val": 1.4401518106460571,
      "num_steps": 370,
      "converged": true,
      "reached_max_steps": false
    },
    "23": {
      "function_val": 1.4584522247314453,
      "num_steps": 339,
      "converged": true,
      "reached_max_steps": false
    },
    "24": {
      "function_val": 1.5117287635803223,
      "num_steps": 312,
      "converged": true,
      "reached_max_steps": false
    },
    "25": {
      "function_val": 1.5249820947647095,
      "num_steps": 308,
      "converged": true,
      "reached_max_steps": false
    },
    "26": {
      "function_val": 1.4821455478668213,
      "num_steps": 306,
      "converged": true,
      "reached_max_steps": false
    },
    "27": {
      "function_val": 1.4599612951278687,
      "num_steps": 294,
      "converged": true,
      "reached_max_steps": false
    },
    "28": {
      "function_val": 1.4808930158615112,
      "num_steps": 299,
      "converged": true,
      "reached_max_steps": false
    },
    "29": {
      "function_val": 1.5247465372085571,
      "num_steps": 303,
      "converged": true,
      "reached_max_steps": false
    },
    "30": {
      "function_val": 1.5427711009979248,
      "num_steps": 284,
      "converged": true,
      "reached_max_steps": false
    },
    "31": {
      "function_val": 1.5237263441085815,
      "num_steps": 298,
      "converged": true,
      "reached_max_steps": false
    },
    "32": {
      "function_val": 1.509997844696045,
      "num_steps": 318,
      "converged": true,
      "reached_max_steps": false
    },
    "33": {
      "function_val": 1.523711085319519,
      "num_steps": 305,
      "converged": true,
      "reached_max_steps": false
    },
    "34": {
      "function_val": 1.5424399375915527,
      "num_steps": 306,
      "converged": true,
      "reached_max_steps": false
    },
    "35": {
      "function_val": 1.5759912729263306,
      "num_steps": 278,
      "converged": true,
      "reached_max_steps": false
    },
    "36": {
      "function_val": 1.5633858442306519,
      "num_steps": 295,
      "converged": true,
      "reached_max_steps": false
    },
    "37": {
      "function_val": 1.5365225076675415,
      "num_steps": 286,
      "converged": true,
      "reached_max_steps": false
    },
    "38": {
      "function_val": 1.5630857944488525,
      "num_steps": 327,
      "converged": true,
      "reached_max_steps": false
    },
    "39": {
      "function_val": 1.5540525913238525,
      "num_steps": 306,
      "converged": true,
      "reached_max_steps": false
    },
    "40": {
      "function_val": 1.5278464555740356,
      "num_steps": 280,
      "converged": true,
      "reached_max_steps": false
    },
    "41": {
      "function_val": 1.5367792844772339,
      "num_steps": 322,
      "converged": true,
      "reached_max_steps": false
    },
    "42": {
      "function_val": 1.5630115270614624,
      "num_steps": 303,
      "converged": true,
      "reached_max_steps": false
    },
    "43": {
      "function_val": 1.5758554935455322,
      "num_steps": 289,
      "converged": true,
      "reached_max_steps": false
    },
    "44": {
      "function_val": 1.5636035203933716,
      "num_steps": 311,
      "converged": true,
      "reached_max_steps": false
    },
    "45": {
      "function_val": 1.577812671661377,
      "num_steps": 272,
      "converged": true,
      "reached_max_steps": false
    },
    "46": {
      "function_val": 1.5648775100708008,
      "num_steps": 300,
      "converged": true,
      "reached_max_steps": false
    },
    "47": {
      "function_val": 1.5534398555755615,
      "num_steps": 332,
      "converged": true,
      "reached_max_steps": false
    },
    "48": {
      "function_val": 1.5645842552185059,
      "num_steps": 304,
      "converged": true,
      "reached_max_steps": false
    },
    "49": {
      "function_val": 1.577606201171875,
      "num_steps": 308,
      "converged": true,
      "reached_max_steps": false
    },
    "50": {
      "function_val": 1.5650691986083984,
      "num_steps": 286,
      "converged": true,
      "reached_max_steps": false
    },
    "51": {
      "function_val": 1.524723768234253,
      "num_steps": 344,
      "converged": true,
      "reached_max_steps": false
    },
    "52": {
      "function_val": 1.5125300884246826,
      "num_steps": 335,
      "converged": true,
      "reached_max_steps": false
    },
    "53": {
      "function_val": 1.5247060060501099,
      "num_steps": 336,
      "converged": true,
      "reached_max_steps": false
    },
    "54": {
      "function_val": 1.5647761821746826,
      "num_steps": 282,
      "converged": true,
      "reached_max_steps": false
    },
    "55": {
      "function_val": 1.555175542831421,
      "num_steps": 299,
      "converged": true,
      "reached_max_steps": false
    },
    "56": {
      "function_val": 1.51333487033844,
      "num_steps": 301,
      "converged": true,
      "reached_max_steps": false
    },
    "57": {
      "function_val": 1.5000677108764648,
      "num_steps": 325,
      "converged": true,
      "reached_max_steps": false
    },
    "58": {
      "function_val": 1.5129106044769287,
      "num_steps": 332,
      "converged": true,
      "reached_max_steps": false
    },
    "59": {
      "function_val": 1.5549348592758179,
      "num_steps": 318,
      "converged": true,
      "reached_max_steps": false
    },
    "60": {
      "function_val": 1.5661436319351196,
      "num_steps": 312,
      "converged": true,
      "reached_max_steps": false
    },
    "61": {
      "function_val": 1.5261954069137573,
      "num_steps": 290,
      "converged": true,
      "reached_max_steps": false
    },
    "62": {
      "function_val": 1.5130221843719482,
      "num_steps": 365,
      "converged": true,
      "reached_max_steps": false
    },
    "63": {
      "function_val": 1.5260385274887085,
      "num_steps": 318,
      "converged": true,
      "reached_max_steps": false
    },
    "64": {
      "function_val": 1.5659925937652588,
      "num_steps": 289,
      "converged": true,
      "reached_max_steps": false
    },
    "65": {
      "function_val": 1.5774335861206055,
      "num_steps": 315,
      "converged": true,
      "reached_max_steps": false
    },
    "66": {
      "function_val": 1.5647591352462769,
      "num_steps": 309,
      "converged": true,
      "reached_max_steps": false
    },
    "67": {
      "function_val": 1.5557060241699219,
      "num_steps": 287,
      "converged": true,
      "reached_max_steps": false
    },
    "68": {
      "function_val": 1.564873456954956,
      "num_steps": 296,
      "converged": true,
      "reached_max_steps": false
    },
    "69": {
      "function_val": 1.5773687362670898,
      "num_steps": 294,
      "converged": true,
      "reached_max_steps": false
    }
  },
  "converged": true
}
```

### Seed 100: jitter

Wall time: 1491.9s; peak RSS: 18.269 GiB; converged: True.

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable |
| --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 0.0000 | 90 | 0 | 0 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.0000 | 250 | 0 | 0 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.0000 | 250 | 0 | 0 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.0000 | 250 | 0 | 0 |
| L2_pyramidal->L2_basket / ampa / soma | 0.5944 | 1.0000 | 248 | 2 | 0 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.4944 | 1.0000 | 596 | 4 | 0 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.4944 | 1.0000 | 596 | 4 | 0 |
| L2_pyramidal->L5_basket / ampa / soma | 0.5571 | 1.0000 | 248 | 2 | 0 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.5327 | 1.0000 | 621 | 4 | 0 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.5327 | 1.0000 | 621 | 4 | 0 |
| L5_basket->L5_basket / gabaa / soma | — | 0.0000 | 90 | 0 | 0 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.0000 | 250 | 0 | 0 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.0000 | 250 | 0 | 0 |
| L5_pyramidal->L5_basket / ampa / soma | 0.5397 | 1.0000 | 248 | 2 | 0 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.6333 | 1.0000 | 596 | 4 | 0 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.6333 | 1.0000 | 596 | 4 | 0 |

Diagnostics:
```json
{
  "function_val": 1.45742666721344,
  "num_steps": 412,
  "converged": true,
  "reached_max_steps": false
}
```

### Seed 200: ccg

Wall time: 22.5s; peak RSS: 0.811 GiB; converged: None.

| Class | Weight rho | Sign accuracy | Evaluated | Outside window | Unestimable |
| --- | --- | --- | --- | --- | --- |
| L2_basket->L2_basket / gabaa / soma | — | 0.0000 | 90 | 0 | 0 |
| L2_basket->L2_pyramidal / gabaa / soma | — | 0.0000 | 250 | 0 | 0 |
| L2_basket->L2_pyramidal / gabab / soma | — | 0.0000 | 250 | 0 | 0 |
| L2_basket->L5_pyramidal / gabaa / distal | — | 0.0000 | 250 | 0 | 0 |
| L2_pyramidal->L2_basket / ampa / soma | 0.4853 | 1.0000 | 248 | 2 | 0 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 0.4653 | 1.0000 | 596 | 4 | 0 |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 0.4653 | 1.0000 | 596 | 4 | 0 |
| L2_pyramidal->L5_basket / ampa / soma | 0.3406 | 1.0000 | 248 | 2 | 0 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 0.5075 | 1.0000 | 621 | 4 | 0 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 0.5075 | 1.0000 | 621 | 4 | 0 |
| L5_basket->L5_basket / gabaa / soma | — | 0.0000 | 90 | 0 | 0 |
| L5_basket->L5_pyramidal / gabaa / soma | — | 0.0000 | 250 | 0 | 0 |
| L5_basket->L5_pyramidal / gabab / soma | — | 0.0000 | 250 | 0 | 0 |
| L5_pyramidal->L5_basket / ampa / soma | 0.5761 | 1.0000 | 248 | 2 | 0 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 0.6370 | 1.0000 | 596 | 4 | 0 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 0.6370 | 1.0000 | 596 | 4 | 0 |

## Matched latency calibration

| True lag ms | Recovered median ms | Across-edge SD ms |
| --- | --- | --- |
| 1 | 3.5000 | 2.2463 |
| 2 | 4.0000 | 2.0554 |
| 4 | 4.0000 | 1.6456 |
| 7 | 6.0000 | 1.4888 |

All fits converged: True. Smallest resolved adjacent separation: None.
adjacent recovered median gap exceeds hypotenuse of across-edge SDs; descriptive, one seed
No tested adjacent separation passes this criterion. This does not establish that no latency information exists under any conditions. No HNN latency claim is licensed by this run.

## Synthetic calibration: all saved seeded runs

These historical runs use eight basis functions. Missing pairwise results are not reconstructed or filled in. Historical latency errors are reported for completeness, not as a substitute for the matched five-basis resolution calibration.

| Duration s | Seed | Estimator | Spikes | Connections | Rho | Sign accuracy | Historical latency error ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 120.0 | 0 | population GLM | 21807 | 99 | 0.6990 | 0.9798 | 2.8788 |
| 120.0 | 0 | CCG baseline | 21807 | 99 | 0.4251 | 0.8788 | — |
| 120.0 | 0 | jitter null | 21807 | 99 | 0.0430 | 0.7980 | — |
| 120.0 | 1 | population GLM | 21828 | 123 | 0.6579 | 0.9756 | 3.0000 |
| 120.0 | 1 | CCG baseline | 21828 | 123 | 0.2881 | 0.9268 | — |
| 120.0 | 1 | jitter null | 21828 | 123 | 0.0560 | 0.6423 | — |
| 120.0 | 2 | population GLM | 22031 | 119 | 0.6554 | 0.9748 | 3.1345 |
| 120.0 | 2 | pairwise GLM | 22031 | 119 | 0.6387 | 0.9748 | — |
| 120.0 | 2 | CCG baseline | 22031 | 119 | 0.3283 | 0.9244 | — |
| 120.0 | 2 | jitter null | 22031 | 119 | 0.0437 | 0.7395 | — |
| 300.0 | 0 | population GLM | 54087 | 99 | 0.7966 | 1.0000 | 2.9798 |
| 300.0 | 0 | CCG baseline | 54087 | 99 | 0.5189 | 0.9394 | — |
| 300.0 | 0 | jitter null | 54087 | 99 | 0.1161 | 0.8384 | — |
| 300.0 | 1 | population GLM | 54561 | 123 | 0.8042 | 1.0000 | 2.7724 |
| 300.0 | 1 | pairwise GLM | 54561 | 123 | 0.7922 | 1.0000 | — |
| 300.0 | 1 | CCG baseline | 54561 | 123 | 0.4237 | 0.9593 | — |
| 300.0 | 1 | jitter null | 54561 | 123 | 0.3552 | 0.7805 | — |
| 300.0 | 2 | population GLM | 55032 | 119 | 0.8050 | 0.9916 | 2.8908 |
| 300.0 | 2 | pairwise GLM | 55032 | 119 | 0.7840 | 0.9916 | — |
| 300.0 | 2 | CCG baseline | 55032 | 119 | 0.4435 | 0.9664 | — |
| 300.0 | 2 | jitter null | 55032 | 119 | 0.1252 | 0.7395 | — |
| 600.0 | 0 | population GLM | 108777 | 99 | 0.8956 | 1.0000 | 2.9293 |
| 600.0 | 0 | CCG baseline | 108777 | 99 | 0.6293 | 1.0000 | — |
| 600.0 | 0 | jitter null | 108777 | 99 | 0.3661 | 0.8586 | — |
| 600.0 | 1 | population GLM | 109243 | 123 | 0.8448 | 1.0000 | 2.8049 |
| 600.0 | 1 | pairwise GLM | 109243 | 123 | 0.8264 | 0.9919 | — |
| 600.0 | 1 | CCG baseline | 109243 | 123 | 0.5084 | 0.9919 | — |
| 600.0 | 1 | jitter null | 109243 | 123 | 0.2487 | 0.8130 | — |
| 600.0 | 2 | population GLM | 110587 | 119 | 0.8727 | 1.0000 | 2.8992 |
| 600.0 | 2 | pairwise GLM | 110587 | 119 | 0.8505 | 1.0000 | — |
| 600.0 | 2 | CCG baseline | 110587 | 119 | 0.5891 | 0.9748 | — |
| 600.0 | 2 | jitter null | 110587 | 119 | 0.3369 | 0.8655 | — |

| Duration s | Estimator | Mean rho | Sample SD | Seeds |
| --- | --- | --- | --- | --- |
| 120.0 | CCG baseline | 0.3472 | 0.0704 | 3 |
| 120.0 | jitter null | 0.0475 | 0.0073 | 3 |
| 120.0 | pairwise GLM | 0.6387 | — | 1 |
| 120.0 | population GLM | 0.6708 | 0.0244 | 3 |
| 300.0 | CCG baseline | 0.4621 | 0.0503 | 3 |
| 300.0 | jitter null | 0.1988 | 0.1355 | 3 |
| 300.0 | pairwise GLM | 0.7881 | 0.0058 | 2 |
| 300.0 | population GLM | 0.8019 | 0.0046 | 3 |
| 600.0 | CCG baseline | 0.5756 | 0.0616 | 3 |
| 600.0 | jitter null | 0.3173 | 0.0611 | 3 |
| 600.0 | pairwise GLM | 0.8384 | 0.0170 | 2 |
| 600.0 | population GLM | 0.8710 | 0.0254 | 3 |

## Solver and memory experiments (historical)

Saved fits are not rerun. These older summaries used an overwritten single-class label per pair and different boundary handling; their recovery tables are superseded by the current per-class analysis. The old held_out_mean_rate field came from an intercept-only placeholder, not full held-out predictions, and must not be used as predictive validation. Peak_gb was ru_maxrss/1e6 (Linux KiB units), not a rigorously converted decimal GB measurement.

| Run | Solver | float32 | Requested bins | Basis | Seconds | Legacy peak_gb |
| --- | --- | --- | --- | --- | --- | --- |
| LBFGS_f32 | LBFGS | True | 400000 | 5 | 239.0933 | 3.2109 |
| LBFGS_f64 | LBFGS | False | 400000 | 5 | 474.4057 | 5.2894 |
| SVRG_f32 | SVRG | True | 400000 | 5 | 387.0004 | 3.1188 |
| SVRG_f64 | SVRG | False | 400000 | 5 | 837.3780 | 5.2219 |
| production_full | LBFGS | True | 2560000 | 5 | 1943.7381 | 18.7569 |
| scale_1200000 | LBFGS | False | 1200000 | 5 | 1573.8746 | 13.6695 |
| scale_200000 | LBFGS | False | 200000 | 5 | 147.5360 | 3.0837 |
| scale_400000 | LBFGS | False | 400000 | 5 | 283.3924 | 5.2910 |
| scale_800000 | LBFGS | False | 800000 | 5 | 1020.8940 | 9.4867 |

Saved LBFGS float32/float64 filter correlation: 0.9999999999985.
This supports numerical agreement for the compared configuration, not universal float32 validity.

## Ground-truth audits: every anatomical class

Weights and delays are perfectly rank-confounded within each default class. E/I weight ranges and inhibitory within-class spread prevent interpreting a pooled weight rank. Audit counts retain their original autapse conventions; current inter-neuron scoring excludes autapses.

### Mesh 5x5

| Class | Pairs | Weight CV | Delay min ms | Delay max ms | Inside 25ms fraction | Weight-delay rho |
| --- | --- | --- | --- | --- | --- | --- |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 600 | 0.5425 | 1.1175 | 35.0073 | 0.9933 | -1.0000 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 600 | 0.5425 | 1.1175 | 35.0073 | 0.9933 | -1.0000 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 600 | 0.5425 | 1.1175 | 35.0073 | 0.9933 | -1.0000 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 600 | 0.5425 | 1.1175 | 35.0073 | 0.9933 | -1.0000 |
| L2_basket->L2_pyramidal / gabaa / soma | 250 | 0.0027 | 1.0000 | 1.0129 | 1.0000 | -1.0000 |
| L2_basket->L2_pyramidal / gabab / soma | 250 | 0.0027 | 1.0000 | 1.0129 | 1.0000 | -1.0000 |
| L5_basket->L5_pyramidal / gabaa / soma | 250 | 0.0014 | 1.0000 | 1.0066 | 1.0000 | -1.0000 |
| L5_basket->L5_pyramidal / gabab / soma | 250 | 0.0014 | 1.0000 | 1.0066 | 1.0000 | -1.0000 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 625 | 0.5471 | 1.0000 | 35.0073 | 0.9936 | -1.0000 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 625 | 0.5471 | 1.0000 | 35.0073 | 0.9936 | -1.0000 |
| L2_basket->L5_pyramidal / gabaa / distal | 250 | 0.0027 | 1.0000 | 1.0129 | 1.0000 | -1.0000 |
| L2_pyramidal->L2_basket / ampa / soma | 250 | 0.5774 | 1.0000 | 35.0073 | 0.9920 | -1.0000 |
| L2_basket->L2_basket / gabaa / soma | 100 | 0.0176 | 1.0000 | 1.0645 | 1.0000 | -1.0000 |
| L5_basket->L5_basket / gabaa / soma | 90 | 0.0169 | 1.0050 | 1.0645 | 1.0000 | -1.0000 |
| L5_pyramidal->L5_basket / ampa / soma | 250 | 0.5774 | 1.0000 | 35.0073 | 0.9920 | -1.0000 |
| L2_pyramidal->L5_basket / ampa / soma | 250 | 0.5774 | 1.0000 | 35.0073 | 0.9920 | -1.0000 |

### Mesh 10x10

| Class | Pairs | Weight CV | Delay min ms | Delay max ms | Inside 25ms fraction | Weight-delay rho |
| --- | --- | --- | --- | --- | --- | --- |
| L2_pyramidal->L2_pyramidal / nmda / proximal | 9900 | 1.3646 | 1.1175 | 65659969.1373 | 0.5269 | -1.0000 |
| L2_pyramidal->L2_pyramidal / ampa / proximal | 9900 | 1.3646 | 1.1175 | 65659969.1373 | 0.5269 | -1.0000 |
| L5_pyramidal->L5_pyramidal / nmda / proximal | 9900 | 1.3646 | 1.1175 | 65659969.1373 | 0.5269 | -1.0000 |
| L5_pyramidal->L5_pyramidal / ampa / proximal | 9900 | 1.3646 | 1.1175 | 65659969.1373 | 0.5269 | -1.0000 |
| L2_basket->L2_pyramidal / gabaa / soma | 3500 | 0.0112 | 1.0000 | 1.0669 | 1.0000 | -1.0000 |
| L2_basket->L2_pyramidal / gabab / soma | 3500 | 0.0112 | 1.0000 | 1.0669 | 1.0000 | -1.0000 |
| L5_basket->L5_pyramidal / gabaa / soma | 3500 | 0.0057 | 1.0000 | 1.0336 | 1.0000 | -1.0000 |
| L5_basket->L5_pyramidal / gabab / soma | 3500 | 0.0057 | 1.0000 | 1.0336 | 1.0000 | -1.0000 |
| L2_pyramidal->L5_pyramidal / ampa / proximal | 10000 | 1.3650 | 1.0000 | 65659969.1373 | 0.5316 | -1.0000 |
| L2_pyramidal->L5_pyramidal / ampa / distal | 10000 | 1.3650 | 1.0000 | 65659969.1373 | 0.5316 | -1.0000 |
| L2_basket->L5_pyramidal / gabaa / distal | 3500 | 0.0112 | 1.0000 | 1.0669 | 1.0000 | -1.0000 |
| L2_pyramidal->L2_basket / ampa / soma | 3500 | 1.3846 | 1.0000 | 65659969.1373 | 0.5214 | -1.0000 |
| L2_basket->L2_basket / gabaa / soma | 1225 | 0.0695 | 1.0000 | 1.4369 | 1.0000 | -1.0000 |
| L5_basket->L5_basket / gabaa / soma | 1190 | 0.0690 | 1.0050 | 1.4369 | 1.0000 | -1.0000 |
| L5_pyramidal->L5_basket / ampa / soma | 3500 | 1.3846 | 1.0000 | 65659969.1373 | 0.5214 | -1.0000 |
| L2_pyramidal->L5_basket / ampa / soma | 3500 | 1.3846 | 1.0000 | 65659969.1373 | 0.5214 | -1.0000 |

## Earlier pilots and superseded artifacts

### hnn_first_5x5_t5000.json

Historical short pilot; not a completed production experiment.
```json
{
  "config": {
    "tstop": 5000.0,
    "mesh": [
      5,
      5
    ],
    "history_ms": 25.0,
    "n_basis": 8,
    "n_procs": 4,
    "drive_rate": 10.0,
    "regularizer": 1e-06,
    "seed": 2,
    "out": "results"
  },
  "sim_wall_s": 61.29078435897827,
  "n_spikes": 1180,
  "mean_rate_hz": 3.371428571428572,
  "n_silent": 0,
  "per_class": {
    "L2_basket->L2_basket|gabaa|soma": {
      "n_evaluated": 100,
      "n_outside_support": 0,
      "weight_spearman": 0.44549072325605055,
      "sign_accuracy": 0.99,
      "latency_error_ms": NaN
    },
    "L2_basket->L2_pyramidal|gabab|soma": {
      "n_evaluated": 250,
      "n_outside_support": 0,
      "weight_spearman": 0.3893645341077087,
      "sign_accuracy": 0.936,
      "latency_error_ms": NaN
    },
    "L2_basket->L5_pyramidal|gabaa|distal": {
      "n_evaluated": 250,
      "n_outside_support": 0,
      "weight_spearman": -0.13268559373595787,
      "sign_accuracy": 0.516,
      "latency_error_ms": NaN
    },
    "L2_pyramidal->L2_basket|ampa|soma": {
      "n_evaluated": 248,
      "n_outside_support": 2,
      "weight_spearman": 0.32233365758681626,
      "sign_accuracy": 0.5766129032258065,
      "latency_error_ms": NaN
    },
    "L2_pyramidal->L2_pyramidal|ampa|proximal": {
      "n_evaluated": 596,
      "n_outside_support": 4,
      "weight_spearman": 0.4838441356575673,
      "sign_accuracy": 0.43288590604026844,
      "latency_error_ms": NaN
    },
    "L2_pyramidal->L5_basket|ampa|soma": {
      "n_evaluated": 248,
      "n_outside_support": 2,
      "weight_spearman": -0.005052053489573499,
      "sign_accuracy": 0.42338709677419356,
      "latency_error_ms": NaN
    },
    "L2_pyramidal->L5_pyramidal|ampa|distal": {
      "n_evaluated": 621,
      "n_outside_support": 4,
      "weight_spearman": 0.06851247025994847,
      "sign_accuracy": 0.6747181964573269,
      "latency_error_ms": NaN
    },
    "L5_basket->L5_basket|gabaa|soma": {
      "n_evaluated": 90,
      "n_outside_support": 0,
      "weight_spearman": 0.21933250638090887,
      "sign_accuracy": 1.0,
      "latency_error_ms": NaN
    },
    "L5_basket->L5_pyramidal|gabab|soma": {
      "n_evaluated": 250,
      "n_outside_support": 0,
      "weight_spearman": -0.011421109730341878,
      "sign_accuracy": 0.572,
      "latency_error_ms": NaN
    },
    "L5_pyramidal->L5_basket|ampa|soma": {
      "n_evaluated": 248,
      "n_outside_support": 2,
      "weight_spearman": 0.15058754822636813,
      "sign_accuracy": 0.6048387096774194,
      "latency_error_ms": NaN
    },
    "L5_pyramidal->L5_pyramidal|ampa|proximal": {
      "n_evaluated": 596,
      "n_outside_support": 4,
      "weight_spearman": 0.11501377918467756,
      "sign_accuracy": 0.4714765100671141,
      "latency_error_ms": NaN
    }
  },
  "pooled_warning_only": {
    "weight_spearman": 0.2295717690821709,
    "sign_accuracy": 0.5865027166142408,
    "n_evaluated": 3497
  }
}
```

### location_5x5_t6000.json

Historical short pilot; not a completed production experiment.
```json
{
  "config": {
    "tstop": 6000.0,
    "mesh": [
      5,
      5
    ],
    "seeds": [
      2
    ],
    "history_ms": 25.0,
    "n_basis": 8,
    "n_procs": 2,
    "regularizer": 0.001,
    "max_iter": 2000,
    "out": "results"
  },
  "records": []
}
```

## What remains

1. Finish seed-200 baselines and seed-300 simulation/grid/baselines.
2. Resolve all proxy-fit iteration caps before interpreting the proxy comparison.
3. Investigate strong jitter-null scores, repeat null realizations, and assess comparable surviving neuron pairs.
4. Match synthetic calibration to the production basis before making strong claims about estimator versus model mismatch.
5. Location and sparse-topology production experiments are still queued, but are optional extensions to the primary study.
6. No upstream PRs have been opened.

## Files supplied

`all_metrics.csv` contains every saved primary-grid and baseline per-class metric in this snapshot. `raw_results.zip` includes raw result JSON, audit CSV, fitted-array checkpoints, spike caches, source/configuration files, figures, and a SHA-256 manifest. Logs and lock files are excluded. Older JSON artifacts may contain legacy NaN tokens; the CSV represents missing values as empty fields.

