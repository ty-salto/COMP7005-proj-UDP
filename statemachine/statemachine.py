import enum
import json
import inspect

class State(enum.Enum):
    INIT = 0
    LISTEN = 1
    RECEIVE = 2
    PROCESS = 3
    SEND = 4
    CLOSING = 5

class StateMachine:
    def __init__(self, class_ref, state_action_file, state_transition_file):
        self.class_ref = class_ref
        self.state_actions = {}
        self.state_transition = {}
        self.current_state = State.INIT

        self.__generate_state_action(state_action_file)
        self.__generate_state_transition(state_transition_file)


    def __generate_state_action(self, filepath):
        with open(filepath) as f:
            state_action = json.load(f)

        try:
            for key, value in state_action.items():
                self.state_actions[State[key]] = getattr(self.class_ref, value)
        except KeyError:
            print(f"Warning: '{key}' is not a valid state in the State enum. Skipping...")
        except AttributeError:
            print(f"Warning: '{value}' is not a valid method in {self.class_ref.__name__}. Skipping...")

        # Remove once done debugging
        print(self.state_actions)

    def __generate_state_transition(self, filepath):
        with open(filepath) as f:
            state_action = json.load(f)
        try:
            for key, value in state_action.items():
                self.state_transition[State[key]] = [State[state] for state in value]
                # for state in value:
                #     self.state_transition[State[key]].append(State[state])
        except KeyError:
            print(f"Warning: '{key}' is not a valid state in the State enum. Skipping...")
        except AttributeError:
            print(f"Warning: '{value}' is not a valid method in {self.class_ref.__name__}. Skipping...")

        # Remove once done debugging
        print(self.state_transition)

    def run(self,*args):
        isRun = True
        while isRun:
            action = self.state_actions[self.current_state]

            if action:
                signature = inspect.signature(action)
                param_count = len(signature.parameters)

                if param_count == 0:
                    result = action()
                else:
                    result = action(*args)

                if isinstance(result, tuple):
                    next_args = result  # Unpack tuple as arguments for next state
                else:
                    next_args = (result,) if result is not None else ()

            if self.current_state in self.state_transition:
                next_states = self.state_transition[self.current_state]
                if next_states:
                    self.current_state = next_states[0]
                    args = next_args
                else:
                    isRun = False
