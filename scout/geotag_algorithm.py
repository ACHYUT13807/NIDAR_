"""Scout target-geotagging specification; no projection code is implemented."""


def estimate_target_position(bbox_center_px, camera_model, body_pose, camera_mount_pose, ground_model):
    """Define pixel-to-ground geotagging.

    Pseudocode:
    1. Validate timestamp alignment among image, vehicle attitude, GPS, and
       camera/gimbal pose. Reject or inflate uncertainty if unsynchronized.
    2. Invert the calibrated camera model to obtain the camera-frame viewing ray.
    3. Transform ray through camera-to-body and body-to-world rotations.
    4. Intersect with the selected ground model:
         - local plane only when flat-ground assumption is documented; or
         - terrain/depth intersection where available.
    5. Convert resulting world point to WGS-84 and estimate uncertainty.
    6. Return position plus covariance/uncertainty, never a naked coordinate.

    Equations:
      normalized ray ~= [(u-cx)/fx, (v-cy)/fy, 1]^T
      ray_world = R_world_body R_body_camera ray_camera
      p(lambda) = camera_origin_world + lambda * ray_world, lambda > 0

    TODO: declare all transforms, altitude datum, lens-distortion handling, and
    maximum acceptable pose/image timestamp skew.
    """


def fuse_target_observations(observations):
    """Specify multi-observation fusion.

    Preserve observation provenance. Candidate approaches: robust weighted mean,
    covariance-weighted fusion, or a filter. Decide after measuring real GPS,
    attitude, and camera-calibration error; do not average different people that
    happen to fall within an arbitrary radius.
    """
