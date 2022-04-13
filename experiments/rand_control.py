from sim.simulator import Simulator
from sim import cfg

from recommenders.rand_reco import RandomRecommender

displays = cfg.get_display_names()
agents = {}

for d in displays:
    agents[d] = RandomRecommender(disp=d)

sim = Simulator.build_sim()
sim.main(agents)