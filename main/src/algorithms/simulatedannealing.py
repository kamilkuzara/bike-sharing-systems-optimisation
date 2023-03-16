import math
import random


hyperparameters = {
    "initial_probability_threshold": 0.95,
    "alpha": 0.75,   # rate of change for temperature, should be within range (0.8, 0.99)
    "beta": 1.05,    # rate of change for phase length, should be > 1
    "min_temp": 5,   # termination criterion, we stop the search when the temperature gets below this value
    "initial_phase_length": 10
}


# Compute the initial temperature such that the probability for accepting all neighbours
# is at or above a certain level speciied as "initial_probability_threshold" in the hyperparameters dict.
#
# Note, that the neighbours with the maximal negative difference of cost to the current solution will be
# the least likely to be accepted. As such, to make sure that all neighbours of the initial solution will
# be accepted with a given threshold probability, we need to compute the temperature for the maximum possible
# difference.
#
# @return initial temperature that accepts all neighbours with at least the threshold probability
def compute_initial_temp(max_cost_difference):
    return -1 * max_cost_difference / math.log( hyperparameters["initial_probability_threshold"] )


def update_temp(temp):
    return hyperparameters["alpha"] * temp


def update_phase_length(phase_length):
    return math.ceil( hyperparameters["beta"] * phase_length )


# def compute_initial_phase_length():
#     pass


def simulated_annealing(problem):
    # compute the initial solution/configuration
    current_config = problem.generate_solution()
    best_config = current_config

    phase_length = hyperparameters["initial_phase_length"]
    temp = compute_initial_temp(current_config.get_max_cost_difference())

    finished = False
    while not finished:
        for i in range(phase_length):
            new_config = current_config.generate_neighbour()

            if new_config.cost < current_config.cost: # remember, lower cost is better
                # accept the new configuration, i.e. move to this solution
                current_config = new_config
                if new_config.cost < best_config.cost:    # if also the best config yet, update the best
                    best_config = new_config
            # else (if new config is worse than current config), accept with certain probability
            elif math.exp( (current_config.cost - new_config.cost) / temp ) >= random.random():
                current_config = new_config

        phase_length = update_phase_length(phase_length)
        temp = update_temp(temp)

        if temp < hyperparameters["min_temp"]:  # stopping criterion for the search
            finished = True

    return best_config
