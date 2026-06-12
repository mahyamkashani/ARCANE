
class Metrics:
    def __init__(self):
        self.done_text="DONE"
        self.degradation= None
        self.slowdown = None

    def compute_degradation(self, result, elapsed_time, baseline_time):
        #Relative slowdown of a task versus its undisrupted baseline.
        if result != self.done_text:
            return self.degradation, self.slowdown

        if not baseline_time:  # None or 0 -> no usable baseline (and no zero-division)
            return self.degradation, self.slowdown

        self.slowdown = elapsed_time - baseline_time
        self.degradation = max(0.0, self.slowdown / baseline_time)
        return self.degradation, self.slowdown