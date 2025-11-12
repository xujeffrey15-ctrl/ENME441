import time
import multiprocessing
from Shifter import shifter  # your custom module

# Shared array for two steppers (integers)
myArray = multiprocessing.Array('i', 2)

class Stepper:
    seq = [0b0001, 0b0011, 0b0010, 0b0110, 0b0100, 0b1100, 0b1000, 0b1001]
    delay = 12000
    steps_per_degree = 4096 / 360
    final = 0b00000000

    def __init__(self, shifter, lock, index):
        self.s = shifter
        self.lock = lock
        self.index = index
        self.angle = 0
        self.step_state = 0
        self.shifter_bit_start = 4 * index

    def _sgn(self, x):
        return 0 if x == 0 else int(abs(x)/x)

    def _step(self, delta):
        with lock:
            dir = self._sgn(delta)
            self.step_state = (self.step_state + dir) % 8
            myArray[self.index] &= ~(0b1111 << self.shifter_bit_start)
            myArray[self.index] |= (Stepper.seq[self.step_state] << self.shifter_bit_start)
            self.angle = (self.angle + dir / Stepper.steps_per_degree) % 360
            Stepper.final |= myArray[self.index]
 

    def rotate(self, delta):
        steps = int(Stepper.steps_per_degree * abs(delta))
        p = multiprocessing.Process(target=self._step, args=(delta,))
        for _ in range(steps):
            p.start()
            p.join()
            self.s.shiftByte(Stepper.final)
            time.sleep(Stepper.delay / 1e6)
            
    def zero(self):
        self.angle = 0


if __name__ == '__main__':
    s = shifter(16, 21, 20)
    lock = multiprocessing.Lock()

    m1 = Stepper(s, lock, 0)
    m2 = Stepper(s, lock, 1)

    m1.rotate(90)
    m2.rotate(90)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nend")



































































































