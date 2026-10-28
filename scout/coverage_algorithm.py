"""Scout coverage specification.

No navigation implementation belongs in this file. It describes generation of
a fixed preflight coverage mission over a search polygon.
"""


def plan_boustrophedon_sweep(search_polygon, flight_altitude_m, camera_hfov_deg, overlap_fraction):
    """Specify an ordered coverage-waypoint sequence.

    Pseudocode:
    1. Validate polygon, altitude, field of view, and overlap domain.
    2. Estimate ground swath width:
         swath_width = 2 * altitude * tan(HFOV / 2)
         line_spacing = swath_width * (1 - overlap_fraction)
    3. Select sweep orientation, normally near the longest useful polygon axis,
       while considering wind, no-fly boundaries, and takeoff location.
    4. Generate parallel lines at `line_spacing`; clip every line to polygon.
    5. Order valid segments in alternating directions (boustrophedon) and add
       safe turn/entry/exit waypoints.
    6. Estimate length, duration, and energy. Reject the plan if reserve energy
       or geofence constraints are violated.
    7. Produce a reviewable mission artifact before upload.

    TODO: choose geometry library and a clear local-map projection. Geographic
    degree arithmetic is not adequate for metre-level line spacing.
    """


def should_replan_coverage(vehicle_status, mission_status, environment_status):
    """Define only the replan decision policy.

    Candidate triggers: surveyed area invalidated, geofence change, safety
    event, weather/wind constraint, or manual GCS instruction. A person
    detection alone should not perturb coverage unless the GCS policy says so.
    """
