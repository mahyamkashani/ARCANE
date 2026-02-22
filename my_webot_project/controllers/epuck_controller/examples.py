# T - task(s)
# G - goal(s)
# tau - task criticality
# epsilon - goal criticality

test_example = {
    "T": {"TransportCube"},
    "G": {"AvoidCollision"},
    "tau": {
        ("left_wheel", "TransportCube"): 2,
        ("right_wheel", "TransportCube"): 2,
        ("camera", "TransportCube"): 1,
        ("distance_sensor", "TransportCube"): 1
    },
    "epsilon": {
        ("left_wheel", "AvoidCollision"): 1,
        ("right_wheel", "AvoidCollision"): 1,
        ("camera", "AvoidCollision"): 2,
        ("distance_sensor", "AvoidCollision"): 1
    },
    "kappa": {
        "left_wheel": 0.4,
        "right_wheel": 0.4,
        "camera": 0.8,
        "distance_sensor": 0.8
    }
}

example_A = {
    "T": {"TransportCube"},
    "G": {"AvoidCollision"},
    "tau": {
        ("C1", "TransportCube"): 2,
        ("C2", "TransportCube"): 1,
        ("C3", "TransportCube"): 1,
        ("C4", "TransportCube"): 1,
        ("C5", "TransportCube"): 1,
        ("C6", "TransportCube"): 1,
        ("C7", "TransportCube"): 1,
        ("C8", "TransportCube"): 1,
        ("A1", "TransportCube"): 2,
        ("A2", "TransportCube"): 1,
        ("A3", "TransportCube"): 1,
        ("A4", "TransportCube"): 1
        },
    "epsilon": {
        ("C1", "AvoidCollision"): 2,
        ("C2", "AvoidCollision"): 1,
        ("C3", "AvoidCollision"): 1,
        ("C4", "AvoidCollision"): 1,
        ("C5", "AvoidCollision"): 1,
        ("C6", "AvoidCollision"): 1,
        ("C7", "AvoidCollision"): 1,
        ("C8", "AvoidCollision"): 1,
        ("A1", "AvoidCollision"): 1,
        ("A2", "AvoidCollision"): 1,
        ("A3", "AvoidCollision"): 1,
        ("A4", "AvoidCollision"): 1
    },
    "kappa": {
        "C1": 0.4,
        "C2": 0.8,
        "C3": 0.8,
        "C4": 0.8,
        "C5": 0.8,
        "C6": 0.8,
        "C7": 0.8,
        "C8": 0.8,
        "A1": 0.4,
        "A2": 0.8,
        "A3": 0.8,
        "A4": 0.8
    }
    }

