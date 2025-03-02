from utils.args_parser import ArgsParser
from server.server import Server
from statemachine.statemachine import StateMachine


if __name__ == '__main__':
    """
    Start the server

    So far Proxy server has hard-coded values for easy testing and simulating conditions.
    Those are just the ip and port it binds to.

    to run the server, use the following command:
    python server_run.py --ip <ip_address> --port <port_number>
    """

    parse_args = ArgsParser("Server", "./server/server.json")
    args = parse_args.get_args()

    server = Server(args.ip, args.port)

    # server.server_listen()

    sm = StateMachine(server, "./server/server_state_actions.json", "./server/server_state_transition.json")
    sm.run()
