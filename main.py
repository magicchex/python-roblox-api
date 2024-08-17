import json
import time
import requests
import tkinter
from universe import Universe
from place import Place
import pyblox_config as pb_config
import pyblox_header as pb_header


def get_universe(
    universe_id: int, do_try: int = 3, wait_sec: int = 2
) -> Universe | None:
    """Searches the id on the Roblox API

    Args:
        universe_id (int): your universe id
        do_try (int, optional): number of attempts if it fails. Defaults to 3.
        wait_sec (int, optional): the amount of time to pause between each request. Defaults to 2.

    Returns:
        Universe | None: _description_
    """
    for _ in range(do_try):
        data = requests.get(
            f"{pb_config.BASE_UNIVERSE}{universe_id}",
            headers=pb_header.setup(pb_config.API_KEY),
        )
        if data.status_code == 200:
            return Universe(json.loads(data.content))
        if data.status_code > 399:
            return
        time.sleep(wait_sec)

def get_place(
    universe_id: int, place_id: int, do_try: int = 3, wait_sec = 2
) -> Place | None:
    for _ in range(do_try):
        data = requests.get(
            f"{pb_config.BASE_UNIVERSE}{universe_id}/places/{place_id}",
            headers=pb_header.setup(pb_config.API_KEY),
        )
        if data.status_code == 200:
            return Place(json.loads(data.content))
        if data.status_code > 399:
            return
        time.sleep(wait_sec)

if __name__ == "__main__":
    for data in pb_config.UNIVERSE:
        universe = get_universe(data["id"])
        print(universe.vr_enabled)
        universe.toggle_vr()
        print(universe.push(pb_config.API_KEY))
        for place_id in data["place"]:
            place = get_place(universe.get_id(), place_id)
            print(place.display_name)
            print(place.set_description("test"))
            print(place.push(pb_config.API_KEY, universe.get_id()))
