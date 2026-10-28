"""
Sobel Edge Feature -- NIDAR RescueSwarm

One of two parallel low-level feature extractors (the other is
gabor.py) whose outputs are combined in detection_fusion.py before
reaching yolo_detector.py.
"""

def compute_sobel_edges(frame):
    """
    ALGORITHM:
    1. Convert frame to grayscale if not already.
    2. Apply Sobel kernels in x and y directions to get gradient
       components Gx, Gy.
    3. Combine into gradient magnitude: sqrt(Gx^2 + Gy^2) (and
       optionally direction: atan2(Gy, Gx), if detection_fusion.py
       wants orientation info, not just magnitude).
    4. Normalize output to a consistent range so it fuses cleanly with
       gabor.py's output and the raw image channels.
    5. Return the edge-magnitude map, same spatial size as frame.
    """
    raise NotImplementedError
