from Shifter import shifter
import multiprocessing
import time

shared_state = multiprocessing.Array('i', 2)

class Stepper:
    #Class variables
    seq = [0b0001, 0b0011, 0b0010, 0b0110, 0b0100, 0b1100, 0b1000, 0b1001]
    delay = 0.005
    steps_per_degree = 4096 / 360

    def __init__(self, lock, index):
        #Class initiation variables (need to pass to construct class)
        self.s = shifter(16,21,20)
        self.lock = lock
        self.index = index
        #Variables that track data
        self.step_state = 0              
        self.current_angle = 0.0       
        #Set up multiprocessing events and queues
        self.event = multiprocessing.Event() #Necessary to set up "on/off" switches for mutiprocessing, all processes wait until set() before continuing
        self.q = multiprocessing.Queue() #Necessary to insert multiple commands and have them execute sequentially
        #Set up the multiprocessing themselves
        self.proc = multiprocessing.Process(target=self._run, daemon=True)
        self.proc.start()
        
    def _sgn(self, x):    #Function to convert a degree into a value of 0, 1, or -1 depending on the degree desired (ex. -90 --> -1)
        return 0 if x == 0 else (1 if x > 0 else -1)
        
    def _step(self, direction):
        self.step_state = (self.step_state + direction) % 8        #Code that causes the motor to either increase by one step or go back one step depending on the direction. The mod 8 keeps the values from exceeding 8 as the sequence only has 8 possible values.

        with self.lock:    #Lock to prevent race conditions
            shared_state[self.index] = Stepper.seq[self.step_state] << (4 * self.index) #Self.index governs which interger value in the shared memory array each motor can access. For instance, when self.index = 1 then that motor would be able to update the Array[1] integer.
                                                                                       #The second half of the code updates the respective 4 bits for that motor.
            output_byte = 0     #Placeholder value for combining as |= does bitwise comparison that results a 1 if there is a 1 in either comparison objects
            for motor_val in shared_state: #Iterates through both array integers
                output_byte |= motor_val #Gets final combined code

            self.s.shiftByte(output_byte) #Pushes to Shifter

        time.sleep(self.delay) #Delay

    def _rotate(self, angle):
        steps = int(abs(angle) * self.steps_per_degree) #Calculates the total num of steps needed for the angle
        direction = self._sgn(angle)                    #Calculates direction

        for _ in range(steps):
            self._step(direction)

        self.current_angle += angle                    #Updates angle

    def _run(self):    #Function to continously get queued commands and runs it
        while True:
            angle = self.q.get()                        
            self._rotate(angle)
            self.event.set()     #Signal completion
            
    def goAngle(self, angle):    #Function to put command in queue
        self.event.clear()
        self.q.put(angle)




