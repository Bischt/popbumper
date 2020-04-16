import requests
from tabulate import tabulate
import json
from pprint import pprint


class PlayfieldService:

    def __init__(self, host):
        self.host = host

    @staticmethod
    def action_names():
        return {"create", "read", "update", "delete"}

    @staticmethod
    def resource_names():
        return {"system", "machine", "player", "location"}

    def playfield_operations(self):
        """
        Returns a dictionary mapping action name strings to functions.

        :returns: a function implementing a CLI action
        :rtype: Function
        """
        mapping = {}
        for name in PlayfieldService.resource_names():
            mapping[name] = getattr(self, "pb_" + name)

        return mapping

    def pb_system(self, action):
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

    def pb_machine(self, action):
        machine = Machine(self.host)

        all_machines = machine.get_all_machines()

        # Display output unless error
        if all_machines is not "Error":
            machine.display_machines(all_machines)
        else:
            print("Error connecting to server")

    def pb_player(self, action):
        player = Player(self.host)

        all_players = player.get_all_players()

        if all_players is not "Error":
            player.display_players(all_players)
        else:
            print("Error connecting to server")

    def pb_location(self, action):
        location = Location(self.host)

        all_locations = location.get_all_locations()

        if all_locations is not "Error":
            location.display_locations(all_locations)
        else:
            print("Error connecting to server")


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

    @staticmethod
    def display_players(player_data):
        headers = [
            "player_id",
            "nick",
            "name",
            "email",
            "phone",
            "location",
            "ifpanumber",
            "pinside",
            "notes",
            "status",
            "active"
        ]
        rows = []

        player_json = json.loads(player_data)

        for player in player_json['data']:
            rows.append(
                [
                    player['player_id'],
                    player['nick'],
                    player['name'],
                    player['email'],
                    player['phone'],
                    player['location'],
                    player['ifpanumber'],
                    player['pinside'],
                    player['notes'],
                    player['status'],
                    player['active']
                ]
            )

        table = Table(headers, rows)
        table.display()

    def get_all_players(self):

        url = f'http://{self.host}/api/v1/resources/player/all_players'

        try:
            response = requests.get(url)
        except requests.ConnectionError as e:
            return "Error"

        if response.status_code == 200:
            return response.json()
        else:
            return None


class Location:
    def __init__(self, host):
        self.host = host

    @staticmethod
    def display_locations(location_data):
        headers = [
            "location_id",
            "name",
            "address",
            "addressPrivate",
            "notes",
            "locType",
            "active"
        ]
        rows = []

        location_json = json.loads(location_data)

        for location in location_json['data']:
            rows.append(
                [
                    location['location_id'],
                    location['name'],
                    location['address'],
                    location['addressPrivate'],
                    location['notes'],
                    location['locType'],
                    location['active']
                ]
            )

        table = Table(headers, rows)
        table.display()

    def get_all_locations(self):

        url = f'http://{self.host}/api/v1/resources/location/all_locations'

        try:
            response = requests.get(url)
        except requests.ConnectionError as e:
            return "Error"

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
