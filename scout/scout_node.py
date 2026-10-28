"""Scout orchestration interface (intentionally non-executable)."""


class ScoutMissionState:
    """Suggested states: PREFLIGHT, COVERAGE_TRANSIT, SEARCHING, REPORTING,
    LINK_DEGRADED, RETURNING, FAILSAFE. Define permitted transitions before
    connecting to Pixhawk or the radio layer.
    """


def scout_cycle(frame, vehicle_pose, coverage_state, link_state):
    """High-level sequence only.

    1. Acquire synchronized frame and vehicle state.
    2. Run the agreed perception specification.
    3. Geotag eligible observations and create versioned reports.
    4. Queue reports through the reliable communication layer.
    5. Continue fixed coverage unless safety/GCS policy changes it.
    6. Publish Scout health: battery, GPS quality, sensor health, coverage
       progress, radio state, perception FPS, and report queue depth.
    """
