# Open design questions and acceptance criteria

## Questions that must be settled before implementation

1. **Perception fusion:** Is Gabor + Sobel/Sable preprocessing an input enhancement, auxiliary detector channel, late fusion signal, or only a comparison baseline? The training and inference paths must match exactly.
2. **Sable terminology:** Confirm whether `Sable` is an existing named algorithm/module or a mistaken spelling of Sobel. Do not encode both as distinct requirements until verified.
3. **Target validation:** Is one high-confidence observation sufficient, or are multiple temporal observations / Scout viewpoints required?
4. **Dedup radius:** How does it vary with geotag uncertainty, altitude, GPS quality, and the realistic minimum spacing between different people?
5. **Carrier obstacle model:** Is LiDAR/depth only for terminal vertical ranging, or also approved for lateral obstacle avoidance? Define sensor field of view and safe fallback.
6. **Terminal perception:** What visual marker/object is center-finding—the person, the payload landing zone, or a defined drop zone near the person?
7. **Delivery verification:** What evidence promotes `DELIVERED` to `VERIFIED`? Servo command alone is insufficient.
8. **Route updates:** May GCS insert/remove assignments while the Carrier is en route? Define the commit point after which the current stop cannot be changed.
9. **Retry policy:** For a failed/unknown release, how many attempts are permitted, and when is a target requeued versus abandoned?
10. **Failsafes:** Specify link-loss behaviour for Scout, Carrier, and GCS separately, along with geofence, low battery, manual override, and GPS degradation rules.

## Minimum acceptance tests (specification only)

- Synthetic duplicate reports within/outside the dedup radius produce exactly one/new target as intended.
- A continuously detected target ages without resetting `first_detected_at`.
- Stale and duplicate assignments are rejected without changing Carrier execution state.
- ACK loss causes bounded retry and a visible link-loss status, not duplicate physical actions.
- Release result `unknown` never becomes `DELIVERED`.
- Carrier terminal-centering timeout exits to a documented safe action.
- One end-to-end dry run records each target state transition with message IDs and timestamps.
