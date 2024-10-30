from src.models.weapon import Weapon

class Upgrade:
    def __init__(self, name, description, apply_upgrade):
        self.name = name
        self.description = description
        self.apply_upgrade = apply_upgrade

    def apply(self, player):
        self.apply_upgrade(player)

def increase_fire_rate(player):
    player.weapon.shoot_delay = max(100, player.weapon.shoot_delay - 100)

def change_weapon(player):
    new_weapon = Weapon("Gun")
    player.change_weapon(new_weapon)

def increase_speed(player):
    player.speed += 1
    
def increase_health(player):
    player.health += 1

# Define available upgrades
available_upgrades = [
    Upgrade("Increase Fire Rate", "Decreases the time between shots.", increase_fire_rate),
    Upgrade("Change Weapon", "Changes the weapon to a gun.", change_weapon),
    Upgrade("Increase Speed", "Increases the player's speed.", increase_speed),
    Upgrade("Increase Health", "Increases the player's health.", increase_health)
]