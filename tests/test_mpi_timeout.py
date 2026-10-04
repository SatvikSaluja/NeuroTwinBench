"""MPI communication timeout must be scoped and restored on failure."""
import unittest
from unittest.mock import patch
from hnn_core import parallel_backends
from neurotwinbench.simulate import _mpi_output_timeout


class TimeoutTests(unittest.TestCase):
    def test_extends_short_timeout_and_restores_after_exception(self):
        with patch.object(parallel_backends, 'run_subprocess') as original:
            with self.assertRaisesRegex(RuntimeError, 'failure'):
                with _mpi_output_timeout(600):
                    parallel_backends.run_subprocess('cmd', {}, 60, env={})
                    original.assert_called_once_with('cmd', {}, 600, env={})
                    raise RuntimeError('failure')
            self.assertIs(parallel_backends.run_subprocess, original)

    def test_keeps_already_longer_timeout(self):
        with patch.object(parallel_backends, 'run_subprocess') as original:
            with _mpi_output_timeout(600):
                parallel_backends.run_subprocess('cmd', {}, 900)
            original.assert_called_once_with('cmd', {}, 900)


if __name__ == '__main__':
    unittest.main()
