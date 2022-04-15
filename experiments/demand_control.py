import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from sim.simulator import Simulator
from sim import cfg

from recommenders.demand_match_agent import DemandMatchRecommender
from recommenders.reco_manager import RecommendationManager

def exec_sim():
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
    return sim

def main(n_runs):
    ids = []
    for i in range(n_runs):
        sim = exec_sim()
        ids.append(sim.sim_id)

    print(ids)

if __name__ == "__main__":
    main(n_runs=5)