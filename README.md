# NIDAR RescueSwarm — Team Pushpak

Two-drone heterogeneous swarm for area search and payload delivery.

## Structure

- `architecture/` — diagrams, notes, open design decisions
- `scout/` — Scout drone: coverage sweep, detection (YOLO + Gabor/Sable), geotagging, telemetry out
- `carrier/` — Carrier drone: waypoint nav, center-find final approach, release mechanism control
- `gcs/` — Ground control station: target queue, de-dup, dispatch logic, MAVLink relay to both drones
- `mission/` — GCS-owned target lifecycle and aging-based priority specifications
- `communication/` — protocol, ACK/retry, idempotency, and link-loss contracts

## Implementation boundary

Every Python file in this project is a specification scaffold only: docstrings,
interfaces, data contracts, equations, pseudocode, assumptions, and TODOs. No
flight, vision, radio, control, or release algorithm is implemented here. The
user will write the actual implementation.

## Open decisions (as of Aug 2026)

- Carrier LiDAR: confirm in-scope for this build or future-scope (cost not yet in BOM)
- Detection pipeline ordering/fusion: YOLOv8 with Gabor + Sobel/Sable preprocessing must match the training path
- Dispatch: single-target reassignment vs. batch-of-5 per sortie
- Priority score "urgency" term: confirm it's wait-time-based (aging), not something else

## Note

An earlier version of this folder was set up under `training_ground/NIDAR` but that
directory became unreachable (stat failure, not a permissions issue) before this one
was created. If `training_ground` turns up again, check it for anything not carried
over here.
