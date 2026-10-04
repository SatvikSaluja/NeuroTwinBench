"""Shared per-class scoring and durable experiment records."""
from dataclasses import fields
import json
from pathlib import Path
import numpy as np
from .ground_truth import GroundTruth
from . import metrics


def write_json(path, payload):
    """Publish a complete checkpoint atomically; JSON null denotes unavailable."""
    def clean(value):
        if isinstance(value, dict):
            return {str(k): clean(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [clean(v) for v in value]
        if isinstance(value, np.ndarray):
            return clean(value.tolist())
        if isinstance(value, np.generic):
            return clean(value.item())
        if isinstance(value, float) and not np.isfinite(value):
            return None
        if isinstance(value, Path):
            return str(value)
        return value
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(clean(payload), indent=2, allow_nan=False) + '\n')
    temporary.replace(path)


def per_class(gt, gids, areas, evaluable, history_ms):
    """Score each anatomical class without overwriting overlapping receptors.

    A GLM estimates total pair influence, not an individual receptor/location.
    Overlapping anatomical classes therefore share an estimate, explicitly.
    Autapses are excluded from inter-neuron recovery. Inhibitory ranks remain
    unavailable: their anatomical spread is degenerate in the default model.
    """
    output = {}
    for name, rows in gt.by_class():
        group = GroundTruth(**{f.name: getattr(gt, f.name)[rows] for f in fields(gt)})
        weights, delays, connected = group.to_matrices(gids)
        np.fill_diagonal(connected, False)
        eligible = connected & evaluable
        result = metrics.evaluate(weights, areas, eligible,
                                  true_delay_ms=delays, history_ms=history_ms)
        values = np.abs(weights[eligible & (delays <= history_ms)])
        cv = float(values.std() / values.mean()) if len(values) and values.mean() else None
        rank_informative = bool(len(values) > 1 and np.ptp(values) > 0
                                and not name.startswith(('L2_basket', 'L5_basket')))
        output[name] = {
            'weight_spearman': result.weight_spearman if rank_informative else None,
            'sign_accuracy': result.sign_accuracy,
            'n_evaluated': result.n_evaluated,
            'n_outside_support': result.n_outside_support,
            'n_unestimable': int((connected & ~evaluable).sum()),
            'weight_cv': cv, 'rank_informative': rank_informative,
            'interpretation': 'total pair influence compared with this anatomical class',
        }
    return output


def load_recording(path, legacy_chunk_bins=320000):
    """Load production cache, retaining independent simulation boundaries."""
    with np.load(path, allow_pickle=False) as z:
        data = {k: z[k] for k in z.files}
    n = len(data['spikes'])
    if 'segment_lengths' not in data:
        # The original production cache predates provenance fields. Its eight
        # independent 320 s chunks are recorded in CODEX_HANDOFF.md.
        if n == 2560000 and legacy_chunk_bins == 320000:
            data['segment_lengths'] = np.full(8, legacy_chunk_bins)
        else:
            raise ValueError('cache lacks segment_lengths; supply a recording with explicit boundaries')
    lengths = data['segment_lengths']
    if np.sum(lengths) != n or np.any(lengths <= 0):
        raise ValueError('invalid segment_lengths in cache')
    if len(data['drives']) != n or len(data['gids']) != data['spikes'].shape[1]:
        raise ValueError('recording dimensions disagree')
    return data


def segment_transform(array, lengths, transform):
    offsets = np.r_[0, np.cumsum(lengths)]
    return np.concatenate([transform(array[lo:hi]) for lo, hi in zip(offsets[:-1], offsets[1:])])
