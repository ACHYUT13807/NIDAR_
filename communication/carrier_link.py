"""GCS-side interface to the Carrier radio link (Radio Link B).

Carrier's own onboard half of this link is implemented separately in
Carrier's own code using communication/protocol.py directly -- this file
is the GCS side only.
"""


def send_assignment(radio_handle, assignment):
    """Specify sending a versioned Assignment (architecture/data_contracts.md)
    via communication/reliability.py's send_reliably(). Must not be resent
    silently as a "retry" if the assignment itself changed -- a changed
    assignment is a new message with a new mission_revision, not a retry of
    the old one.
    """


def receive_carrier_messages(radio_handle):
    """Specify polling and decoding inbound Carrier telemetry/results.

    Pseudocode:
    1. Read and decode via communication/protocol.py, validate before
       trusting.
    2. Route Carrier status/telemetry to vehicle status tracking.
    3. Route DELIVERY_RESULT to mission/target_lifecycle.py's
       transition_target() -- outcome UNKNOWN must not silently become
       DELIVERED (architecture/data_contracts.md, DeliveryResult).
    4. ACK per idempotency rules; note that a DELIVERY_RESULT ACK confirms
       receipt only, never confirms the physical release succeeded.
    5. Return counts/summary for the GCS event loop's bookkeeping.
    """
