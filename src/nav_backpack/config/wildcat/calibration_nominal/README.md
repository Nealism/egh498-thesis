# Calibrating

This folder contains the nominal calibration files for nav backpacks for wildcat which is used to bootstrap the actual calibration values.

See https://confluence.csiro.au/display/WildcatSupport/Examples+-+Calibrating
for a general Wildcat calibration guide. This package also includes several scripts that can be used to automate the process.

## `wildcat_static_calibrate.py`
Performs a calibration of the lidar and encoder, this is only required once for each lidar/encoder and stays with the hardware. This is done by calibrating the scans against a known benchmark scan, this means **the static scan must be captured in the same location**. The current scans used for this is on the [wiki](https://confluence.csiro.au/display/SubT/Backpack+Calibration).

Usage:

  1. Capture a dataset consisting of a static scan of the designated location with a duration of 60 seconds.
  2. Download the benchmark of the location as per the wiki instructions.
  3. Create a directory containing:
    * input.bag
      * Static scan
    * bench_points.txt
      * Benchmark scan downloaded from the wiki
  4. In the directory run:
```
rosrun nav_backpack wildcat_static_calibrate.py -v VERSION
```
    * Where VERSION is the unit type (v1, v2, etc.)
  5. This will create the calibration file `static_calibration.yaml`

## `wildcat_dynamic_calibrate.py`
Performs a system calibration of the extrinsics of the system, updating it's transforms etc.. This is required every time the system is re-built. The general guide for this is on the [wiki](https://confluence.csiro.au/display/SubT/Backpack+Calibration).

Usage:

  1. Capture a dataset consisting of a scan of a large areas with large amounts of axis excitment as per the the wiki instructions with a duration of 60 seconds
  2. Create a directory containing:
    * input.bag
      * Dynamic scan
    * static_calibration.yaml
      * Static calibration results
  3. In the directory run:
```
rosrun nav_backpack wildcat_dynamic_calibrate.py -v VERSION
```
    * Where VERSION is the unit type (v1, v2, etc.)
  4. This will create the calibration file `dynamic_calibration.yaml`

## `wildcat_full_calibrate.py`
Runs the static and dynamic calibration according to the previous steps outputting both calibration files and the merged calibration overrides.

Usage:

  1. Capture the two datasets as per the previous instructions
  2. Create a directory containing:
    * static.bag
      * Static scan
    * dynamic.bag
      * Dynamic scan
    * bench_points.txt
      * Benchmark scan downloaded from the wiki
  3. In the directory run:
```
rosrun nav_backpack wildcat_full_calibrate.py -v VERSION
```
    * Where VERSION is the unit type (v1, v2, etc.)
  4. This will create the calibration file `static_calibration.yaml`, `dynamic_calibration.yaml`, and `calibration_overrides.yaml`

## `wildcat_create_calibration_overrides.py`
Merges the results of a calibration together from the nominal, static, and dynamic outputs into a single yaml file that can be used as overrides for wildcat called calibration_overrides.yaml.

Input:
 * static_calibration.yaml
   * Static calibration results.
 * dynamic_calibration.yaml
   * Dynamic calibration results.

Usage:

  1. Create a directory containing:
    * static_calibration.yaml
      * Static scan calibration result
    * dynamic_calibration.yaml
      * Dynamic scan calibration result
  3. In the directory run:
```
rosrun nav_backpack wildcat_create_calibration_overrides.py -v VERSION
```
    * Where VERSION is the unit type (v1, v2, etc.)
  4. This will create the file `calibration_overrides.yaml` which is the final merged overrides to apply to wildcat.
