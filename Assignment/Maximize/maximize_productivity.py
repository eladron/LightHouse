import pulp
import pandas as pd
import sys
import re
import random
import json


CANTWORK = -1000000 # represents a worker that can't work in a station
STATIONS_NAMES = ["piston", "handle", "water", "screw"] # The names of the stations
STATIONS_NAMES_HEBREW = ["בוכנה", "ידית ישר","עמדת מים", "ברגים"] # The names of the stations

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
    exit(0)

# Handle the is coming column
def handle_is_comming(df: pd.DataFrame):
    if df.iloc[0:1, 0].values[0] != "האם מגיע?":
        error("העמודה הראשונה האם מגיע? חסרה")
    is_all_integers = df.iloc[1:-1, 0].apply(lambda x: x==0 or x==1).all()
    if not is_all_integers:
        error("העמודה האם מגיע? מכילה מספרים שאינם 0 או 1")
    df = df.loc[df.iloc[:, 0] != 0]
    df = df.iloc[:, 1:] # Remove the is coming column
    return df

# Handle the station counts row
def handle_station_counts(df: pd.DataFrame):
    station_counts = list(df.iloc[-1])
    if (any( not isinstance(x, int) or x <= 0 for x in station_counts)):
        error("השורה של כמות המכונות אינה מכילה מספרים חיובים שלמים")
    df.drop(index=df.index[-1], axis=0, inplace=True)
    return station_counts, df

# Handle the workers productivity
def handle_workers_productivity(df: pd.DataFrame):
    for i in range(0, len(df.columns)):
        are_positive_integers = df.iloc[:, i].apply(lambda x: isinstance(x, int) and (x>0 or x == CANTWORK)).all()
        if not are_positive_integers:
            error(f"העמודה {STATIONS_NAMES[i]}  # אינה מכילה מספרים שלמים חיוביים למעט")

def preprocess():
    try:
        df = pd.read_excel(sys.argv[1], index_col=0)
    except:
        error("הקובץ אינו קובץ מסוג אקסל")
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


def solve_aux(workers_names, station_counts, prod, Q, P, T, S, add_kedam):
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
        tmp = Q[s]
        if s < 2:
            tmp = max(Q[s], Q[s+1] - P[s+1]) # The station inside the pipeline has to have at the end of the day more that what that next station had to made
        problem += P[s] + pulp.lpSum(assign[w][s] * prod[w][s] * T for w in workers) >= tmp # At the end of the day, each station has made at least the required amount of product
    if add_kedam:
        for i in range(2):
            problem += P[i] + pulp.lpSum(assign[w][i] * prod[w][i] * T for w in workers) >= P[i+1] + pulp.lpSum(assign[w][i+1] * prod[w][i+1] * T for w in workers) # every station has more product than the next station
    #problem += P[0] + pulp.lpSum((assign[w][0] * prod[w][0] + assign[w][2] * prod[w][2])* T for w in workers)  <= P[1] + pulp.lpSum(assign[w][1] * prod[w][1] * T * 2 for w in workers) # Delta constraint 

    solver = pulp.PULP_CBC_CMD(msg=0)
    problem.solve(solver=solver)
    count = 0 if add_kedam else 2
    able_to_remove = 2 if add_kedam else 0
    finish = len(problem.constraints) - able_to_remove
    while (problem.status != pulp.LpStatusOptimal):
        if len(problem.constraints) == finish:
            return 0, None, count
        problem.constraints.popitem()
        count += 1
        problem.solve(solver=solver)
    return pulp.value(problem.objective), assign, count


def solve(workers_names, station_counts, prod, Q, P, T, S ,add_kedam = True):
    best_productivity = 0
    best_assign = None
    best_count = 3
    n = len(STATIONS_NAMES)
    i = sum(station_counts) - len(workers_names) if len(workers_names) < sum(station_counts) else 0
    for arr in generate_arrays(i, n):
        new_station_counts = [station_counts[j] - arr[j] for j in range(n)]
        product, assign, count = solve_aux(workers_names, new_station_counts, prod, Q, P, T, S, add_kedam)
        if best_count > count:
            best_count = count
            best_productivity = product
            best_assign = assign
        elif best_count == count and product > best_productivity:
            best_productivity = product
            best_assign = assign
    return best_productivity, best_assign, best_count


def get_product_made(stations, workers,  P, assign, prod, T):
    made = [0] * len(stations)
    for s in stations:
        made[s] = P[s] + sum(pulp.value(assign[w][s]) * prod[w][s] * T for w in workers)
    return made


def start_ascending(workers_names, station_counts, prod, Q, P, T, S, assign):
    best_assign = assign
    while True:
        made = get_product_made(range(len(STATIONS_NAMES)), range(len(workers_names)),  P, best_assign, prod, T)
        min_made = min(made[:2])
        min_index = made.index(min_made)
        last_Q_i = Q[min_index]
        Q[min_index] = int(Q[min_index] * 1.1)
        temp_prod, tmp_assign, _ = solve(workers_names, station_counts, prod, Q, P, T, S, False)
        if temp_prod == 0:
            Q[min_index] = last_Q_i
            break
        else:
            best_assign = tmp_assign
    return best_assign


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
    prod = [list(df.loc[worker]) for worker in workers_names]

    best_productivity , best_assign, best_count = solve(workers_names, station_counts, prod, Q, P, T, S)


    if best_productivity == 0:
        error("אין שיבוץ אפשרי, אנא בדוק את הנתונים שהוכנסו בקובץ האקסל או הנתונים באתר")

    
    if best_count != 0:
        print("Warning: not all constrains are met")
        last_Q = Q.copy()
        best_assign = start_ascending(workers_names, station_counts, prod, Q, P, T, S, best_assign)
        Q = last_Q
    

    workers = range(len(workers_names))
    stations = range(len(STATIONS_NAMES))
    random_workers = workers #random.sample(workers, len(workers_names))
    assigned_workers = []

    data["Status"] = "Success"

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
    
    made = get_product_made(stations, workers,  P, best_assign, prod, T)
    for s in stations:
        tmp = made[s]
        if s in [1,2]:
            tmp = made[s] if made[s] < made[s-1] else made[s-1]
        print(f"{STATIONS_NAMES[s]} made {tmp} and needed {Q[s]}")
    
    data['product_piston'] = made[0]
    data['product_handle'] = made[1] if made[1] < made[0] else made[0]
    data['product_water'] = made[2] if made[2] < made[1] else min(made[0], made[1])
    data['product_screw'] = made[3] 
    
    best_productivity = min(made[:3]) * S[0] + made[3] * S[1]
    print("Total Productivity:", best_productivity / 100)
    data['revenue'] = str(best_productivity / 100)

    print("Constrains removed:", best_count)

    with open("output.json", 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    main()  