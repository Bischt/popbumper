import requests
from tabulate import tabulate
import json
from pprint import pprint


class PlayfieldService:

    def __init__(self, host):
        self.host = host

    @staticmethod
    def action_names():
        return {"system", "machine", "player"}

    def playfield_actions(self):
        """
        Returns a dictionary mapping action name strings to functions.

        :returns: a function implementing a CLI action
        :rtype: Function
        """
        mapping = {}
        for name in PlayfieldService.action_names():
            mapping[name] = getattr(self, "pb_" + name)

        return mapping

    def pb_system(self):
        sys_check = SystemCheck(self.host)

        info = sys_check.get_info()

        headers = [
            "Host",
            "Version",
            "Live",
            "Ready",
        ]
        rows = []

        if info != "Error":
            rows.append(
                [
                    self.host,
                    info[0]['api_version'],
                    info[0]['live'],
                    info[0]['ready']
                ]
            )
            table = Table(headers, rows)
            table.display()
        else:
            # System not available, so it's unhealthy
            rows.append(
                [
                    self.host,
                    "ERROR",
                    "NOT OK",
                    "NOT OK"
                ]
            )
            table = Table(headers, rows)
            table.display()
            print("Error connecting to server")

    def pb_machine(self):
        machine = Machine(self.host)

        all_machines = machine.get_all_machines()

        # Display output unless error
        if all_machines is not "Error":
            machine.display_machines(all_machines)
        else:
            print("Error connecting to server")

    def pb_player(self):
        player = Player(self.host)

        all_players = player.get_all_players()


class Machine:
    def __init__(self, host):
        self.host = host

    @staticmethod
    def display_machines(machine_data):
        headers = [
            "id",
            "name",
            "abbr",
            "manufacturer",
        ]
        rows = []

        machine_json = json.loads(machine_data)

        for machine in machine_json['data']:
            rows.append(
                [
                    machine['machine_id'],
                    machine['name'],
                    machine['abbr'],
                    machine['manufacturer']
                ]
            )

        table = Table(headers, rows)
        table.display()

    def get_all_machines(self):
        """
        Retrieve all machines currently in the system
        :return:
        """
        url = f'http://{self.host}/api/v1/resources/machine/all_machines'

        try:
            response = requests.get(url)
        except requests.ConnectionError as e:
            return "Error"

        if response.status_code == 200:
            return response.json()
        else:
            return None


class Player:
    def __init__(self, host):
        self.host = host

    def get_all_players(self):

        url = f'http://{self.host}/api/v1/resources/player/all_players'

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None


class Location:
    def __init__(self, host):
        self.host = host

    def get_all_locations(self):

        url = f'http://{self.host}/api/v1/resources/location/all_locations'

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None


class SystemCheck:
    def __init__(self, host):
        self.host = host

    def get_info(self):
        info_url = f"http://{self.host}/"

        try:
            info_response = requests.get(info_url)
        except requests.ConnectionError as e:
            return "Error"

        if info_response.status_code == 200:
            return info_response.json()
        else:
            return info_response.status_code

    def get_version(self):

        version_url = f"http://{self.host}/version"

        try:
            version_response = requests.get(version_url)
        except requests.ConnectionError as e:
            return "Error"

        if version_response.status_code == 200:
            return version_response.json()
        else:
            return "Unknown"

    def get_ready_check(self):

        ready_url = f'http://{self.host}/ready'

        try:
            ready_response = requests.get(ready_url)
        except requests.ConnectionError as e:
            return "Error"

        if ready_response.status_code == 200:
            # TODO: Actually parse response to ensure true
            return "OK"
        else:
            return "NOT OK"

    def get_live_check(self):
        live_url = f'http://{self.host}/live'

        try:
            live_response = requests.get(live_url)
        except requests.ConnectionError as e:
            return "Error"

        if live_response.status_code == 200:
            # TODO: Actually parse response to ensure true
            return "OK"
        else:
            return "NOT OK"


class Table:
    def __init__(self, headers, data):
        self.headers = headers
        self.data = data

    def display(self, fmt=None):
        """
        Display data in tabular format with headers using tabulate
        :param fmt:
        :return:
        """
        print(tabulate(self.data, headers=self.headers, tablefmt="plain"))
