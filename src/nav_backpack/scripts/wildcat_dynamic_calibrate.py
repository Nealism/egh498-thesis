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
Performs a dynamic calibration of the system, producing the file dynamic_calibration.yaml which supplies calibration overrides for the systems extrinsics.

Input:
 * input.bag
   * Input bag containing the dynamic scan, doing the calibration dance.
 * static_calibration.yaml
   * Static calibration results

This is dependant on static_calibration.yaml, from a previous call to wildcat_static_calibrate.

These calibrations are assembly specific and will need to be re-calibrated if the system itself is reconfigured (things unscrewed etc.).
"""

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("-v", "--version", help="Version name of the system to calibration, he config nav_backpack/config/wildcat/calibration_nominal/$(version).yaml must exist which supplies the nominal values.", required=True)
  args = parser.parse_args()

  # Get config and cal dir
  config_dir = os.path.join(rospkg.RosPack().get_path("nav_backpack"), "config", "wildcat")
  cal_dir = os.path.join(config_dir, "calibration_nominal")

  # Build command
  cmd = ["rosrun", "wildcat_ros", "pipeline"]
  cmd += ["-p", os.path.join(config_dir, "wildcat.yaml"), os.path.join(cal_dir, "{}.yaml".format(args.version)), "static_calibration.yaml"]
  cmd += ["-o", "nominalOverrides", "offlineOverrides", "dynamicCalibrationOverrides"]
  cmd += ["-n", "dynamicCalibration"]
  cmd += ["--anonymous"]

  # Calibrate!
  print("Running '{}'".format(" ".join(cmd)))
  subprocess.check_call(cmd)
  print("Calibration written to 'dynamic_calibration.yaml'")
