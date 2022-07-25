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

description = """
Performs a full calibration of the system, producing the file static_calibration.yaml, dynamic_calibration.yaml, calibration_overrides.yaml as per the associated scripts.

Input:
 * static.bag
   * Input data containing the static scan, positioned in the bench points origin.
 * bench_points.txt
   * Benchmark to calibrate against.
 * dynamic.bag
   * Input bag containing the dynamic scan, doing the calibration dance.
"""

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("-v", "--version", help="Version name of the system to calibration, the config nav_backpack/config/wildcat_$(version)_nominal.yaml must exist which supplies the nominal values.", required=True)
  args = parser.parse_args()

  # First do static
  # Link to the bag
  subprocess.check_call(["ln", "-sf", "static.bag", "input.bag"])
  # Run it
  cmd = ["rosrun", "nav_backpack", "wildcat_static_calibrate.py", "-v", args.version]
  print("Running '{}'".format(" ".join(cmd)))
  subprocess.check_call(cmd)

  # Then dynamic
  # Link to the bag
  subprocess.check_call(["ln", "-sf", "dynamic.bag", "input.bag"])
  # Run it
  cmd = ["rosrun", "nav_backpack", "wildcat_dynamic_calibrate.py", "-v", args.version]
  print("Running '{}'".format(" ".join(cmd)))
  subprocess.check_call(cmd)

  # Remove links
  subprocess.check_call(["rm", "input.bag"])

  # Merge down
  cmd = ["rosrun", "nav_backpack", "wildcat_create_calibration_overrides.py", "-v", args.version]
  print("Running '{}'".format(" ".join(cmd)))
  subprocess.check_call(cmd)

  # Done!
  print("Calibration written to 'static_calibration.yaml', 'dynamic_calibration.yaml', and 'calibration_overrides.yaml'")
