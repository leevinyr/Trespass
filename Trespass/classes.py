import time

class Entity:
    def __init__(self, health):
        self.health = health

class Player(Entity):
    def __init__(self, name, age, gender):
        self.name = name
        self.age = int(age)
        self.gender = gender
        self.exp = 0
        self.level = 0
        self.inventory = []
        self.health = 100
        self.in_room = Room

    # Lisää annetun esineen pelaajan inventoryyn
    def collect_item(self, item):
        if(len(self.inventory) == 8):
            print("Inventory is full.")
            time.sleep(1)
        else:
            self.inventory.append(item)
            self.in_room.items.remove(item)
    # Poistaa annetun esineen pelaajan inventorystä.
    def discard_item(self, item):
        self.inventory.remove(item)

    # Laskee pelaajan inventoryn kokonaisarvon.
    def total_inventory_value(self):
        total_inventory_value = 0
        
        for i in range(0, len(self.inventory), 1):
            total_inventory_value += self.inventory[i].value

        return total_inventory_value

    # Tulostaa pelaajan inventoryn sisällön ja sen kokonaisarvon näytölle.
    def show_inventory(self):
        for i in range(0, len(self.inventory), 1):
            print(f"{i} {self.inventory[i].name} {self.inventory[i].value}$")

        print(f"\nTotal value: {self.total_inventory_value()}$")

class Room:
    def __init__(self, name, items):
        self.name = name
        self.items = items
                
class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value
