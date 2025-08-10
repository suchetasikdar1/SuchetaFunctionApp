import azure.functions as func
import logging
import os
import urllib.parse

animal_to_park = {
    "caribou": "Akami-Uapishkᵁ-KakKasuak-Mealy Mountains National Park",
    "black bear": "Bruce Peninsula National Park",
    "arctic fox": "Auyuittuq National Park",
    "muskox": "Aulavik National Park",
    "arctic hare": "Qausuittuq National Park",
    "snowy owl": "Vuntut National Park",
    "polar bear": "Wapusk National Park",
    "seal": "Auyuittuq National Park",
    "elk": "Banff National Park",
    "grizzly bear": "Banff National Park",
    "mountain goat": "Banff National Park",
    "wolf": "Banff National Park",
    "massasauga rattlesnake": "Bruce Peninsula National Park",
    "deer": "Bruce Peninsula National Park",
    "moose": "Cape Breton Highlands National Park",
    "bobcat": "Cape Breton Highlands National Park",
    "coyote": "Cape Breton Highlands National Park",
    "plains bison": "Elk Island National Park",
    "beaver": "Elk Island National Park",
    "red fox": "Forillon National Park",
    "whale": "Forillon National Park",
    "peregrine falcon": "Fundy National Park",
    "osprey": "Georgian Bay Islands National Park",
    "white-tailed deer": "Georgian Bay Islands National Park",
    "wolverine": "Glacier National Park",
    "lynx": "Glacier National Park",
    "prairie dog": "Grasslands National Park",
    "swift fox": "Grasslands National Park",
    "sea lion": "Gulf Islands National Park Reserve",
    "bald eagle": "Gulf Islands National Park Reserve",
    "orca": "Gulf Islands National Park Reserve",
    "humpback whale": "Gwaii Haanas National Park Reserve",
    "dall sheep": "Kluane National Park and Reserve",
    "golden eagle": "Kluane National Park and Reserve",
    "grey seal": "Kouchibouguac National Park",
    "loon": "La Mauricie National Park",
    "puffin": "Mingan Archipelago National Park Reserve",
    "seabirds": "Mingan Archipelago National Park Reserve",
    "marmot": "Mount Revelstoke National Park",
    "river otter": "Kejimkujik National Park",
    "barred owl": "Kejimkujik National Park",
    "snapping turtle": "Rouge Urban National Park",
    "sea otter": "Pacific Rim National Park Reserve",
    "grey whale": "Pacific Rim National Park Reserve",
    "monarch butterfly": "Point Pelee National Park",
    "raccoon": "Point Pelee National Park",
    "cormorant": "Prince Edward Island National Park",
    "narwhal": "Sirmilik National Park",
    "beluga whale": "Sirmilik National Park",
    "porcupine caribou": "Vuntut National Park",
    "cougar": "Waterton Lakes National Park",
    "whooping crane": "Wood Buffalo National Park",
    "wild horses": "Sable Island National Park Reserve",
    "arctic wolf": "Torngat Mountains National Park",
    "falcon": "Tuktut Nogait National Park"
}

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing request for Canadian animal to national park.")

    if req.method == "GET":
        html_path = os.path.join(os.path.dirname(__file__), "index.html")
        try:
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            return func.HttpResponse(html_content, mimetype="text/html")
        except Exception as e:
            logging.error(f"Error reading HTML file: {e}")
            return func.HttpResponse("Error loading page", status_code=500)

    elif req.method == "POST":
        try:
            content_type = req.headers.get("Content-Type", "")
            if "application/x-www-form-urlencoded" in content_type:
                body_bytes = req.get_body()
                parsed_body = urllib.parse.parse_qs(body_bytes.decode())
                animal = parsed_body.get("animal", [None])[0]
            else:
                return func.HttpResponse("Unsupported content type", status_code=415)
        except Exception as e:
            logging.error(f"Error parsing request: {e}")
            return func.HttpResponse("Invalid request format", status_code=400)

        logging.info(f"Received animal: {animal}")

        if animal:
            park = animal_to_park.get(animal.lower())
            if park:
                return func.HttpResponse(f"The {animal.title()} can be found in {park}.")
            else:
                return func.HttpResponse(f"Sorry, no data for '{animal}'.", status_code=404)
        else:
            return func.HttpResponse("Please select an animal.", status_code=400)
