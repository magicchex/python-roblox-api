import json
import time
import requests
import tkinter
from functools import partial
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

def loadUniverseUI(universe: Universe, places: list[Place]):
    print("You clicked load Universe UI!")
    print(universe)
    print(places)

def loadPlaceUI(place: Place):
    print("You clicked loadPlaceUI")
    print(place)

if __name__ == "__main__":
    window = tkinter.Tk()
    window.title("Pyblox Cloud")
    window.geometry("480x360")
    window.minsize(480,360)
    window_menu = tkinter.Menu(window)
    universe_menu = tkinter.Menu(window_menu)
    # Load Universes and Places into the menu bar
    for universe_data in pb_config.UNIVERSE:
        universe = get_universe(universe_data["id"], 3, 1/32)
        if universe is None:
            continue
        universe_options_menu = tkinter.Menu()
        counter = 1
        places = []
        for place_id in universe_data["place"]:
            place = get_place(universe.get_id(),place_id, 3, 1/32)
            if place is None:
                continue
            places.append(place)
            universe_options_menu.add_command(label=f"Place {counter}: {place.display_name}", command=partial(loadPlaceUI,place))
            counter += 1
        universe_options_menu.add_separator()
        universe_options_menu.add_command(label=f'Edit "{universe._display_name}"?', command=partial(loadUniverseUI,universe, places))
        universe_menu.add_cascade(label=universe._display_name, menu=universe_options_menu)
    
    window_menu.add_cascade(label="Universe",menu=universe_menu)
    window.config(menu=window_menu)
    window.mainloop()
