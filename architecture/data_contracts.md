# NIDAR data and interface contracts

These are schemas and semantics, not implementations. Serialization may be
JSON, MAVLink extension messages, Protobuf, or another radio-safe format; pick
one before integration and keep these field meanings stable.

## Coordinate convention

- Geographic positions: WGS-84 latitude/longitude in degrees and altitude in metres, with altitude datum explicitly declared.
- Local perception geometry: use one declared local frame (ENU or NED); never mix frames silently.
- Time: UTC epoch milliseconds, monotonic time for local timeout measurement.

## Core data structures

```text
DetectionObservation
  observation_id, scout_id, timestamp_utc_ms
  bbox_xyxy_px, image_size_px, person_confidence
  camera_intrinsics_id, camera_to_body_transform_id
  vehicle_pose, range_or_ground_model, feature_pipeline_version

TargetRecord
  target_id, position_lat_lon_alt, position_uncertainty_m
  first_detected_at, last_seen_at, confidence, observation_count
  state, assigned_carrier_id, assigned_payload_bay
  failure_count, evidence_refs, revision

Assignment
  assignment_id, target_id, carrier_id, target_revision
  route_index, payload_bay, issued_at, expires_at, mission_revision

DeliveryResult
  assignment_id, target_id, carrier_id, timestamp_utc_ms
  outcome {released, not_released, unknown}, evidence_refs, detail
```

## Required message envelope

Every radio message must carry:

```text
message_id, message_type, sender_id, receiver_id,
created_at_utc_ms, sequence_number, protocol_version,
requires_ack, payload, checksum_or_integrity_tag
```

`ACK` references `message_id` and reports `accepted`, `rejected`, or
`duplicate`. An ACK only confirms receipt and validation of the message; it is
not proof that the requested physical action succeeded.

## Function/interface sketches

```python
def make_detection_report(observation: "DetectionObservation") -> "DetectionReport":
    """Define serialization-ready report fields; do not perform radio I/O here."""

def ingest_detection_report(report: "DetectionReport") -> "TargetRecord":
    """Specify GCS validation, deduplication, and state update contract."""

def issue_assignment(target: "TargetRecord", carrier: "CarrierStatus") -> "Assignment":
    """Create a versioned, time-bounded order after GCS policy approves it."""

def report_delivery_result(result: "DeliveryResult") -> None:
    """Carrier-to-GCS outcome report; GCS owns the resulting state transition."""
```

## Versioning rule

Assignments must identify both a target revision and a mission revision. The
Carrier rejects stale, expired, malformed, or incompatible assignments and
reports that rejection. This avoids acting on a route that the GCS has replaced.
