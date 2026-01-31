from utils import GameData

def simulation_engine():
    for i in range(len(GameData.aliens_list)):
        GameData.aliens_list[i].simulate(GameData.aliens_list, i)