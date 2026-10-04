"""Fit cached production data with the validated LBFGS/float32 configuration.

Uses the same durable per-class worker as the full grid. The previous pooled
SVRG sanity gate has been retired. See results/solver for completed validation.

    python experiments/fit_production.py --from-cache results/production_spikes.npz
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experiments.grid import main

if __name__ == '__main__':
    if '--from-cache' not in sys.argv:
        sys.argv += ['--from-cache', 'results/production_spikes.npz']
    sys.argv += ['--cell', 'full', 'true']
    main()
