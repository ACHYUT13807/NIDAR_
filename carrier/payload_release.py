"""Ten-pack payload-release specification; interfaces only."""


def authorize_release(assignment, terminal_evidence, payload_inventory):
    """Required preconditions:
    - assignment is current and names an unused physical bay;
    - terminal approach reports stable release conditions;
    - GCS/Carrier mission state is not in an emergency override;
    - inventory and bay identity agree.

    A release command is not itself delivery confirmation.
    """


def determine_release_outcome(bay_telemetry, payload_sensor, camera_evidence):
    """Classify only as RELEASED, NOT_RELEASED, or UNKNOWN.

    Prefer independent evidence such as a bay light-break/limit sensor plus
    camera evidence. Servo position or elapsed time alone should be recorded as
    weak evidence, not asserted as successful delivery.
    """


def update_payload_inventory(outcome, bay_index):
    """Specify atomic inventory bookkeeping. A bay becomes unavailable only when
    the physical outcome is sufficiently confirmed. UNKNOWN requires a defined
    operator/GCS policy because assuming either empty or full can be unsafe.
    """
