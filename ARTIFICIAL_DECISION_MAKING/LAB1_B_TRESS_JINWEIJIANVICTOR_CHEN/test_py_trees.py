#!/usr/bin/env python
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import py_trees
import random
# Condition Node to Check if i already arrived
class locacheck(py_trees.behaviour.Behaviour):
 # minimal one-time initialization
     def __init__(self, name, threshold=5):
         super(locacheck, self).__init__(name)
         self.threshold = threshold

         print("locacheck behavior at __init__")
         # method executed every time ticked
     def update(self):
         print("locacheck at update")

         print(f"Checking location")
         if location < self.threshold:
            print("go on, time to go to location")
            return py_trees.common.Status.FAILURE
         else:
             print("oh oh time to stop LOCARTIO ARRIVED")
             return py_trees.common.Status.SUCCESS
# Action Node for actually going to place
class GoingTolocation(py_trees.behaviour.Behaviour):
     def __init__(self, name,init_location = 0, goal = 5):
         super(GoingTolocation, self).__init__(name)
         print("location fixed behavior at __init__")
         self.threshold = goal
     def update(self):
         print("location fixed...")
         if location < self.threshold:
            print("MOVING TO LOCA")
            location +=1

            return py_trees.common.Status.FAILURE
         else:
             print("oh oh time to stop LOCARTIO ARRIVED")
             return py_trees.common.Status.SUCCESS

class picking(py_trees.behaviour.Behaviour):
    def __init__(self,
# Building the Behavior Tree
def create_behavior_tree():
     battery_check = BatteryCheck("Battery Check", threshold=0.5)
     move_forward = GoingToCharger("Going to Charger")
     selector = py_trees.composites.Selector("check location and move to",True, [#check location and move])
     root = py_trees.composites.Sequence("picking an object", True, [battery_check, move_forward])
     return root
# Main Function to Run the Tree
if __name__ == "__main__":
     root_check_and_charge = create_behavior_tree()
     # Initialize and execute the tree
     behaviour_tree = py_trees.trees.BehaviourTree(root_check_and_charge)
     behaviour_tree.tick() # BT ticking once
     #behaviour_tree.tick_tock(500) # try this line if you wantto tick your BT every 500ms continuosly
     py_trees.display.unicode_tree(behaviour_tree.root,show_status=True)

