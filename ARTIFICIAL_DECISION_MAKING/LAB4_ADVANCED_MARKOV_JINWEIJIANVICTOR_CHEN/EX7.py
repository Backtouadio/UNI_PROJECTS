"""The Searching Object Problem.

This is a POMDP problem; Namely, it specifies both
the POMDP (i.e. state, action, observation space)
and the T/O/R for the agent as well as the environment.

A robot in a warehouse is tasked with finding a specific object among four shelves. Each
shelf has to be inspected to find the object. The robot has a limited view and can only
observe the contents of a shelf when it is close enough. The robot’s objective is to locate
the desired object while minimizing unnecessary movement and avoiding miss-identifications.

The robot can:
•	Move Left or Move Right between shelves.
•	Inspect the current shelf to identify if it contains the object.

The robot receives a reward when it finds the target object and incurs a small penalty for
each move and a larger penalty for a miss-identification (searching for the object but not
finding it).

States: shelf1, shelf2, shelf3, shelf4
Actions: inspect, move-left, move-right
Rewards:
    +50 for finding the object. -10 for miss-identification.
    -1 for moving.
Observations: You can detect either "object-found", or "not-found", but consider that the
perceptual information is noisy.

"""

import pomdp_py
import random

NUM_SHELVES = 4 # number of states where the desired object might be

# Define the states
class ObjectState(pomdp_py.State):
    S0 = "shelf1"
    S1 = "shelf2"
    S2 = "shelf3"
    S3 = "shelf4"

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, ObjectState):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return "ObjectState(%s)" % self.name

    def other(self):
        if self.name == ObjectState.S0:
            return ObjectState(random.choice([ObjectState.S1, ObjectState.S2, ObjectState.S3]))
        elif self.name == ObjectState.S1:
            return ObjectState(random.choice([ObjectState.S0, ObjectState.S2, ObjectState.S3]))
        elif self.name == ObjectState.S2:
            return ObjectState(random.choice([ObjectState.S0, ObjectState.S1, ObjectState.S3]))
        else:
            return ObjectState(random.choice([ObjectState.S0, ObjectState.S1, ObjectState.S2]))


OBJECT_STATE = ObjectState(ObjectState.S1) # Hidden position of the target object (unknown to the agent)

# Define the actions
class ObjectAction(pomdp_py.Action):
    INSPECT = "inspect"
    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, ObjectAction):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return "ObjectAction(%s)" % self.name

# Define the robot's observations
class ObjectObservation(pomdp_py.Observation):
    FOUND_OBJECT = "found"
    NOT_FOUND = "not_found"

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, ObjectObservation):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name

    def __repr__(self):
        return "ObjectObservation(%s)" % self.name


# Define the observation model--> if the robot inspects the correct shelf, it has a high probability of observing that
#                                 the object is present; otherwise, it likely observes that the object is not there.
class ObservationModel(pomdp_py.ObservationModel):
    def __init__(self, noise=0.15):
        self.noise = noise

    def probability(self, observation, next_state, action):
        if action.name == ObjectAction.INSPECT:
            # High probability of finding the object if it's inspected at the correct position
            if observation.name == ObjectObservation.FOUND_OBJECT and next_state.name == OBJECT_STATE.name:
                return 1.0 - self.noise
            # High probability of not finding the object if it's inspected at the wrong position
            elif observation.name == ObjectObservation.NOT_FOUND and next_state.name != OBJECT_STATE.name:
                return 1.0 - self.noise
            return self.noise
        else:
            # Not inspecting, so we should observe NOT_FOUND with high probability
            if observation.name == ObjectObservation.NOT_FOUND:
                return 1.0 - self.noise
            return self.noise

    def sample(self, next_state, action):
        if action.name == ObjectAction.INSPECT:
            if next_state.name == OBJECT_STATE.name and random.uniform(0, 1) < 1.0 - self.noise:
                return ObjectObservation(ObjectObservation.FOUND_OBJECT)
        return ObjectObservation(ObjectObservation.NOT_FOUND)

    def get_all_observations(self):
        return [ObjectObservation(s) for s in {ObjectObservation.FOUND_OBJECT, ObjectObservation.NOT_FOUND}]


# Define the transition model
# Define the transition model
class TransitionModel(pomdp_py.TransitionModel):
    def probability(self, next_state, state, action):
        if action.name == ObjectAction.INSPECT:
            if next_state.name == state.name:
                return 0.9  # High probability to stay in place when inspecting
            return 0.1 / (NUM_SHELVES - 1)  # Small chance to randomly move elsewhere
            
        elif action.name == ObjectAction.MOVE_LEFT:
            if state.name == ObjectState.S0 and next_state.name == ObjectState.S0:
                return 0.95  # Stay at leftmost shelf with high probability
            if next_state.name == state.name:
                return 0.1  # Small chance to stay in place
            shelf_num = int(state.name[-1])
            next_shelf_num = int(next_state.name[-1])
            if shelf_num > 0 and next_shelf_num == shelf_num - 1:
                return 0.9  # High probability to move left one shelf
            return 0.0
            
        else:  # MOVE_RIGHT
            if state.name == ObjectState.S3 and next_state.name == ObjectState.S3:
                return 0.95  # Stay at rightmost shelf with high probability
            if next_state.name == state.name:
                return 0.1  # Small chance to stay in place
            shelf_num = int(state.name[-1])
            next_shelf_num = int(next_state.name[-1])
            if shelf_num < NUM_SHELVES - 1 and next_shelf_num == shelf_num + 1:
                return 0.9  # High probability to move right one shelf
            return 0.0

    def sample(self, state, action):
        curr_idx = int(state.name[-1])
        
        if action.name == ObjectAction.INSPECT:
            # 90% chance to stay in place when inspecting
            if random.random() < 0.9:
                return state
            # 10% chance to move to a random different shelf
            possible_states = [s for s in [ObjectState.S0, ObjectState.S1, ObjectState.S2, ObjectState.S3] if s.name != state.name]
            return random.choice(possible_states)
            
        elif action.name == ObjectAction.MOVE_LEFT:
            rand = random.random()
            if curr_idx == 0:  # At shelf1
                if rand < 0.95:  # 95% chance to stay
                    return ObjectState(ObjectState.S0)
                else:  # 5% chance to move right
                    return ObjectState(ObjectState.S1)
            else:  # At shelf2, shelf3, or shelf4
                if rand < 0.9:  # 90% chance to move left
                    return ObjectState(f"shelf{curr_idx-1}")
                else:  # 10% chance to stay
                    return state
            
        else:  # MOVE_RIGHT
            rand = random.random()
            if curr_idx == 3:  # At shelf4
                if rand < 0.95:  # 95% chance to stay
                    return ObjectState(ObjectState.S3)
                else:  # 5% chance to move left
                    return ObjectState(ObjectState.S2)
            else:  # At shelf1, shelf2, or shelf3
                if rand < 0.9:  # 90% chance to move right
                    return ObjectState(f"shelf{curr_idx+1}")
                else:  # 10% chance to stay
                    return state

    def get_all_states(self):
        return [ObjectState(s) for s in {ObjectState.S0, ObjectState.S1, ObjectState.S2, ObjectState.S3}]
# Define the reward model
# RewardModel implementation
class RewardModel(pomdp_py.RewardModel):
    def _reward_func(self, state, action):
        # Found object while inspecting (correct identification)
        if action.name == ObjectAction.INSPECT and state.name == OBJECT_STATE.name:
            return 50
        # Misidentification penalty
        elif action.name == ObjectAction.INSPECT and state.name != OBJECT_STATE.name:
            return -10
        # Movement penalty
        else:
            return -1

    def sample(self, state, action, next_state):
        return self._reward_func(state, action)
# Policy Model
class PolicyModel(pomdp_py.RolloutPolicy):
    """A simple policy model with uniform prior over a
    small, finite action space"""

    ACTIONS = [ObjectAction(s) for s in {ObjectAction.INSPECT, ObjectAction.MOVE_LEFT, ObjectAction.MOVE_RIGHT}]

    def sample(self, state):
        return random.sample(self.get_all_actions(), 1)[0]
    """
    def sample(self, state):
        if random.uniform(0, 1) < 0.5:  # Favor inspect over move actions
            return ObjectAction(ObjectAction.INSPECT)
        else:
            return random.choice([ObjectAction(ObjectAction.MOVE_LEFT), ObjectAction(ObjectAction.MOVE_RIGHT)])"""


    def rollout(self, state, history=None):
        return self.sample(state)

    def get_all_actions(self, state=None, history=None):
        return PolicyModel.ACTIONS


# Define the POMDP Problem
class ObjectProblem(pomdp_py.POMDP):
    def __init__(self, obs_noise, init_true_state, init_belief):

        # The agent has access to the belief (initially a probabilistic guess of the environment's state) and models
        # for transitions, observations, and rewards. agent encapsulates the agent's models and belief
        agent = pomdp_py.Agent(
            init_belief,                 # initial belief distribution over the possible state
            PolicyModel(),               # policy model used to choose actions
            TransitionModel(),           # transition model
            ObservationModel(obs_noise), # observation model
            RewardModel(),               # reward model
        )

        # env represents the true environment with access to the state, transition model, and reward model
        env = pomdp_py.Environment(
            init_true_state,
            TransitionModel(),
            RewardModel()
        )

        super().__init__(agent, env, name="ObjectProblem")


def test_planner(object_problem, planner, nsteps):
    """
    Runs the action-feedback loop of Object problem POMDP

    Args:
        object_problem (ObjectProblem): a problem instance
        planner (Planner): a planner
        nsteps (int): Maximum number of steps to run this loop.
    """
    for i in range(nsteps):
        action = planner.plan(object_problem.agent)

        print("==== Step %d ====" % (i + 1))
        print(f"True state: {object_problem.env.state}")
        print(f"Belief: {object_problem.agent.cur_belief}")
        print(f"Action: {action}")

        reward = object_problem.env.state_transition(action, execute=True)  # the environment state is transitioned
        print("Reward:", reward)

        # Let's create some simulated real observation;
        real_observation = object_problem.agent.observation_model.sample(object_problem.env.state, action)
        print(">> Observation:", real_observation)
        object_problem.agent.update_history(action, real_observation)

        # Update the belief. If the planner is POMCP, planner.update
        # also automatically updates agent belief.
        planner.update(object_problem.agent, action, real_observation)
        if isinstance(object_problem.agent.cur_belief, pomdp_py.Histogram):
            new_belief = pomdp_py.update_histogram_belief(
                object_problem.agent.cur_belief,
                action,
                real_observation,
                object_problem.agent.observation_model,
                object_problem.agent.transition_model,
            )
            object_problem.agent.set_belief(new_belief)


def make_object_problem(noise=0.15, init_state=ObjectState.S0, init_belief=[0.25, 0.25, 0.25, 0.25]):
    """Convenient function to quickly build a my_object_problem domain.
    Useful for testing"""
    my_object_problem = ObjectProblem(
        noise,
        ObjectState(init_state),
        pomdp_py.Histogram(
            {
                ObjectState(ObjectState.S0): init_belief[0],
                ObjectState(ObjectState.S1): init_belief[1],
                ObjectState(ObjectState.S2): init_belief[2],
                ObjectState(ObjectState.S3): init_belief[3]
            }
        ),
    )
    return my_object_problem


if __name__ == "__main__":
    search_object = make_object_problem()

    print("** Testing value iteration **")
    vi = pomdp_py.ValueIteration(horizon=3, discount_factor=0.95)
    test_planner(search_object, vi, nsteps=10)