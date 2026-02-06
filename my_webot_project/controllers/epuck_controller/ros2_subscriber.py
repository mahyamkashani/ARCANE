from rclpy.node import Node
from my_attack_interfaces.msg import AttackState

# ROS subscriber to attack node
class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')

        self.subscription = self.create_subscription(AttackState, '/attack_state', self.listener_callback, 10)
        self.attack_state = {}
        self.subscription

    def listener_callback(self, msg):
        self.attack_state = {
            "camera": msg.camera,
            "left_wheel": msg.left_wheel,
            "right_wheel": msg.right_wheel,
            "distance_sensor": msg.distance_sensor
        }