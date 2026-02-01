from bullet import Bullet
from alien import Alien
from utils import GameData


def bullet_collision(bullet: Bullet, alien: Alien):
    if bullet.position.distance_squared_to(alien.position) <= bullet.col_radius * bullet.col_radius + alien.col_radius * alien.col_radius\
            and bullet.ded == False and alien.ded == False:
        return True
    return False

def check():
    for bul in GameData.bullet_list:
        for ali in GameData.aliens_list:
            if bullet_collision(bul, ali):
                ali.on_hit(bul.dmg, bul.player)
                bul.on_hit()
