"""Fixed-design corrected HNN studies. Cached chunks and per-fit checkpoints."""
import argparse,json,sys,time
from pathlib import Path
from dataclasses import replace
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from neurotwinbench import simulate as sim,fit,metrics
from neurotwinbench.ground_truth import extract_ground_truth
from neurotwinbench.reporting import write_json
from neurotwinbench.uncertainty import paired_node_bootstrap,paired_location_bootstrap
from experiments.topology import candidate_mask,THINNED
from experiments.design_pilots import check_swap

def recording(root,config,chunks,chunk_s):
    root.mkdir(parents=True,exist_ok=True);dest=root/'recording.npz'
    spec={'config':config.__dict__,'chunks':chunks,'chunk_s':chunk_s,'bin_s':.001}
    signature=json.dumps(spec,sort_keys=True,default=str)
    if dest.exists():
        with np.load(dest,allow_pickle=False) as z:
            if str(z['signature'])!=signature:raise ValueError('recording protocol mismatch')
            return {k:z[k] for k in z.files}
    xs=[];ds=[]
    for index in range(chunks):
        cfg=replace(config,tstop_ms=chunk_s*1000,event_seed=config.event_seed+index)
        write_json(root/'status.json',{'status':'SIMULATING','chunk':index+1,'total':chunks,'updated_unix':time.time()})
        a=sim.run(cfg,n_procs=4);xs.append(a.spikes);ds.append(a.drive_spikes)
    data=dict(spikes=np.concatenate(xs),drives=np.concatenate(ds),gids=a.gids,cell_types=a.cell_types,
        drive_names=np.asarray(a.drive_names),lengths=np.array([len(x) for x in xs]),bin_s=a.bin_s,signature=signature)
    tmp=root/'recording.tmp.npz';np.savez_compressed(tmp,**data);tmp.replace(dest);return data

def fitted(root,data,condition,exog=None,jitter=None):
    path=root/f'{condition}.npz';meta=root/f'{condition}.json'
    if path.exists() and meta.exists():
        with np.load(path) as z:out={k:z[k] for k in z.files}
        return out,json.load(open(meta))
    spikes=data['spikes']
    if jitter is not None:
        spikes=np.empty_like(spikes);offset=0
        for idx,length in enumerate(data['lengths']):
            spikes[offset:offset+length]=metrics.jitter(data['spikes'][offset:offset+length],width_bins=50,seed=jitter+idx);offset+=length
    model=fit.fit_population_glm(spikes,bin_s=.001,history_ms=25,n_basis=5,exogenous=exog,
        regularizer_strength=.001,max_iter=2000,float32=False,solver='DISK_LBFGS',segment_lengths=data['lengths'])
    arrays={'areas':model.areas,'filters':model.filters,'evaluable':model.evaluable,'gids':data['gids']}
    tmp=path.with_suffix('.tmp.npz');np.savez_compressed(tmp,**arrays);tmp.replace(path)
    diagnostic={'condition':condition,'diagnostics':model.diagnostics,'jitter_seed':jitter,'spikes':int(spikes.sum()),
        'rates_hz':(spikes.mean(axis=0)/.001).tolist(),'power':fit.power_check(spikes,5,n_exog=0 if exog is None else exog.shape[1])}
    write_json(meta,diagnostic);return arrays,diagnostic

def topology_scores(config,data,a,b):
    gt=extract_ground_truth(sim.build_network(config));potential=extract_ground_truth(sim.build_network(replace(config,connection_probability={})))
    _,_,connected=gt.to_matrices(data['gids']);_,delays,edges=potential.to_matrices(data['gids'])
    output={}
    for projection in THINNED:
        mask=candidate_mask(potential,data['gids'],(projection,)) & edges & (delays<=25) & a['evaluable'] & b['evaluable']
        output[projection]={'original':metrics.edge_detection(connected,a['areas'],candidate=mask),
          'control':metrics.edge_detection(connected,b['areas'],candidate=mask),
          'paired_uncertainty':paired_node_bootstrap(connected,a['areas'],b['areas'],mask),
          'distance_control':metrics.edge_detection(connected,1/np.maximum(delays,1e-12),candidate=mask)}
    return output

def run_study(args):
    root=args.out;root.mkdir(parents=True,exist_ok=True)
    sparse={p:.3 for p in THINNED}
    base=sim.SimulationConfig(event_seed=args.event_seed,conn_seed=args.conn_seed,connection_probability=sparse)
    if args.kind=='topology':
        data=recording(root,base,args.chunks,args.chunk_s)
        a,am=fitted(root,data,'original');controls=[]
        for seed in [101,202,303]:
            b,bm=fitted(root,data,f'jitter{seed}',jitter=seed)
            controls.append({'jitter_seed':seed,'scores':topology_scores(base,data,a,b),'converged':am['diagnostics']['converged'] and bm['diagnostics']['converged']})
        result={'controls':controls}
    elif args.kind=='shared':
        # Private-only sparse reference shares anatomy and event schedule.
        data=recording(root/'mixed',replace(base,network='mixed_shared'),args.chunks,args.chunk_s)
        names=list(data['drive_names']);shared=data['drives'][:,[names.index('shared_component')]]
        a,am=fitted(root/'mixed',data,'shared_observed',exog=shared)
        b,bm=fitted(root/'mixed',data,'shared_hidden')
        d=recording(root/'private',base,args.chunks,args.chunk_s);c,cm=fitted(root/'private',d,'private_hidden')
        result={'observed_vs_hidden':topology_scores(replace(base,network='mixed_shared'),data,a,b),
            'mixed_hidden_vs_private_hidden':topology_scores(base,data,b,c),
            'fit_diagnostics':[am,bm,cm],
            'interpretation':'same mean external event rate per target: private10Hz vs private5+shared5Hz. Only shared source is observed; private inputs hidden in all fits. Output rates/variance are not matched. Anatomical contrasts use identical candidate pairs.'}
    else:
        configs=[replace(base,network=n,connection_probability={}) for n in ['location','location_swapped']]
        design=check_swap(*(sim.build_network(c) for c in configs));fits=[];data=[];meta=[]
        for cfg in configs:
            d=recording(root/cfg.network,cfg,args.chunks,args.chunk_s);a,m=fitted(root/cfg.network,d,'fit',exog=d['drives']);fits.append(a);data.append(d);meta.append(m)
        gids=data[0]['gids'];idx={int(g):i for i,g in enumerate(gids)}
        mask=np.zeros((len(gids),len(gids)),bool);orientation=np.zeros_like(mask,dtype=float)
        gt=extract_ground_truth(sim.build_network(configs[0]))
        for s,t,st,tt,rec,loc,delay in zip(gt.src_gid,gt.target_gid,gt.src_type,gt.target_type,gt.receptor,gt.loc,gt.delay_ms):
            if st=='L2_pyramidal' and tt=='L5_pyramidal' and rec=='ampa' and delay<=25:
                i,j=idx[int(s)],idx[int(t)];mask[i,j]=True;orientation[i,j]=1 if loc=='basal_2' else -1
        mask &= fits[0]['evaluable'] & fits[1]['evaluable']
        delta=orientation*(fits[1]['areas']-fits[0]['areas'])
        np.savez_compressed(root/'paired_effects.npz',delta=delta,mask=mask,gids=gids)
        result={'design':design,'apical_minus_basal':paired_location_bootstrap(delta,mask),'fits':meta,
            'interpretation':'same pairs, same weights/delays, paired event seeds, location swapped jointly. Total network consequence of the manipulation, not isolated single-synapse causal effect; no latency claim.'}
    write_json(root/'report.json',{'status':'DONE','kind':args.kind,'conn_seed':args.conn_seed,'event_seed':args.event_seed,'duration_s':args.chunks*args.chunk_s,**result})

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--kind',choices=['topology','shared','location'],required=True);p.add_argument('--conn-seed',type=int,required=True);p.add_argument('--event-seed',type=int,required=True);p.add_argument('--chunks',type=int,default=8);p.add_argument('--chunk-s',type=float,default=320);p.add_argument('--out',type=Path,required=True);run_study(p.parse_args())
