'''
GOAL
- Receive attack msg from subscriber node 
- Reason about {component: attack_type}
- Apply attacks
'''
from pr2_control import MAX_WHEEL_SPEED, LEFT_FINGER_MOTOR, RIGHT_FINGER_MOTOR # 3.0   

class AttackExecutor:

    def __init__(self, supervisor, component_map):
        self.supervisor = supervisor
        self.component_map = component_map
        self.active_attacks = []

    def update(self, attacks):
        """Ex attack msg: {component: "left_wheels": "type": "DOS"}"""
        self.active_attacks = attacks

    def has_active_attacks(self):
        #print("active attacks")
        return len(self.active_attacks) > 0
    
    def neutralized(self, neutralized_devices):
        """Remove attacks that has been mitigated by RM"""
        self.active_attacks = [
            attack for attack in self.active_attacks
            if attack["component"] not in neutralized_devices
        ]


    def apply(self):
        for attack in self.active_attacks:
            self.apply_attack(attack["component"], attack["type"])

    
    # Attack Types
    def apply_attack(self, component_name, attack_type):
        # Get low level representation
        component = self.component_map.get(component_name, [])


        if attack_type == "STOP":
            for name in component:
                #print(name)
                motor = self.supervisor.getDevice(name)
                if motor:
                    #print(f'settng motor speed')
                    motor.setPosition(float('inf'))
                    motor.setVelocity(0.0)
        # overspeed
        if attack_type == "OVERSPEED":
            for name in component:
                #print(name)
                motor = self.supervisor.getDevice(name)
                if motor:
                    #print(f'settng motor speed')
                    motor.setPosition(float('inf'))
                    motor.setVelocity(MAX_WHEEL_SPEED * 1.5)

        # underspeed
        if attack_type == "UNDERSPEED":
            #print("applying underspeed attack")
            for name in component:
                #print(name)
                motor = self.supervisor.getDevice(name)
                if motor:
                    #print(f'settng motor speed')
                    motor.setPosition(float('inf'))
                    motor.setVelocity(MAX_WHEEL_SPEED * 0.5)

        # underspeed
        if attack_type == "BACKWARD":
            for name in component:
                #print(name)
                motor = self.supervisor.getDevice(name)
                if motor:
                    #print(f'settng motor speed')
                    motor.setPosition(float('inf'))
                    motor.setVelocity(-MAX_WHEEL_SPEED * 0.5)

        # Gripper attacks
        if attack_type == "GRIP_WEAK":
            """Reduce gripper torque to make gripping weak"""
            if component_name == "left_gripper":
                motor = self.supervisor.getDevice(LEFT_FINGER_MOTOR)
                if motor:
                    motor.setAvailableTorque(0.01)  # Set to minimal torque
            
            elif component_name == "right_gripper":
                motor = self.supervisor.getDevice(RIGHT_FINGER_MOTOR)
                if motor:
                    motor.setAvailableTorque(0.01)  # Set to minimal torque

        # In progress...
        if attack_type == "GRIP_STRONG":
            """Increase gripper torque to make gripping very strong"""
            if component_name == "left_gripper":
                motor = self.supervisor.getDevice(LEFT_FINGER_MOTOR)
                if motor:
                    max_torque = motor.getMaxTorque()
                    motor.setAvailableTorque(max_torque * 10.0)  # Increase beyond normal
            
            elif component_name == "right_gripper":
                motor = self.supervisor.getDevice(RIGHT_FINGER_MOTOR)
                if motor:
                    max_torque = motor.getMaxTorque()
                    motor.setAvailableTorque(max_torque * 10.0)  # Increase beyond normal

