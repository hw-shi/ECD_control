TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
END_OPT_STRING = "\n" + "=" * 60 + "\n"
import numpy as np
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)  # supress warnings
import h5py

import ECD_control.ECD_optimization.tf_quantum as tfq
import qutip as qt
import datetime
import time
from typing import List, Dict


class GateSet:

    """
    This class is intended to be a barebones implementation of a specific gate set. Here, we only want to define the blocks in the gate
    set and the parameters that will be optimized. This class will be passed to the GateSynthesizer class which will call the optimizer
    your choice to optimize the GateSet parameters.
    """
    
    def __init__(
        self,
        N_blocks=20,
        name="ECD_control",
        **kwargs
    ): # some of the above may not be necessary. i.e. dimension, N_blocks, n_parameters are implicit in some of the defs below. think about this
        self.parameters = {
            'N_blocks' : N_blocks,
            'name' : name,
            }
        self.parameters.update(kwargs)
        

    def modify_parameters(self, **kwargs):
        # currently, does not support changing optimization type.
        # todo: update for multi-state optimization and unitary optimziation
        parameters = kwargs
        for param, value in self.parameters.items():
            if param not in parameters:
                parameters[param] = value
        self.__init__(**parameters)

    @tf.function
    def batch_construct_block_operators(self, opt_params: Dict[str, tf.Variable], *args):
        """
        This function must take a dict of tf.Variable defined in the same order as randomize_and_set_vars()
        and construct a batch of block operators. Note that the performance of the optimization depends heavily
        on your implementation of this function. For the best performance, do everything with vectorized operations
        and decorate your implementation with @tf.function.

        Parameters
        -----------
        opt_params  :   dict of optimization parameters. This dict must be of the same length
                        as the one defined in ``randomize_and_set_vars``. Each element in the dict
                        should be of dimension (N_blocks, N_multistart).
        
        Returns
        -----------
        tf.tensor of block operators U of size (N_multistart, U.shape)
        """
        
        pass

    def randomize_and_set_vars(self, parallel):
        """
        This function creates the tf variables over which we will optimize and randomizes their initial values.

        Parameters
        -----------
        parallel    :   Second dimension of initial variables. This is the length of the batch axis which the optimizer
                        optimizes simultaneously.

        Returns
        -----------
        dict of tf.Variable (no tf.constants are allowed) of dimension (N_blocks, parallel) with initialized values.
        Note that the variables in this dict that will be optimized must have ``trainable=True``
        """

        pass

    def create_optimization_mask(self, parallel, *args):
        """
        Parameters
        -----------
        parallel  :   Length of optimization mask to create. This is the length of the batch axis which the optimizer
                    optimizes simultaneously.
                    

        Returns
        -----------
        Dict of integer arrays with as many items as the dict returned by ``randomize_and_set_vars``.
        This mask is used to exclude some parameters from the gradient calculation. The shape of each array
        should be (N_blocks, parallel)
        """
        
        self.optimization_mask = None
        pass

    def preprocess_params_before_saving(self, opt_params: Dict[str, tf.Variable], *args):
        """
        When defined, this function defines a way to process the optimization parameters before they are saved
        in the h5 file. See the ECD_gate_set for an example of this in action.

        Parameters
        -----------
        opt_params  :   Dict of optimization parameters. This dict must be of the same length
                        as the one defined in ``randomize_and_set_vars``. Each element in the dict
                        should be of dimension (N_blocks, N_multistart).

        Returns
        -----------
        Dict of tf.Variable. This dict does not need to be the same length as opt_params. Conversion to numpy 
        arrays is handled in the batch optimizer.
        
        """
        
        return opt_params