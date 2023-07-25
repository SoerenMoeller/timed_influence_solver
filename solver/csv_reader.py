import csv
import os


def read_csv(file_name: str):
    """
    Read a csv file and extract the data point entries

    Parameters:
        file_name (str): Name of the csv file

    Returns:
        data (dict):
            Contains the read data points. Mapping from the variable pairs
            to the (list) of related statements
    """

    # get the (full) file name
    dir_name = os.path.dirname
    parent_dir: str = dir_name(dir_name(os.path.realpath(__file__)))
    path: str = os.path.join(parent_dir, "examples", f"{file_name}.csv")

    # save data in list first, to store data under specific index
    result = set()
    with open(path, encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for line in reader:
            line = list(map(lambda x: x.strip(), line))

            st = [line[0]]
            for i in range(1, len(line) - 1, 2):
                st.append((float(line[i]), float(line[i + 1])))
            if len(line) == 8:
                st.append(line[-1])

            result.add(tuple(st))

    return result
