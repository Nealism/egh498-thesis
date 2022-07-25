#!/usr/bin/env python

from __future__ import print_function
import collections
import packaging.version
import rospy

# Checks dependencies at runtime
# Dependencies are given as private parameters
# Each dependency should be specified with:
#   package_version_is: string containing version of package available
#   package_version_expect_lt: string containing the maximum (non-inclusive) version of package to expect
#   package_version_expect_le: string containing the maximum (inclusive) version of package to expect
#   package_version_expect_eq: string containing version of package to expect
#   package_version_expect_ge: string containing the minimum (inclusive) version of package to expect
#   package_version_expect_gt: string containing the minimum (non-inclusive) version of package to expect
# Where `package` should be replaced with whatever name you want

# TODO: Also check the exec_depends of all packages as roslaunch does not.

STATEMENTS = {
  "version_is": None,
  "version_expect_lt": {
    "check": lambda version_is, version_compare: version_is < version_compare,
    "translation": "less than",
  },
  "version_expect_le": {
    "check": lambda version_is, version_compare: version_is <= version_compare,
    "translation": "less than or equal to",
  },
  "version_expect_eq": {
    "check": lambda version_is, version_compare: version_is == version_compare,
    "translation": "equal to",
  },
  "version_expect_ge": {
    "check": lambda version_is, version_compare: version_is >= version_compare,
    "translation": "greater than or equal to",
  },
  "version_expect_gt": {
    "check": lambda version_is, version_compare: version_is > version_compare,
    "translation": "greater than",
  },
}

def main():
  rospy.init_node("check_depends")
  dependencies = collections.defaultdict(dict)
  for name, value in rospy.get_param("~").items():
    for statement in sorted(STATEMENTS.keys()):
      if name.endswith(statement):
        package = name[:-(len(statement) + 1)]
        dependencies[package][statement] = packaging.version.parse(value.strip())
  passed = True
  for package in sorted(dependencies.keys()):
    version_is = dependencies[package].pop("version_is")
    for statement, version_compare in dependencies[package].items():
      if version_is is None or not STATEMENTS[statement]["check"](version_is, version_compare):
        rospy.logerr("expected a version of \"{}\" {} \"{}\" but \"{}\" was found".format(
          package, STATEMENTS[statement]["translation"], version_compare, version_is))
        passed = False
  if not passed:
    rospy.logerr("Some dependency checks failed, if you encounter problems try resolving the dependencies first.")

if __name__ == "__main__":
  main()
