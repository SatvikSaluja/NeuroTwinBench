import unittest
import numpy as np
import jax
jax.config.update('jax_enable_x64',True)
import jax.numpy as jnp
import nemos as nmo
from nemos.glm.params import GLMParams
from neurotwinbench.fit import _build_design,_basis_kernels
from neurotwinbench.disk_fit import features,objective

class DiskFitTests(unittest.TestCase):
    def test_features_loss_gradient_against_nemos(self):
        rng=np.random.default_rng(32)
        spikes=rng.poisson(.2,(170,4));drive=rng.poisson(.15,(170,1));h=25;k=5
        xx,yy,_,basis,_=_build_design(spikes,.001,25,k,drive,segment_lengths=[81,89])
        kernels=_basis_kernels(basis,h,k)
        x=np.concatenate([features(np.column_stack((spikes[a:b],drive[a:b])),kernels) for a,b in [(0,81),(81,170)]])
        np.testing.assert_allclose(x,xx,rtol=1e-12,atol=1e-12)
        coef=rng.normal(0,.02,(25,4));b=np.full(4,np.log(.2));vector=np.r_[coef.ravel(),b]
        value,gradient=objective(vector,x,yy,.01,chunk=17)
        glm=nmo.glm.PopulationGLM(regularizer='Ridge',regularizer_strength=.01)
        params=GLMParams(coef=jnp.array(coef),intercept=jnp.array(b))
        fun=glm.regularizer.penalized_loss(glm._compute_loss,params,glm.regularizer_strength)
        expected,g=jax.value_and_grad(fun)(params,jnp.array(xx),jnp.array(yy))
        self.assertAlmostEqual(value,float(expected),places=11)
        np.testing.assert_allclose(gradient,np.r_[np.array(g.coef).ravel(),np.array(g.intercept)],atol=1e-11)
        value2,g2=objective(vector,x,yy,.01,chunk=41)
        self.assertAlmostEqual(value,value2,places=11)
        np.testing.assert_allclose(gradient,g2,atol=1e-11)

if __name__=='__main__':unittest.main()
