"""Scout perception-fusion specification; the fusion method is unresolved
pending open_design_questions.md item 1 and must match training exactly."""


def fuse_features(frame, sobel_map, gabor_map):
    """Specify how sobel_map and gabor_map combine with the raw frame before
    yolo_detector.py runs.

    This is not free to choose independently: it must reproduce whatever
    fusion scheme model.onnx was actually trained with, or inference will be
    silently wrong. Candidate schemes, pick one and document it:
      - channel-stack: concatenate frame's RGB with sobel_map/gabor_map as
        extra input channels (detector input channel count changes)
      - weighted blend: combine sobel_map/gabor_map into the existing RGB
        channels (detector input stays 3-channel)

    Preconditions: frame, sobel_map, gabor_map must be the same spatial
    resolution; resize/crop mismatches before fusing, do not silently
    broadcast.

    TODO: resolve whether "Sable" (open_design_questions.md item 2) is a
    third distinct feature to fuse here or the same thing as sobel_map under
    a different name -- the function signature changes depending on the
    answer.
    """


def validate_fusion_consistency(fusion_config, model_metadata):
    """Specify a startup check comparing the fusion scheme this module is
    configured for against whatever metadata the exported model records
    about its own training-time input format. Fail loudly rather than
    running inference against a mismatched input shape.
    """
