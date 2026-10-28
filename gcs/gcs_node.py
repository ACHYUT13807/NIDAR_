"""GCS orchestration specification. The GCS is the mission authority."""


def gcs_event_loop(inbound_messages, target_store, carrier_statuses, mission_policy):
    """Event-driven pseudocode:
    1. Validate and acknowledge inbound Scout/Carrier messages through the
       communication contract.
    2. Route detection reports through target creation/dedup/validation.
    3. Route Carrier telemetry and release evidence through lifecycle guards.
    4. Update vehicle/link status and mark stale information explicitly.
    5. When dispatch is permitted, propose a capacity/battery-aware route using
       the priority specification and issue versioned assignments.
    6. Persist an audit trail and publish a human-readable mission view.

    The loop must not generate actuator commands directly. It issues mission
    orders; the Carrier must validate and execute them under its safety policy.
    """


def review_operator_actions(action, current_mission_state):
    """Specify approval, authentication, logging, and allowed effects for pause,
    resume, target override, assignment cancel, manual-release prohibition,
    return, and emergency actions. Human intervention must be attributable in
    the history.
    """
