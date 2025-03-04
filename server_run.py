from utils.args_parser import ArgsParser
from server.server import Server
from server.server_states import ServerState
from statemachine.statemachine import StateMachine


if __name__ == '__main__':
    parse_args = ArgsParser("Server", "./server/server.json")
    args = parse_args.get_args()

    server = Server(args.listen_ip, args.listen_port)

    # server.server_listen()

    sm = StateMachine(ServerState, server, "./server/server_state_actions.json", "./server/server_state_transition.json")
    sm.run()