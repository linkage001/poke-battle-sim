from __future__ import annotations
import pokemon as pk
import battlefield as bf
import battle as bt
from poke_sim import PokeSim
from move import Move
import random
import global_settings as gs
import global_data as gd
import process_move as pm

def selection_abilities(poke: pokemon.Pokemon, battlefield: bf.Battlefield, battle: bt.Battle):
    if poke.has_ability('drizzle') and battlefield.weather != gs.RAIN:
        battlefield.weather = gs.RAIN
        battlefield.weather_count = 999
        battle._add_text('It started to rain!')
    elif poke.has_ability('limber') and poke.nv_status == gs.PARALYZED:
        pm._cure_nv_status(gs.PARALYZED, poke, battle)
    elif poke.has_ability('insomnia') and poke.nv_status == gs.ASLEEP:
        pm._cure_nv_status(gs.ASLEEP, poke, battle)
    elif poke.has_ability('immunity'):
        if poke.nv_status == gs.POISONED:
            pm._cure_nv_status(gs.POISONED, poke, battle)
        if poke.nv_status == gs.BADLY_POISONED:
            pm._cure_nv_status(gs.BADLY_POISONED, poke, battle)
    elif poke.has_ability('cloud-nine') and battlefield.weather != gs.CLEAR:
            battle._add_text('The effects of weather disappeared.')
            battlefield.weather = gs.CLEAR
    elif poke.has_ability('own-tempo') and poke.v_status[gs.CONFUSED]:
        battle._add_text(attacker.nickname + ' snapped out of its confusion!')
        poke.v_status[gs.CONFUSED] = 0

def end_turn_abilities(poke: pk.Pokemon, battle: bt.Battle):
    if poke.has_ability('speed-boost'):
        pm._give_stat_change(poke, battle, gs.SPD, 1)

def type_protection_abilities(defender: pk.Pokemon, move_data: Move, battle: bt.Battle) -> bool:
    if defender.has_ability('volt-absorb') and move_data.type == 'electric':
        battle._add_text(defender.nickname + ' absorbed ' + move_data.name + ' with Volt Absorb!')
        if not defender.cur_hp == defender.max_hp:
            defender.heal(defender.max_hp // 4)
        return True
    if defender.has_ability('water-absorb') and move_data.type == 'water':
        battle._add_text(defender.nickname + ' absorbed ' + move_data.name + ' with Water Absorb!')
        if not defender.cur_hp == defender.max_hp:
            defender.heal(defender.max_hp // 4)
        return True
    if defender.has_ability('flash-fire') and move_data.type == 'fire':
        battle._add_text('It doesn\'t affect ' + defender.nickname)
        defender.ability_activated = True
        return True
    return False

def on_hit_abilities(attacker: pk.Pokemon, defender: pk.Pokemon, move_data: Move, battle: bt.Battle):
    made_contact = move_data.name in gd.CONTACT_CHECK
    if made_contact and defender.has_ability('static') and random.randrange(10) < 3:
        pm._paralyze(attacker, battle)
    if defender.has_ability('color-change') and move_data.type not in defender.types:
        defender.types = (move_data.type, None)
        battle._add_text(defender.nickname + ' transformed into the ' + move_data.type.upper() + ' type!')
