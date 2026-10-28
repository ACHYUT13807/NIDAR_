"""Scout local frame-to-frame tracking specification.

Purpose: Scout re-observes the same person across many consecutive frames
during a single pass. Without this, every frame's detection becomes a
separate DETECTION_REPORT, flooding the GCS dedup logic with near-identical
observations from one pass rather than one clean report per person.
"""


def update_tracks(frame_detections, active_tracks, frame_timestamp):
    """Specify per-frame track association and lifecycle.

    Pseudocode:
    1. Match frame_detections against active_tracks by spatial proximity
       (bbox IoU or centroid distance in image space -- choose based on how
       much a person's box moves between consecutive frames at your frame
       rate).
    2. Matched detections update the corresponding track's position,
       confidence, and last_seen_frame.
    3. Unmatched detections start a new provisional track.
    4. A track not matched for N consecutive frames is finalized as ended
       (person left frame).
    5. A track only becomes eligible to report once it has persisted for a
       minimum number of consecutive frames -- this is what filters single-
       frame false positives out before they ever reach the GCS.
    6. Return (updated active_tracks, tracks newly eligible to report this
       frame).

    TODO: minimum-persistence threshold and IoU/distance matching threshold
    both need values chosen from real flight footage, not assumed.
    """


def track_to_observation(track, synced_pose):
    """Specify packaging an eligible track's current bbox and synced_pose
    into the DetectionObservation structure that
    scout/geotag_algorithm.py's estimate_target_position() consumes.
    Provenance (which frames contributed) should be preserved, not
    discarded at this step.
    """
