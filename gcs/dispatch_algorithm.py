"""
GCS Dispatch Algorithm -- NIDAR RescueSwarm
============================================

Mission constraint: Carrier launches ONCE with capacity for MAX_PAYLOAD
packs and cannot return mid-mission (per problem statement). All routing
decisions must account for this -- there is no "return to reload" cycle.

Target lifecycle (8 states, per architecture diagram):
    DETECTED -> VALIDATED -> UNASSIGNED -> ASSIGNED -> EN_ROUTE
    -> AT_TARGET -> DELIVERED -> VERIFIED

This module owns: de-duplication of incoming detections, priority
scoring, and dynamic route construction for the carrier's single
continuous sortie.

HARDWARE NOTE: current release mechanism design shows 5 servo actuators /
5 bays, but mission capacity needs to be 10 packs. Confirm hardware
before this dispatch logic assumes MAX_PAYLOAD = 10.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


MAX_PAYLOAD = 10          # per problem statement -- confirm against actual release rack capacity
DEDUP_RADIUS_M = None      # tune against realistic spacing between people in the field
ALPHA_URGENCY = None       # weight for wait-time term
BETA_CONFIDENCE = None     # weight for detection confidence
GAMMA_DISTANCE = None      # weight for distance penalty


class TargetState(Enum):
    DETECTED = "detected"
    VALIDATED = "validated"
    UNASSIGNED = "unassigned"
    ASSIGNED = "assigned"
    EN_ROUTE = "en_route"
    AT_TARGET = "at_target"
    DELIVERED = "delivered"
    VERIFIED = "verified"


@dataclass
class Target:
    id: str
    lat: float
    lon: float
    alt: float
    confidence: float
    state: TargetState
    first_detected_at: float   # basis for the urgency/aging term
    last_seen_at: float
    assigned_to: Optional[str] = None


# ---------------------------------------------------------------------
# 1. DE-DUPLICATION
# ---------------------------------------------------------------------

def ingest_detection(new_lat, new_lon, confidence, timestamp, target_db):
    """
    ALGORITHM:
    1. Compute great-circle (haversine) distance from (new_lat, new_lon)
       to every target currently in target_db, regardless of state
       (including DELIVERED / VERIFIED -- a re-detection of an already
       served target must be suppressed, not re-queued).
    2. If nearest existing target is within DEDUP_RADIUS_M:
         - If that target's state is DELIVERED or VERIFIED: discard the
           new detection entirely (already served, do nothing).
         - Otherwise: treat as the same person. Update confidence
           (e.g. running max, or exponential moving average -- pick one
           and justify it) and last_seen_at. Do NOT reset
           first_detected_at (that timestamp drives the aging term and
           must reflect when this person was first found, not last
           re-seen).
    3. If no existing target within DEDUP_RADIUS_M: create a new Target
       in DETECTED state, first_detected_at = last_seen_at = timestamp.
    4. Detections above a minimum confidence threshold transition
       DETECTED -> VALIDATED (decide the threshold; low-confidence
       detections can sit in DETECTED without entering the dispatch
       pool until confirmed on a later pass).
    """
    raise NotImplementedError


def haversine_distance_m(lat1, lon1, lat2, lon2):
    """Standard great-circle distance. Implement directly -- no algorithm
    ambiguity here, just the formula."""
    raise NotImplementedError


# ---------------------------------------------------------------------
# 2. PRIORITY SCORING
# ---------------------------------------------------------------------

def priority_score(target, carrier_lat, carrier_lon, now):
    """
    score = ALPHA_URGENCY * urgency(target, now)
          + BETA_CONFIDENCE * target.confidence
          - GAMMA_DISTANCE * distance_from_carrier(target, carrier_lat, carrier_lon)

    ALGORITHM for urgency (wait-time / aging term -- this is what
    prevents starvation of an early-detected, far-away target as scout
    keeps finding closer ones):
    1. elapsed = now - target.first_detected_at
    2. urgency should be monotonically increasing in elapsed, and
       should be normalized/scaled so it's comparable in magnitude to
       the confidence and distance terms (pick a normalization --
       e.g. elapsed / some_reference_mission_duration, or a saturating
       function like 1 - exp(-elapsed / tau)).
    3. Tune ALPHA/BETA/GAMMA so that no single term dominates by
       construction -- validate empirically against a few hand-built
       scenarios (one far+old target, several near+new targets) before
       trusting it on real data.

    Higher score = more urgent to dispatch next.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------
# 3. ROUTE CONSTRUCTION (single continuous sortie, MAX_PAYLOAD capacity)
# ---------------------------------------------------------------------

def build_initial_route(unassigned_targets, launch_lat, launch_lon, now):
    """
    Runs once, when carrier is about to launch.

    ALGORITHM (greedy nearest-neighbor seed, capacity-limited):
    1. current_position = (launch_lat, launch_lon)
    2. route = []
    3. While len(route) < MAX_PAYLOAD and unassigned_targets is non-empty:
         a. Score every remaining unassigned target using priority_score()
            evaluated from current_position.
         b. Pick the highest-scoring target, append to route, remove
            from unassigned_targets, set state -> ASSIGNED.
         c. current_position = that target's location (simulate the
            route walk for the *next* distance term -- this makes it a
            greedy route-builder, not just a static top-10 sort).
    4. Return route (ordered list of Target).

    NOTE: this is greedy nearest/highest-priority-neighbor, not an
    optimal TSP solve. For 10 stops an exact or near-exact solve
    (e.g. held-karp for small N, or 2-opt improvement on the greedy
    route) is computationally cheap and worth doing as a refinement --
    flag as an upgrade path, not required for first version.
    """
    raise NotImplementedError


def insert_new_target_into_route(route, new_target, current_carrier_position, now):
    """
    Called when scout validates a new target WHILE carrier is already
    mid-mission with a route in progress.

    ALGORITHM (cheapest insertion, capacity-aware):
    1. If len(route) >= MAX_PAYLOAD: do not modify the route. (Optional
       upgrade: compare new_target's priority_score against the LOWEST
       remaining-priority stop still ahead in the route -- if new_target
       clearly dominates, swap it in. Only add this once the basic
       version works and is tested -- swapping mid-flight has real
       failure modes, e.g. carrier already past the point where the
       swap would help.)
    2. Otherwise, for each possible insertion position i in the
       remaining (not-yet-visited) part of the route, compute the extra
       distance added by inserting new_target between stop[i-1] and
       stop[i]:
           extra = dist(stop[i-1], new_target) + dist(new_target, stop[i])
                   - dist(stop[i-1], stop[i])
       Pick the position with minimum extra distance.
    3. Insert new_target at that position, set state -> ASSIGNED.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------
# 4. STATE TRANSITIONS DRIVEN BY CARRIER TELEMETRY / ACKS
# ---------------------------------------------------------------------

def on_carrier_departs_for(target):
    """ASSIGNED -> EN_ROUTE. Triggered when GCS sends the waypoint
    command and carrier acknowledges."""
    raise NotImplementedError


def on_carrier_arrives_at(target):
    """EN_ROUTE -> AT_TARGET. Triggered by carrier's own
    waypoint-reached telemetry."""
    raise NotImplementedError


def on_delivery_confirmed(target, verified):
    """
    AT_TARGET -> DELIVERED -> VERIFIED (or stay at DELIVERED if
    verification is a separate later step / not yet confirmed).

    ALGORITHM:
    1. Mark DELIVERED as soon as the release-mechanism ack arrives.
    2. Mark VERIFIED only once independent confirmation exists (e.g.
       carrier's own camera confirms the payload left the bay AND the
       drop landed near the intended point -- define exactly what
       "verified" means for this mission before implementing).
    3. This target must now be excluded from all future de-dup
       insertions and route modifications -- ingest_detection() already
       handles this by checking DELIVERED/VERIFIED state.
    """
    raise NotImplementedError


def on_delivery_timeout(target):
    """
    Safety case: ack never arrives (radio dropout, servo fault).

    ALGORITHM:
    1. If AT_TARGET or EN_ROUTE for longer than some timeout threshold
       without a state-advancing ack, revert target to UNASSIGNED (not
       DELIVERED) and log the failure.
    2. Do NOT silently leave it stuck at AT_TARGET/EN_ROUTE forever --
       that's a target that looks "handled" in the DB but was never
       actually served.
    3. Consider whether carrier should retry this stop or skip and
       continue the route -- depends on why the timeout happened
       (define retry policy).
    """
    raise NotImplementedError
