import pathlib
import os
from sim.sim_cfg import SimCfg

dir = pathlib.Path(__file__).parent.resolve()

cfg = SimCfg(os.path.join(dir, "cfg.yaml"))