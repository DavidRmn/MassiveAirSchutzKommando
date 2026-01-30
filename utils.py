from dataclasses import dataclass

@dataclass
class GameData:
    title: str = 'Massive Air Schutz Kommando'
    width: int = 1280
    height: int = 720

    background_layer_path: str = 'sprites/background.png'
    depth_layer_one_path: str = 'sprites/depth.png'
    depth_layer_two_path: str = 'sprites/depth.png'
    foreground_layer_path: str = 'sprites/foreground.png'

    player_sprite_path: str = 'sprites/player.png'