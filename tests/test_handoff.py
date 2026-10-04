"""Regression checks for the production handoff; no NEURON simulations."""
import json
import sys
import tempfile
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from neurotwinbench import fit
from neurotwinbench.ground_truth import GroundTruth
from neurotwinbench.reporting import per_class, write_json, load_recording


def test_overlapping_classes_are_not_overwritten():
    gt = GroundTruth(src_gid=np.array([0, 0, 0, 0]), target_gid=np.array([1, 2, 1, 2]),
        src_type=np.array(['L2_pyramidal'] * 4), target_type=np.array(['L5_pyramidal'] * 4),
        receptor=np.array(['ampa', 'ampa', 'nmda', 'nmda']), loc=np.array(['proximal'] * 4),
        weight=np.array([1., 2., 2., 1.]), delay_ms=np.ones(4), sign=np.ones(4), lamtha=np.ones(4))
    areas = np.zeros((3, 3)); areas[0, 1:] = [1, 2]
    rows = per_class(gt, np.arange(3), areas, np.ones((3, 3), bool), 25)
    assert len(rows) == 2
    assert np.isclose(rows['L2_pyramidal->L5_pyramidal|ampa|proximal']['weight_spearman'], 1)
    assert np.isclose(rows['L2_pyramidal->L5_pyramidal|nmda|proximal']['weight_spearman'], -1)


def test_segment_history_matches_independent_convolution():
    rng = np.random.default_rng(3)
    x = rng.poisson(.1, (200, 3)); exog = rng.poisson(.2, (200, 1))
    together = fit._build_design(x, .001, 25, 5, exog, float32=True, segment_lengths=[80, 120])
    a = fit._build_design(x[:80], .001, 25, 5, exog[:80], float32=True)
    b = fit._build_design(x[80:], .001, 25, 5, exog[80:], float32=True)
    np.testing.assert_array_equal(together[0], np.concatenate([a[0], b[0]]))
    np.testing.assert_array_equal(together[1], np.concatenate([a[1], b[1]]))
    assert together[0].dtype == np.float32
    assert len(together[0]) == 150
    try:
        fit._build_design(x, .001, 25, 5, exog, segment_lengths=[199])
    except ValueError:
        pass
    else:
        raise AssertionError('invalid boundaries accepted')


def test_pairwise_silent_neurons_and_float32():
    rng = np.random.default_rng(4)
    spikes = rng.poisson(.03, (1200, 3)); spikes[:, 1] = 0
    drive = rng.poisson(.1, (1200, 1))
    r = fit.fit_pairwise_glm(spikes, n_basis=5, max_iter=10, float32=True,
                            exogenous=drive, segment_lengths=[600, 600])
    assert r.filters.shape == (3, 3, 25)
    assert np.isfinite(r.filters).all()
    assert not r.evaluable[1].any() and not r.evaluable[:, 1].any()
    assert np.all(r.filters[1] == 0) and np.all(r.filters[:, 1] == 0)


def test_population_diagnostics():
    rng = np.random.default_rng(1)
    r = fit.fit_population_glm(rng.poisson(.04, (1200, 3)), n_basis=5,
        max_iter=5, float32=True, segment_lengths=[600, 600])
    assert 'converged' in r.diagnostics
    assert 'num_steps' in r.diagnostics
    assert np.isfinite(r.filters).all()


def test_atomic_json_and_recording_metadata():
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / 'result.json'
        write_json(path, {'value': np.nan, 'count': np.int64(3)})
        assert json.loads(path.read_text()) == {'value': None, 'count': 3}
        assert not path.with_suffix('.json.tmp').exists()
        cache = Path(d) / 'spikes.npz'
        np.savez(cache, spikes=np.zeros((60, 2)), drives=np.zeros((60, 1)), gids=[0, 1], segment_lengths=[30, 30])
        assert load_recording(cache)['spikes'].shape == (60, 2)


def test_production_creates_output_and_preserves_segments():
    from experiments import production
    from neurotwinbench.simulate import Simulation
    from unittest.mock import patch
    def fake_run(config, **kwargs):
        return Simulation(spikes=np.ones((40, 2), dtype=np.int16),
            gids=np.array([0, 1]), cell_types=np.array(['L2_pyramidal'] * 2),
            drive_spikes=np.ones((40, 1), dtype=np.int16), drive_names=['sustained'],
            bin_s=.001, config=config)
    with tempfile.TemporaryDirectory() as directory:
        out = Path(directory) / 'new'
        with patch.object(sys, 'argv', ['production.py', '--chunks', '2', '--chunk-s', '.04',
                '--base-seed', '200', '--simulate-only', '--out', str(out)]), \
                patch.object(production.simmod, 'run', side_effect=fake_run):
            production.main()
        data = load_recording(out / 'production_spikes.npz')
        assert data['segment_lengths'].tolist() == [40, 40]
        assert int(data['base_seed']) == 200
        assert json.loads(str(data['simulation_config']))['event_seed'] == 201
        assert not (out / 'production_spikes.tmp.npz').exists()


if __name__ == '__main__':
    for name, fn in sorted(list(globals().items())):
        if name.startswith('test_'):
            print(name, flush=True); fn()
    print('all handoff checks passed', flush=True)
