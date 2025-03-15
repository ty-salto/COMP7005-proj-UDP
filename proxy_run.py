from statemachine.statemachine import StateMachine
from utils.args_parser import ArgsParser
from proxy.proxy import Proxy
from proxy.proxy_states import ProxyState

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
    if args.preset == "default":
        proxy = Proxy(proxy_ip=args.listen_ip, proxy_port=args.listen_port, target_ip="127.0.0.1", target_port=4301, client_drop=0.0, server_drop=0.0, client_delay=0.0, server_delay=0.0, server_delay_time="200", client_delay_time="200")
    else:
        proxy = Proxy(proxy_ip=args.listen_ip, proxy_port=args.listen_port, target_ip=args.target_ip, target_port=args.target_port, client_drop=args.client_drop, server_drop=args.server_drop, client_delay=args.client_delay, server_delay=args.server_delay, server_delay_time=args.server_delay_time, client_delay_time=args.client_delay_time)
    # proxy = Proxy("127.0.0.1", 4001)

    sm = StateMachine(ProxyState, proxy, "./proxy/proxy_state_actions.json", "./proxy/proxy_state_transition.json")
    sm.run()
