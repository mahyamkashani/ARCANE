class IDS:

    def __init__(self, D):
        self.D = D
        self.I = {d: 0.0 for d in D}

    def update_attack_state(self, attack_state: dict): 
        for d in self.D:
            if d in attack_state and attack_state[d]:
                self.I[d] = 1.0
            else:
                self.I[d] = 0.0
 
    def get_probability_output(self):
        return self.I.copy()
    
    def task_criticality(self):
        return
    
    def goal_criticality(self):
        return
