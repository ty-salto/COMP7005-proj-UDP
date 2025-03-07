import json
import inspect



class StateMachine:
    def __init__(self, class_state, class_ref: object, state_action_file: str, state_transition_file:str):
        self.class_ref = class_ref
        self.state_actions = {}
        self.state_transition = {}
        self.class_state = class_state
        self.current_state = class_state.INIT

        self.__generate_state_action(state_action_file)
        self.__generate_state_transition(state_transition_file)


    def __generate_state_action(self, filepath):
        """
        Generate state-action mapping from JSON file.
        This populates the state_actions dictionary where the key is the state and the value is derived from the class.
        """
        with open(filepath) as f:
            state_action = json.load(f)

        try:
            for key, value in state_action.items():
                self.state_actions[self.class_state[key]] = getattr(self.class_ref, value)
        except KeyError:
            print(f"Warning: '{key}' is not a valid state in the State enum. Skipping...")
        except AttributeError:
            print(f"Warning: '{value}' is not a valid method in {self.class_ref.__name__}. Skipping...")

        # Remove once done debugging
        print(self.state_actions)

    def __generate_state_transition(self, filepath):
        """
        Generate state-transition mapping from JSON file.
        This populates the state_transition dictionary where the key is the state and the value is a list of states that can be transitioned to.
        """
        with open(filepath) as f:
            state_action = json.load(f)
        try:
            for key, value in state_action.items():
                self.state_transition[self.class_state[key]] = [self.class_state[state] for state in value]
                # for state in value:
                #     self.state_transition[State[key]].append(State[state])
        except KeyError:
            print(f"Warning: '{key}' is not a valid state in the State enum. Skipping...")
        except AttributeError:
            print(f"Warning: '{value}' is not a valid method in {self.class_ref.__name__}. Skipping...")

        # Remove once done debugging
        print(self.state_transition)

    def run(self,*args):
        """
        Run the state machine.
        This method executes the actions associated with the current state and transitions to the next state based on the returned index.
        First 5 integers of the returned tuple are used to transition to the next state.
        """
        isRun = True
        while isRun:
            action = self.state_actions[self.current_state]

            if action: # Checks to see if there is an action associated with the current state
                signature = inspect.signature(action)
                param_count = len(signature.parameters)

                result = action() if param_count == 0 else action(*args) # Executes the action with the appropriate arguments

                # if param_count == 0:
                #     result = action()
                # else:
                #     result = action(*args)

                # Checks to see if the result is a tuple and if the first element is an integer less than 5 (This will represent the next state index)
                if isinstance(result, tuple):
                    if isinstance(result[0], int) and result[0] < 5:
                        next_state_index, *next_args = result  # Unpack tuple
                    else:
                        next_state_index = 0
                        next_args = result
                else:
                    next_state_index = result if result != None else 0
                    next_args = ()

            if self.current_state in self.state_transition:
                next_states = self.state_transition[self.current_state]

                if next_states:
                    self.current_state = next_states[next_state_index]
                    args = next_args
                else:
                    isRun = False


    # def run(self,*args):
    #     isRun = True
    #     while isRun:
    #         action = self.state_actions[self.current_state]

    #         if action:
    #             signature = inspect.signature(action)
    #             param_count = len(signature.parameters)

    #             if param_count == 0:
    #                 result = action()
    #             else:
    #                 result = action(*args)

    #             if isinstance(result, tuple):
    #                 next_args = result  # Unpack tuple as arguments for next state
    #             else:
    #                 next_args = (result,) if result is not None else ()

    #         if self.current_state in self.state_transition:
    #             next_states = self.state_transition[self.current_state]
    #             if next_states:
    #                 self.current_state = next_states[0]
    #                 args = next_args
    #             else:
