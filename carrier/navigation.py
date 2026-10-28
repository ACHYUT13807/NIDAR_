"""Carrier point-to-point navigation specification.

Transit between assigned stops is direct GPS waypoint travel above surveyed
obstacle height -- deliberately not corridor-following or lateral path
planning. That problem shape does not exist here (see
architecture/system_architecture.md); only the terminal approach needs
vision/depth refinement.
"""


def transit_to_assignment(assignment, vehicle_state):
    """Specify commanding direct GPS transit to an assignment's waypoint at
    the agreed cruise altitude.

    Preconditions: assignment is current and unexpired (see
    communication/protocol.py classify_delivery_semantics and
    architecture/data_contracts.md Assignment.expires_at) -- do not transit
    toward a stop the GCS has since cancelled or replaced.

    Pseudocode:
    1. Confirm cruise altitude clears surveyed obstacle height for this
       route segment, with margin.
    2. Command GPS waypoint transit under Pixhawk/approved controller.
    3. Monitor waypoint-reached telemetry; on arrival inside acceptance
       radius, hand off to carrier/terminal_approach.py.

    TODO: cruise altitude and acceptance radius both need values from a
    site survey, not assumed -- flagged already in
    architecture/open_design_questions.md item 5.
    """


def execute_return_to_home(reason):
    """Specify standard RTH: climb to a safe RTH altitude at or above
    cruise altitude, direct GPS transit to launch point, land.

    This must be callable at any point in the mission cycle regardless of
    "cannot return until mission complete" being the nominal plan --
    battery, geofence, and link-loss failsafes override the nominal plan by
    design (architecture/system_architecture.md, Safety invariants).
    Record `reason` for the mission audit trail.
    """
