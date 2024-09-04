import csv
import json


def json_to_csv(name, csv_name):
    with open(name, "r") as f:
        data = json.loads(f.read())

    keys = list(data[0].keys())

    with open(csv_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for item in data:
            writer.writerow([item[key] for key in keys])


# json_to_csv("FINAL_customers.json")
