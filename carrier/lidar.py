"""Carrier LiDAR/depth specification.

Scope, per architecture/system_architecture.md and pending resolution of
open_design_questions.md item 5: terminal vertical ranging during descent,
not lateral obstacle mapping. Lateral obstacles are handled structurally by
cruising above surveyed obstacle height, not sensed. Confirm this scope
decision before implementing -- if lateral avoidance is actually required,
this module's responsibility grows substantially.
"""


def read_range(lidar_handle):
    """Specify a single range measurement read with basic validity handling.

    Pseudocode:
    1. Read raw range from the sensor.
    2. Reject/flag readings outside the sensor's validated operating
       envelope (both too-close and too-far bounds -- LiDAR rangefinders
       commonly misbehave at both extremes, not just max range).
    3. Smooth/filter if the raw signal is noisy at your sensor's sample
       rate (e.g. short rolling median) -- terminal_approach.py must not
       make a release-altitude decision off a single unfiltered sample.
    4. Return (range_m, valid) rather than a bare number -- callers must be
       able to distinguish "no reliable reading" from "reading is zero."
    """


def is_within_operating_envelope(range_m, sensor_spec):
    """Specify the min/max range and any angular/surface-reflectivity
    caveats from the specific LiDAR module's datasheet. Do not assume a
    generic envelope -- confirm against the actual part.
    """
