"""Conditional neuron-cluster bootstrap; never treats dyads as iid samples."""
import numpy as np
from sklearn.metrics import roc_auc_score,average_precision_score

def paired_node_bootstrap(truth, scores, control, mask, repeats=1000, seed=732):
    truth=np.asarray(truth,dtype=bool);mask=np.array(mask,dtype=bool,copy=True)
    np.fill_diagonal(mask,False)
    i,j=np.where(mask);y=truth[i,j];a=np.abs(np.asarray(scores)[i,j]);b=np.abs(np.asarray(control)[i,j])
    nodes=np.unique(np.r_[i,j]);rng=np.random.default_rng(seed);samples=[]
    if len(np.unique(y))<2:return {'status':'UNAVAILABLE','reason':'one edge class'}
    for _ in range(repeats):
        # One multiplicity per neuron used in both source and target roles.
        m=np.bincount(rng.choice(nodes,len(nodes),replace=True),minlength=len(truth));w=m[i]*m[j]
        if w[y].sum()==0 or w[~y].sum()==0:continue
        samples.append([roc_auc_score(y,a,sample_weight=w)-roc_auc_score(y,b,sample_weight=w),
                        average_precision_score(y,a,sample_weight=w)-average_precision_score(y,b,sample_weight=w)])
    samples=np.asarray(samples)
    return {'status':'DONE','n_nodes':len(nodes),'n_pairs':len(y),'bootstrap_valid':len(samples),
        'auc_difference':float(roc_auc_score(y,a)-roc_auc_score(y,b)),
        'ap_difference':float(average_precision_score(y,a)-average_precision_score(y,b)),
        'auc_difference_interval95':np.quantile(samples[:,0],[.025,.975]).tolist(),
        'ap_difference_interval95':np.quantile(samples[:,1],[.025,.975]).tolist(),
        'scope':'conditional on fitted models and fixed circuit; neuron-cluster resampling, not refitting, not an independent-circuit confidence interval'}

def paired_location_bootstrap(delta,mask,repeats=1000,seed=733):
    i,j=np.where(mask);sources=np.unique(i);targets=np.unique(j);rng=np.random.default_rng(seed);vals=[]
    for _ in range(repeats):
        a=np.bincount(rng.choice(sources,len(sources),replace=True),minlength=len(mask))
        b=np.bincount(rng.choice(targets,len(targets),replace=True),minlength=len(mask));w=a[i]*b[j]
        if w.sum():vals.append(float(np.average(delta[i,j],weights=w)))
    return {'mean_paired_area_difference':float(np.mean(delta[mask])), 'conditional_node_interval95':np.quantile(vals,[.025,.975]).tolist(),'n_pairs':int(mask.sum()),'scope':'crossed source/target cluster resampling of fixed fitted contrasts; excludes fit uncertainty'}
