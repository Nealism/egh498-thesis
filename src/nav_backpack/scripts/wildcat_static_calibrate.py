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
Performs a static calibration of the system, producing the file static_calibration.yaml which supplies calibration overrides for the laser & encoder components.

Input:
 * input.bag
   * Input data containing the static scan, positioned in the bench points origin.
 * bench_points.txt
   * Benchmark to calibrate against.


These calibrations are hardware specific and should not need to be re-calibrated if the system itself is reconfigured.
"""

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("-v", "--version", help="Version name of the system to calibration, the config nav_backpack/config/wildcat/calibration_nominal/$(version).yaml must exist which supplies the nominal values.", required=True)
  args = parser.parse_args()

  # Get config and cal dir
  config_dir = os.path.join(rospkg.RosPack().get_path("nav_backpack"), "config", "wildcat")
  cal_dir = os.path.join(config_dir, "calibration_nominal")

  # Build command
  cmd = ["rosrun", "wildcat_ros", "pipeline"]
  cmd += ["-p", os.path.join(config_dir, "wildcat.yaml"), os.path.join(cal_dir, "{}.yaml".format(args.version))]
  cmd += ["-o", "nominalOverrides", "offlineOverrides", "staticCalibrationOverrides"]
  cmd += ["-n", "staticCalibration"]
  cmd += ["--anonymous"]

  # Calibrate!
  print("Running '{}'".format(" ".join(cmd)))
  subprocess.check_call(cmd)
  print("Calibration written to 'static_calibration.yaml'")
