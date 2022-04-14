from sim.simulator import Simulator
from sim import cfg

from recommenders.demand_match_agent import DemandMatchRecommender
from recommenders.reco_manager import RecommendationManager

displays = cfg.get_display_names()
agents = []

for d in displays:
    agents.append(
        DemandMatchRecommender(
            disp=d, prod2idx=cfg.prod2idx
        )
    )

reco_manager = RecommendationManager(agents)

sim = Simulator.build_sim()
sim.main(reco_manager)