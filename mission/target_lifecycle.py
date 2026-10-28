"""Authoritative target lifecycle specification, owned by the GCS."""


class TargetState:
    """DETECTED, VALIDATED, UNASSIGNED, ASSIGNED, EN_ROUTE, AT_TARGET,
    DELIVERED, VERIFIED, FAILED, REQUEUED.

    `REQUEUED` may be represented as an event returning a target to UNASSIGNED;
    choose one representation and keep database history either way.
    """


def transition_target(target, event, evidence):
    """Permitted transitions:

    DETECTED --validation evidence--> VALIDATED
    VALIDATED --dispatchable--> UNASSIGNED
    UNASSIGNED --assignment ACK--> ASSIGNED
    ASSIGNED --Carrier departs--> EN_ROUTE
    EN_ROUTE --arrival evidence--> AT_TARGET
    AT_TARGET --confirmed release--> DELIVERED
    DELIVERED --independent verification--> VERIFIED

    Failure paths:
    DETECTED/VALIDATED --rejection/expiry--> FAILED
    ASSIGNED/EN_ROUTE/AT_TARGET --recoverable failure--> REQUEUED -> UNASSIGNED
    ASSIGNED/EN_ROUTE/AT_TARGET --terminal failure--> FAILED

    Rules:
    - Every transition records actor, timestamp, message/evidence reference,
      reason, and prior target revision.
    - No direct transition to DELIVERED or VERIFIED.
    - Do not requeue after VERIFIED without a separately defined exceptional
      incident workflow.
    """


def is_dispatchable(state):
    """Specify this as true only for validated, unassigned, non-expired targets
    with sufficient localization confidence and no unresolved duplicate claim.
    """
