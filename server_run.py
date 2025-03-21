from utils.args_parser import ArgsParser
from utils import helper
from server.server import Server
from server.server_states import ServerState
from statemachine.statemachine import StateMachine


if __name__ == '__main__':
    parse_args = ArgsParser("Server", "./server/server.json")
    args = parse_args.get_args()

    try:
        helper.is_valid_address_port(args.listen_ip, args.listen_port)
        server = Server(args.listen_ip, args.listen_port)
        

        # server.server_listen()

        sm = StateMachine(ServerState, server, "./server/server_state_actions.json", "./server/server_state_transition.json")
        sm.run()
    except ValueError as e:
        print(f"ValueError: {e}")

