###Directory structure
  The content of the project is divided into 3 directories - main, test, data.

  *main* directory - contains the source code for the solver
  *test* directory - contains the test problems, SA hyperparameters for parameter tuning
                     as well as the solutions produced during testing and the gathered data
  *data* directory - contains the real-world data (or download scripts) used for exploratory data analysis
                     and test problem generation; the directory also contains the code written for EDA and the results of the analysis

###Usage
  ./main/main.py <problem_file> [algorithm_code] [solution_file]

  Available algorithms:
    1 (default) - Simulated Annealing on a single instance of SBRP
    2 - Simulated Annealing on multiple instances of 1-PDTSP

###Requirements
  python3 [version 3.7.5 or higher]

  For the main software (/main):
    scikit-learn [version 0.24.2 or higher]
    geopy [version 2.3.0 or higher]

  For data analysis and visualisation (/data):
    pandas [version 1.3.5 or higher]
    geopandas [version 0.10.2 or higher]
    matplotlib [version 3.5.3 or higher]
