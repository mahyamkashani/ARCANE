'''
Responsibility
- Separate devices into kappa_crit and kappa_base
- Receive attack_state 
- Update and return compromised set S 
- Clear S when device been neutralized
'''
import random
from component_mapping import COMPONENT_MAP

class IDS:

    def __init__(self, D):
        self.D_low = D # low level representation of devices
        self.S = set()

        self.D_high = {} # high-level representation of devices
        for comp, devices in COMPONENT_MAP.items():
            for d in devices:
                self.D_high[d] = comp
        
        # Task and goal specific criticality values
        self.tau = {}
        self.epsilon = {}
        self.current_task = None
        self.current_goal = None
        
        # Criticality-based device sets
        self.kappa_crit_set = set()
        self.kappa_base_set = set()

        # Kappa = 1 - detection probability
        self.kappa_crit = 0.0
        self.kappa_base = 0.0

        self.tested_devices = set()

# ------------------------------------------------------------------
    def load_kappa_sets(self, tau, epsilon, current_task, current_goal):
        """Load task/goal specific parameters and build criticality sets"""
        self.tau = tau
        self.epsilon = epsilon
        self.current_task = current_task
        self.current_goal = current_goal

        # Create criticality sets based on tau/epsilon
        self.kappa_crit_set.clear()
        self.kappa_base_set.clear()

        for d in self.D_low:
            comp = self.D_high.get(d)
            if comp is None:
                continue

            is_critical = (
                self.tau.get((comp, self.current_task), 0) == 2 or
                self.epsilon.get((comp, self.current_goal), 0) == 2
            )
            if is_critical:
                self.kappa_crit_set.add(d)
            else:
                self.kappa_base_set.add(d)
        
        
    # Probability that the IDS detects an ongoing attack
    def update_attack_state(self, attack_state):
        components = {attack["component"] for attack in attack_state}

        # Clear components who are no longer compromised 
        for comp in list(self.tested_devices):
            if comp not in components:
                self.tested_devices.discard(comp)
                # Remove from S
                for d in COMPONENT_MAP.get(comp, []):
                    self.S.discard(d)

        # Random confidence that the attack was detected by IDS
        for comp in components:
            if comp in self.tested_devices:
                continue 

            devices = COMPONENT_MAP.get(comp, [])
            is_critical = any(d in self.kappa_crit_set for d in devices)
            kappa = self.kappa_crit if is_critical else self.kappa_base

            confidence = random.random()
            if confidence >= kappa:
                for d in devices:
                    self.S.add(d)

            self.tested_devices.add(comp)

    # Called when RM neutralizes a component
    def clear_device(self, comp):
            self.tested_devices.discard(comp)
            for d in COMPONENT_MAP.get(comp, []):
                self.S.discard(d)