from main import *

if __name__ == "__main__":
    for universe_data in pyblox_config.UNIVERSE:
        universe = get_universe(universe_data["id"])
        if universe == None:
            continue
        places = []
        for place_id in universe_data["place"]:
            place = get_place(universe.get_id(), place_id)
            if place == None:
                continue
            for entry in os.listdir(os.path.join(".","places")):
                if os.path.isdir(entry):
                    continue
                if entry.find(place.display_name) > -1:
                    os.chdir(os.path.join(".","places"))
                    response = place.push_place(pyblox_config.API_KEY, universe.get_id(), entry, "Published")
                    print(response)
                    if response.status_code == 200:
                        print(f"Successfully uploaded '{entry}' to '{place.display_name}' ({place.get_id()})")
                    else:
                        print(f"Failed to upload '{entry}' to '{place.display_name}' ({place.get_id()})")
            places.append(place)