#!/usr/bin/env python3
import py_trees
import random
import time
class DetectHuman(py_trees.behaviour.Behaviour):
    def __init__(self, name="Detect Human"):
        super(DetectHuman, self).__init__(name)

    def update(self):
        human_detected = random.choices([True, False], weights=[0.25, 0.75])[0] # 25% chance of detecting a human
        if human_detected:
            print("Human detected! :)")
            return py_trees.common.Status.SUCCESS
        else:
            print("No human detected. :(")
            return py_trees.common.Status.FAILURE

class Greet(py_trees.behaviour.Behaviour):
    def __init__(self, name="Greet"):
        super(Greet, self).__init__(name)

    def update(self):
        print("Hello! Nice to meet you.")
        return py_trees.common.Status.SUCCESS

class EngageConversation(py_trees.behaviour.Behaviour):
    def __init__(self, name="Engage in Conversation"):
        super(EngageConversation, self).__init__(name)

    def update(self):
        print("How are you today?")
        print("Good!!, what a handsome robot you are.")
        print("Thanks man, it's been great talking to you.")
        return py_trees.common.Status.SUCCESS

class NeedAssistance(py_trees.behaviour.Behaviour):
    def __init__(self, name="Need Assistance"):
        super(NeedAssistance, self).__init__(name)

    def update(self):
        assistance_needed = random.choices([True, False], weights=[0.6, 0.4])[0]
        if assistance_needed:
            print("User needs assistance.")
            return py_trees.common.Status.SUCCESS
        else:
            print("User doesn't need assistance.")
            return py_trees.common.Status.FAILURE

class ProvideAssistance(py_trees.behaviour.Behaviour):
    def __init__(self, name="Provide Assistance"):
        super(ProvideAssistance, self).__init__(name)

    def update(self):
        print("Here's the assistance you needed!")
        return py_trees.common.Status.SUCCESS

class Idle(py_trees.behaviour.Behaviour):
    def __init__(self, name="Idle"):
        super(Idle, self).__init__(name)

    def update(self):
        print("Robot is in idle state.")
        print("Robot sleeping 4 seconds")
        time.sleep(4)
        
        return py_trees.common.Status.SUCCESS

def create_behavior_tree():
    #define the types of compositor we need
    root = py_trees.composites.Selector("Root",memory=True)

    interact_sequence = py_trees.composites.Sequence("Interaction Sequence", memory=True)
    assist_sequence = py_trees.composites.Sequence("Assistance Sequence", memory=True)
# initialize functions and decorators
    detect_human = DetectHuman()
    retry_detection = py_trees.decorators.Retry(name="Retry Detection", child=detect_human,num_failures=3)

    greet = Greet()
    one_shot_greet = py_trees.decorators.OneShot(name="One Shot Greet",child=greet, policy=py_trees.common.OneShotPolicy.ON_SUCCESSFUL_COMPLETION)

    engage_conversation = EngageConversation()
    need_assistance = NeedAssistance()
    provide_assistance = ProvideAssistance()
  
    assist_sequence.add_children([need_assistance, provide_assistance])
    
    interact_sequence.add_children([
        retry_detection,
        one_shot_greet,
        engage_conversation,
        assist_sequence
    ])

    idle = Idle()

    root.add_children([interact_sequence, idle])

    return root

if __name__ == "__main__":
    root = create_behavior_tree()
    behavior_tree = py_trees.trees.BehaviourTree(root)

    for _ in range(5):  # Run the tree for 5 ticks
        print(f"\n--- Tick { _ +1 } ---")
        behavior_tree.tick()
        print(py_trees.display.ascii_tree(behavior_tree.root, show_status=True))
