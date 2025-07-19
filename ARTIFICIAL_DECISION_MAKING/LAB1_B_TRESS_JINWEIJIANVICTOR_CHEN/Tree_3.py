#!/usr/bin/env python3
import py_trees
import random

# Condition Node to Check Current Location
class LocationCheck(py_trees.behaviour.Behaviour):
    def __init__(self, name, target_location):
        super(LocationCheck, self).__init__(name)
        self.target_location = target_location
        print("LocationCheck behavior initialized")

    def update(self):
        print("Checking current location...")
        current_location = random.randint(0, 10)  # Simulating current location
        print(f"Current location: {current_location}, Target location: {self.target_location}")
        if current_location == self.target_location:
            print("Already at the target location")
            return py_trees.common.Status.SUCCESS
        else:
            print("Not at the target location")
            return py_trees.common.Status.FAILURE

# Action Node for Moving to Location
class MoveToLocation(py_trees.behaviour.Behaviour):
    def __init__(self, name, target_location):
        super(MoveToLocation, self).__init__(name)
        self.target_location = target_location
        print("MoveToLocation behavior initialized")

    def update(self):
        print(f"Moving to location {self.target_location}...")
        success_probability = 0.5  # 50% chance of successful movement
        if random.choices([True, False], weights=[success_probability, 1-success_probability])[0]:
            print("Successfully moved to the target location")
            return py_trees.common.Status.SUCCESS
        else:
            print("Failed to move to the target location")
            return py_trees.common.Status.FAILURE

# Action Node for Picking Up Object
class PickUpObject(py_trees.behaviour.Behaviour):
    def __init__(self, name):
        super(PickUpObject, self).__init__(name)
        print("PickUpObject behavior initialized")

    def update(self):
        print("Attempting to pick up the object...")
        success_probability = 0.8  # 80% chance of successful pickup
        if random.choices([True, False], weights=[success_probability, 1-success_probability])[0]:
            print("Successfully picked up the object")
            return py_trees.common.Status.SUCCESS
        else:
            print("Failed to pick up the object")
            return py_trees.common.Status.FAILURE

# Building the Behavior Tree
def create_behavior_tree():
    target_location = 5  # Set the target location

    # Create behavior nodes
    location_check = LocationCheck("Check Location", target_location)
    move_to_location = MoveToLocation("Move to Location", target_location)
    pick_up_object = PickUpObject("Pick Up Object")

    # Create composite nodes
    move_sequence = py_trees.composites.Selector("Move Sequence", memory=True)
    move_sequence.add_children([location_check, move_to_location])

    root = py_trees.composites.Sequence("Pick Object Sequence", memory=True)
    root.add_children([move_sequence, pick_up_object])

    return root

# Main Function to Run the Tree
if __name__ == "__main__":
    root = create_behavior_tree()
    behaviour_tree = py_trees.trees.BehaviourTree(root)
    i = 0
    
    # Run the tree for a few ticks to simulate different scenarios
    for _ in range(5):
        i = _ + 1
        print(f"\n--- New Tick {i} ---")
        behaviour_tree.tick()
        print(py_trees.display.ascii_tree(behaviour_tree.root, show_status=True))
