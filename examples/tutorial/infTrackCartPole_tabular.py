"""
Cart-pole balancing with tabular representation
"""
from rlpy.Domains import InfCartPoleBalance
from rlpy.Agents import Q_Learning
from rlpy.Representations import *
from rlpy.Policies import eGreedy
from rlpy.Experiments import Experiment
import numpy as np
from hyperopt import hp

param_space = {'discretization': hp.quniform("resolution", 4, 40, 1),
               'lambda_': hp.uniform("lambda_", 0., 1.),
               'boyan_N0': hp.loguniform("boyan_N0", np.log(1e1), np.log(1e5)),
               'initial_alpha': hp.loguniform("initial_alpha", np.log(5e-2), np.log(1))}


def make_experiment(
        id=1, path="./Results/Temp/{domain}/{agent}/{representation}/",
        boyan_N0=753,
        initial_alpha=.7,
        discretization=20.,
        lambda_=0.75):
    max_steps = 5000
    num_policy_checks = 10
    checks_per_policy = 10

    domain = InfCartPoleBalance(episodeCap=1000)
    representation = Tabular(domain,
                             discretization=discretization)
    policy = eGreedy(representation, epsilon=0.1)
    agent = Q_Learning(
        representation, policy, domain, lambda_=lambda_, initial_alpha=initial_alpha,
        alpha_decay_mode="boyan", boyan_N0=boyan_N0)
    experiment = Experiment(**locals())
    return experiment

if __name__ == '__main__':
    experiment = make_experiment(1)
    experiment.run_from_commandline()
    experiment.plot()