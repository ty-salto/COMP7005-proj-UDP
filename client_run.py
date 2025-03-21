from utils.args_parser import ArgsParser
from utils import helper
from client.client import Client 
from client.client_states import ClientState
from statemachine.statemachine import StateMachine



if __name__ == '__main__':
    parse_args = ArgsParser("Client", "./client/client.json")
    args = parse_args.get_args()

    try:
        helper.is_valid_address_port(args.target_ip, args.target_port)

        #print(args)
        client = Client(args.target_ip, args.target_port)

        sm = StateMachine(ClientState, client, "./client/client_state_actions.json", "./client/client_state_transition.json")
        sm.run()
    except ValueError as e:
        print(f"ValueError: {e}")

