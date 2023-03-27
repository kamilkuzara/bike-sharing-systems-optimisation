import json

init_prob = 0.95
init_phase = 10
params_sets = []
alpha_values = [0.8, 0.85, 0.95]
beta_values = [1.05, 1.10, 1.20]
min_temp_values = [0.01, 0.005, 0.001]

for a_val in alpha_values:
    for b_val in beta_values:
        for t_val in min_temp_values:
            hyperparameters = {
                "initial_probability_threshold": init_prob,
                "alpha": a_val,
                "beta": b_val,
                "min_temp_percentage": t_val,
                "initial_phase_length": init_phase
            }
            params_sets.append(hyperparameters)

counter = 1
for params in params_sets:
    filename = "hyperparameters" + str(counter) + ".json"
    try:
        with open(filename, "w") as params_file:
            json.dump(params, params_file, indent = "  ")
        counter += 1
    except Exception as e:
        print(e)
        print("Unable to save the hyperparameters to a file")
