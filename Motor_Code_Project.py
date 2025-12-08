from Shifter import shifter  # your custom module
import time

myArray = multiprocessing.Array('i', 2)

class Stepper:
    seq = [0b0001, 0b0011, 0b0010, 0b0110, 0b0100, 0b1100, 0b1000, 0b1001]
    delay = 12000  
    steps_per_degree = 4096 / 360

    def __init__(self, shifter, lock, index):
        self.s = shifter
        self.lock = lock
        self.index = index
        self.angle = 0
        self.step_state = 0
        self.shifter_bit_start = 4 * index
        
    def _sgn(self, x):
        return 0 if x == 0 else int(abs(x)/x)

    def _step(self, direction):
        with self.lock:
            self.step_state = (self.step_state + direction) % 8
            # Clear previous 4 bits
            myArray[self.index] &= ~(0b1111 << self.shifter_bit_start)
            # Set new bits
            myArray[self.index] |= (Stepper.seq[self.step_state] << self.shifter_bit_start)

            # Combine all motor bytes
            final = 0
            for val in myArray:
                final |= val

            # Send to shift register
            self.s.shiftByte(final)

            # Update angle
            self.angle = (self.angle + direction / Stepper.steps_per_degree) % 360

        time.sleep(Stepper.delay / 1e6)

    def _rotate(self, delta):
        steps = int(Stepper.steps_per_degree * abs(delta))
        direction = self._sgn(delta)
        for _ in range(steps):
            self._step(direction)

    def _run(self):
        while True:
            delta = self.q.get()   # Wait for command
            self._rotate(delta)
            self.both.set()        # Signal "done"

    def zero(self):
        self.angle = 0

    def goAngle(self, target_angle):
        # Compute shortest rotation path
        diff = target_angle - self.angle
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360

        self.both.clear()  # Must clear before new command
        self.q.put(diff)   # Background worker handles it
        
if __name__ == '__main__':
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting")































































