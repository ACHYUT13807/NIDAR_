"""GCS-side interface to the Scout radio link (Radio Link A).

Scout's own onboard half of this link is implemented separately in
Scout's own code using communication/protocol.py directly -- this file is
the GCS side only.
"""


def receive_scout_messages(radio_handle):
    """Specify polling and decoding inbound messages on this link.

    Pseudocode:
    1. Read available bytes from the radio.
    2. Decode via communication/protocol.py; run validate_message() before
       trusting content -- a garbled or malformed packet must not reach
       mission logic.
    3. Route by MessageType: DETECTION_REPORT to gcs/target_database.py's
       merge_or_create_target() pipeline, Scout health/status to vehicle
       status tracking, HEARTBEAT to communication/reliability.py's
       evaluate_link_health().
    4. ACK every validated message per classify_delivery_semantics()'s
       idempotency rules for its type.
    5. Return counts/summary for this call, for the GCS event loop's
       bookkeeping.
    """


def send_scout_command(radio_handle, message):
    """Specify outbound sends to Scout over this link (e.g. abort, replan
    trigger) via communication/reliability.py's send_reliably() -- Scout's
    coverage is normally autonomous and pre-planned, so this path should be
    the exception, not routine traffic.
    """
