import csv

def read_positions_from_csv(filename):
    positions = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader) # skipping my header
        for row in reader:
            positions.append((float(row[0]), float(row[1]), float(row[2])))
    return positions

a = read_positions_from_csv('settings_terasaki_positions.csv')