import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.gold = 100
        self.inventory = []

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100

    def add_item(self, item):
        self.inventory.append(item)

    def show_status(self):
        status = self.get_status()
        print(f"\n{self.name}: Zdrowie = {self.health}, Złoto = {self.gold}, Status = {status}")
        print("Ekwipunek:", ", ".join(self.inventory) if self.inventory else "Brak")

    def get_status(self):
        if self.gold >= 1000:
            return "Król"
        elif self.gold >= 601:
            return "Szlachta"
        elif self.gold >= 301:
            return "Rycerz"
        elif self.gold >= 101:
            return "Giermek"
        else:
            return "Początkujący"

def generate_random_place():
    places = ["las", "jaskinia", "zamek", "miasto", "wioska", "ruiny"]
    place = random.choice(places)
    print(f"\nWędrujesz i dotarłeś do: {place.capitalize()}.")
    return place

def random_event(player, place, move_count):
    print(f"\nCo chcesz zrobić w {place}?")
    print("1. Przeszukaj obszar.")
    print("2. Odpocznij (koszt: 100 złota).")
    print("3. Sprawdź status postaci.")
    print("4. Zakończ grę.")

    choice = input("> ")

    if choice == "1":
        move_count += 1
        if place in ["las", "jaskinia", "wioska"]:
            event = random.choice(["enemy", "treasure", "nothing", "special_event", "traveler"])
        else:
            event = random.choice(["enemy", "treasure", "nothing", "special_event"])
        
        if event == "enemy":
            if not enemy_attack(player, place):
                return False, move_count
        elif event == "treasure":
            find_treasure(player, place)
        elif event == "special_event":
            special_event(player, place)
        elif event == "traveler":
            if not traveler_encounter(player):
                return False, move_count
        else:
            print(f"\nNie znalazłeś nic ciekawego w {place}.")
    elif choice == "2":
        if player.gold >= 100:
            move_count += 1
            player.gold -= 100
            player.heal(40)
            print(f"\n{player.name} odpoczywa i odzyskuje zdrowie. Koszt odpoczynku: 100 złota.")
        else:
            print("\nNie masz wystarczającej ilości złota, aby odpocząć!")
    elif choice == "3":
        player.show_status()
    elif choice == "4":
        print("\nGra zakończona. Do zobaczenia!")
        return False, move_count

    if player.gold >= 1000:
        print(f"\nGratulacje! {player.name} został królem! Ukończyłeś grę w {move_count} ruchach.")
        return False, move_count
    
    return True, move_count

def enemy_attack(player, place):
    enemies = {
        "las": "wilk",
        "jaskinia": "troll",
        "zamek": "rycerz",
        "miasto": "bandyta",
        "wioska": "zbójca",
        "ruiny": "duch"
    }
    enemy = enemies[place]
    print(f"\nNapotkałeś {enemy} w {place}!")
    enemy_damage = random.randint(10, 30)
    print(f"\n{enemy.capitalize()} atakuje i zadaje {enemy_damage} punktów obrażeń.")
    player.take_damage(enemy_damage)

    if player.health == 0:
        print(f"\n{player.name} został pokonany przez {enemy}.")
        return False
    return True

def find_treasure(player, place):
    treasures = {
        "las": ["magiczny grzyb", "kryształ leśnych duchów"],
        "jaskinia": ["stalowy młot", "stary zwój"],
        "zamek": ["diamentowa korona", "złoty miecz"],
        "miasto": ["rzadki klejnot", "złota bransoleta"],
        "wioska": ["tajemnicze nasiono", "drewniany amulet"],
        "ruiny": ["starożytny artefakt", "zniszczona mapa skarbów"]
    }
    treasure_values = {
        "las": 20,
        "jaskinia": 30,
        "zamek": 80,
        "miasto": 50,
        "wioska": 40,
        "ruiny": 60
    }
    found_treasure = random.choice(treasures[place])
    print(f"\nZnalazłeś skarb: {found_treasure} w {place.capitalize()}!")
    player.add_item(found_treasure)

    gold_earned = treasure_values[place]
    player.gold += gold_earned
    print(f"\nZdobywasz {gold_earned} złota za znalezienie skarbu w {place.capitalize()}.")

def special_event(player, place):
    events = {
        "las": "Spotkałeś starego druida, który oferuje ci miksturę zdrowia.",
        "jaskinia": "Znalazłeś tajemne przejście do ukrytego skarbca.",
        "zamek": "Król zaprosił cię na ucztę i wręczył 200 złota.",
        "miasto": "Natknąłeś się na tłum ludzi i ktoś cię okradł (-50 złota).",
        "wioska": "Miejscowy zielarz ofiarował ci magiczne zioła (odnawiają 30 zdrowia).",
        "ruiny": "Natrafiłeś na pradawny rytuał, który zwiększa twoją siłę w walce."
    }
    event = events[place]
    print(f"\n{event}")

    if place == "las":
        player.heal(30)
    elif place == "zamek":
        player.gold += 200
    elif place == "miasto":
        player.gold -= 50
        if player.gold <= 0:
            print(f"\n{player.name} stracił całe swoje złoto. Gra skończona.")
            return False
    elif place == "wioska":
        player.heal(30)

    return True

def traveler_encounter(player):
    print("\nSpotkałeś wędrowca, który potrzebuje pomocy. Co robisz?")
    print("1. Pomóż wędrowcowi.")
    print("2. Okradnij wędrowca.")

    choice = input("> ")

    if choice == "1":
        print("\nWędrowiec dziękuje ci i wręcza 50 złota.")
        player.gold += 50
    elif choice == "2":
        success = random.random()
        if success < 0.75:
            print("\nOkradłeś wędrowca i zdobyłeś 100 złota.")
            player.gold += 100
        else:
            print("\nWędrowiec okazuje się silniejszy i zabiera ci 50 złota.")
            player.gold -= 50
            if player.gold <= 0:
                print(f"\n{player.name} stracił całe swoje złoto. Gra skończona.")
                return False
    return True

def game_over_screen():
    print("\nTwoja postać zginęła. Co chcesz zrobić?")
    print("1. Zagraj ponownie.")
    print("2. Zakończ grę.")

    choice = input("> ")
    if choice == "1":
        start_game()
    elif choice == "2":
        print("\nGra zakończona. Dziękujemy za grę!")
        exit()

def start_game():
    print("\nWitaj w tekstowej przygodzie!")
    print("Celem gry jest zebranie 1000 złota i zostanie królem w jak najmniejszej liczbie ruchów.\n")
    name = input("Podaj imię swojego bohatera: ")
    player = Player(name)
    move_count = 0

    print(f"\nWitaj, {player.name}! Rozpoczynasz swoją podróż.")
    
    playing = True
    while playing:
        if player.health <= 0:
            game_over_screen()
            return

        place = generate_random_place()
        playing, move_count = random_event(player, place, move_count)

    print(f"\nDziękujemy za grę! Ukończyłeś grę w {move_count} ruchach.")

if __name__ == "__main__":
    start_game()
