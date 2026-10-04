import unittest
import numpy as np
from neurotwinbench.uncertainty import paired_node_bootstrap,paired_location_bootstrap
from neurotwinbench.simulate import SimulationConfig,build_network
from experiments.design_pilots import check_swap

class Phase2Tests(unittest.TestCase):
    def test_identical_scores_have_zero_paired_interval(self):
        rng=np.random.default_rng(8);truth=rng.random((9,9))<.3;scores=rng.normal(size=(9,9));mask=np.ones((9,9),bool)
        r=paired_node_bootstrap(truth,scores,scores,mask,repeats=30)
        np.testing.assert_equal(r['auc_difference_interval95'],[0.,0.]);np.testing.assert_equal(r['ap_difference_interval95'],[0.,0.]);self.assertTrue(mask.diagonal().all())
    def test_location_constant_effect(self):
        mask=np.zeros((8,8),bool);mask[:4,4:]=True
        a=paired_location_bootstrap(np.full((8,8),2.),mask,repeats=30)
        np.testing.assert_equal(a['conditional_node_interval95'],[2.,2.])
    def test_shared_design_and_swap(self):
        mixed=build_network(SimulationConfig(network='mixed_shared'))
        self.assertEqual(len(mixed.gid_ranges['shared_component']),1)
        self.assertFalse(mixed.external_drives['shared_component']['cell_specific'])
        self.assertTrue(mixed.external_drives['sustained']['cell_specific'])
        check_swap(build_network(SimulationConfig(network='location')),build_network(SimulationConfig(network='location_swapped')))
if __name__=='__main__':unittest.main()
