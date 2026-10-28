# NIDAR system architecture

NIDAR is a heterogeneous two-drone rescue system. The Scout searches and
creates reliable target reports. The GCS is the only mission authority. The
Carrier receives GCS-authorized assignments and delivers its ten payload packs
in one continuous sortie.

```text
IMX477 + Jetson + Pixhawk + LiDAR                 Pixhawk + GPS + LiDAR/depth
             SCOUT                                      CARRIER
  coverage -> perception -> geotag -> report       transit -> terminal -> release
             |                                           ^
             +-------- reliable radio link -----------+ |
                                |                       |
                                v                       |
                         GCS / mission authority -------+
                  target DB, dedup, priority, dispatch
```

## Responsibility boundaries

| Component | Owns | Must not decide |
|---|---|---|
| Scout | Search coverage, detection evidence, local geotag estimate, report retransmission | Final target validity, target priority, Carrier route |
| GCS | Target database, validation policy, deduplication, aging-based priority, assignment, global lifecycle | Low-level flight stabilization, servo waveform |
| Carrier | Execution of an acknowledged assignment, local terminal safety, release outcome telemetry | Creating targets, changing priority, silently declaring a delivery complete |
| Communication layer | Message identity, ACK/retry, sequencing, link state, retransmission | Mission policy or payload decisions |

## Nominal information flow

1. The Scout follows a preplanned boustrophedon coverage path.
2. Per-frame perception produces person observations with confidence and image location.
3. The Scout converts an observation to a georeferenced target estimate and sends a `DETECTION_REPORT`.
4. The GCS acknowledges the report, deduplicates it, validates it, and stores the target.
5. The GCS ranks dispatchable targets using wait-time aging, confidence, and route cost.
6. The GCS sends an assignment or route update to the Carrier; Carrier execution starts only after a valid assignment is acknowledged.
7. The Carrier transits by GPS above surveyed obstacles, then uses vision centering and LiDAR/depth during terminal approach.
8. Carrier reports every state transition and release result. GCS updates the authoritative target record.

## Safety invariants

- GCS is authoritative: a local observation is not a delivery order.
- No `DELIVERED` transition without a release-result message; no `VERIFIED` transition without the agreed independent evidence.
- Loss of communications is observable state, never interpreted as success.
- A target with uncertain delivery outcome is requeued or explicitly marked failed according to the retry policy.
- Battery, geofence, vehicle failsafe, and manual pilot intervention override the nominal delivery plan.

## Hardware assumptions to verify

- Scout: IMX477, Jetson Orin Nano, Pixhawk, LiDAR, approximately 12,000 mAh battery.
- Carrier: Pixhawk 2.4.8, GPS, LiDAR/depth, 22,000 mAh 22.2 V 30C battery, and capacity for ten payload packs.
- Verify that the physical release rack, actuator count, and confirmation sensors truly support ten individually addressable packs.
