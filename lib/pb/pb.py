import requests
from tabulate import tabulate
import json
import urllib.parse
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

    def pb_system(self, action, param, param_data):
        sys_check = SystemCheck(self.host)

        info = sys_check.get_info()
        print(action)
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

    def pb_machine(self, action, param, param_data):
        machine = Machine(self.host)

        if action == "read":

            if param == "all":

                all_machines = self.api_request(self.host, "get", "machine", "all_machines", None)

                # Display output unless error
                if all_machines is not "Error":
                    machine.display_machines(all_machines)
                else:
                    print("Error connecting to server")
            elif param == "by_id":
                if not isinstance(param_data, int):

                    machine_by_id = self.api_request(self.host, "get", "machine", "machine_by_id", param_data)

                    # Display output unless error
                    if machine_by_id is not "Error":
                        machine.display_machines(machine_by_id)
                    else:
                        print("Error connecting to server")
                else:
                    print("ID must be a valid integer")
            elif param == "by_name":
                if param_data != "":

                    machine_by_name = self.api_request(self.host, "get", "machine", "machine_by_name", param_data)

                    # Display output unless error
                    if machine_by_name is not "Error":
                        machine.display_machines(machine_by_name)
                    else:
                        print("Error connecting to server")
                else:
                    print("You must enter a name to search for")
            elif param == "by_abbr":
                if param_data != "":

                    machine_by_abbr = self.api_request(self.host, "get", "machine", "machine_by_abbr", param_data)

                    # Display output unless error
                    if machine_by_abbr is not "Error":
                        machine.display_machines(machine_by_abbr)
                    else:
                        print("Error connecting to server")
                else:
                    print("You must enter an abbr to search for")
            elif param == "by_manufacturer":
                if param_data != "":

                    machine_by_manufacturer = self.api_request(self.host, "get", "machine", "machine_by_manufacturer", param_data)

                    # Display output unless error
                    if machine_by_manufacturer is not "Error":
                        machine.display_machines(machine_by_manufacturer)
                    else:
                        print("Error connecting to server")
                else:
                    print("You must enter an manufacturer to search for")
            else:
                print("Invalid Operation")

    def pb_player(self, action, param, param_data):
        player = Player(self.host)

        if action == "read":

            if param == "all":

                all_players = self.api_request(self.host, "get", "player", "all_players", None)

                if all_players is not "Error":
                    player.display_players(all_players)
                else:
                    print("Error connecting to server")
            elif param == "by_id":
                if not isinstance(param_data, int):

                    player_by_id = self.api_request(self.host, "get", "player", "player_by_id", param_data)

                    # Display output unless error
                    if player_by_id is not "Error":
                        player.display_players(player_by_id)
                    else:
                        print("Error connecting to server")
                else:
                    print("ID must be a valid integer")
            elif param == "by_name":
                if param_data != "":

                    player_by_name = self.api_request(self.host, "get", "player", "player_by_name", param_data)

                    # Display output unless error
                    if player_by_name is not "Error":
                        player.display_players(player_by_name)
                    else:
                        print("Error connecting to server")
                else:
                    print("You must enter a name to search for")
            else:
                print("Invalid Operation")
        elif action == "create":
            print("Creating New Player...")

            player.create_new_player()

    def pb_location(self, action, param, param_data):
        location = Location(self.host)

        if action == "read":

            if param == "all":

                all_locations = self.api_request(self.host, "get", "location", "all_locations", None)

                if all_locations is not "Error":
                    location.display_locations(all_locations)
                else:
                    print("Error connecting to server")
            elif param == "by_id":
                if not isinstance(param_data, int):

                    location_by_id = self.api_request(self.host, "get", "location", "location_by_id", param_data)

                    # Display output unless error
                    if location_by_id is not "Error":
                        location.display_locations(location_by_id)
                    else:
                        print("Error connecting to server")
                else:
                    print("ID must be a valid integer")
            elif param == "by_name":
                if param_data != "":

                    location_by_name = self.api_request(self.host, "get", "location", "location_by_name", param_data)

                    # Display output unless error
                    if location_by_name is not "Error":
                        location.display_locations(location_by_name)
                    else:
                        print("Error connecting to server")
                else:
                    print("You must enter a name to search for")
            else:
                print("Invalid Operation")

        elif action == "create":
            print("Creating New Location...")

            location.create_new_location()

    @staticmethod
    def api_request(host, method, resource, function, data):

        if method.lower() == "get" and data is not None:
            url = f'http://{host}/api/v1/resources/{resource}/{function}/{urllib.parse.quote(data)}'
        else:
            url = f'http://{host}/api/v1/resources/{resource}/{function}'

        try:
            if method.lower() == "get":
                response = requests.get(url)
            elif method.lower() == "post":
                response = requests.post(url, data)
        except requests.ConnectionError as e:
            return "Error"

        if response.status_code == 200:
            return response.json()
        else:
            return None


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

    def create_new_player(self):
        (nick, name, email, phone, location, ifpanumber, pinside, notes, status, active, currentrank, currentwpprvalue,
         bestfinish, activeevents) = self._prompt_for_new_player()

        result = self._add_player_to_database(nick, name, email, phone, location, ifpanumber, pinside, notes, status,
                                              active, currentrank, currentwpprvalue, bestfinish, activeevents)

        if result is not 200:
            print("Error connecting to API")
        else:
            print("Player added successfully!")

    @staticmethod
    def _prompt_for_new_player():
        name = input("Name of player: ")
        nick = input("Nickname: ")
        email = input("Email address: ")
        phone = input("Phone number: ")
        location = input("Location: ")
        ifpanumber = ''
        pinside = ''
        notes = input("Notes: ")
        status = 0
        while True:
            active = input("Active? (yes/no) ").lower()
            if active == "yes" or active == "no":
                break
        currentrank = 0
        currentwpprvalue = 0.0
        bestfinish = 0
        activeevents = 0

        print("\n\n")
        print("A player is to be created with the following details:")
        print("Name: {}".format(name))
        print("Nickname: {}".format(nick))
        print("Email: {}".format(email))
        print("Phone: {}".format(phone))
        print("Location: {}".format(location))
        print("Notes: {}".format(notes))
        print("Active? {}".format(active))

        while True:
            verify_create = input("Should this location be created? (yes/no) ").lower()
            if verify_create == "yes" or verify_create == "no":
                break

        if verify_create == "yes":
            # Morph some user input values into DB values
            if active == "yes":
                active = True
            else:
                active = False

            return nick, name, email, phone, location, ifpanumber, pinside, notes, status, active, currentrank, currentwpprvalue, bestfinish, activeevents
        else:
            exit(0)

    def _add_player_to_database(self, nick, name, email, phone, location, ifpanumber, pinside, notes, status, active,
                                currentrank, currentwpprvalue, bestfinish, activeevents):
        print("Adding to database...")

        url = f'http://{self.host}/api/v1/resources/player/add_player'
        data = dict(name=name,
                    nick=nick,
                    email=email,
                    phone=phone,
                    location=location,
                    ifpanumber=ifpanumber,
                    pinside=pinside,
                    notes=notes,
                    status=status,
                    active=active,
                    currentrank=currentrank,
                    currentwpprvalue=currentwpprvalue,
                    bestfinish=bestfinish,
                    activeevents=activeevents)

        try:
            response = requests.post(url, data)
        except requests.ConnectionError as e:
            return "Error"

        return response.status_code


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

    def create_new_location(self):
        (name, address, address_private, notes, loc_type, active) = self._prompt_for_new_location()

        result = self._add_to_database(name, address, address_private, notes, loc_type, active)

        if result is not 200:
            print("Error connecting to API")
        else:
            print("Location added successfully!")

    @staticmethod
    def _prompt_for_new_location():
        name = input("Name of location: ")
        address = input("Address: ")
        while True:
            address_private = input("Is the address private? (yes/no) ").lower()
            if address_private == "yes" or address_private == "no":
                break
        notes = input("Notes or special considerations: ")
        while True:
            loc_type = input("Location Type? (business or residence) ").lower()
            if loc_type == "business" or loc_type == "residence":
                break
        while True:
            active = input("Make active? (yes/no) ").lower()
            if active == "yes" or active == "no":
                break

        print("\n\n")
        print("A location is to be created with the following details:")
        print("Name: {}".format(name))
        print("Address: {}".format(address))
        print("Address kept private? {}".format(address_private))
        print("Notes: {}".format(notes))
        print("Location Type: {}".format(loc_type))
        print("Location active? {}".format(active))

        while True:
            verify_create = input("Should this location be created? (yes/no) ").lower()
            if verify_create == "yes" or verify_create == "no":
                break

        if verify_create == "yes":
            # Morph some user input values into DB values
            if address_private == "yes":
                address_private = True
            else:
                address_private = False
            if loc_type == "business":
                loc_type = 1
            else:
                loc_type = 2
            if active == "yes":
                active = True
            else:
                active = False

            return name, address, address_private, notes, loc_type, active
        else:
            exit(0)

    def _add_to_database(self, name, address, address_private, notes, loc_type, active):
        print("Adding to database...")

        url = f'http://{self.host}/api/v1/resources/location/add_location'
        data = dict(name=name,
                    address=address,
                    address_private=address_private,
                    notes=notes,
                    locType=loc_type,
                    active=active)

        try:
            response = requests.post(url, data)
        except requests.ConnectionError as e:
            return "Error"

        return response.status_code


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
