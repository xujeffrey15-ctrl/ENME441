# Motor_Code_Project/Stepper.py
import multiprocessing
import time

# Shared motor state array: 2 motors (expandable)
shared_state = multiprocessing.Array('i', 2)


class Stepper:
    # Half-step sequence
    seq = [0b0001, 0b0011, 0b0010, 0b0110,
           0b0100, 0b1100, 0b1000, 0b1001]

    delay = 0.0025                  # 2.5 ms delay per step (400 steps/sec)
    steps_per_degree = 4096 / 360   # one full rev

    def __init__(self, shifter, lock, index):
        self.s = shifter
        self.lock = lock
        self.index = index

        self.step_state = 0               # REQUIRED to prevent crash
        self.current_angle = 0.0          # absolute angle tracking

        self.event = multiprocessing.Event()
        self.q = multiprocessing.Queue()

        # Process worker
        self.proc = multiprocessing.Process(target=self._run)
        self.proc.daemon = True
        self.proc.start()

    # ------------------------------------------
    # Utility: signed direction
    def _sgn(self, x):
        return 0 if x == 0 else (1 if x > 0 else -1)

    # ------------------------------------------
    # Perform a single half-step
    def _step(self, direction):
        self.step_state = (self.step_state + direction) % 8

        with self.lock:
            # Clear this motor's 4 output bits
            shared_state[self.index] = Stepper.seq[self.step_state] << (4 * self.index)

            # Combine all motors into one byte
            output_byte = 0
            for motor_val in shared_state:
                output_byte |= motor_val

            self.s.shiftByte(output_byte)

        time.sleep(self.delay)

    # ------------------------------------------
    # Rotate delta degrees
    def _rotate(self, delta):
        steps = int(abs(delta) * self.steps_per_degree)
        direction = self._sgn(delta)

        for _ in range(steps):
            self._step(direction)

        self.current_angle += delta

    # ------------------------------------------
    # Worker: receive delta angles and move
    def _run(self):
        while True:
            delta = self.q.get()
            self._rotate(delta)
            self.event.set()   # signal completion

    # ------------------------------------------
    # Public: Move to absolute angle
    def goToAngle(self, absolute_angle):
        delta = absolute_angle - self.current_angle
        self.goAngle(delta)

    # ------------------------------------------
    # Public: Rotate by delta degrees
    def goAngle(self, delta):
        self.event.clear()
        self.q.put(delta)

