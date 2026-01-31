from dataclasses import dataclass, field
import alien, bullet

@dataclass
class GameData:
    title: str = 'Massive Air Schutz Kommando'
    width: int = 1280
    height: int = 720

    # states
    is_running = True

    background_layer_path: str = 'Images/Background1.png'
    depth_layer_one_path: str = 'Images/Background2.png'
    depth_layer_two_path: str = 'Images/Background3.png'
    foreground_layer_path: str = 'Images/Ground.png'
    tower_layer_path: str = 'Images/Tower.png'

    player_sprite_path: str = 'Images/Turret/'
    player_animation_cooldown: int = 85

    # lists
    aliens_list: list[alien.Alien] = field(default_factory=alien.Alien)
    bullet_list: list[bullet.Bullet] = field(default_factory=bullet.Bullet)
    drops_list = []