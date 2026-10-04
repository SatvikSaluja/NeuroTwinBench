"""Bounded pilots for shared-input and paired location-swap study designs.

These 20-second runs verify manipulations and firing regimes; they do not
establish recovery or power. Preserve original experiments unchanged.
"""
import argparse,json,sys,time
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from neurotwinbench.simulate import SimulationConfig,build_network,run
from neurotwinbench.reporting import write_json
from neurotwinbench.ground_truth import extract_ground_truth


def check_shared(net):
 drive=net.external_drives['sustained']
 assert drive['cell_specific'] is False
 assert len(net.gid_ranges['sustained'])==1
 targets=set()
 for c in net.connectivity:
  if c['src_type']=='sustained':
   for values in c['gid_pairs'].values():targets.update(values)
 assert len(targets)==sum(len(net.gid_ranges[k]) for k in net.cell_types)
 return {'cell_specific':False,'drive_cells':1,'target_neurons':len(targets)}


def check_swap(a,b):
 ga,gb=extract_ground_truth(a),extract_ground_truth(b)
 def rows(g):
  return {(int(s),int(t)):(str(l),float(w),float(d)) for s,t,l,w,d,st,tt,r in zip(g.src_gid,g.target_gid,g.loc,g.weight,g.delay_ms,g.src_type,g.target_type,g.receptor)
   if st=='L2_pyramidal' and tt=='L5_pyramidal' and r=='ampa'}
 aa,bb=rows(ga),rows(gb);assert aa.keys()==bb.keys()
 for key in aa:
  assert aa[key][0]!=bb[key][0]
  np.testing.assert_allclose(aa[key][1:],bb[key][1:],rtol=0,atol=0)
 return {'matched_pairs':len(aa),'every_pair_location_swapped':True,'weights_and_delays_identical':True}


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--kind',choices=['shared','location_swap'],required=True);p.add_argument('--build-only',action='store_true');a=p.parse_args()
 configs=[SimulationConfig(network='shared',tstop_ms=20000,event_seed=100000)] if a.kind=='shared' else [SimulationConfig(network=n,tstop_ms=20000,event_seed=200000) for n in ('location','location_swapped')]
 nets=[build_network(c) for c in configs]
 design=check_shared(nets[0]) if a.kind=='shared' else check_swap(*nets)
 print(design,flush=True)
 if a.build_only:return
 root=Path('results/design_pilots')/a.kind;root.mkdir(parents=True,exist_ok=True)
 records=[]
 for config in configs:
  started=time.time();sim=run(config,n_procs=4)
  np.savez_compressed(root/f'{config.network}_spikes.npz',spikes=sim.spikes,drives=sim.drive_spikes,gids=sim.gids,cell_types=sim.cell_types,bin_s=sim.bin_s,segment_lengths=[len(sim.spikes)],simulation_config=json.dumps(config.__dict__),base_seed=config.event_seed)
  records.append({'network':config.network,'config':config.__dict__,'seconds':time.time()-started,'spikes':int(sim.spikes.sum()),'silent':int((sim.rates_hz==0).sum()),'rates_hz':sim.rates_hz.tolist(),'cache_key':config.key()})
  write_json(root/'report.json',{'status':'DONE' if len(records)==len(configs) else 'RUNNING','design':design,'records':records,'interpretation':'20-second manipulation/firing-regime pilot, not a powered recovery result; no rate matching claim'})

if __name__=='__main__':main()
