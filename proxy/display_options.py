from tabulate import tabulate

def available_params():
    parameters = {
        "client_drop": float,
        "server_drop": float,
        "client_delay": float,
        "server_delay": float,
        "client_delay_time": str,
        "server_delay_time": str,
    }

    table_data = [(param, str(value).split("'")[1]) for param, value in parameters.items()]
    print(tabulate(table_data, headers=["Parameter", "Data Type"], tablefmt="pretty"))


def options():
    options = {
        "1": "Display options",
        "2": "Display current setup",
        "3": "Quit"
    }
    table_data = [(key, value) for key, value in options.items()]
    print(tabulate(table_data, headers=["Option", "Description"], tablefmt="pretty"))

def current_setup(cdrop, sdrop, cdelay, sdelay, cdelay_time, sdelay_time):
    curr_setup = {
        "Client Drop": cdrop,
        "Server Drop": sdrop,
        "Client Delay": cdelay,
        "Server Delay": sdelay,
        "Client Delay Time": cdelay_time,
        "Server Delay Time": sdelay_time
    }
    print(tabulate(curr_setup.items(), headers=["Option", "Value"], tablefmt="pretty"))
