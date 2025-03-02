from statemachine.statemachine import StateMachine
from utils.args_parser import ArgsParser
from proxy.proxy import Proxy

if __name__ == "__main__":
    """
    Start the Proxy

    So far Proxy server has hard-coded values for easy testing and simulating conditions.
    Those are just the ip and port it binds to.

    to run the server, use the following command:
    python proxy_run.py --ip <ip_address> --port <port_number>
    """

    parse_args = ArgsParser("Proxy", "./proxy/proxy.json")
    args = parse_args.get_args()
    proxy = Proxy(args.ip, args.port)

    sm = StateMachine(proxy, "./proxy/proxy_state_actions.json", "./proxy/proxy_state_transition.json")
    sm.run()
