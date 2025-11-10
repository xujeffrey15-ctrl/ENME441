import time
import multiprocessing
from Shifter import shifter   # our custom Shifter class

class Stepper:
    # Class attributes:
    num_steppers = 0      # track number of Steppers instantiated
    shifter_outputs = 0   # track shift register outputs for all motors
    seq = [0b00000001,0b00000011,0b00000010,0b00000110,0b00000100,0b00001100,0b00001000,0b00001001] # CCW sequence
    delay = 1200          # delay between motor steps [us]
    steps_per_degree = 4096/360    # 4096 steps/rev * 1/360 rev/deg

    def __init__(self, shifter, lock):
        self.s = shifter           # shift register
        self.angle = 0             # current output shaft angle
        self.step_state = 0        # track position in sequence
        self.shifter_bit_start = 4*Stepper.num_steppers  # starting bit position
        self.lock = lock           # multiprocessing lock

        Stepper.num_steppers += 1   # increment the instance count

    # Signum function:
    def __sgn(self, x):
        if x == 0: return(0)
        else: return(int(abs(x)/x))

    # Move a single +/-1 step in the motor sequence:
    def __step(self, dir):
        self.step_state += dir    # increment/decrement the step
        self.step_state %= 8      # ensure result stays in [0,7]
        Stepper.shifter_outputs |= 0b1111<<self.shifter_bit_start
        Stepper.shifter_outputs &= Stepper.seq[self.step_state]<<self.shifter_bit_start
        self.s.shiftByte(Stepper.shifter_outputs)
        self.angle += dir/Stepper.steps_per_degree
        self.angle %= 360         # limit to [0,359.9+] range

    # Move relative angle from current position:
    def __rotate(self, delta):
        self.lock.acquire()                 # wait until the lock is available
        numSteps = int(Stepper.steps_per_degree * abs(delta))    # find the right # of steps
        dir = self.__sgn(delta)        # find the direction (+/-1)
        for s in range(numSteps):      # take the steps
            self.__step(dir)
            time.sleep(Stepper.delay/1e6)
        self.lock.release()

    # Move relative angle from current position:
    def rotate(self, delta):
        time.sleep(0.1)
        p = multiprocessing.Process(target=self.__rotate, args=(delta,))
        p.start()

    # Move to an absolute angle taking the shortest possible path:
    def goAngle(self, angle):
        angle %= 360
        delta = angle - self.angle
        if delta > 180:
            delta -= 360
        elif delta <= -180:
            delta += 360
        self.rotate(delta)

    # Set the motor zero point
    def zero(self):
        self.angle = 0


# Example use:

if __name__ == '__main__':

    s = shifter(16,21,20)   # set up Shifter

    # Use multiprocessing.Lock() to prevent motors from trying to 
    # execute multiple operations at the same time:
    lock = multiprocessing.Lock()

    # Instantiate 2 Steppers:
    m1 = Stepper(s, lock)
    m1.zero()
    m1.rotate(90)
    m1.rotate(-90)
    m1.rotate(30)
    print('done')

    try:
        while True:
            pass
    except:

        print('\nend')











