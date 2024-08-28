from typing import Literal
def setup(api_key: str, content_type: Literal["json", "xml", "octet-stream"] = None) -> dict:
    """Setup the header information of a http request

    Args:
        api_key (str): roblox api key

    Returns:
        dict: to be used in requests
    """
    if content_type:
        return {"x-api-key": api_key, "Content-Type": f"application/{content_type}"}
    return {"x-api-key": api_key}
