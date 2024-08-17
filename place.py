from typing import TypedDict, Literal
import pyblox_header
import json
import requests

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
    def push(self, api_key: str, universe_id: int, url: str = "https://apis.roblox.com/cloud/v2/universes", updateOnly: list[Literal["display.name", "description", "server.size"]] | None = None):
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
        data = requests.patch(url, headers=pyblox_header.setup(api_key, True), data=json.dumps(self.to_dict_allowed()))
        return data