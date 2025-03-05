import argparse
import json

class ArgsParser:
    TYPE_MAP = {
        "str": str,
        "int": int,
        "float": float,
    }

    def __init__(self, appname, filepath):
        self.appname = appname
        self.filepath = filepath
        self.parser = argparse.ArgumentParser(description=f"{appname} command arguments")
        self.__add_args()

    def __add_args(self):
        with open(self.filepath) as f:
            config = json.load(f)
        for section, values in config.items():
            arg_name = values.get("arg")
            arg_type = self.TYPE_MAP.get(values.get("type"), str)
            arg_is_required = values.get("required") == "true"
            arg_help = values.get("help", "")

            if arg_name:
                self.parser.add_argument(arg_name, type=arg_type, help=arg_help, required=arg_is_required)



    def get_args(self):
        return self.parser.parse_args()
