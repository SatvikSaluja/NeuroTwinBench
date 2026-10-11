#!/usr/bin/env bash
set -euo pipefail

cd /home/satvik/hnn_neuro_bridge
while [[ ! -f results/phase2_full/topology_c13_e1020000/report.json ]]; do
  sleep 300
done
grep -q '"status": "DONE"' results/phase2_full/topology_c13_e1020000/report.json

export PATH=/home/satvik/miniconda3/envs/neurotwin/bin:$PATH
(
  while true; do
    date -Is >> results/phase2_full/long_topology_disk_usage.log
    df -h . >> results/phase2_full/long_topology_disk_usage.log
    sleep 600
  done
) &
monitor_pid=$!
trap 'kill "$monitor_pid"' EXIT

taskset -c 0-3 /home/satvik/miniconda3/envs/neurotwin/bin/python -u \
  experiments/phase2_studies.py --kind topology --conn-seed 15 --event-seed 1040000 \
  --chunks 40 --chunk-s 320 --out results/phase2_full/topology_c15_e1040000 \
  2>&1 | tee -a results/phase2_full/long_topology.queue.log
