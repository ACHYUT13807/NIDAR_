"""
Scout Camera Capture -- NIDAR RescueSwarm

Handles frame acquisition from the IMX477 and synchronizes each frame
with the drone's pose at capture time (needed later by geotag.py).
"""

def capture_frame(camera_handle):
    """
    ALGORITHM:
    1. Pull the next frame from the IMX477 driver/ROS topic.
    2. Timestamp the frame at capture time (not at processing time --
       processing delay would introduce geotagging error if pose is
       sampled later instead).
    3. Return (frame, capture_timestamp).
    """
    raise NotImplementedError


def get_synced_pose(capture_timestamp, pose_buffer):
    """
    ALGORITHM:
    1. Pixhawk telemetry (position + attitude) arrives on its own
       cadence, generally faster than camera frame rate but not
       perfectly aligned in time.
    2. Maintain a small rolling buffer of recent (timestamp, pose)
       samples.
    3. Given capture_timestamp, find the two buffered poses that
       bracket it and interpolate (or take the nearest sample if
       interpolation isn't worth the complexity at your frame rate) to
       get pose-at-capture-time.
    4. Return the interpolated pose -- this is what geotag.py needs,
       not whatever the "current" pose happens to be when processing
       runs.
    """
    raise NotImplementedError
