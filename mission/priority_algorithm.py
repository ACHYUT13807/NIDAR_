"""GCS priority/routing specification; implementation intentionally omitted."""


def score_target(target, carrier_position, now):
    """Define a normalized priority model.

    Suggested form:
      score = a * aging(wait_time)
            + b * confidence_term
            + c * mission_severity_term
            - d * route_cost_term

    where `wait_time = now - target.first_detected_at`, never time since the
    most recent duplicate observation. A bounded aging term is one option:
      aging(t) = 1 - exp(-t / tau)

    All terms must be scaled from real data so one unit change does not dominate
    merely due to different numerical units. Mission severity is optional and
    must have a defensible input source; do not infer medical severity from a
    person detector alone.
    """


def propose_capacity_limited_route(dispatchable_targets, carrier_status):
    """Pseudocode:
    1. Filter to targets eligible for this carrier and remaining payload bays.
    2. Rank by priority and construct an initial route using route-aware cost.
    3. Enforce ten-pack capacity, battery reserve, geofence, and deadline rules.
    4. Optionally improve route with a bounded local-search pass.
    5. Present assignment proposal to the GCS authority and issue versioned
       assignments only after policy acceptance.

    TODO: define whether a late high-priority target can displace an already
    assigned but uncommitted stop.
    """
