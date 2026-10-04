"""Disk-backed exact dense Poisson fitting with bounded feature working buffers.

Features are computed once into NPY memory maps, then analytic gradients are
accumulated in chunks. Same causal NeMoS basis, ridge on coefficients only,
explicit segment boundaries and exogenous predictors. Never allocate full X
in RAM. L-BFGS checkpoints restart parameters, not optimizer history.
"""
from pathlib import Path
import hashlib
import json
import mmap
import os
import time
import numpy as np
from scipy.optimize import minimize
from scipy.signal import lfilter
from .reporting import write_json


def evict(array):
    if hasattr(array,'_mmap') and hasattr(array._mmap,'madvise'):
        array._mmap.madvise(mmap.MADV_DONTNEED)


def features(block,kernels):
    h,k=kernels.shape
    out=np.empty((len(block)-h,block.shape[1]*k),dtype=np.float64)
    for j in range(k):
        filtered=lfilter(kernels[:,j],[1.],block,axis=0)
        out[:,j::k]=filtered[h-1:-1]
    return out


def objective(vector,x,y,ridge,chunk=8192):
    p,n=x.shape[1],y.shape[1]
    w=vector[:p*n].reshape(p,n);b=vector[p*n:]
    value=0.;gw=np.zeros_like(w);gb=np.zeros_like(b)
    for start in range(0,len(x),chunk):
        xx=x[start:start+chunk];yy=y[start:start+chunk]
        eta=xx@w+b
        with np.errstate(over='ignore',invalid='ignore'):
            rate=np.exp(eta)
        if not np.isfinite(rate).all():
            return np.inf,np.zeros_like(vector)
        residual=rate-yy
        value+=np.sum(rate-yy*eta)
        gw+=xx.T@residual;gb+=residual.sum(axis=0)
        del xx,yy,eta,rate,residual
        evict(x);evict(y)
    value=value/len(x)+.5*ridge*np.sum(w*w)
    grad=np.r_[(gw/len(x)+ridge*w).ravel(),gb/len(x)]
    return float(value),grad


def fit_disk(spikes,bin_s,history_ms,n_basis,exogenous,ridge,max_iter,tol,segment_lengths):
    import jax
    jax.config.update('jax_enable_x64',True)
    import nemos as nmo
    from .fit import FitResult,_basis_kernels,_unpack
    counts=np.asarray(spikes)
    active=counts.sum(axis=0)>0
    if not active.any():raise ValueError('no active neurons')
    h=int(round(history_ms/(1000*bin_s)))
    lengths=np.asarray([len(counts)] if segment_lengths is None else segment_lengths,dtype=int)
    if lengths.sum()!=len(counts) or np.any(lengths<=h):raise ValueError('invalid segment lengths')
    exog=None if exogenous is None else np.asarray(exogenous)
    if exog is not None and exog.ndim==1:exog=exog[:,None]
    if exog is not None and len(exog)!=len(counts):raise ValueError('drive length mismatch')
    n=int(active.sum());q=0 if exog is None else exog.shape[1]
    basis=nmo.basis.RaisedCosineLogConv(n_basis_funcs=n_basis,window_size=h)
    kernels=_basis_kernels(basis,h,n_basis)
    digest=hashlib.sha256(json.dumps({'lengths':lengths.tolist(),'active':active.tolist(),'bin_s':bin_s,'ridge':ridge,'kernels':kernels.tolist(),'schema':1},sort_keys=True).encode())
    for array in (counts,exog):
        if array is not None:
            for start in range(0,len(array),8192):digest.update(np.ascontiguousarray(array[start:start+8192],dtype=np.float64).tobytes())
    root=Path('cache/disk_features')/digest.hexdigest()[:24];root.mkdir(parents=True,exist_ok=True)
    marker=root/'complete.json';rows=int(sum(lengths)-len(lengths)*h);cols=(n+q)*n_basis
    if not marker.exists():
        x=np.lib.format.open_memmap(root/'design.npy',mode='w+',dtype='float64',shape=(rows,cols))
        y=np.lib.format.open_memmap(root/'target.npy',mode='w+',dtype='float64',shape=(rows,n))
        offset=dest=0
        for length in lengths:
            for local in range(h,int(length),8192):
                size=min(8192,int(length)-local)
                block=counts[offset+local-h:offset+local+size,active].astype(float)
                if exog is not None:block=np.column_stack((block,exog[offset+local-h:offset+local+size]))
                x[dest:dest+size]=features(block,kernels)
                y[dest:dest+size]=counts[offset+local:offset+local+size,active]
                dest+=size
                x.flush();y.flush();evict(x);evict(y)
                write_json(root/'status.json',{'status':'BUILDING','rows_done':dest,'rows':rows,'pid':os.getpid(),'updated_unix':time.time()})
            offset+=int(length)
        del x,y
        write_json(marker,{'rows':rows,'cols':cols,'targets':n,'dtype':'float64'})
    x=np.load(root/'design.npy',mmap_mode='r');y=np.load(root/'target.npy',mmap_mode='r')
    checkpoint=root/'checkpoint.npz'
    if checkpoint.exists():
        with np.load(checkpoint) as z:initial=z['vector']
    else:
        means=np.zeros(n)
        for start in range(0,len(y),8192):means+=y[start:start+8192].sum(axis=0);evict(y)
        initial=np.r_[np.zeros(cols*n),np.log(np.maximum(means/len(y),1e-12))]
    started=time.time();evaluations=0
    def fun(vector):
        nonlocal evaluations
        value,grad=objective(vector,x,y,ridge);evaluations+=1
        if np.isfinite(value):
            status={'status':'FITTING','pid':os.getpid(),'evaluation':evaluations,'objective':value,'gradient_inf_norm':float(np.max(np.abs(grad))),'elapsed_s':time.time()-started,'updated_unix':time.time()}
            write_json(root/'status.json',status);print(status,flush=True)
        return value,grad
    def accepted(vector):
        tmp=root/'checkpoint.tmp.npz';np.savez(tmp,vector=vector);tmp.replace(checkpoint)
    fitted=minimize(fun,initial,method='L-BFGS-B',jac=True,callback=accepted,
        options={'maxiter':max_iter,'ftol':min(tol,1e-12),'gtol':tol,'maxcor':10,'maxls':30})
    accepted(fitted.x)
    coef=fitted.x[:cols*n].reshape(cols,n)
    coupling=_unpack(coef[:n*n_basis],n,n_basis)
    filt=np.zeros((counts.shape[1],counts.shape[1],h));filt[np.ix_(active,active)]=np.einsum('ijk,tk->ijt',coupling,kernels)
    b=np.zeros(counts.shape[1]);b[active]=fitted.x[cols*n:]
    xf=None if q==0 else np.einsum('ijk,tk->ijt',_unpack(coef[n*n_basis:],q,n_basis),kernels)
    norm=float(np.max(np.abs(fitted.jac)))
    diagnostics={'function_val':float(fitted.fun),'num_steps':int(fitted.nit),'converged':bool(fitted.success and norm<=max(tol,1e-5)),
        'optimizer_success':bool(fitted.success),'gradient_inf_norm':norm,'reached_max_steps':bool(fitted.nit>=max_iter),
        'message':str(fitted.message),'solver':'DISK_LBFGS','precision':'float64','feature_cache':str(root),'resume':'parameter-only L-BFGS restart'}
    write_json(root/'status.json',{'status':'DONE','updated_unix':time.time(),**diagnostics})
    return FitResult(filt,b,kernels,xf,bin_s,active,diagnostics)
