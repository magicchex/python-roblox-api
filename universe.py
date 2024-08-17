from typing import TypedDict, Literal
import json
import requests
import pyblox_header


class SocialLink(TypedDict):
    """A class used for social media

    title: title of the link
    uri: uri of the social link
    """

    title: str
    uri: str


class UniverseType(TypedDict):
    """Last updated on August 8th, 2024\n
    Universe is a JSON object (dictionary) obtained through the base url of Roblox API
    """

    path: str
    createTime: str
    updateTime: str
    displayName: str
    description: str
    user: str
    group: str
    visibility: str
    facebookSocialLink: SocialLink
    twitterSocialLink: SocialLink
    youtubeSocialLink: SocialLink
    twitchSocialLink: SocialLink
    discordSocialLink: SocialLink
    robloxGroupSocialLink: SocialLink
    guildedSocialLink: SocialLink
    voiceChatEnabled: bool
    ageRating: str
    privateServerPriceRobux: int
    desktopEnabled: bool
    mobileEnabled: bool
    tabletEnabled: bool
    consoleEnabled: bool
    vrEnabled: bool


class Universe:
    """Universe (also named Experience for front-end users) is a JSON object
    (dictionary) obtained through the base url of Roblox API

    You will need to create a instance of this class to use its methods.
    """

    def __init__(self, data: UniverseType) -> None:
        self.path = data["path"]
        self._create_time = data["createTime"]
        self._update_time = data["updateTime"]
        self._display_name = data["displayName"]
        self._description = data["description"]
        try:
            self._user = data["user"]
            self.__OWNER = "user"
            self._group = None
        except KeyError:
            self._group = data["group"]
            self.__OWNER = "group"
            self._user = None
        self._visibility = data["visibility"]
        try:
            self.facebook_social_link = data["facebookSocialLink"]
        except KeyError:
            self.facebook_social_link = {"title": None, "uri": None}
        try:
            self.twitter_social_link = data["twitterSocialLink"]
        except KeyError:
            self.twitter_social_link = {"title": None, "uri": None}
        try:
            self.youtube_social_link = data["youtubeSocialLink"]
        except KeyError:
            self.youtube_social_link = {"title": None, "uri": None}
        try:
            self.guilded_social_link = data["guildedSocialLink"]
        except KeyError:
            self.guilded_social_link = {"title": None, "uri": None}
        self.voice_chat_enabled = data["voiceChatEnabled"]
        self._age_rating = data["ageRating"]
        try:
            self.private_server_price_robux = data["privateServerPriceRobux"]
        except KeyError:
            self.private_server_price_robux = False
        self.desktop_enabled = data["desktopEnabled"]
        self.mobile_enabled = data["mobileEnabled"]
        self.tablet_enabled = data["tabletEnabled"]
        self.console_enabled = data["consoleEnabled"]
        self.vr_enabled = data["vrEnabled"]

    def get_id(self) -> str:
        """Gets Universe ID

        Returns:
            int: universe id
        """
        return int(self.path.split("/")[-1])

    def update_facebook(self, title: str, uri: str):
        """Update Facebook for the given universe
        Args:
            title (str): Title of your link that users will be seeing
            uri (str): Your FULL Facebook page link
        """
        self.facebook_social_link["title"] = title
        self.facebook_social_link["uri"] = uri

    def update_twitter(self, title: str, uri: str):
        """Update Twitter for the given universe

        Args:
            title (str): Title of your link that users will be seeing
            uri (str): Your FULL Twitter page link
        """
        self.twitter_social_link["title"] = title
        self.twitter_social_link["uri"] = uri

    def update_x(self, title: str, uri: str):
        """Update X for the given universe

        Args:
            title (str): Title of your link that users will be seeing
            uri (str): your FULL X page link
        """
        self.update_twitter(title, uri)

    def update_youtube(self, title: str, uri: str):
        """Update Youtube for the given universe

        Args:
            title (str): Title of your link that users will be seeing
            uri (str): Your FULL Youtube page link
        """
        self.youtube_social_link["title"] = title
        self.youtube_social_link["uri"] = uri

    def update_guilded(self, title: str, uri: str):
        """Update Guilded for the given universe

        Args:
            title (str): Title of your link that users will be seeing
            uri (str): Your Guilded Invite Link
        """
        self.guilded_social_link["title"] = title
        self.guilded_social_link["uri"] = uri

    def update_private_server_pricing(self, price: int) -> Literal["Error"]:
        """Update the cost of robux to purchase a private server in your universe

        Args:
            price (int): robux as a integer which is positive
        Returns:
            Literal["Error"]: Receiving this means your universe does not support private servers. You may want to look into the settings.
        """
        if isinstance(self.private_server_price_robux, bool):
            return "Error"
        self.private_server_price_robux = abs(price)

    def set_private_server_pricing(self, price: int):
        """Set the cost of robux to purchase a private server in your universe

        Args:
            price (int): robux as a integer which is positive
        """
        self.update_private_server_pricing(price)

    def toggle_voice_chat(self) -> bool:
        """Whether to enable voice chat to players

        Returns:
            bool: voice chat enabled?
        """
        self.voice_chat_enabled = not self.voice_chat_enabled
        return self.voice_chat_enabled

    def toggle_desktop(self) -> bool:
        """Whether players can play on PC or laptop

        Returns:
            bool: desktop enabled?
        """
        self.desktop_enabled = not self.desktop_enabled
        return self.desktop_enabled

    def toggle_mobile(self) -> bool:
        """Whether players can play on phones

        Returns:
            bool: mobile enabled?
        """
        self.mobile_enabled = not self.mobile_enabled
        return self.mobile_enabled

    def toggle_phone(self) -> bool:
        """Whether players can play on phones

        Returns:
            bool: mobile enabled?
        """

    def toggle_tablet(self) -> bool:
        """Whether players can play on tablets or iPads

        Returns:
            bool: tablet enabled?
        """
        self.tablet_enabled = not self.tablet_enabled
        return self.tablet_enabled

    def toggle_console(self) -> bool:
        """Whether players can play on console

        Returns:
            bool: console enabled?
        """
        self.console_enabled = not self.console_enabled
        return self.console_enabled

    def toggle_vr(self) -> bool:
        """Whether players can play in VR

        Returns:
            bool: vr enabled?
        """
        self.vr_enabled = not self.vr_enabled
        return self.vr_enabled

    def to_dict(self) -> dict:
        """Converts to dictionary

        Returns:
            dict: Universe data
        """
        data = {
            "path": self.path,
            "createTime": self._create_time,
            "updateTime": self._update_time,
            "displayName": self._display_name,
            "description": self._description,
            "visibility": self._visibility,
            "voiceChatEnabled": self.voice_chat_enabled,
            "desktopEnabled": self.desktop_enabled,
            "mobileEnabled": self.mobile_enabled,
            "tabletEnabled": self.tablet_enabled,
            "consoleEnabled": self.console_enabled,
            "vrEnabled": self.vr_enabled,
        }
        if self.__OWNER == "user":
            data[self.__OWNER] = self._user
        else:
            data[self.__OWNER] = self._group
        if (
            self.facebook_social_link["title"] is not None
            or self.facebook_social_link["uri"] is not None
        ):
            data["facebookSocialLink"] = self.facebook_social_link
        if (
            self.twitter_social_link["title"] is not None
            or self.twitter_social_link["uri"] is not None
        ):
            data["twitterSocialLink"] = self.twitter_social_link
        if (
            self.youtube_social_link["title"] is not None
            or self.youtube_social_link["uri"] is not None
        ):
            data["youtubeSocialLink"] = self.youtube_social_link
        if (
            self.guilded_social_link["title"] is not None
            or self.guilded_social_link["uri"] is not None
        ):
            data["guildedSocialLink"] = self.guilded_social_link
        if not isinstance(self.private_server_price_robux, bool):
            data["privateServerPriceRobux"] = self.private_server_price_robux
        return data

    def to_dict_allowed(self):
        """Based on Roblox Universe API, it allows certain fields to be changed

        Returns:
            dict: allowed fields
        """
        data = self.to_dict()
        data.pop("path")
        data.pop("createTime")
        data.pop("updateTime")
        data.pop("displayName")
        data.pop("description")
        data.pop(self.__OWNER)
        data.pop("visibility")
        return data

    def push(
        self,
        api_key: str,
        url: str = "https://apis.roblox.com/cloud/v2/universes",
        update_only: list[
            Literal[
                "facebook.title",
                "facebook.uri",
                "twitter.title",
                "twitter.uri",
                "youtube.title",
                "youtube.uri",
                "guilded.title",
                "guilded.uri",
                "voicechat.enabled",
                "desktop.enabled",
                "mobile.enabled",
                "tablet.enabled",
                "console.enabled",
                "vr.enabled",
                "private.server",
            ]
        ] = None,
    ) -> requests.Response:
        """Pushes universe info to production

        Args:
            url (str): Roblox Universe API with no ending '/'. Defaults to "https://apis.roblox.com/cloud/v2/universes"
            api_key (str): your API Key for Roblox
            update_only (list[Literal[]], optional): Update specified fields. Defaults to None.

        Returns:
            requests.Response: http response
        """
        format_url = f"{url}/{self.get_id()}"
        field_mask = ""
        if not update_only is None:
            for item in update_only:
                if item == "facebook.title":
                    field_mask += "facebookSocialLink.title, "
                if item == "facebook.uri":
                    field_mask += "facebookSocialLink.uri, "
                if item == "twitter.title":
                    field_mask += "twitterSocialLink.title, "
                if item == "twitter.uri":
                    field_mask += "twitterSocialLink.uri, "
                if item == "youtube.title":
                    field_mask += "youtubeSocialLink.title, "
                if item == "youtube.uri":
                    field_mask += "youtubeSocialLink.uri, "
                if item == "guilded.title":
                    field_mask += "guildedSocialLink.title, "
                if item == "guilded.uri":
                    field_mask += "guildedSocialLink.uri, "
                if item == "voicechat.enabled":
                    field_mask += "voiceChatEnabled, "
                if item == "desktop.enabled":
                    field_mask += "desktopEnabled, "
                if item == "mobile.enabled":
                    field_mask += "mobileEnabled, "
                if item == "tablet.enabled":
                    field_mask += "tabletEnabled, "
                if item == "console.enabled":
                    field_mask += "consoleEnabled, "
                if item == "vr.enabled":
                    field_mask += "vrEnabled, "
                if item == "private.server":
                    field_mask += "privateServerPriceRobux, "
            format_url += r"?updateMask={" + field_mask + r"}"
        data = requests.patch(
            format_url,
            headers=pyblox_header.setup(api_key, True),
            data=json.dumps(self.to_dict_allowed()),
        )
        return data

    def restart(
        self, api_key: str, url: str = "https://apis.roblox.com/cloud/v2/universes"
    ) -> requests.Response:
        """Restarts the Roblox Servers of the Universe

        Args:
            api_key (str): Your roblox API key
            url (str, optional): Roblox universe API with no ending '/'. Defaults to "https://apis.roblox.com/cloud/v2/universes".
        Returns:
            Response: http response
        """
        return requests.post(
            f"{url}/{self.get_id()}:restartServers",
            headers=pyblox_header.setup(api_key, True),
            data=json.dumps({}),
        )
