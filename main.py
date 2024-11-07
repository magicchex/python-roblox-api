import json
import time
import requests
from universe import Universe
from place import Place
import pyblox_config
import pyblox_header
import os
import click
import sys

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
            f"{pyblox_config.BASE_UNIVERSE}{universe_id}",
            headers=pyblox_header.setup(pyblox_config.API_KEY),
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
            f"{pyblox_config.BASE_UNIVERSE}{universe_id}/places/{place_id}",
            headers=pyblox_header.setup(pyblox_config.API_KEY),
        )
        if data.status_code == 200:
            return Place(json.loads(data.content))
        if data.status_code > 399:
            return
        time.sleep(wait_sec)

if __name__ == "__main__":
    print(sys.argv)
    
    """
    for universe_data in pyblox_config.UNIVERSE:
        universe = get_universe(universe_data["id"])
        if universe == None:
            continue
        # Universe scripting
        print("universe: " + universe._display_name)
        # End of Universe scripting
        places = []
        for place_id in universe_data["place"]:
            place = get_place(universe.get_id(), place_id)
            if place == None:
                continue
            # Add place scripting
            print("place: " + place.display_name)
            # End of place scripting
            places.append(place)
    """