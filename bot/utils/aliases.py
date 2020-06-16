import json
import os
import re

DEFAULT_FORMAT = {"maps": {}, "players": {}, "teams": {}}
MAP_NAME_REGEX = r"UGC[0-9]*"


def check_map_already_label(name):
    if re.match(MAP_NAME_REGEX, name):
        return True
    return False


def check_player_already_int(name):
    try:
        int(name)
        return True
    except ValueError:
        return False


class AliasNotFoundError(Exception):
    def __init__(self, alias_type: str, alias: str):
        self.alias_type = alias_type
        self.alias = alias


class Aliases:
    def __init__(self, filename="aliases.json"):
        self._filename = filename
        self._aliases = {}
        self.AliasNotFoundError = AliasNotFoundError
        if not os.path.isfile(filename):
            with open(filename, "w") as file:
                json.dump(DEFAULT_FORMAT, file)
        with open(filename) as file:
            data = json.load(file)
            self._aliases = data

    def get(self, alias_type: str, name: str):
        data = self._aliases.get(alias_type, {})
        alias = data.get(name)
        if alias is None:
            for key in data.keys():
                if key.lower() == name.lower():
                    alias = data.get(key)
                    break
            else:
                raise AliasNotFoundError(alias_type, name)
        return alias

    def get_map(self, name: str):
        if check_map_already_label(name):
            return name
        return self.get("maps", name)

    def get_player(self, name: str):
        if check_player_already_int(name):
            return name
        return self.get("players", name)

    def get_team(self, name: str):
        return self.get("teams", name)

    def find_alias(self, alias_type: str, search: str):
        data = self._aliases.get(alias_type, {})
        for alias, label in data.items():
            if str(label) == search:
                return alias

    def find_map_alias(self, map_label: str):
        return self.find_alias("maps", map_label)

    def find_player_alias(self, unique_id: str):
        return self.find_alias("players", unique_id)

    def get_maps(self):
        return self._aliases.get("maps", {})

    def get_players(self):
        return self._aliases.get("players", {})

    def get_teams(self):
        return self._aliases.get("teams", {})