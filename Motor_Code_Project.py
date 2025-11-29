import time
import multiprocessing
from Shifter import shifter  # your custom module
import Json_Reader

XY = Json_Reader.goanglexy
Z = Json_Reader.goanglez
numturrets = len(Json_Reader.TurretData)
numball = len(Json_Reader.BallData)

myArray = multiprocessing.Array('i', 2)

class Stepper:
    seq = [0b0001, 0b0011, 0b0010, 0b0110,
           0b0100, 0b1100, 0b1000, 0b1001]
    delay = 12000  # microseconds
    steps_per_degree = 1024 / 360

    def __init__(self, shifter, lock, index):
        self.s = shifter
        self.lock = lock
        self.index = index
        self.angle = 0
        self.step_state = 0
        self.shifter_bit_start = 4 * index
        self.q = multiprocessing.Queue()

        # Start a dedicated process to run commands from the queue
        self.proc = multiprocessing.Process(target=self._run)
        self.proc.daemon = True  # ends when main program ends
        self.proc.start()

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
        """ Continuously run commands from the queue """
        while True:
            delta = self.q.get()  # blocks until a new command
            self._rotate(delta)

    def zero(self):
        self.angle = 0

    def goAngle(self, target_angle):
        """ Calculate shortest path and queue the movement """
        diff = target_angle - self.angle
        # Choose shortest rotation
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
        self.q.put(diff)

if __name__ == '__main__':
    s = shifter(16, 21, 20)
    lock = multiprocessing.Lock()

    m1 = Stepper(s, lock, 0)
    m2 = Stepper(s, lock, 1)

    # Initialize angles
    m1.zero()
    m2.zero()

    # Automated movements
    for t in range(1,numturrets):
        m1.goAngle(XY[f"turret_{t}"])
    for b in range(1,numball):
        m1.goAngle(XY[f"ball_{b}"])
        m2.goAngle(Z[f"ball_{b}"])
        
    m1.goAngle(0)
    m2.goAngle(0)

    # Keep main program running
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting")














































