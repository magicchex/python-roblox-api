from typing import TypedDict
import requests
import pyblox_header
import json

class Page_Token(TypedDict):
    page_token: str
class GroupType(TypedDict):
    path: str
    createTime: str
    updateTime: str
    id: str
    displayName: str
    description: str
    owner: str | None
    memberCount: int
    publicEntryAllowed: bool
    locked: bool
    verified: bool

class Group:
    def __init__(self, data: GroupType) -> None:
        self._path = data.get("path", None)
        self._create_time = data.get("createTime", None)
        self._update_time = data.get("updateTime", None)
        self._id = data.get("id", None)
        self._owner = data.get("owner", None)
        self._member_count = data.get("memberCount", 0)
        self._locked = data.get("locked", None)
        self._verified = data.get("verified", None)
        self.display_name = data.get("displayName")
        self.description = data.get("description")
        self.public_entry_allowed = data.get("publicEntryAllowed")

    def get_id(self):
        return int(self._path.split("/")[-1])
    
    def list_join_requests(self, api_key: str, filter: str = None, page_token: str = None, max_page_size: int = 10, url = "https://apis.roblox.com/cloud/v2/groups/") -> requests.Response:
        """Get the group current join requests

        Args:
            api_key (str): your api key with the "group:read" permission
            filter (str, optional): Example: "player_name == "users/player_id". Defaults to None.
            page_token (str, optional): recursive, page token is the nth set of max_page_size. Defaults to None.
            max_page_size (int, optional): 1 to 20. Defaults to 10.
            url (str, optional): change the url manually if it stops working. Defaults to "https://apis.roblox.com/cloud/v2/groups/".

        Returns:
            dict: Response data as a dictionary
        """
        if url is None:
            url = f"https://apis.roblox.com/cloud/v2/groups/{self.get_id()}/join-requests?maxPageSize={max_page_size}"
        else:
            url += f"{self.get_id()}/join-requests?maxPageSize={max_page_size}"
        if page_token is not None:
            url += f"&{page_token}"
        if filter is not None:
            url += f"&{filter}"
        data = requests.get(url, headers=pyblox_header.setup(api_key))
        data_dict = json.dumps(data.content)
        """
        {
            "groupJoinRequests": [
                {
                    "path": "groups/group_id/join-requests/join_request_id",
                    "createTime": "time"
                    "user": "users/player_id"
                }
            ],
            "nextPageToken": "string"
        }
        """
        return data_dict
    def accept_join_request(self, api_key: str, join_request_id: str, url="https://apis.roblox.com/cloud/v2/groups/"):
        url += f"{self.get_id()}"
    