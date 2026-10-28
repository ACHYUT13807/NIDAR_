"""Carrier terminal-approach specification; no flight-control implementation."""


def execute_terminal_approach(assignment, vehicle_state, perception_state, depth_state):
    """Pseudocode:
    1. Confirm an active, unexpired GCS assignment and acceptable battery/link/
       GPS/vehicle-health conditions.
    2. Enter terminal mode only after arriving inside the GPS acceptance region.
    3. Descend through predefined altitude gates. Use vision centering to reduce
       horizontal error relative to the agreed target/drop-zone definition.
    4. Use LiDAR/depth as the authoritative close-range height/clearance signal
       only within its validated operating envelope.
    5. Require stable centered error, valid depth, and low-enough lateral motion
       for a defined dwell interval before authorizing release.
    6. If confidence, range, obstacle clearance, link, or timeout checks fail,
       execute the selected abort: climb to safe altitude, mark outcome
       uncertain/failed, and request GCS direction according to link policy.

    TODO: define numeric gates, controller ownership (Pixhawk vs companion),
    detection target, obstruction policy, and all abort transitions.
    """
