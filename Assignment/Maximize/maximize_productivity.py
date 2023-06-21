import pulp
import pandas as pd
import sys
import re
import random
import json


CANTWORK = -1000000 # represents a worker that can't work in a station
STATIONS_NAMES = ["piston", "handle", "water", "screw"] # The names of the stations

# Custom function to replace strings representing numbers with integers
def replace_string_with_integer(cell):
    if isinstance(cell, str):
        num_str = re.findall('\d+', cell)
        if num_str:
            return int(''.join(num_str))
    return cell

def replace_special_strings(df: pd.DataFrame):
    df.replace("#",CANTWORK, inplace=True)
    df.replace("- ∞", CANTWORK, inplace=True)
    df.replace(0, CANTWORK, inplace=True)

# Insert each station to the data dictionary
def insert_to_data(data: dict, station: int, worker_name: str, station_name: str):
    data[station] = {"worker": worker_name, "station": station_name}

# Print error message and exit
def error(message: str = ""):
    data = {"Status" : "Error","Message": message}
    with open("output.json", 'w') as f:
        json.dump(data, f, indent=4)
    exit(1)

# Handle the is coming column
def handle_is_comming(df: pd.DataFrame):
    if df.iloc[0:1, 0].values[0] != "האם מגיע?":
        error("is coming column is missing isn't the first column")
    is_all_integers = df.iloc[1:-1, 0].apply(lambda x: x==0 or x==1).all()
    if not is_all_integers:
        error("is coming column is not all 0 or 1")
    df = df.loc[df.iloc[:, 0] != 0]
    df = df.iloc[:, 1:] # Remove the is coming column
    return df

# Handle the station counts row
def handle_station_counts(df: pd.DataFrame):
    station_counts = list(df.iloc[-1])
    df.drop(index=df.index[-1], axis=0, inplace=True)
    return station_counts, df

# Handle the workers productivity
def handle_workers_productivity(df: pd.DataFrame):
    for i in range(0, len(df.columns)):
        is_all_integers = df.iloc[:, i].apply(lambda x: isinstance(x, int)).all()
        if not is_all_integers:
            error(f"column {STATIONS_NAMES[i]} is not all integers")

def preprocess():
    df = pd.read_excel(sys.argv[1], index_col=0)
    df = df.applymap(replace_string_with_integer)
    df = handle_is_comming(df)
    replace_special_strings(df)
    df.drop(columns = df.columns[-1], inplace=True) # Last column is irrelevant
    station_counts, df = handle_station_counts(df)
    handle_workers_productivity(df)
    workers_names = [int(x) for x in list(df.index)]
    df.index = workers_names
    return df, station_counts, workers_names

def generate_arrays(i, n):
    if n == 1:
        yield [i]
        return
    for j in range(i + 1):
        for arr in generate_arrays(i - j, n - 1):
            yield [j] + arr

def solve(workers_names, station_counts, prod, Q, P, T, S):
    workers = range(len(workers_names))
    stations = range(len(STATIONS_NAMES))


    problem = pulp.LpProblem("Worker_Station_Assignment", pulp.LpMaximize)
    # create the decision variables
    assign = pulp.LpVariable.dicts("Assign", (workers, stations), lowBound=0, upBound=1, cat=pulp.LpInteger)

    # define the objective function to maximize the total productivity    
    objective = pulp.lpSum(((prod[i][2] * assign[i][2] * S[0] + prod[i][3] * assign[i][3] * S[1]) * T) for i in workers)
    problem += objective

    # add the constraints
    for w in workers:
        problem += pulp.lpSum(assign[w][s] for s in stations) <= 1 # every worker is assigned to exactly one station
    for s in stations:
        problem += pulp.lpSum(assign[w][s] for w in workers) == station_counts[s] # every station has exactly the required number of workers
    problem += pulp.lpSum(assign[w][s] for w in workers for s in stations) == min(len(workers_names), 20) # at most 20 workers are assigned
    for s in stations:
        tmp = Q[s] if s > 2 else Q[2]
        problem += P[s] + pulp.lpSum(assign[w][s] * prod[w][s] * T for w in workers) >= tmp # every station has at least the required amount of product
    for i in range(2):
        problem += P[i] + pulp.lpSum(assign[w][i] * prod[w][i] * T for w in workers) >= P[i+1] + pulp.lpSum(assign[w][i+1] * prod[w][i+1] * T for w in workers) # every station has at least the required amount of product
    #problem += P[0] + pulp.lpSum((assign[w][0] * prod[w][0] + assign[w][2] * prod[w][2])* T for w in workers)  <= P[1] + pulp.lpSum(assign[w][1] * prod[w][1] * T * 2 for w in workers) # Delta constraint 

    solver = pulp.PULP_CBC_CMD(msg=0)
    problem.solve(solver=solver)
    count = 0
    finish = len(problem.constraints) - 2
    while (problem.status != pulp.LpStatusOptimal):
        if len(problem.constraints) == finish:
            return 0, None, count
        problem.constraints.popitem()
        count += 1
        problem.solve(solver=solver)
    return pulp.value(problem.objective), assign, count

def main():
    if len(sys.argv) != 13:
        print("Usage: python maximize_productivity.py  <input_file> <Amount1> <Amount2> <Amount3> <Amount4> <reserve1> <reserve2> <reserve3> <reserve4> <hours> <profit3> <profit4>")
        error("Wrong number of arguments")

    df, station_counts, workers_names  = preprocess()

    data = {}

    Q = [int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])] #  needed_amount
    P = [int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]), int(sys.argv[9])] # reservers
    T = float(sys.argv[10])
    S = [float(sys.argv[11]), float(sys.argv[12])]
    print(f"Q = {Q}")
    print(f"P = {P}")
    print(f"T = {T}")
    print(f"S = {S}")
    places_for_station_water = [1, 2, 5]

    best_productivity = 0
    best_assign = None
    best_count = 3

    # define the objective function to maximize the total grade
    prod = [list(df.loc[worker]) for worker in workers_names]
    n = len(STATIONS_NAMES)
    i = sum(station_counts) - len(workers_names) if len(workers_names) < sum(station_counts) else 0
    for arr in generate_arrays(i, n):
        new_station_counts = [station_counts[j] - arr[j] for j in range(n)]
        product, assign, count = solve(workers_names, new_station_counts, prod, Q, P, T, S)
        if best_count > count:
            best_count = count
            best_productivity = product
            best_assign = assign
        elif best_count == count and product > best_productivity:
            best_productivity = product
            best_assign = assign

    if best_productivity == 0:
        error("No solution found")

    print("Total Productivity:", best_productivity / 100)
    print("Constrains removed:", best_count)
    workers = range(len(workers_names))
    stations = range(len(STATIONS_NAMES))
    random_workers = random.sample(workers, len(workers_names))
    assigned_workers = []

    for i in range(1, 21):
        if i in places_for_station_water:
            for w in random_workers:
                if pulp.value(best_assign[w][2]) == 1 and workers_names[w] not in assigned_workers:
                    print(f"Station {i},{STATIONS_NAMES[2]} is assigned with worker {workers_names[w]}")
                    insert_to_data(data, i, workers_names[w], STATIONS_NAMES[2])
                    assigned_workers.append(workers_names[w])
                    break
        else:
            for w in random_workers:
                if workers_names[w] not in assigned_workers:
                    assigned = 0
                    for s in stations:
                        if pulp.value(best_assign[w][s]) == 1:
                            assigned = s
                            break
                    insert_to_data(data, i, workers_names[w], STATIONS_NAMES[assigned])
                    print(f"Station {i},{STATIONS_NAMES[assigned]} is assigned with worker {workers_names[w]}")
                    assigned_workers.append(workers_names[w])
                    break
    for s in stations:
        made = P[s] + sum(pulp.value(best_assign[w][s]) * prod[w][s] * T for w in workers)
        needed = Q[s] if s > 2 else Q[2]
        print(f"{STATIONS_NAMES[s]} made {made} and needed {needed}")
    
    with open("output.json", 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()  