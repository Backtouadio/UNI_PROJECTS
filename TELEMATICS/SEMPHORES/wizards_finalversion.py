import threading as th
from threading import Thread, Condition
import random
from time import sleep

MAX_BRIDGE_CAPACITY = 5 #max wizards on the bridge
MAX_BURST = 10
NEVILLEDIR = 1  
HOGWARTSDIR = -1
MAX_NEVILLE_CAPACITY = 10 #max wizards on neville side

class Bridge:
    def __init__(self):
        self.flow = 0 #0 if no one is crossing, 1 if going towards Neville, -1 towards Hogwarts
        self.wizards = 0 #number of wizards currently on the bridge
        self.nevilleside = 0 #number of wizards on neville side  
           #the burst condition will be defined as the sum of the wizards on nevilleside and the bridge 
        self.condition = Condition()

    def in_bridge(self, who, direction, other_direction):
        #called when a wizard is trying to get into the bridge, 
        #they can only cross if they are notified to do so, as
        #long as the wizard wants to go on the same direction of the
        #flow of the bridge, there are less than 5 wizards on it, and
        #burst condition hasn't been reached
        with self.condition:
            if not (self.wizards + self.nevilleside == MAX_NEVILLE_CAPACITY  and direction == HOGWARTSDIR and self.nevilleside == MAX_NEVILLE_CAPACITY):
                while (self.wizards == MAX_BRIDGE_CAPACITY or self.flow == other_direction or self.nevilleside==MAX_NEVILLE_CAPACITY or self.wizards + self.nevilleside == MAX_NEVILLE_CAPACITY):
                    self.condition.wait()

             
            #when there is no one on the bridge, the first wizard to come
            #decides the flow of the bridge
            if self.flow == 0:
                self.flow = direction
            if self.flow == HOGWARTSDIR:
                self.nevilleside -= 1
                print("Wizards at Neville side: ",self.nevilleside)
                print("Wizards in Bridge: ", self.wizards+1)

            self.wizards += 1
                         
    def out_bridge(self):
        with self.condition:
            self.wizards -= 1
            if self.flow == NEVILLEDIR:
                self.nevilleside += 1
                print("Wizards at Neville side: ",self.nevilleside)
                print("Wizards in Bridge: ", self.wizards)
            if self.wizards == 0:
                self.flow = 0
            self.condition.notify_all()
    
    def __str__(self):
        if self.flow == NEVILLEDIR:
            return "Bridge flow: H->N. Wizards bridge: "+ str(self.wizards)
        elif self.flow == HOGWARTSDIR:
            return "Bridge flow: N->H. Wizards bridge: "+ str(self.wizards)
        else:
            return "Bridge flow: None. Wizards bridge: "+ str(self.wizards)
            

class Wizard(Thread):
    def __init__(self, bridge, name):
        Thread.__init__(self)
        self.direction = NEVILLEDIR 
        self.name = name
        self.bridge = bridge

    def __str__(self):
        if self.direction == NEVILLEDIR:
            return "[H->N " + self.name + "]"
        else:
            return "[N->H " + self.name + "]"

    def where(self, direction): 
        #prints where the wizard is currently
        if direction == HOGWARTSDIR:
            return "I'm with Neville"
        else: 
            return "I'm at Hogwarts"

    def run(self):
        #code executed for each wizard
        #the for is used to make the wizard go and come back afterwards
        ini_direction = NEVILLEDIR
        for i in range(2):
            
            sleep(random.random())
            self.bridge.in_bridge(self, ini_direction, -ini_direction)
            print(f"{self}: Wizard IN bridge")
            sleep(random.random())
            print(f"{self}: Wizard OUT bridge")
            self.direction = self.direction*-1
            self.bridge.out_bridge()
            #the direction is changed to Hogwarts and the code is repeapted once more
            ini_direction = HOGWARTSDIR
            if i == 0:
                print(f"{self}: {self.where(ini_direction)}")
            if i == 1:
                print (f"{self}: I am done!")
            

def main():
    bridge = Bridge()
    #we create the wizards needed, as instances of the class Wizard
    for i in range(100):
        Wizard(bridge, str(i)).start()

if __name__ == "__main__":
    main()