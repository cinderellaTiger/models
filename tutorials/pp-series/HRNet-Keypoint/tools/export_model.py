# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

# add python path of PadleDetection to sys.path
parent_path = os.path.abspath(os.path.join(__file__, *(['..'] * 2)))
sys.path.insert(0, parent_path)

# ignore warning log
import warnings
warnings.filterwarnings('ignore')
import glob

import paddle
from lib.utils.workspace import load_config, merge_config
from lib.slim import build_slim_model
from lib.core.trainer import Trainer
from lib.utils.check import check_gpu, check_version, check_config
from lib.utils.cli import ArgsParser
from lib.utils.logger import setup_logger

logger = setup_logger('eval')


def parse_args():
    parser = ArgsParser()
    parser.add_argument(
        "--save-inference-dir",
        default='output_inference',
        type=str,
        help="Evaluation directory, default is current directory.")

    args = parser.parse_args()
    return args


def main():
    FLAGS = parse_args()
    cfg = load_config(FLAGS.config)
    # cfg['output_eval'] = FLAGS.output_eval
    merge_config(FLAGS.opt)

    if cfg.use_gpu:
        paddle.set_device('gpu')
    else:
        paddle.set_device('cpu')

    if 'slim' in cfg:
        cfg = build_slim_model(cfg, mode='test')

    check_config(cfg)
    check_gpu(cfg.use_gpu)
    check_version()

    # build trainer
    trainer = Trainer(cfg, mode='test')

    # load weights
    trainer.load_weights(cfg.weights)

    # export model
    trainer.export(output_dir=FLAGS.save_inference_dir)


if __name__ == '__main__':
    main()
