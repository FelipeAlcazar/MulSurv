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

def increase_speed(player):
    player.speed += 1
    
def increase_health(player):
    player.health += 1

def decrease_speed(player, enemies):
    for enemy in enemies:
        # Reduce la velocidad de cada enemigo
        enemy.speed = max(1, enemy.speed - 1)

def double_shoot(player):
    player.double_shoot_enabled = True

def triple_shoot(player):
    player.triple_shoot_enabled = True
   

# Define available upgrades
available_upgrades = [
    Upgrade("Increase Fire Rate", "Decreases the time between shots.", increase_fire_rate),
    Upgrade("Increase Speed", "Increases the player's speed.", increase_speed),
    Upgrade("Increase Health", "Increases the player's health.", increase_health),
    Upgrade("Enemies less aggressive", "Decreases the speed of the enemies.", decrease_speed),
    Upgrade("Double Shoot", "Allows the player to shoot two bullets at once.", double_shoot),
    Upgrade("Triple Shoot", "Allows the player to shoot three bullets at once.", triple_shoot)
]