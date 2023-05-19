import random
import pandas as pd
import sys

def duplicate_prefs(prefs, station_counts):
    new_prefs = []
    sorted_prefs = sorted(enumerate(prefs), key=lambda x: x[1])
    sorted_prefs = [i[0] + 1 for i in sorted_prefs if i[1] != 0]
    for station in sorted_prefs:
        new_prefs.extend([station] * station_counts[station-1])
    return new_prefs

def preprocessor_df(df):
    stations = [1,2,3,4]
    workers = [i for i in range(1, 21)]
    df.replace("#" , 0, inplace=True)
    df.dropna(how='all', inplace=True)
    df.drop(df.columns[4], axis=1, inplace=True)
    df1 = df.iloc[23:, :]
    df1.drop(df1.index[-1], inplace=True)
    df1.columns = stations.copy()
    df1.index = workers.copy()
    df2 = df.iloc[0:21, :]
    df2 = df2.transpose()
    df2 = df2.iloc[:, 1:]
    df2.index = stations.copy()
    df2.columns = workers.copy()
    return df1 , df2

def main():
    if len(sys.argv) != 2:
        print("Usage: python lloyd-shaply.py info.xlsx")
        exit(1)

    df = pd.read_excel(sys.argv[1], index_col=0)
    df1, df2 = preprocessor_df(df)


    station_counts = [3, 3, 3, 11]
    free_workers = [i for i in range(1, 21)]
    assignments = {}

    # Check Tables
    if df1.index.tolist() != df2.columns.tolist():
        print("The two tables must have the same workers.")
        exit(1)
    if df1.columns.tolist() != df2.index.tolist():
        print("The two tables must have the same stations.")
        exit(1)
    if len(df1.index.to_list()) != sum(station_counts):
        print("The number of workers should be equal to the number of stations.")
        exit(1)

    while free_workers:
        worker = random.choice(free_workers)
        prefs = duplicate_prefs(df1.loc[worker].tolist(), station_counts)
        free_workers.remove(worker)
        for station in prefs:
            if station not in assignments.values():
                assignments[worker] = station
                break
            elif len([s for s in assignments.values() if s == station]) < station_counts[station-1]:
                assignments[worker] = station
                break
            else:
                currents = [w for w in assignments.keys() if assignments[w] == station]
                worst_grade = 0
                worst_worker = None
                for current in currents:
                    if df2[current][station] > worst_grade:
                        worst_grade = df2[current][station]
                        worst_worker = current 
                if df2[worker][station] > worst_grade:
                    assignments[worker] = station
                    del assignments[worst_worker]
                    free_workers.append(worst_worker)
                    break

    # print the final assignments
    print("Final Assignments:")
    for worker, station in sorted(assignments.items()):
        print(f"worker {worker}: station {station}")


if __name__ == "__main__":
    main()