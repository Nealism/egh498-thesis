#!/usr/bin/env python

from __future__ import print_function

import argparse
import datetime
import glob
import os
import rospkg
import shutil
import subprocess
import sys
import yaml

description = """
Merges the results of a calibration together from the nominal, static, and dynamic outputs into a single yaml file that can be used as overrides for wildcat called calibration_overrides.yaml.

Input:
 * static_calibration.yaml
   * Static calibration results.
 * dynamic_calibration.yaml
   * Dynamic calibration results.
"""

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("-v", "--version", help="Version name of the system, the config nav_backpack/config/wildcat_$(version)_nominal.yaml must exist which supplies the nominal values.", required=True)
  args = parser.parse_args()

  # Get configs
  with open(os.path.join(rospkg.RosPack().get_path("nav_backpack"), "config", "wildcat", "calibration_nominal", "{}.yaml".format(args.version)), 'r') as stream:
    nominal_calibration = yaml.safe_load(stream)
  with open("static_calibration.yaml", 'r') as stream:
    static_calibration = yaml.safe_load(stream)
  with open("dynamic_calibration.yaml", 'r') as stream:
    dynamic_calibration = yaml.safe_load(stream)

  # Merge down
  output = {}
  for key in nominal_calibration:
    output[key] = nominal_calibration[key]
  for key in static_calibration:
    output[key] = static_calibration[key]
  for key in dynamic_calibration:
    output[key] = dynamic_calibration[key]

  # Output
  with open("calibration_overrides.yaml", "w") as stream:
    yaml.dump(output, stream, default_flow_style=False)
