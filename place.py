from typing import TypedDict, Literal
import pyblox_header
import json
import requests
import os

class PlaceType(TypedDict):
    path: str
    createTime: str
    updateTime: str
    displayName: str
    description: str
    serverSize: int

class Place():
    def __init__(self, data: PlaceType) -> None:
        self.path = data['path']
        self._create_time = data['createTime']
        self._update_time = data['updateTime']
        self.display_name = data['displayName']
        self.description = data['description']
        self.serverSize = data['serverSize']
    def get_id(self):
        return int(self.path.split("/")[-1])
    def update_display_name(self, text: str):
        self.display_name = text
    def set_display_name(self, text: str):
        self.update_display_name(text)
    def update_description(self, text: str):
        self.description = text
    def set_description(self, text: str):
        self.update_description(text)
    def update_server_size(self, size: int):
        self.serverSize = abs(size)
    def set_server_size(self, size: int):
        self.update_server_size(size)
    def to_dict(self):
        return {
            "path": self.path,
            "createTime": self._create_time,
            "updateTime": self._update_time,
            "displayName": self.display_name,
            "description": self.description,
            "serverSize": self.serverSize
        }
    def to_dict_allowed(self):
        data = self.to_dict()
        data.pop("path")
        data.pop("createTime")
        data.pop("updateTime")
        return data
    def push_settings(self, api_key: str, universe_id: int, url: str = "https://apis.roblox.com/cloud/v2/universes", updateOnly: list[Literal["display.name", "description", "server.size"]] | None = None) -> requests.Response:
        """Updates the settings of a place

        Args:
            api_key (str): your roblox api key for the "universe" api system
            universe_id (int): your experience id
            url (str, optional): If this is broken, you can replace the url in the meantime. Defaults to "https://apis.roblox.com/cloud/v2/universes".
            updateOnly (list[Literal["display.name", "description", "server.size"]] | None, optional): Updates particular parameters. Defaults to None.

        Returns:
            requests.Response: the response from requests.patch(). Is most likely a dictionary.
        """
        url += f"/{universe_id}/places/{self.get_id()}"
        filter_mask = ""
        if updateOnly is not None:
            for i in updateOnly:
                if i == "display.name":
                    filter_mask += "displayName, "
                if i == "description":
                    filter_mask += "description, "
                if i == "server.size":
                    filter_mask += "serverSize, "
            url += r"?updateMask={" + filter_mask + r"}"
        data = requests.patch(url, headers=pyblox_header.setup(api_key, "json"), data=json.dumps(self.to_dict_allowed()))
        return data
    def push_place(self, api_key: str, universe_id: int, roblox_place_file: str, mode: Literal["Published", "Saved"], url: str = "https://apis.roblox.com/universes/v1") -> requests.Response:
        """Updates the place with your specified "file.rbxlx" or "file.rbxl"

        Args:
            api_key (str): your api key for the "universe-places" api system
            universe_id (int): your experience id
            roblox_place_file (str): the path to your file
            mode ("Published", "Saved"): "Published" means pushing your place to production whereas "Saved" uploads your place as a version.
            url (str, optional): If broken, you can replace the url in the meantime. Defaults to "https://apis.roblox.com/universes/v1".

        Returns:
            requests.Response: the response from requests.post(). Is most likely a dictionary
        """
        url += f"/{universe_id}/places/{self.get_id()}/version?versionType={mode}"
        file = open(roblox_place_file, "rb")
        if roblox_place_file.endswith(".rbxlx"):
            data = requests.post(url, headers=pyblox_header.setup(api_key, "xml"), data=file.read())
        if roblox_place_file.endswith(".rbxl"):
            data = requests.post(url, headers=pyblox_header.setup(api_key, "octet-stream"), data=file.read())
        file.close()
        return data