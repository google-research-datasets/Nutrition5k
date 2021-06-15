r"""Script to compute statistics on nutrition predictions.

This script takes in a csv of nutrition predictions and computes absolute and
percentage mean average error values comparable to the metrics used to eval
models in the Nutrition5k paper. The input csv file of nutrition predictions
should be in the form of:
dish_id, calories, mass, carbs, protein
And the groundtruth values will be pulled from the metadata csv file provided
in the Nutrition5k dataset release where the first 5 fields are also:
dish_id, calories, mass, carbs, protein

Example Usage:
python compute_statistics.py path/to/groundtruth.csv path/to/predictions.csv \
path/to/output_statistics.json
"""

import json
from os import path
import statistics
import sys

DISH_ID_INDEX = 0
DATA_FIELDNAMES = ["dish_id", "calories", "mass", "fat", "carb", "protein"]


def ReadCsvData(filepath):
  if not path.exists(filepath):
    raise Exception("File %s not found" % path)
  parsed_data = {}
  with open(filepath, "r") as f_in:
    filelines = f_in.readlines()
    for line in filelines:
      data_values = line.strip().split(",")
      parsed_data[data_values[DISH_ID_INDEX]] = data_values
  return parsed_data

if len(sys.argv) != 4:
  raise Exception("Invalid number of arguments\n\n%s" % __doc__)

groundtruth_csv_path = sys.argv[1]
predictions_csv_path = sys.argv[2]
output_path = sys.argv[3]

groundtruth_data = ReadCsvData(groundtruth_csv_path)
prediction_data = ReadCsvData(predictions_csv_path)

groundtruth_values = {}
err_values = {}
output_stats = {}

for field in DATA_FIELDNAMES[1:]:
  groundtruth_values[field] = []
  err_values[field] = []

for dish_id in prediction_data:
  for i in range(1, len(DATA_FIELDNAMES)):
    groundtruth_values[DATA_FIELDNAMES[i]].append(
        float(groundtruth_data[dish_id][i]))
    err_values[DATA_FIELDNAMES[i]].append(abs(
        float(prediction_data[dish_id][i])
        - float(groundtruth_data[dish_id][i])))

for field in DATA_FIELDNAMES[1:]:
  output_stats[field + "_MAE"] = statistics.mean(err_values[field])
  output_stats[field + "_MAE_%"] = (100 * statistics.mean(err_values[field]) /
                                    statistics.mean(groundtruth_values[field]))

with open(output_path, "w") as f_out:
  f_out.write(json.dumps(output_stats))
