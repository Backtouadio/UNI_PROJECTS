#!/usr/bin/env python3
import py_trees
import random

# Condition Node: Check for obstacles
class CheckForObstacles(py_trees.behaviour.Behaviour):
    def __init__(self, name="Check For Obstacles"):
        super(CheckForObstacles, self).__init__(name)

    def update(self):
        # Simulating detecting obstacle
        obstacle_detected = random.choices([True, False],
                                           weights=[0.25, 0.75])[0]
        if obstacle_detected:
            print("Obstacle detected!")
            return py_trees.common.Status.FAILURE
        else:
            print("No obstacle detected.")
            return py_trees.common.Status.SUCCESS

# Condition Node: Check battery status
class CheckBatteryLevel(py_trees.behaviour.Behaviour):
    def __init__(self, name="Check Battery Level", threshold=50):
        super(CheckBatteryLevel, self).__init__(name)
        self.threshold = threshold

    def update(self):
        # Simulating battery level between 1% and 100%
        battery_level = random.randint(1,100)
        if battery_level > self.threshold:
            print(f"Battery level ok: {battery_level}%")
            return py_trees.common.Status.SUCCESS
        else:
            print(f"Battery level too low: {battery_level}%")
            return py_trees.common.Status.FAILURE

# Action Node: Navigate
class Navigate(py_trees.behaviour.Behaviour):
    def __init__(self, name="Move Forward"):
        super(Navigate, self).__init__(name)

    def update(self):
        print("Navigating safely...")
        return py_trees.common.Status.SUCCESS

# Build the behavior tree
def create_behavior_tree():
    # Root: Parallel Node to run both checks simultaneously
    parallel_check = py_trees.composites.Parallel("Parallel: Obstacle and Battery Check",
                                        py_trees.common.ParallelPolicy.SuccessOnAll(False))
    root = py_trees.composites.Sequence("move forward", memory=True)


    # Obstacle and battery check nodes
    check_obstacles = CheckForObstacles()
    check_battery = CheckBatteryLevel()

    # Move forward action
    move_forward = Navigate()

    # Add condition checks and action node to the parallel node
    root.add_children([parallel_check,move_forward])
    parallel_check.add_children([check_obstacles, check_battery])

    return root

# Main function to run the behavior tree
if __name__ == "__main__":
    root = create_behavior_tree()
    # Create and run the behavior tree
    bt = py_trees.trees.BehaviourTree(root)
    bt.tick()
    print(py_trees.display.ascii_tree(bt.root, show_status=True))
