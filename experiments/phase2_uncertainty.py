"""Report conditional node-cluster and independent-circuit uncertainty separately."""
import json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from neurotwinbench.uncertainty import paired_node_bootstrap
from neurotwinbench.reporting import write_json
from neurotwinbench.simulate import SimulationConfig,build_network

root=Path('results/phase2');root.mkdir(exist_ok=True,parents=True)
rows=[]
net=build_network(SimulationConfig());type_by_gid={int(g):t for t in net.cell_types for g in net.gid_ranges[t]}
for circuit in [3,4]:
    original=next(Path(f'results/topology_c{circuit}/disk_fit').glob('filters*.npz'))
    with np.load(original) as z:a={k:z[k] for k in z.files}
    for seed in [101,202,303]:
        with np.load(next(Path(f'results/topology_c{circuit}/jitter{seed}').glob('filters*.npz'))) as z:b={k:z[k] for k in z.files}
        for cell in ['L2_pyramidal','L5_pyramidal']:
            selected=np.array([type_by_gid[int(g)]==cell for g in a['gids']]);mask=a['eligible']&b['eligible']&selected[:,None]&selected[None,:]
            rows.append({'circuit':circuit,'jitter_seed':seed,'projection':cell,'uncertainty':paired_node_bootstrap(a['connected'],a['filters'].sum(axis=2),b['filters'].sum(axis=2),mask)})
write_json(root/'existing_uncertainty.json',{'records':rows,'scope':'fixed fitted models; neuron dependence accounted for by cluster resampling; no claim of full estimator or circuit uncertainty'})
# Nested event observations are averaged within circuit before circuit bootstrap.
replicates=[]
for p in root.glob('topology_*/report.json'):
    d=json.load(open(p))
    for projection in ['L2_pyramidal->L2_pyramidal','L5_pyramidal->L5_pyramidal']:
        controls=[x for x in d['controls'] if x['converged']]
        if len(controls)!=3:continue
        delta=np.mean([x['scores'][projection]['paired_uncertainty']['auc_difference'] for x in controls])
        replicates.append({'circuit':d['conn_seed'],'event_seed':d['event_seed'],'projection':projection,'auc_difference':float(delta)})
summary={};rng=np.random.default_rng(938)
for projection in sorted({x['projection'] for x in replicates}):
    values=[np.mean([x['auc_difference'] for x in replicates if x['circuit']==c and x['projection']==projection]) for c in sorted({x['circuit'] for x in replicates})]
    summary[projection]={'circuit_means':values,'mean':float(np.mean(values)), 'n_circuits':len(values),
      'exploratory_circuit_interval95':np.quantile(np.mean(rng.choice(values,(5000,len(values))),axis=1),[.025,.975]).tolist() if len(values)>=3 else None}
write_json(root/'replication_uncertainty.json',{'records':replicates,'summary':summary,'warning':'only three new circuits planned; intervals remain exploratory; event seeds are nested within circuit, not iid edges'})
