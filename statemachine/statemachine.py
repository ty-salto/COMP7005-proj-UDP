class StateMachine:
    def __init__(self, class_ref, state_action_file, state_transition_file):
        self.class_ref = class_ref
        self.state_actions = {}
        self.state_transition = {}

        self.__generate_state_action(state_action_file)


    def __generate_state_action(self, filepath):
        pass

    def __generate_state_transition(self, filepat):
        pass