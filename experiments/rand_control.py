from sim.simulator import Simulator
from sim import cfg

from recommenders.rand_reco import RandomRecommender
from recommenders.reco_manager import RecommendationManager

displays = cfg.get_display_names()
agents = []

for d in displays:
    agents.append(RandomRecommender(disp=d))

reco_manager = RecommendationManager(agents)

sim = Simulator.build_sim()
sim.main(reco_manager)