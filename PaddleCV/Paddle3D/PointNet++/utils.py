#  Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserve.
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
"""
Contains common utility functions.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import logging
import numpy as np
import paddle.fluid as fluid

__all__ = ["chech_gpu"]

logger = logging.getLogger(__name__)


def check_gpu(use_gpu):
    """
    Log error and exit when set use_gpu=True in paddlepaddle
    cpu version.
    """
    err = "Config use_gpu cannot be set as True while you are " \
          "using paddlepaddle cpu version ! \nPlease try: \n" \
          "\t1. Install paddlepaddle-gpu to run model on GPU \n" \
          "\t2. Set --use_gpu=False to run model on CPU"

    try:
        if use_gpu and not fluid.is_compiled_with_cuda():
            logger.error(err)
            sys.exit(1)
    except Exception as e:
        pass


def parse_outputs(outputs):
    keys, values = [], []
    for k, v in outputs.items():
        keys.append(k)
        v.persistable = True
        values.append(v.name)
    return keys, values


class Stat(object):
    def __init__(self):
        self.stats = {}

    def update(self, keys, values):
        for k, v in zip(keys, values):
            if k not in self.stats:
                self.stats[k] = []
            self.stats[k].append(v)

    def reset(self):
        self.stats = {}

    def get_mean_log(self):
        log = ""
        for k, v in self.stats.items():
            log += "avg_{}: {:.4f}, ".format(k, np.mean(v))
        return log