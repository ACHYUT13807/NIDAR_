"""Carrier mission-orchestration specification (intentionally non-executable)."""


class CarrierMissionState:
    """Suggested states: PREFLIGHT, WAITING_FOR_ASSIGNMENT, TRANSITING,
    TERMINAL_APPROACH, RELEASE_PENDING, REPORTING_RESULT, RETURNING, FAILSAFE.
    Specify a guarded transition table before coding.
    """


def carrier_mission_cycle(vehicle_status, assignment_queue, link_state):
    """Sequence:
    1. Publish vehicle, battery, navigation, depth, payload-inventory, and link
       health to GCS.
    2. Validate a versioned assignment; acknowledge receipt/rejection.
    3. Execute GPS waypoint transit under Pixhawk/approved controller authority.
    4. Run terminal approach specification, then payload-release specification.
    5. Report result with evidence; wait for GCS lifecycle update.
    6. Return/hold/failsafe according to battery, link, and manual-control rules.
    """
