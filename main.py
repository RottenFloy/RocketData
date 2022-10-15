from NaturaSiberica import get_items_natura
from json_loader import json_saver
from Oriencoop import get_items_oriencoop
from som1 import get_items_som1

if __name__ == "__main__":
    json_saver(get_items_natura(), "NaturaSiberica.json")
    json_saver(get_items_oriencoop(), "Oriencoop.json")
    json_saver(get_items_som1(), "som1.json")
