import time
import multiprocessing
from multiprocessing.managers import SharedMemoryManager
from Shifter import shifter   # our custom Shifter class

class Stepper:
    myValue = multiprocessing.Value('i',0b11111111)
    num_steppers = 0      # track number of Steppers instantiated
    shifter_outputs = 0   # track shift register outputs for all motors
    seq = [0b0001,0b0011,0b0010,0b0110,0b0100,0b1100,0b1000,0b1001] # CCW sequence
    delay = 12000          # delay between motor steps [us]
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
        self.lock.acquire()
        self.step_state += dir    # increment/decrement the step
        self.step_state %= 8      # ensure result stays in [0,7]
        Stepper.shifter_outputs &= Stepper.seq[self.step_state]<<self.shifter_bit_start
        self.angle += dir/Stepper.steps_per_degree
        self.angle %= 360
        Stepper.myValue.value &= Stepper.shifter_outputs
        self.lock.release()
        print(bin(Stepper.myValue.value))
        time.sleep(1)

    # Move relative angle from current position:
    def __rotate(self, delta):
        numSteps = int(Stepper.steps_per_degree * abs(delta))    # find the right # of steps
        dir = self.__sgn(delta)        # find the direction (+/-1)
        for s in range(numSteps):      # take the steps
            self.__step(dir)
            time.sleep(Stepper.delay/1e6)
            self.s.shiftByte(Stepper.myValue.value)
            Stepper.myValue.value = 0b11111111

    def rotate(self, delta):
        time.sleep(0.1)
        p = multiprocessing.Process(target=self.__rotate, args=(delta,))
        p.start()

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
    m2 = Stepper(s, lock)

    m1.zero()
    m2.zero()
    m1.rotate(-90)
    m2.rotate(90)
    # While the motors are running in their separate processes, the main
    # code can continue doing its thing: 
    try:
        while True:
            pass
    except:
        print('\nend')



























































