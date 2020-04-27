#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright (c) 2019. ContinualAI. All rights reserved.                        #
# Copyrights licensed under the CC BY 4.0 License.                             #
# See the accompanying LICENSE file for terms.                                 #
#                                                                              #
# Date: 15-07-2019                                                             #
# Author: ContinualAI                                                          #
# E-mail: contact@continualai.org                                              #
# Website: continualai.org                                                     #
################################################################################

""" Avalanche usage examples """

# Python 2-3 compatible
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import torch
from torch.utils.tensorboard import SummaryWriter

from avalanche.benchmarks import CMNIST
from avalanche.evaluation.metrics import ACC, CF, RAMU, CM
from avalanche.extras.models import SimpleMLP
from avalanche.training.strategies import Naive
from avalanche.evaluation import EvalProtocol


# Tensorboard setup
from avalanche.training.strategies.ar1 import AR1

exp_name = "mnist_test"
log_dir = '../logs/' + exp_name
writer = SummaryWriter(log_dir)

# load the model with PyTorch for example
model = SimpleMLP()

# load the benchmark as a python iterator object
cdata = CMNIST()

# Eval Protocol
evalp = EvalProtocol(metrics=[ACC, CF, RAMU, CM], tb_writer=writer)

# adding the CL strategy
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
clmodel = Naive(model, eval_protocol=evalp, device=device)

# getting full test set beforehand
test_full = cdata.get_full_testset()

results = []

# loop over the training incremental batches
for i, (x, y, t) in enumerate(cdata):

    # training over the batch
    print("Batch {0}, task {1}".format(i, t))
    clmodel.train(x, y, t)

    # here we could get the growing test set too
    # test_grow = cdata.get_growing_testset()

    # testing
    results.append(clmodel.test(test_full))

writer.close()
