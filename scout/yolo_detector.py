"""YOLO detection specification; TensorRT engine invocation, no training code."""


def run_inference(fused_input, engine):
    """Specify the forward pass through the TensorRT-converted YOLOv11 engine
    on Jetson Orin Nano.

    Pseudocode:
    1. Validate fused_input shape/dtype against the engine's expected input
       binding before running -- a silent shape mismatch is worse than a
       loud failure here.
    2. Execute inference.
    3. Return raw per-anchor outputs (boxes, class scores, objectness) before
       any thresholding -- keep this function a pure forward pass so
       postprocessing can be tuned independently.
    """


def postprocess_detections(raw_outputs, confidence_threshold, nms_iou_threshold):
    """Specify confidence filtering, class restriction to "person", and NMS.

    Pseudocode:
    1. Discard anchors below confidence_threshold.
    2. Restrict to the "person" class only.
    3. Apply NMS at nms_iou_threshold to collapse duplicate boxes for the
       same object.
    4. Return list of (bbox_xyxy_px, confidence) -- this is what feeds
       target_tracker.py, not raw_outputs directly.

    TODO: confidence_threshold and nms_iou_threshold need values chosen from
    a validation set, not guessed defaults.
    """
