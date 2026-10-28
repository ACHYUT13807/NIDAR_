"""NIDAR radio protocol specification and reference implementation.

Transport is deliberately unspecified: it may be a telemetry radio, a MAVLink
channel, or an independent data link. The semantics below must remain the same
regardless of transport.
"""

from __future__ import annotations

import hashlib
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional

SUPPORTED_VERSIONS = (1,)
VALID_RECEIVERS = ("scout", "carrier", "gcs", "broadcast")
PROTOCOL_VERSION = 1


class MessageType:
    """Required types: HEARTBEAT, DETECTION_REPORT, TARGET_UPDATE,
    ASSIGNMENT, ASSIGNMENT_CANCEL, CARRIER_STATUS, DELIVERY_RESULT, ACK,
    NACK, LINK_STATUS, and EMERGENCY_NOTICE.
    """
    HEARTBEAT = 1
    DETECTION_REPORT = 2
    TARGET_UPDATE = 3
    ASSIGNMENT = 4
    ASSIGNMENT_CANCEL = 5
    CARRIER_STATUS = 6
    DELIVERY_RESULT = 7
    ACK = 8
    NACK = 9
    LINK_STATUS = 10
    EMERGENCY_NOTICE = 11

    _NAMES = {
        1: "HEARTBEAT", 2: "DETECTION_REPORT", 3: "TARGET_UPDATE",
        4: "ASSIGNMENT", 5: "ASSIGNMENT_CANCEL", 6: "CARRIER_STATUS",
        7: "DELIVERY_RESULT", 8: "ACK", 9: "NACK", 10: "LINK_STATUS",
        11: "EMERGENCY_NOTICE",
    }

    @classmethod
    def name_of(cls, message_type):
        return cls._NAMES.get(message_type, "UNKNOWN")

    @classmethod
    def is_valid(cls, message_type):
        return message_type in cls._NAMES


# Mirrors mission/target_lifecycle.py -- kept here only for message-level
# sanity checking, not as the authoritative state machine (GCS owns that).
_VALID_TARGET_TRANSITIONS = {
    "DETECTED": {"VALIDATED", "FAILED"},
    "VALIDATED": {"UNASSIGNED", "FAILED"},
    "UNASSIGNED": {"ASSIGNED", "FAILED"},
    "ASSIGNED": {"EN_ROUTE", "UNASSIGNED", "FAILED"},
    "EN_ROUTE": {"AT_TARGET", "REQUEUED", "FAILED"},
    "AT_TARGET": {"DELIVERED", "REQUEUED", "FAILED"},
    "DELIVERED": {"VERIFIED", "FAILED"},
    "REQUEUED": {"UNASSIGNED", "ASSIGNED"},
    "VERIFIED": set(),
    "FAILED": {"REQUEUED"},
}


@dataclass
class Message:
    """Wire-level envelope for every NIDAR protocol message.

    message_id: globally unique ID (UUID4), used for dedup/ACK correlation.
    message_type: one of MessageType.*
    sender / receiver: logical roles ("scout", "carrier", "gcs").
    version: protocol version this message was built with.
    timestamp: unix time (seconds, float) at creation.
    expiration: unix time after which the message must be rejected.
    payload: message-type-specific dict.
    checksum: SHA-256 hex digest, set via seal().
    state_transition: optional (from_state, to_state) tuple for
        TARGET_UPDATE / DELIVERY_RESULT messages.
    """
    message_type: int
    sender: str
    receiver: str
    payload: dict
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    version: int = PROTOCOL_VERSION
    timestamp: float = field(default_factory=time.time)
    expiration: Optional[float] = None
    checksum: Optional[str] = None
    state_transition: Optional[tuple] = None

    def _canonical_bytes(self):
        parts = [
            self.message_id, str(self.message_type), self.sender,
            self.receiver, str(self.version), f"{self.timestamp:.6f}",
            repr(sorted(self.payload.items())),
        ]
        return "|".join(parts).encode("utf-8")

    def seal(self):
        """Compute and attach the integrity checksum. Call after all other
        fields are finalized and before transmission."""
        self.checksum = hashlib.sha256(self._canonical_bytes()).hexdigest()
        return self


def is_valid_checksum(message):
    if message.checksum is None:
        return False
    return hashlib.sha256(message._canonical_bytes()).hexdigest() == message.checksum


def is_valid_state_transition(message):
    """Only meaningful for messages carrying a state_transition tuple.
    Messages without one pass trivially -- transition legality is not
    their concern.
    """
    if message.state_transition is None:
        return True
    from_state, to_state = message.state_transition
    allowed = _VALID_TARGET_TRANSITIONS.get(from_state)
    if allowed is None:
        return False
    return to_state in allowed


def current_time():
    return time.time()


def validate_message(message):
    """Specification:

    Reject messages with an unknown protocol version, malformed fields, invalid
    checksum/integrity tag, expired assignment, wrong receiver, or impossible
    state transition. Return an explicit reason suitable for a NACK/log.
    """
    if not MessageType.is_valid(message.message_type):
        return f"Unknown message type: {message.message_type}"
    if message.version not in SUPPORTED_VERSIONS:
        return "Unsupported protocol version"
    if not message.message_id or not message.sender or not message.receiver:
        return "Malformed fields: message_id, sender, and receiver are required"
    if not is_valid_checksum(message):
        return "Invalid checksum"
    if message.expiration is not None and message.expiration < current_time():
        return "Message expired"
    if message.receiver not in VALID_RECEIVERS:
        return "Invalid receiver"
    if not is_valid_state_transition(message):
        return "Invalid state transition"
    return None


def classify_delivery_semantics(message_type):
    """Define idempotency before implementation.

    - Detection and telemetry may be repeated; receivers deduplicate by ID.
    - Assignment messages are idempotent only for the same assignment/version.
    - Release commands must never be retried blindly after an ACK timeout.
      Query state/evidence first; physical action requires a separate agreed
      idempotency and actuator-safety design.
    """
    if message_type in (MessageType.DETECTION_REPORT, MessageType.TARGET_UPDATE):
        return "Idempotent: deduplicate by ID"
    if message_type == MessageType.ASSIGNMENT:
        return "Idempotent: same assignment/version"
    if message_type == MessageType.ASSIGNMENT_CANCEL:
        return "Idempotent: same assignment/version"
    if message_type == MessageType.CARRIER_STATUS:
        return "Idempotent: same carrier/version"
    if message_type == MessageType.DELIVERY_RESULT:
        return ("NOT freely retryable: physical release outcome. Query "
                "carrier state/evidence before resending; never infer "
                "success from a repeated ACK timeout.")
    if message_type == MessageType.ACK:
        return "Idempotent: same ACK/version"
    if message_type == MessageType.NACK:
        return "Idempotent: same NACK/version"
    if message_type == MessageType.LINK_STATUS:
        return "Idempotent: same link/version"
    if message_type == MessageType.EMERGENCY_NOTICE:
        return "Non-idempotent: always act, never suppressed as duplicate"
    return "Non-idempotent"


def build_message(message_type, sender, receiver, payload, ttl_seconds=5.0,
                   state_transition=None):
    """Convenience constructor: stamps timestamp/expiration and seals the
    checksum in one call. Time-critical types (ASSIGNMENT, ASSIGNMENT_CANCEL,
    EMERGENCY_NOTICE) should pass an explicit, shorter ttl_seconds.
    """
    now = current_time()
    message = Message(
        message_type=message_type, sender=sender, receiver=receiver,
        payload=payload, timestamp=now, expiration=now + ttl_seconds,
        state_transition=state_transition,
    )
    return message.seal()
