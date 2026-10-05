import random
import time
import json
import subprocess
import platform
import sys

from classes import Entity, Player, Item, Room
from items import all_items

# Luo tyhjän player-olion
player = Player("", 0, "")

# Luo kopion kaikkien tavaroiden listasta, jotta siitä voi poistaa käytettyjä tavaroita ilman, että ne poistuvat pelin käytöstä kokonaan
available_items = all_items.copy()

# Luo pelin huoneet ilman tavaroita
Entryway = Room("Entryway", [])
Kitchen = Room("Kitchen", [])
Living_room = Room("Living room", [])
Bathroom = Room("Bathroom", [])
Attic = Room("Attic", [])
Bedroom = Room("Bedroom", [])

# Lisää kaikki huoneet listaan
rooms = [Entryway, Kitchen, Living_room, Bathroom, Attic, Bedroom]

# Pelin controllit
controls_text = "Controls: \nCollect item: 1, Discard item: 2, Change room: 3"

# Generoi satunnaisen määrän item-olioita mahdollisia tavaroita sisältävästä listasta
def generate_items():
    room_items = []

    for i in range(0, random.randint(1, 5)):
        random_item = random.randint(0, len(available_items)-1)
        room_items.append(available_items[random_item])
        available_items.pop(random_item)

    return room_items

# Funktio, joka etsii item-olion kaikkien tavaroiden listasta pelkästään sen nimi-attribuutilla
def find_item_by_name(name):
    for item in all_items:
        if item.name == name:
            return item

# Funktio, joka etsii room-olion kaikkien huoneiden listasta pelkästään sen nimi-attribuutilla 
def find_room_by_name(name):
    for room in rooms:
        if room.name == name:
            return room

# Tulostaa pelin lopetuksen näytölle. Pelin lopetuksella on monta versiota, jotka riippuvat pelaajan omista tiedoista.
def game_over_sequence():

    time.sleep(1)
    clear_screen()
    time.sleep(2)

    print("""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣾⠟⢀⡘⠉⠁⠀⣀⠙⠉⢿⣀⣄⣲⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠖⠛⠉⠀⠄⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠝⠃⠨⠿⣷⡆⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡄⠀⠠⣌⠙⠿⣷⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⠀⠈⠻⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣁⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠲⢄⠀⠀⢠⣝⢻⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣾⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢿⣮⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣤⣀⣠⣤⣤⣤⣴⣤⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠈⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⠀⠀⠀⠀⠀⠀⠀⠰⠃⠻⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡖⣯⠓⠀⠀⠀⠀⠀⠀⠀⢪⣧⢸⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⡗⣮⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣯⣷⡾⣵⠃⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠌⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣯⡿⣷⢧⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡻⠁⠀⠀⠈⠁⠻⠗⠻⣿⣿⡿⠿⠋⠉⠀⠀⠙⠉⠛⠻⢿⣿⣷⣾⣿⣽⣟⣿⢺⡄⠀⠀⠀⠀⠀⠀⠀⠘⡳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡄⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⣼⣟⣿⣾⣻⡜⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣷⣀⠀⠀⠀⠀⢀⣠⣿⣿⣷⣠⣀⠀⠀⠀⠀⠠⢄⠀⠀⣀⢀⠀⣀⣸⣿⣿⣧⠅⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣯⣀⣤⣴⣾⣿⣿⢟⣤⣿⣿⣿⣟⣁⠒⠚⠁⠀⠀⣿⣿⣿⣿⣿⣿⣿⡞⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢬⣯⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣿⣤⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢧⡛⡄⢠⠀⠀⠀⠰⣁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢼⣿⢸⣿⣿⣿⣿⢟⣿⣿⣧⣿⣷⡄⠀⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡃⠈⢌⡑⢎⡆⢀⡀⠽⢀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣾⣿⣿⣿⣇⠘⠛⠿⠏⠉⠿⠟⠄⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠧⠀⠀⠀⠆⠌⠀⣠⣾⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣶⣤⡄⠀⠀⠀⣀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣛⢒⣂⠀⠀⠀⡄⠂⠈⠠⣿⣻⠆⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠿⣿⣿⣷⣶⣿⣾⣿⠛⠿⣿⣿⣿⣿⣿⣟⣿⢳⢯⡍⡤⠀⢀⠒⡌⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠁⠀⣉⣁⣀⣀⣀⣀⠀⡉⠀⠀⠈⠁⢻⣿⣏⡿⢯⠶⡤⡄⢠⠎⡰⠀⠀⡞⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣦⣾⣿⣿⣟⡉⠉⠻⢿⡿⢿⣿⣦⣴⣿⣿⣻⣝⢪⢿⡱⢃⢇⡚⠀⠀⡜⠁⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⡟⣿⣿⣿⣿⣿⣿⣿⣷⣦⣶⣿⣿⡿⣿⣿⠏⠑⣪⢯⡓⡹⠌⠂⠀⠀⡐⠀⣰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⡗⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣶⠶⠍⡤⠋⢨⡗⡖⠉⠀⠀⠀⠀⠀⡀⢹⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡟⣿⣿⣿⡿⣿⣿⣿⣿⡿⢿⡽⡇⠀⠀⠀⠜⠁⠊⠀⠀⠀⠀⠀⠀⡰⡁⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⠹⠛⠿⠆⠈⠉⠀⠀⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠴⢡⠂⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠂⣸⣿⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡉⢖⣍⠂⢸⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢠⣿⣿⡄⢻⣷⣤⡀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠄⣀⠰⢣⢎⡱⢎⡄⠿⣷⡀⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢼⣿⣿⣷⡈⢿⣿⣿⣖⠦⣄⡀⠀⠀⠀⠀⠀⠀⡀⢌⠲⣌⠳⣍⠞⡜⠦⡀⢠⣿⡇⠈⣣⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣄⠻⣿⣿⣿⣿⣿⣤⣤⡼⣸⢃⠧⣘⡘⣣⢄⠿⣠⢟⣻⠀⢠⡿⣿⠇⠀⠻⣧⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣷⣌⠻⣿⣿⣿⣿⣛⡿⢷⣯⣿⣵⣏⣳⣾⡹⢾⠌⢁⣴⠟⣱⡿⠀⠀⠀⠙⢿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣷⣌⠻⣿⣿⣿⣿⣶⣿⣿⣿⣿⣷⡿⠙⣠⣶⡿⢋⣴⣿⡟⠀⠀⠀⠀⠀⠙⢾⣿⣿⠗⠶⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠛⢿⣿⣿⣿⣿⣿⡿⢋⣤⣾⣿⣿⣥⣾⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠉⠈⠛⠀⠀⢄⡈⠑⠲⡄⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⠙⠛⠛⠛⣩⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠔⠀⠀⠈⠣⠀⠩⣝⣲⣤⣀⠀⠀⠀
⡀⠄⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉⠈⡉⠁⠈⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠖⠀⠛⢻⣿⣶
⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⣿⣿⣿⣿⣿⠟⠉⠠⣀⣀⠐⠾⠁⠀⠀⠀⣠⡈⠻⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠹⡿
⠑⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠟⣋⣤⣤⣴⣾⣿⣿⡇⠈⡃⠀⠀⠈⣿⣷⣤⣬⡙⠻⢿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠛⢡⣾⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⣼⣿⣿⣿⣿⡿⢿⡷⢆⠙⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⠿⣿⣿⣿⣿⣿⣿⣿⡿⠀⣀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣌⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⢿⡿⠁⠰⢧⠀⠀⠈⠾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀""")
     
     # Jos pelaaja on 18 tai yli ja alle 30
    if(30 > player.age >= 18 and player.gender == "male"):
          time.sleep(1)
          print("Hm. So you did it. As expected, from a young man like you. Alright, you're free to go.")
          time.sleep(2)
    elif(30 > player.age >= 18 and player.gender == "female"):
          time.sleep(1)
          print("Hm. So you did it. As expected, from a young woman like you. Alright, you're free to go.")
          time.sleep(2)
    elif(30 > player.age >= 18 and player.gender == "other"):
            time.sleep(1)
            print("Hm. So you did it. As expected, from a young person like you. Alright, you're free to go.")
            time.sleep(2)

     # Jos pelaaja on alle 18
    elif(player.age < 18 and player.gender == "male"):
          time.sleep(1)
          print("You're just.. a boy. Well done. You may go now. And stay out of trouble.")
          time.sleep(2)
    elif(player.age < 18 and player.gender == "female"):
          time.sleep(1)
          print("You're just.. a girl. Well done. You may go now. And stay out of trouble.")
          time.sleep(2)
    elif(player.age < 18 and player.gender == "female"):
            time.sleep(1)
            print("You're just.. a child. Well done. You may go now. And stay out of trouble.")
            time.sleep(2)

     # Jos pelaaja on 30 tai yli ja alle 50
    if(50 > player.age >= 30 and player.gender == "male"):
          time.sleep(1)
          print("And he does it. Not bad. Alright, you can go now.")
          time.sleep(2)
    elif(50 > player.age >= 30 and player.gender == "female"):
          time.sleep(1)
          print("And she does it. Not bad. Alright, you can go now.")
          time.sleep(2)
    elif(50 > player.age >= 30 and player.gender == "other"):
          time.sleep(1)
          print("And they do it. Not bad. Alright, you can go now.")
          time.sleep(2)

     # Jos pelaaja on 50 tai yli
    elif(player.age >= 50 and player.gender == "male"):
          time.sleep(1)
          print("Not bad for a man of your age. Hope you didn't strain any muscles in there. You can go.")
          time.sleep(2)
    elif(player.age >= 50 and player.gender == "female"):
          time.sleep(1)
          print("Not bad for a woman of your age. Hope you didn't strain any muscles in there. You can go.")
          time.sleep(2)
    elif(player.age >= 50 and player.gender == "other"):
            time.sleep(1)
            print("Not bad for a person of your age. Hope you didn't strain any muscles in there. You can go.")
            time.sleep(2)

    print("You win.")
    time.sleep(2)
    play_again_input = input("Press enter to wipe your save and exit.")
    open("../../save.json", "w").close()
    sys.exit(0)


# Tulostaa pelin lopetuksen näytölle silloin, kun pelaaja on hävinnyt pelin.
def show_game_failed_screen():
     clear_screen()
     print("Nothing more valuable in there huh? Well, I'll take it. You're not getting out though.")
     time.sleep(2)
     print("You are now trapped in the house for eternity.")
     time.sleep(2)
     print("You lost.")
     time.sleep(2)
     open("../../save.json", "w").close()
     sys.exit(0)

# Tulostaa hahmonluontivalikon näytölle, ja asettaa käyttäjän antamat arvot player-oliolle.
def show_create_character_screen():
    given_name = input(("What is your name?\n"))
    player.name = given_name

    given_age = input("\nWhat is your age?\n")
    if(given_age == ""):
         print("Invalid age.")
    elif(int(given_age) < 12):
         print("You must be 12 or older to play trespass.")
         time.sleep(2)
         sys.exit(0)
    else:
         player.age = int(given_age)

    given_gender = input("\nWhat is your gender?\n1 Male\n2 Female\n3 Other\nSelection: ")
    if(given_gender == "1" or given_gender.lower() == "male"):
        given_gender = "male"
    elif(given_gender == "2" or given_gender.lower() == "female"):
        given_gender = "female"
    elif(given_gender == "3" or given_gender.lower() == "other"):
        given_gender = "other"

    player.gender = given_gender

    print(f"\nName: {player.name}, Age: {player.age}, Gender: {player.gender}\n")

    player_info_confirmation = input("Is this correct? (y/n) ")
    if(player_info_confirmation == "y"):
        print("\n")
        input("Character saved. Press enter to begin.")
    else:
        print("\n")

        show_create_character_screen()
    
# Tallentaa pelin tilan
def save_game_state():
     data_to_save = {
                 "player_name": player.name,
                 "player_age": player.age,
                 "player_gender": player.gender,
                 "saved_health": player.health,
                 "saved_inventory": [item.name for item in player.inventory],
                 "saved_exp": player.exp,
                 "saved_level": player.level,
                 "saved_room": player.in_room.name,
                 
                 "entryway_items": [item.name for item in Entryway.items],
                 "living_room_items": [item.name for item in Living_room.items],
                 "kitchen_items": [item.name for item in Kitchen.items],
                 "attic_items": [item.name for item in Attic.items],
                 "bedroom_items": [item.name for item in Bedroom.items],
                 "bathroom_items": [item.name for item in Bathroom.items],
              }

     with open("../../save.json", "w") as save_file:
          json.dump(data_to_save, save_file)

# Lataa pelin tallennetun tilan
def load_saved_game_state():
    with open("../../save.json", "r") as save_file:
        read_data = json.load(save_file)

    player.name, player.age, player.gender, player.health, player.exp, player.level = read_data["player_name"], read_data["player_age"], read_data["player_gender"], read_data["saved_health"], read_data["saved_exp"], read_data["saved_level"]
    player.in_room = find_room_by_name(read_data["saved_room"])
    player.inventory = [find_item_by_name(item_name) for item_name in read_data["saved_inventory"]]
    Entryway.items = [find_item_by_name(item_name) for item_name in read_data["entryway_items"]]
    Living_room.items = [find_item_by_name(item_name) for item_name in read_data["living_room_items"]]
    Kitchen.items = [find_item_by_name(item_name) for item_name in read_data["kitchen_items"]]
    Attic.items = [find_item_by_name(item_name) for item_name in read_data["attic_items"]]
    Bedroom.items = [find_item_by_name(item_name) for item_name in read_data["bedroom_items"]]
    Bathroom.items = [find_item_by_name(item_name) for item_name in read_data["bathroom_items"]]

# Tulostaa pelin huoneiden kartan näytölle sen perusteella, missä huoneessa pelaaja on.
def show_current_map():
    if(player.in_room == Entryway):
        print("""
    +-----------+     +----------+
    |  Bedroom  |-----| Bathroom |
    +-----------+     +----------+
           |
           |
    +-----------+     +----------+
    |   Attic   |-----| Kitchen  |
    +-----------+     +----------+
                         |
                         |
                    +----------+
                    |  Living  |
                    |   room   |
                    +----------+
                         |
                         |
                    +----------+
                    |*ENTRYWAY*|
                    +----------+
    """)
    elif(player.in_room == Living_room):
        print("""
+-----------+     +----------+
|  Bedroom  |-----| Bathroom |
+-----------+     +----------+
       |
       |
+-----------+     +----------+
|   Attic   |-----|  Kitchen |
+-----------+     +----------+
                     |
                     |
                +----------+
                | *LIVING  |
                |   ROOM*  |
                +----------+
                     |
                     |
                +----------+
                | Entryway |
                +----------+
""")
    elif(player.in_room == Kitchen):
        print("""
    +-----------+     +----------+
    |  Bedroom  |-----| Bathroom |
    +-----------+     +----------+
           |
           |
    +-----------+     +-----------+
    |   Attic   |-----| *KITCHEN* |
    +-----------+     +-----------+
                         |
                         |
                    +----------+
                    |  Living  |
                    |   room   |
                    +----------+
                         |
                         |
                    +----------+
                    | Entryway |
                    +----------+
    """)
    elif(player.in_room == Attic):
            print("""
    +-----------+     +----------+
    |  Bedroom  |-----| Bathroom |
    +-----------+     +----------+
           |
           |
    +-----------+     +----------+
    |  *ATTIC*  |-----|  Kitchen |
    +-----------+     +----------+
                         |
                         |
                    +----------+
                    |  Living  |
                    |   room   |
                    +----------+
                         |
                         |
                    +----------+
                    | Entryway |
                    +----------+
    """)
    elif(player.in_room == Bedroom):
            print("""
    +-----------+     +----------+
    | *BEDROOM* |-----| Bathroom |
    +-----------+     +----------+
           |
           |
    +-----------+     +----------+
    |   Attic   |-----| Kitchen  |
    +-----------+     +----------+
                         |
                         |
                    +----------+
                    |  Living  |
                    |   room   |
                    +----------+
                         |
                         |
                    +----------+
                    | Entryway |
                    +----------+
    """)
    elif(player.in_room == Bathroom):
            print("""
    +-----------+     +------------+
    |  Bedroom  |-----| *BATHROOM* |
    +-----------+     +------------+
           |
           |
    +-----------+     +----------+
    |   Attic   |-----| Kitchen  |
    +-----------+     +----------+
                         |
                         |
                    +----------+
                    |  Living  |
                    |   room   |
                    +----------+
                         |
                         |
                    +----------+
                    | Entryway |
                    +----------+
    """)

# Laskee, onko pelaajalla inventoryssä jo arvokkaimmat esineet, jotka löytyvät huoneista, ja palauttaa sen perusteella True tai False.
def highest_value_found():
     lowest_inv_value = 11

     for i in player.inventory:
          if i.value < lowest_inv_value:
               lowest_inv_value = i.value

     lowest_house_value = 10
     for room in rooms:
          for item in room.items:
            if item.value < lowest_house_value:
                lowest_house_value = item.value

     if(lowest_inv_value >= lowest_house_value):
          return True
     else:
          return False

# Tulostaa pelaajan hetkellisen huoneen tiedot näytölle, kuten huoneen nimen ja sen sisältämät tavarat.          
def show_room_info():
    if(not player.in_room.items):
         print("No items in this room.\n")
    else:
        print(f"Current room: {player.in_room.name}\n\nItems in room:")
        for i in player.in_room.items:
            print(f"{player.in_room.items.index(i)} {i.name}, {i.value}$")
        print("\n")

# Kysyy käyttäjältä, minkä esineen haluaa lisätä inventoryynsä, ja lisää sen sinne.
def select_item_collect():
     selection = input("Select item to collect: ")
     if(selection == ""):
          print("Invalid selection.")
          time.sleep(1)
     elif(int(selection) >= 0 and int(selection) < len(player.in_room.items)):
        player.collect_item(player.in_room.items[int(selection)])
     else:
        print("Invalid selection.")
        time.sleep(1)

# Kysyy käyttäjältä, minkä tavaran haluaa poistaa inventorystään, ja poistaa sen.
def select_item_discard():
     player.show_inventory()

     selection = input("Select an item to discard: ")
     if(selection == "" or int(selection) < 0 or int(selection) > len(player.inventory) - 1):
          print("Invalid selection.")
          time.sleep(1)
     else:
          player.discard_item(player.inventory[int(selection)])

# Kysyy käyttäjältä, mihin huoneeseen haluaa siirtyä seuraavaksi.     
def select_room_change():
     print("Nearby rooms: ")
     if(player.in_room == Entryway):
          print("1 Living room\n2 Door")
     elif(player.in_room == Living_room):
          print("1 Kitchen\n2 Entryway")
     elif(player.in_room == Kitchen):
              print("1 Attic\n2 Living room")
     elif(player.in_room == Attic):
              print("1 Bedroom\n2 Kitchen")
     elif(player.in_room == Bedroom):
              print("1 Bathroom\n2 Attic")
     elif(player.in_room == Bathroom):
              print("1 Bedroom")
    
     selection = input("Select next room: ")
     if(selection == ""):
          print("Invalid selection.")
          time.sleep(2)
          select_room_change()
     if(player.in_room == Entryway and int(selection) == 1):
          player.in_room = Living_room

     # Tarkistaa, onko pelaajalla jo arvokkaimmat mahdolliset tavarat, ja vastaa sen perusteella.
     elif(player.in_room == Entryway and int(selection) == 2):
          if(player.total_inventory_value() < 50):
               if(highest_value_found()):
                    time.sleep(1)
                    show_game_failed_screen()
               elif(not highest_value_found()):
                    print("Your items are not valuable enough. Try again when they are.")
                    time.sleep(2)
          else:
               game_over_sequence()   

     elif(player.in_room == Living_room and int(selection) == 1):
          player.in_room = Kitchen
     elif(player.in_room == Living_room and int(selection) == 2):
              player.in_room = Entryway
     elif(player.in_room == Kitchen and int(selection) == 1):
              player.in_room = Attic
     elif(player.in_room == Kitchen and int(selection) == 2):
              player.in_room = Living_room
     elif(player.in_room == Attic and int(selection) == 1):
              player.in_room = Bedroom
     elif(player.in_room == Attic and int(selection) == 2):
              player.in_room = Kitchen
     elif(player.in_room == Bedroom and int(selection) == 1):
              player.in_room = Bathroom
     elif(player.in_room == Bedroom and int(selection) == 2):
              player.in_room = Attic
     elif(player.in_room == Bathroom and int(selection) == 1):
              player.in_room = Bedroom
     else:
           print("Invalid selection.")
           time.sleep(1)

# Kysyy käyttäjältä komentoa.     
def ask_next_command():
     command = input("\nEnter command: ")
     if(command == "1"):
          select_item_collect()
     elif(command == "2"):
          select_item_discard()
     elif(command == "3"):
          select_room_change()
     else:
          print("Invalid selection.")
          time.sleep(1)

# Lukee save-tiedoston. Jos se on tyhjä, funktio olettaa, että pelaaja pelaa ensimmäistä kertaa, ja tulostaa näytölle hahmonluontivalikon.
def start_game():
    with open("../../save.json", "r") as save_file:

        # Täyttää saatavilla olevien tavaroiden listan uudelleen, kun peli aloitetaan
        available_items.clear()
        available_items.extend(all_items)

        if(not save_file.read(1)):

            Entryway.items = generate_items()
            Living_room.items = generate_items()
            Kitchen.items = generate_items()
            Attic.items = generate_items()
            Bedroom.items = generate_items()
            Bathroom.items = generate_items()

            player.in_room = Entryway

            with open("../../intro.txt", "r") as f:
                 for line in f:
                      print(line)
                      time.sleep(2)
                 print("\n")

            show_create_character_screen()
        else:
            load_saved_game_state()

# Tyhjentää aiemmat tekstit konsolista käyttöliittymän selventämiseksi. 
def clear_screen():
    if platform.system() == "Windows":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"], shell=True)

# Pääsilmukka
def main():
    start_game()

    while True:
       clear_screen()
       save_game_state()
       print(controls_text)
       show_current_map()
       show_room_info()
       ask_next_command()
        
main()
