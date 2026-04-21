'''
Goal
- Read JSON config
- Set task, tau, epsilon
- Set thresholds (theta_crit and theta_base)
- Listen for attacks via ROS 2
'''
import rclpy
import sys 
import json
import os
from controller import Supervisor

from resilience_manager import ResilienceManager
from ids import IDS
import task
from pr2_control import WHEEL_NAMES, LEFT_ARM_NAMES, RIGHT_ARM_NAMES, LEFT_FINGER_MOTOR, RIGHT_FINGER_MOTOR, TORSO_NAMES, HEAD_NAMES
from attack_executor import AttackExecutor
from component_mapping import COMPONENT_MAP, map_to_high_level

try:
    from ros2_subscriber import SubscriberNode
except ImportError:
    SubscriberNode = None

# ---------------------
# Load Conig
# ---------------------
def run_simulation(config_path, use_ros=True):
    with open(config_path) as f:
        config = json.load(f)

    # ----------------------
    # Webot Setup
    # ----------------------
    supervisor = Supervisor()
    timestep = int(supervisor.getBasicTimeStep())

    # ---------------------
    # ROS2 setup
    # ---------------------
    if use_ros and SubscriberNode is not None:
        rclpy.init()
        subscriber_node = SubscriberNode()
    else:
        subscriber_node = None

    #-----------------------
    # Init core modules
    # ----------------------
    devices = WHEEL_NAMES + LEFT_ARM_NAMES + RIGHT_ARM_NAMES + [LEFT_FINGER_MOTOR] + [RIGHT_FINGER_MOTOR] + TORSO_NAMES + HEAD_NAMES

    RM = ResilienceManager(devices)
    ids = IDS(devices)
    attack_executor = AttackExecutor(supervisor, COMPONENT_MAP)

    # ------------------------
    # Task Setup 
    # ------------------------
    task_type = config["task"]["type"]
    goal_pos_name = config["task"].get("goal")
    object_name = config["task"].get("object")
    arm = config["task"].get("arm")

    # Select task function
    if task_type == "navigate_to_goal":
        current_task = task.navigate_to_goal

    elif task_type == "pickup_object":
        current_task = task.pickup_object

    elif task_type == "navigate_and_pickup":
        current_task = task.navigagte_and_pickup_object

    else:
        raise ValueError(f"Unknown task type: {task_type}")

    # Waypoints from Webots
    waypoints = {}
    if goal_pos_name:
        waypoints[goal_pos_name] = supervisor.getFromDef(goal_pos_name).getPosition()


    # ------------------------------
    # Build tau / epsilon
    # ------------------------------
    task_name = task_type
    goal_name = goal_pos_name

    tau = {}
    epsilon  = {}
    kappa = {}

    for comp, val in config["tau"].items():
        tau[(comp, task_name)] = val

    for comp, val in config["epsilon"].items():
        epsilon[(comp, goal_name)] = val

    #for comp, val in config["kappa"].items():
    #    kappa[(comp)] = val

    RM.load_example(
        tau,
        epsilon,
        {},  # kappa not used anymore
        task_name,
        goal_name
    )

    # Load task/goal parameters into IDS
    ids.load_kappa_sets(tau, epsilon, task_name, goal_name)

    # -----------------------------
    # Thresholds (theta, alpha, kappa)
    # -----------------------------
    RM.theta_crit = config["thresholds"]["theta_crit"]
    RM.theta_base = config["thresholds"]["theta_base"]
    RM.alpha_crit = config["thresholds"]["alpha_crit"]
    RM.alpha_base = config["thresholds"]["alpha_base"]
    ids.kappa_crit = config["thresholds"]["kappa_crit"]
    ids.kappa_base = config["thresholds"]["kappa_base"]
    

    # ----------------------
    # Mitigation
    # ----------------------
    RM.mitigatable_devices = set(config["mitigation"]["enabled_devices"])

    def generate_attacks():
        return [
            {"component": "left_wheels", "type": "UNDERSPEED"}
        ]


    # ------------------------
    # Resilience Check
    # ------------------------
    def check_resilience_live():
        if use_ros and subscriber_node is not None:
            rclpy.spin_once(subscriber_node, timeout_sec=0)
            attack_state = subscriber_node.attack_state
        else:
            attack_state = generate_attacks()

        attack_executor.update(attack_state)
        attack_executor.apply()

        # Update IDS
        ids.update_attack_state(attack_state)

        # High level representation of components -> pass to RM
        S_high = map_to_high_level(ids.S, COMPONENT_MAP)
        RM.S = S_high

        # Check resilience
        result, neutralized = RM.check_resilience()

        # Neutralize attack executor
        if neutralized:
            attack_executor.neutralized(neutralized)
            for comp in neutralized:
                ids.clear_device(comp)

        RM.log_state_changes()
        return result

    # -------------------------------
    # Execute task
    # -------------------------------
    if task_type == "navigate_to_goal":
        result = current_task(
            supervisor,
            waypoints,
            goal_name,
            timestep,
            resilience_check=check_resilience_live,
            resilience_manager=RM,
            attack_executor=attack_executor
        )

    elif task_type == "pickup_object":
        result = current_task(
            supervisor,
            arm,
            object_name,
            timestep,
            resilience_check=check_resilience_live,
            resilience_manager=RM,
            attack_executor=attack_executor
        )

    elif task_type == "navigate_and_pickup":
        result = current_task(
            supervisor,
            waypoints,
            goal_name,
            arm,
            object_name,
            timestep,
            resilience_check=check_resilience_live,
            resilience_manager=RM,
            attack_executor=attack_executor
        )

    print(f"Task result: {result}")

    return {
        "delta": RM.current_delta,
        "gamma": RM.current_gamma,
        "resilient": RM.current_resilient,
        "result": result
    }

if __name__ == "__main__":
    import sys
    run_simulation(sys.argv[1])