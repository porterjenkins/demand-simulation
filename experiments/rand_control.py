import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import argparse

from sim.simulator import Simulator
from sim import cfg

from recommenders.rand_reco import RandomRecommender
from recommenders.reco_manager import RecommendationManager


def exec_sim():
    displays = cfg.get_display_names()
    agents = []

    for d in displays:
        agents.append(RandomRecommender(disp=d))

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--n-runs', type=int, default=None, help='number of runs')
    args = parser.parse_args()
    main(n_runs=args.n_runs)