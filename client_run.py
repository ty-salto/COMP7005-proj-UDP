from utils.args_parser import ArgsParser
from client.client import Client 
from statemachine.statemachine import StateMachine


if __name__ == '__main__':
    parse_args = ArgsParser("Server", "./client/client.json")
    args = parse_args.get_args()

    print(args)
    client = Client(args.target_ip, args.target_port)

    # server.server_listen()

    sm = StateMachine(client, "./client/client_state_actions.json", "./client/client_state_transition.json")
    sm.run()