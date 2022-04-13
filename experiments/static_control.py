from sim.simulator import Simulator
from sim import cfg

from recommenders.static_reco import StaticRecommender, UniformRecommender
from recommenders.reco_manager import RecommendationManager

displays = cfg.get_display_names()
agents = []

for d in displays:
    agents.append(UniformRecommender(disp=d))

reco_manager = RecommendationManager(agents)

sim = Simulator.build_sim()
sim.main(reco_manager)