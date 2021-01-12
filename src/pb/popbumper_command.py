import requests
from tabulate import tabulate
import json
import urllib.parse
from pprint import pprint
from pb.playfield_service import PlayfieldService
from pb.table import Table


class PopbumperCommand:

    def __init__(self, host):
        self.playfield = PlayfieldService(host)

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
        for name in PopbumperCommand.resource_names():
            mapping[name] = getattr(self, "pb_" + name)

        return mapping

    def pb_system(self, action, param, param_data):
        sys_check = SystemCheck()

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
        machine = Machine()

        if action == "read":

            if param == "all":

                all_machines = self.playfield.api_request("get", "machine", "all_machines", None)

                # Display output unless error
                if all_machines != "Error":
                    machine.display_machines(all_machines)
                else:
                    print("Error connecting to server")
            elif param == "by_id":
                if not isinstance(param_data, int):

                    machine_by_id = self.playfield.api_request("get", "machine", "machine_by_id", param_data)

                    # Display output unless error
                    if machine_by_id != "Error":
                        machine.display_machines(machine_by_id)
                    else:
                        print("Error connecting to server")
                else:
                    print("ID must be a valid integer")
            elif param == "by_name":
                if param_data != "":

                    machine_by_name = self.playfield.api_request("get", "machine", "machine_by_name", param_data)

                    # Display output unless error
                    if machine_by_name != "Error":
                        machine.display_machines(machine_by_name)
                    else:
                        print("Error connecting to server")
                else:
                    print("You must enter a name to search for")
            elif param == "by_abbr":
                if param_data != "":

                    machine_by_abbr = self.playfield.api_request("get", "machine", "machine_by_abbr", param_data)

                    # Display output unless error
                    if machine_by_abbr != "Error":
                        machine.display_machines(machine_by_abbr)
                    else:
                        print("Error connecting to server")
                else:
                    print("You must enter an abbr to search for")
            elif param == "by_manufacturer":
                if param_data != "":

                    machine_by_manufacturer = self.playfield.api_request("get", "machine", "machine_by_manufacturer", param_data)

                    # Display output unless error
                    if machine_by_manufacturer != "Error":
                        machine.display_machines(machine_by_manufacturer)
                    else:
                        print("Error connecting to server")
                else:
                    print("You must enter an manufacturer to search for")
            else:
                print("Invalid Operation")

    def pb_player(self, action, param, param_data):
        player = Player()

        if action == "read":

            if param == "all":

                all_players = self.playfield.api_request("get", "player", "all_players", None)

                if all_players != "Error":
                    player.display_players(all_players)
                else:
                    print("Error connecting to server")
            elif param == "by_id":
                if not isinstance(param_data, int):

                    player_by_id = self.playfield.api_request("get", "player", "player_by_id", param_data)

                    # Display output unless error
                    if player_by_id != "Error":
                        player.display_players(player_by_id)
                    else:
                        print("Error connecting to server")
                else:
                    print("ID must be a valid integer")
            elif param == "by_name":
                if param_data != "":

                    player_by_name = self.playfield.api_request("get", "player", "player_by_name", param_data)

                    # Display output unless error
                    if player_by_name != "Error":
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
        location = Location()

        if action == "read":

            if param == "all":

                all_locations = self.playfield.api_request("get", "location", "all_locations", None)

                if all_locations != "Error":
                    location.display_locations(all_locations)
                else:
                    print("Error connecting to server")
            elif param == "by_id":
                if not isinstance(param_data, int):

                    location_by_id = self.playfield.api_request("get", "location", "location_by_id", param_data)

                    # Display output unless error
                    if location_by_id != "Error":
                        location.display_locations(location_by_id)
                    else:
                        print("Error connecting to server")
                else:
                    print("ID must be a valid integer")
            elif param == "by_name":
                if param_data != "":

                    location_by_name = self.playfield.api_request("get", "location", "location_by_name", param_data)

                    # Display output unless error
                    if location_by_name != "Error":
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


class Machine:
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

        if result != 200:
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

        if result != 200:
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
