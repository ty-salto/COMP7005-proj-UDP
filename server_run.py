from utils.args_parser import ArgsParser
from server.server import Server 


if __name__ == '__main__':
    parse_args = ArgsParser("Server", "./server/server.json")
    args = parse_args.get_args()

    server = Server(args.ip, args.port)

    server.server_listen()