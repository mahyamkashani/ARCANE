import rclpy

from controller import Robot
from components.wheel import Wheel
from components.camera import Camera 
from components.distance_sensor import DistanceSensor
from ros2_subscriber import SubscriberNode
from resilience_manager import ResilienceManager


robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Initialise Wheel components
left_wheel = Wheel(robot, "left wheel motor")
right_wheel = Wheel(robot, "right wheel motor")

# Initialise Camera component
camera = Camera(robot, 'camera', timestep)

# ROS init and Node instance
rclpy.init()
sub_node = SubscriberNode()

# Initialise Resilience Manager
resilience_manager = ResilienceManager()

# Webot main loop
while robot.step(timestep) != -1:
    
    rclpy.spin_once(sub_node, timeout_sec=0.0)

    resilience_manager.update_attack_state(sub_node.attack_state)

    velocity = resilience_manager.get_wheel_speed()

    if resilience_manager.camera_enabled():
        camera.enable()
    else:
        camera.disable()
    
    left_wheel.set_speed(velocity)
    right_wheel.set_speed(velocity)

sub_node.destroy_node()
rclpy.shutdown()

