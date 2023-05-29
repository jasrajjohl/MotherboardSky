import numpy as np
import math
import pyinputplus as pyip
from weapon import Weapon, NanoSword, LaserGun, Hammer

CRIT_VALUE_MAX = 2
CORPORATE_START_HP = 21
CORPORATE_START_DMG = 2
CORPORATE_START_CRIT = 0.1
CORPORATE_START_CHIPS = 4
PUNK_START_HP = 17
PUNK_START_DMG = 2
PUNK_START_CRIT = 0.2
PUNK_START_CHIPS = 2
DETECTIVE_START_HP = 24
DETECTIVE_START_DMG = 1
DETECTIVE_START_CRIT = 0.15
DETECTIVE_START_CHIPS = 0
AGENT_BASE_HP = 10
AGENT_BASE_DMG = 1
AGENT_BASE_CRIT = 0.07
LABBEAST_BASE_HP = 8
LABBEAST_BASE_DMG = 2
LABBEAST_BASE_CRIT = 0.03
MUTANT_BASE_HP = 12
MUTANT_BASE_DMG = 1
MUTANT_BASE_CRIT = 0.12
EVILSCIENTIST_BASE_HP = 20 
EVILSCIENTIST_BASE_DMG = 3 
EVILSCIENTIST_BASE_CRIT = 0.15 
ENEMY_CRIT_MAX = 0.5
KILL_COUNT_DIVIDEND = 6

class Character: 
  def __init__(self, name, max_hp, hp, dmg, crit): 
    # TODO Road Plan: Add MP/Max MP 
    self.name = name 
    self.max_hp = max_hp 
    self.hp = hp 
    self.dmg = dmg 
    self.crit = crit 
 
  # TODO All Function Descriptions 
  def restore_health(self, restore_val): 
    self.hp = min(self.hp+restore_val, self.max_hp) 
    print('Clean blood courses through your veins once again. It feels cold.')
    print('HP Restored to {}'.format(self.hp))
 
  def attack(self, other): 
    dmg = self.dmg * np.random.choice([1, CRIT_VALUE_MAX], p=[1-self.crit, self.crit]) 
    other.hp -= dmg 
    print('{0} attacked {1} inflicting {2} damage'.format(self.character_name, other.name, dmg))

# Heroes 

class Hero(Character): 
  def __init__(self, character_name, name, max_hp, hp, dmg, crit, left_hand, right_hand, chips=0): 
    self.character_name = character_name
    super().__init__(name, max_hp, hp, dmg, crit)
    self.left_hand = left_hand 
    self.right_hand = right_hand
    self.chips = chips
    self.kill_count = 0 # Number of enemies killed to scale enemy difficulty with player progression 
 
  def increase_health(self, increase_val): 
    self.max_hp += increase_val 
    self.hp += increase_val 
    print('The metal is cold, but it fits right in place.')
    print('Max HP Increased to {}'.format(self.max_hp))
    print('HP Increase to {}'.format(self.hp))
 
  def increase_chips(self, increase_val): 
    self.chips += increase_val 
    plural = ''
    if self.chips != 1: plural = 's' # Add s to statement if plural
    print('More and more chips for the black market.')
    print('You have {0} chip{1}'.format(self.chips, plural))
 
  def add_item(self, item):
    if item.__class__.__mro__[1].__name__ == 'Weapon':
      hand = ''
      if item.name == self.right_hand.name:
        hand = 'Right' 
        self.right_hand = item
        print("A better {} to replace the old and decrepit.".format(item.name))
      elif not self.left_hand: 
        hand = 'Left' 
        self.left_hand = item 
      else: 
        print(self.left_hand.stats)
        print(self.right_hand.stats)
        hand = pyip.inputMenu(['Left', 'Right', 'New Weapon'], 'You only have so many hands. Which weapon do you want to leave behind?\n', numbered=True) 
        if hand == 'Left': 
          self.left_hand = item 
        elif hand == 'Right': 
          self.right_hand = item
      if hand == 'New Weapon': print("Nope no take backs. Toss it if you want. I much appreciate the donation.")
      if not hand: print("You chose not to take the {}. Now why'd you pick it in the first place?".format(item.name))
      else:
        print('You wrap your {0} hand around the grip of the {1}. You feel the metal breathe.'.format(hand.lower(), item.name))
        print('Back to work.')
      
  def attack(self, other, attack_name): 
    if attack_name in self.right_hand.move_list: 
      _, dmg = self.right_hand.attack(self, attack_name) 
    else: 
      _, dmg = self.left_hand.attack(self, attack_name) 

    other.hp -= (dmg)
    print('{0} used {1} on {2} inflicting {3} damage'.format(self.character_name, attack_name, other.name, dmg))

  @property
  def stats(self):
    if not self.left_hand: left_hand_weapon = '' 
    else: left_hand_weapon = self.left_hand.name

    return """{0} is a {1} character with the following stats:
              HP: {2}/{3}
              Base Damage: {4}
              Base Critical Chance: {5}
              Chips: {6}
              Left Hand Weapon: {7}
              Right Hand Weapon: {8}
              """.format(self.character_name, self.name, self.hp, self.max_hp, self.dmg, self.crit, self.chips, left_hand_weapon, self.right_hand.name)

  # TODO Road Plan: Special Moves Functions 

class Corporate(Hero): 
  def __init__(self, character_name, floor): 
    super().__init__(character_name, 'Corporate', CORPORATE_START_HP, CORPORATE_START_HP,
                     CORPORATE_START_DMG, CORPORATE_START_CRIT, None, NanoSword(floor, 0), CORPORATE_START_CHIPS)
 
class Punk(Hero): 
  def __init__(self, character_name, floor): 
    super().__init__(character_name, 'Punk', PUNK_START_HP, PUNK_START_HP,
                     PUNK_START_DMG, PUNK_START_CRIT, None, Hammer(floor, 0), PUNK_START_CHIPS)

class Detective(Hero): 
  def __init__(self, character_name, floor): 
    super().__init__(character_name, 'Detective', DETECTIVE_START_HP, DETECTIVE_START_HP,
                     DETECTIVE_START_DMG, DETECTIVE_START_CRIT, None, LaserGun(floor, 0), DETECTIVE_START_CHIPS)

# Enemies 
 
class Enemy(Character):
  def __init__(self, floor, kill_count): # name, max_hp, hp, dmg, crit,
    # super().__init__(name) 
    # super().__init__(max_hp) 
    # super().__init__(hp) 
    # super().__init__(dmg) 
    # super().__init__(crit) 
    self.moves = {} 
    self.floor = floor 
    self.kill_count = kill_count 
    # TODO Road Plan: Add Unique Enemy Encounter Text 

class Agent(Enemy): 
  def __init__(self, floor, kill_count): 
    self.name = 'Agent' 
    self.max_hp = self.hp = AGENT_BASE_HP
    self.dmg = math.ceil(AGENT_BASE_DMG*0.75*floor) + int(np.random.choice(range(floor-1, (kill_count // KILL_COUNT_DIVIDEND)+1))) 
    self.crit = min(ENEMY_CRIT_MAX, AGENT_BASE_CRIT + (0.03*floor) + (0.02 * int(np.random.choice(range(floor-1, (kill_count // KILL_COUNT_DIVIDEND)+1))))) # Random Poisson Instead? 

  def attack(self, other): 
    def gunshot(dmg, crit):  
      return 'Gunshot', dmg + (2 * int(np.random.choice([1, CRIT_VALUE_MAX], p=[1-crit, crit]))) 

    def karate(dmg, crit):  
      new_crit = crit+0.05 
      return 'Karate', dmg + (1 * int(np.random.choice([1, CRIT_VALUE_MAX], p=[1-new_crit, new_crit]))) 

    attack_name, dmg = np.random.choice([gunshot, karate])(self.dmg, self.crit) 
    other.hp -= dmg 
    print('{0} used {1} on {2} inflicting {3} damage'.format(self.name, attack_name, other.character_name, dmg)) 

class LabBeast(Enemy): 
  def __init__(self, floor, kill_count): 
    self.name = 'Lab Beast' 
    self.max_hp = self.hp = LABBEAST_BASE_HP
    self.dmg = math.ceil(LABBEAST_BASE_DMG*0.75*floor) + int(np.random.choice(range(floor-1, (kill_count // KILL_COUNT_DIVIDEND)+1))) 
    self.crit = min(ENEMY_CRIT_MAX, LABBEAST_BASE_CRIT + (0.02*floor) + (0.02 * int(np.random.choice(range(floor-1, (kill_count // KILL_COUNT_DIVIDEND)+1))))) # Random Poisson Instead? 

  def attack(self, other): 
    def claw_strike(dmg, crit):  
      return 'Claw Strike', dmg + (2 * int(np.random.choice([1, CRIT_VALUE_MAX], p=[1-crit, crit])))

    def tail_whip(dmg, crit):  
      new_crit = crit+0.03 
      return 'Tail Whip', dmg + (1 * int(np.random.choice([1, CRIT_VALUE_MAX], p=[1-new_crit, new_crit])))

    attack_name, dmg = np.random.choice([claw_strike, tail_whip])(self.dmg, self.crit) 
    other.hp -= dmg 
    print('{0} used {1} on {2} inflicting {3} damage'.format(self.name, attack_name, other.character_name, dmg))

class Mutant(Enemy): 
  def __init__(self, floor, kill_count): 
    self.name = 'Mutant' 
    self.max_hp = self.hp = MUTANT_BASE_HP 
    self.dmg = math.ceil(MUTANT_BASE_DMG*0.75*floor) + int(np.random.choice(range(floor-1, (kill_count // KILL_COUNT_DIVIDEND)+1)))
    self.crit = min(ENEMY_CRIT_MAX, MUTANT_BASE_CRIT + (0.04*floor) + (0.02 * int(np.random.choice(range(floor-1, (kill_count // KILL_COUNT_DIVIDEND)+1))))) # Random Poisson Instead? 

  def attack(self, other): 
    def ooze(dmg, crit):  
      return 'Ooze', dmg + 2 

    def body_crash(dmg, crit):  
      new_crit = crit+0.2 
      return 'Body Crash', dmg + (2 * int(np.random.choice([1, CRIT_VALUE_MAX], p=[1-new_crit, new_crit])))

    attack_name, dmg = np.random.choice([ooze, body_crash])(self.dmg, self.crit) 
    other.hp -= dmg 
    print('{0} used {1} on {2} inflicting {3} damage'.format(self.name, attack_name, other.character_name, dmg))

  # Road Plan: Suffocate insta-kill move 

# TODO Road Plan: This Class 
# class Android(Enemy): 
#   def __init__(self, name, hp, dmg, crit, move_a, move_b): 
#     self.name = 'Android' 
#     super().__init__(hp) 
#     super().__init__(dmg) 
#     super().__init__(crit) 
#     self.move_a = move_a 
#     self.move_b = move_b 
 
#  # TODO Road Plan: Create Moves 

# TODO Road Plan: This Class 
# class Machine(Enemy): 
#   def __init__(self, name, hp, dmg, crit, move_a, move_b): 
#     self.name = 'Machine' 
#     super().__init__(hp) 
#     super().__init__(dmg) 
#     super().__init__(crit) 
#     self.move_a = move_a 
#     self.move_b = move_b 

#  # TODO Road Plan: Create Moves 

# Bosses 

class Boss(Enemy): 
  def __init__(self): 
    self.name = ''
    self.hp = None
    self.dmg = None
    self.crit = None

class EvilScientist(Boss): 
  def __init__(self): 
    self.name = 'Evil Scientist' 
    self.hp = EVILSCIENTIST_BASE_HP
    self.dmg = EVILSCIENTIST_BASE_DMG
    self.crit = EVILSCIENTIST_BASE_CRIT

  def attack(self, other): 
    def chemical_flask(dmg, crit):  
      return 'Chemical Flask', dmg + 2 

    def tesla_coil(dmg, crit):  
      new_crit = crit+0.1 
      return 'Tesla Coil', dmg + (1 * int(np.random.choice([1, CRIT_VALUE_MAX], p=[1-new_crit, new_crit])))

    def nano_bots(dmg, crit):  
      return 'Nano Bots', dmg + (1 * int(np.random.choice([1, CRIT_VALUE_MAX], p=[1-crit, crit])))

    attack_name, dmg = np.random.choice([chemical_flask, tesla_coil, nano_bots])(self.dmg, self.crit) 
    other.hp -= dmg 
    print('{0} used {1} on {2} inflicting {3} damage'.format(self.name, attack_name, other.character_name, dmg))
