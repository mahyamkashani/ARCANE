class ResilienceManager:

    def __init__(self):
        self.attack_active = False

        self.S = set() # Compromised set 
        self.prev_S = set()

        self.D = {
            "camera", 
            "left_wheel", 
            "right_wheel", 
            "distance_sensor"
            } # Component set, 
        
        self.normal_speed = 5.0
        self.degraded_speed = 1.0
        
    
    def update_attack_state(self, attack_state: dict):
        self.prev_S = self.S.copy()
        self.S.clear()

        for component, active in attack_state.items():
            if active and component in self.D:
                self.S.add(component)

        newly_compromised = self.S - self.prev_S
        recovered = self.prev_S - self.S

        for c in newly_compromised:
            print(f"Component under attack: {c}")

        for c in recovered:
            print(f"Component recovered: {c}")

    
    # Mitigating actions..
    def get_wheel_speed(self):
        if "left_wheel" in self.S or "right_wheel" in self.S:
            return self.degraded_speed
        return self.normal_speed 

    def camera_enabled(self):
        return "camera" not in self.S
    
    def distance_sensor_enabled(self):
        return "distance_sensor" not in self.S

