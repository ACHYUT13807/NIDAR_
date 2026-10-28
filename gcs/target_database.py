"""GCS target-record specification; persistence technology is intentionally open."""


def create_target_record(detection_report):
    """Specify creation of a TargetRecord in DETECTED state.

    Persist immutable source-report references, geographical estimate and
    uncertainty, first/last detection times, confidence policy result,
    lifecycle history, and a monotonic revision. The GCS is the only writer of
    authoritative target state.
    """


def find_duplicate_candidates(target_position, position_uncertainty_m, target_records):
    """Specification:

    1. Query spatially nearby non-archived targets.
    2. Compare geodesic distance with a threshold informed by both reports'
       uncertainties and the configured minimum-person separation.
    3. Return candidates and evidence, not merely a Boolean.

    TODO: select spatial index only after target-volume/radio requirements are
    known; a simple in-memory store is adequate for an early controlled test.
    """


def merge_or_create_target(detection_report, duplicate_candidates):
    """GCS dedup policy.

    Merge only when geography and optional appearance/time evidence supports the
    same-person hypothesis. On merge, preserve original `first_detected_at`,
    append provenance, update `last_seen_at`, and recompute confidence/
    uncertainty using the documented policy. On ambiguity, retain an auditable
    unresolved relation rather than silently collapsing two potential people.
    """


def record_lifecycle_event(target_id, event):
    """Append-only audit record: target revision, prior/new state, actor,
    timestamp, reason, and linked radio/evidence IDs. State is reconstructed or
    materialized from this history according to the chosen storage design.
    """
