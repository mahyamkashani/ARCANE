from dispruption_degradation import degradation, disruption 

class ResilienceManager:

    def __init__(self):
        self.attack_active = False
        self.S = set() # Compromised set 

        # Component set
        self.D = {
            "camera", 
            "left_wheel", 
            "right_wheel", 
            "distance_sensor"
            } 
        
        self.kappa = {
            "camera": 0.5,
            "left_wheel": 0.5,
            "right_wheel": 0.5,
            "distance_sensor": 0.5
        }
        
        self.tau = {}
        self.epsilon = {}
        self.kappa = {}
        self.current_task = {}
        self.current_goal = {}

        self.normal_speed = 5.0
        self.degraded_speed = 1.0

        # Used for logger function
        self.prev_S = set()
        self.prev_resilient = None
        self.prev_psi = None

        

    def load_example(self, tau, epsilon, kappa, current_task, current_goal):
        self.tau = tau
        self.epsilon = epsilon
        self.kappa = kappa
        self.current_task = current_task
        self.current_goal = current_goal

    
    def update_compromised_set(self, ids_output: dict):
        #self.prev_S = self.S.copy()
        self.S.clear()

        for d, confidence in ids_output.items():
            #print(f'd: {d} confidence: {confidence}')
            if d in self.D and confidence > self.kappa[d]:
                #print(d)
                self.S.add(d)


    def check_resilience(self):
        delta = disruption(self.S, self.tau, self.epsilon, self.current_task, self.current_goal)
        gamma = degradation(self.S, self.tau, self.epsilon, self.current_task, self.current_goal)
        return delta and gamma



    def log_state_changes(self):
        # Log change in S
        if self.S != self.prev_S:
            print(f"[RM] Compromised set updated: {self.S}")
            self.prev_S = self.S.copy()

        # Log resilience
        delta = disruption(self.S, self.tau, self.epsilon, self.current_task, self.current_goal)
        gamma = degradation(self.S, self.tau, self.epsilon, self.current_task, self.current_goal)
        resilient = (delta == 1 and gamma == 1)

        if resilient != self.prev_resilient:
            print(f"[RM] Resilience state changed: {resilient}")
            self.prev_resilient = resilient

    
    # Mitigating actions..
    def get_wheel_speed(self):
        if not self.check_resilience():
            return self.degraded_speed
        return self.normal_speed 

    '''
    def camera_enabled(self):
        return "camera" not in self.S
    
    def distance_sensor_enabled(self):
        return "distance_sensor" not in self.S
    '''
