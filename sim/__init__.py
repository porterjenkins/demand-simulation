import os
import sys

path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

from sim_cfg import SimCfg
cfg = SimCfg("./cfg.yaml")