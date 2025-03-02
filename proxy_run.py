from utils.args_parser import ArgsParser
from proxy.proxy import Proxy

if __name__ == "__main__":
    parse_args = ArgsParser("Proxy", "./proxy/proxy.json")
    args = parse_args.get_args()
    proxy = Proxy(args.ip, args.port)

    proxy.proxy_init()
    try:
        while True:
            data, addr = proxy.proxy_listen()
            if not data:
                continue
            addr, message = proxy.proxy_receive(data, addr)
            ip, port = addr[0], addr[1]
            proxy.proxy_response(ip, port, message)


    except KeyboardInterrupt:
        print("Shutting down proxy...")
