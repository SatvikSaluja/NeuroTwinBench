"""Explicit proposed experiment recipes. Dry-run by default; no automatic queue."""
import argparse
from pathlib import Path
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def recipes():
    return {
        'mesh270-pilot': ['experiments/production.py', '--mesh', '10', '10', '--chunks', '1', '--chunk-s', '30', '--probability', '0.3', '--conn-seed', '21', '--base-seed', '1100000', '--simulate-only', '--out', 'results/proposed/mesh270_pilot'],
        'mesh270-production': ['experiments/production.py', '--mesh', '10', '10', '--chunks', '8', '--chunk-s', '320', '--probability', '0.3', '--conn-seed', '21', '--base-seed', '1110000', '--simulate-only', '--out', 'results/proposed/mesh270_production'],
        'location-replication': ['experiments/phase2_studies.py', '--kind', 'location', '--conn-seed', '21', '--event-seed', '1120000', '--chunks', '8', '--chunk-s', '320', '--out', 'results/proposed/location_e1120000'],
        'shared-replication': ['experiments/phase2_studies.py', '--kind', 'shared', '--conn-seed', '21', '--event-seed', '1130000', '--chunks', '8', '--chunk-s', '320', '--out', 'results/proposed/shared_c21_e1130000'],
    }

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('experiment', choices=recipes())
    p.add_argument('--run', action='store_true')
    a = p.parse_args()
    cmd = [sys.executable, '-u', *recipes()[a.experiment]]
    print(shlex.join(cmd), flush=True)
    if a.run:
        subprocess.run(cmd, cwd=ROOT, check=True)

if __name__ == '__main__':
    main()
