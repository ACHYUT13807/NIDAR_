"""ACK, retry, and link-loss specification; no radio implementation."""


def send_reliably(message, policy):
    """Pseudocode:
    1. Assign a globally unique message ID and persist enough outbound state to
       correlate ACK/NACK/retry events.
    2. Transmit message and wait ACK_TIMEOUT.
    3. On accepted ACK: mark delivery-to-peer confirmed.
    4. On NACK: stop retrying that message; report reason to owner.
    5. On timeout: retry using bounded count and backoff/jitter policy.
    6. At retry exhaustion: mark link/message delivery failed and notify the
       owning mission component. Do not infer the remote physical outcome.

    TODO: select timeout/retry values from measured latency and packet loss.
    """


def evaluate_link_health(last_heartbeat_at, packet_metrics, now):
    """Define states HEALTHY, DEGRADED, LOST, RECOVERING.

    Suggested inputs: heartbeat age, ACK success ratio, RSSI/SNR if available,
    queue depth, and consecutive failures. State transitions need hysteresis so
    one lost packet does not cause mission churn.
    """


def on_link_loss(vehicle_role):
    """Policy to be decided and verified per vehicle.

    Scout: preserve observations locally; follow preapproved safety/return plan.
    Carrier: stop accepting route changes; execute only the explicitly approved
    loss-of-link policy. It must not silently release a payload on an ambiguous
    command state. GCS: flag all target/vehicle statuses as stale.
    """
