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
Performs a self-strike calibration of a chassis, producing the file self_strike_wildcat.yaml which contains the self-strike locations which can be used as overrides to supply to the system.

Input:
 * input.bag
   * Input bag containing a static scan in a flat area, away from objects as much as possible.

These calibrations are assembly specific and will need to be re-calibrated if the chassis is changed (things mounted etc.) or the system is changed substantially
"""

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("-v", "--version", help="Version name of the chassis to calibrate, the config nav_backpack/config/wildcat/chassis_nominal/$(version).yaml must exist which supplies the nominal values.", required=True)
  parser.add_argument("-p", "--parameters", nargs='+', help="The parameter files to use (IN ADDITION to config nav_backpack/config/wildcat.yaml), usually calibrations etc.", required=True)
  parser.add_argument("--sim", action="store_true", default=False, help="If sim data is going to be calibrated")
  args = parser.parse_args()

  # Get config and cal dir
  config_dir = os.path.join(rospkg.RosPack().get_path("nav_backpack"), "config", "wildcat")
  cal_dir = os.path.join(config_dir, "chassis_nominal")
  nominal_chassis_config_file = os.path.join(cal_dir, "{}.yaml".format(args.version))

  # Build command
  cmd = ["rosrun", "wildcat_ros", "pipeline"]
  cmd += ["-p", os.path.join(config_dir, "wildcat.yaml")] + args.parameters + [nominal_chassis_config_file]
  cmd += ["-o", "nominalOverrides", "offlineOverrides"]
  if args.sim:
    cmd += ["-n", "generateSelfStrikeSphericalImageSim"]
  else:
    cmd += ["-n", "generateSelfStrikeSphericalImage"]
  cmd += ["--anonymous"]

  # Calibrate!
  print("Running '{}'".format(" ".join(cmd)))
  subprocess.check_call(cmd)
  print("Calibration written to 'self_strike_wildcat.yaml', and a (non-essential) output image 'self_strike_wildcat.pgm'")
