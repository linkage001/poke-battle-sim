import csv
import os
import random
from typing import List, Dict
import time

# Import custom classes from the poke_battle_sim package
from poke_battle_sim.core.pokemon import Pokemon
from poke_battle_sim.core.trainer import Trainer
from poke_battle_sim.core.battle import Battle
from poke_battle_sim.conf.global_settings import COMPLETED_MOVES, STAT_NUM

POKE_NUM_MIN = 4
SWITCH = 'switch'
ITEM = 'item'
MOVE = 'move'

# Define a dictionary to map move names to their identifiers
def load_move_dict(moves_file: str) -> Dict[str, int]:
    moves_dict = {}
    with open(moves_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        next(reader)  # Skip header row
        for row in reader:
            identifier = row['identifier']
            index = int(row['id']) - 1
            moves_dict[identifier] = index
    return moves_dict

# Load the move dictionary
DATA_DIR = '/home/gbueno/poke-battle-sim/poke_battle_sim/data/'
MOVE_DICT = load_move_dict(f"{DATA_DIR}/move_list.csv")

# Define the parties for both trainers
def create_party(trainer_name: str) -> List[Pokemon]:
    if not isinstance(trainer_name, str):
        raise ValueError("Trainer name must be a string.")
    
    stats_file = f"{DATA_DIR}/pokemon_stats.csv"
    
    pokemons = []
    with open(stats_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        next(reader)  # Skip header row
        
        for i, row in enumerate(reader):
            if i >= POKE_NUM_MIN or int(row["ndex"]) > COMPLETED_MOVES:
                break
            
            # Randomly select four moves from the first four valid moves based on the Pokedex index
            move_indices = [0, 1, 2, 3]
            random.shuffle(move_indices)
            move_keys = list(MOVE_DICT.keys())
            selected_moves = [move_keys[j] for j in move_indices[:4]]
            pkmn = Pokemon(
                name_or_id='pikachu',
                level=5,
                moves=selected_moves,
                gender="male",
                ability="overgrow",
                nature="adamant",
                cur_hp=50,
                stats_actual=[50,50,50,50,50,50],
                ivs=None,
                evs=None
            )
            pokemons.append(pkmn)
    
    return pokemons

# Initialize the trainers with their respective teams
ash_team = create_party("Ash")
misty_team = create_party("Misty")

# Create instances of each class representing the two trainers
ash = Trainer(name="Ash", poke_list=ash_team)
misty = Trainer(name="Misty", poke_list=misty_team)

# Start the battle simulation
battle_simulation = Battle(t1=ash, t2=misty)
battle_simulation.start()

# Simulate turns until one side is defeated
while True:
    turn_actions = {"action": None}
    current_turn = battle_simulation.cur_text
    
    def get_random_valid_action():
        available_moves = ash.current_poke.get_available_moves()

        return [MOVE, random.choice([move.name for move in available_moves])]
        possible_actions = ["switch", "use_item", "select_move"]
        action = random.choice(possible_actions)
        
        if action == "switch":
            return SWITCH
        elif action == "use_item":
            item_target_pos = random.randrange(len(ash.poke_list))
            return [ITEM, "Full Restore", item_target_pos]
        else:
            available_moves = ash.current_poke.get_available_moves()
            if available_moves:
                return [MOVE, random.choice([move.name for move in available_moves])]
    
    try:
        result = battle_simulation.turn(
            t1_turn=get_random_valid_action(),
            t2_turn=get_random_valid_action()
        )
        print("\n".join(battle_simulation.get_cur_text()))
        is_finished = battle_simulation.is_finished()

        if is_finished:
            winner = battle_simulation.get_winner()      
            if winner is not None:   
                print(f'Winner: {winner.name}')
            else:
                print('Battle is a DRAW!')
            break

    except KeyboardInterrupt:
        print("Battle interrupted by user...")
        break

print("The end!")
