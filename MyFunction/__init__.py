import azure.functions as func
import logging
import os
import urllib.parse
import json

animal_to_park = {
    "caribou": [
        "Akami-Uapishkᵁ-KakKasuak-Mealy Mountains National Park",
        "Gros Morne National Park",
        "Ivvavik National Park",
        "Jasper National Park",
        "Nááts’įhch’oh National Park",
        "Thaidene Nëné National Park",
        "Torngat Mountains National Park",
        "Tuktut Nogait National Park",
        "Ukkusiksalik National Park",
        "Wapusk National Park"
    ],
    "black bear": [
        "Akami-Uapishkᵁ-KakKasuak-Mealy Mountains National Park",
        "Bruce Peninsula National Park",
        "Forillon National Park",
        "Gros Morne National Park",
        "Jasper National Park",
        "Kootenay National Park",
        "La Mauricie National Park",
        "Mount Revelstoke National Park",
        "Pacific Rim National Park Reserve",
        "Prince Albert National Park",
        "Pukaskwa National Park",
        "Riding Mountain National Park",
        "Waterton Lakes National Park"
    ],
    "arctic fox": [
        "Akami-Uapishkᵁ-KakKasuak-Mealy Mountains National Park",
        "Auyuittuq National Park",
        "Ivvavik National Park",
        "Thaidene Nëné National Park",
        "Ukkusiksalik National Park",
        "Wapusk National Park"
    ],
    "muskox": [
        "Aulavik National Park",
        "Qausuittuq National Park",
        "Quttinirpaaq National Park"
    ],
    "arctic hare": [
        "Aulavik National Park",
        "Gros Morne National Park",
        "Qausuittuq National Park",
        "Quttinirpaaq National Park"
    ],
    "snowy owl": [
        "Aulavik National Park",
        "Kouchibouguac National Park",
        "Vuntut National Park"
    ],
    "polar bear": [
        "Auyuittuq National Park",
        "Qausuittuq National Park",
        "Quttinirpaaq National Park",
        "Sirmilik National Park",
        "Torngat Mountains National Park",
        "Ukkusiksalik National Park",
        "Wapusk National Park"
    ],
    "seal": [
        "Auyuittuq National Park",
        "Mingan Archipelago National Park Reserve",
        "Prince Edward Island National Park"
    ],
    "elk": [
        "Banff National Park",
        "Elk Island National Park",
        "Kootenay National Park",
        "Prince Albert National Park",
        "Riding Mountain National Park"
    ],
    "grizzly bear": [
        "Banff National Park",
        "Kluane National Park and Reserve",
        "Nahanni National Park",
        "Yoho National Park"
    ],
    "mountain goat": [
        "Banff National Park",
        "Glacier National Park",
        "Kootenay National Park",
        "Mount Revelstoke National Park",
        "Yoho National Park"
    ],
    "wolf": [
        "Banff National Park",
        "Thaidene Nëné National Park",
        "Vuntut National Park",
        "Wood Buffalo National Park"
    ],
    "massasauga rattlesnake": ["Bruce Peninsula National Park"],
    "deer": [
        "Bruce Peninsula National Park",
        "Rouge Urban National Park",
        "Waterton Lakes National Park"
    ],
    "moose": [
        "Cape Breton Highlands National Park",
        "Fundy National Park",
        "Jasper National Park",
        "La Mauricie National Park",
        "Nahanni National Park",
        "Pukaskwa National Park",
        "Terra Nova National Park"
    ],
    "bobcat": ["Cape Breton Highlands National Park"],
    "coyote": ["Cape Breton Highlands National Park", "Rouge Urban National Park"],
    "bison": ["Elk Island National Park"],
    "beaver": [
        "Elk Island National Park",
        "Georgian Bay Islands National Park",
        "Pituamkek National Park",
        "Terra Nova National Park",
        "Thousand Islands National Park"
    ],
    "red fox": [
        "Forillon National Park",
        "Point Pelee National Park",
        "Prince Edward Island National Park",
        "Terra Nova National Park"
    ],
    "whale": ["Forillon National Park"],
    "peregrine falcon": ["Fundy National Park", "Nahanni National Park"],
    "osprey": [
        "Georgian Bay Islands National Park",
        "Thousand Islands National Park"
    ],
    "white-tailed deer": [
        "Georgian Bay Islands National Park",
        "Kouchibouguac National Park",
        "Thousand Islands National Park"
    ],
    "wolverine": [
        "Glacier National Park",
        "Nááts’įhch’oh National Park"
    ],
    "lynx": [
        "Glacier National Park",
        "Prince Albert National Park",
        "Pukaskwa National Park",
        "Riding Mountain National Park"
    ],
    "prairie dog": ["Grasslands National Park"],
    "swift fox": ["Grasslands National Park"],
    "sea lion": [
        "Gulf Islands National Park Reserve",
        "Gwaii Haanas National Park Reserve"
    ],
    "bald eagle": [
        "Gulf Islands National Park Reserve",
        "Gwaii Haanas National Park Reserve",
        "Waterton Lakes National Park"
    ],
    "orca": ["Gulf Islands National Park Reserve"],
    "humpback whale": ["Gwaii Haanas National Park Reserve"],
    "dall sheep": ["Kluane National Park and Reserve"],
    "golden eagle": ["Kluane National Park and Reserve"],
    "grey seal": [
        "Kouchibouguac National Park",
        "Sable Island National Park Reserve"
    ],
    "loon": ["La Mauricie National Park"],
    "puffin": ["Mingan Archipelago National Park Reserve"],
    "seabirds": [
        "Mingan Archipelago National Park Reserve",
        "Pituamkek National Park",
        "Sable Island National Park Reserve"
    ],
    "marmot": [
        "Mount Revelstoke National Park",
        "Yoho National Park"
    ],
    "river otter": ["Kejimkujik National Park"],
    "barred owl": ["Kejimkujik National Park"],
    "snapping turtle": [
        "Rouge Urban National Park",
        "Kejimkujik National Park"
    ],
    "sea otter": ["Pacific Rim National Park Reserve"],
    "grey whale": ["Pacific Rim National Park Reserve"],
    "monarch butterfly": ["Point Pelee National Park"],
    "raccoon": ["Point Pelee National Park"],
    "cormorant": ["Prince Edward Island National Park"],
    "narwhal": ["Sirmilik National Park"],
    "beluga whale": ["Sirmilik National Park"],
    "porcupine caribou": ["Vuntut National Park"],
    "cougar": ["Waterton Lakes National Park"],
    "whooping crane": ["Wood Buffalo National Park"],
    "wild horses": ["Sable Island National Park Reserve"],
    "arctic wolf": [
        "Torngat Mountains National Park",
        "Tuktut Nogait National Park"
    ],
    "falcon": ["Tuktut Nogait National Park"]
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
            parks = animal_to_park.get(animal.lower())
            if parks:
                # Ensure it's a list
                if isinstance(parks, str):
                    parks = [parks]
                return func.HttpResponse(
                    json.dumps(parks),
                    mimetype="application/json",
                    status_code=200
                )
            else:
                return func.HttpResponse(
                    json.dumps([]),
                    mimetype="application/json",
                    status_code=200
                )
        else:
            return func.HttpResponse("Please select an animal.", status_code=400)

