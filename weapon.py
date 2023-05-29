import numpy as np
import math
import pyinputplus as pyip

NANOSWORD_BASE_DMG = 2
NANOSWORD_BASE_CRIT = 0.04
LASERGUN_BASE_DMG = 3 
LASERGUN_BASE_CRIT = 0.05 
HAMMER_BASE_DMG = 3 
HAMMER_BASE_CRIT = 0.08 
WEAPON_CRIT_MAX = 0.75

class Weapon: 
  def __init__(self, name, dmg, crit, move_list): 
    self.name = name 
    self.dmg = dmg 
    self.crit = crit 
    self.move_list = move_list

  @property
  def stats(self):
    return """{0} has the following stats:
              Base Damage: {1}
              Base Critical Chance: {2}
              Move_List: {3}
              """.format(self.name, self.dmg, self.crit, self.move_list)

class NanoSword(Weapon): 
  def __init__(self, floor, kill_count):
    dmg = math.ceil(NANOSWORD_BASE_DMG*0.75*floor) + int(np.random.choice(range(floor-1, (kill_count // 4)+1)))
    crit = min(WEAPON_CRIT_MAX, NANOSWORD_BASE_CRIT + (0.03*floor) + (0.03 * int(np.random.choice(range(floor-1, (kill_count // 4)+1))))) # Random Poisson Instead? 
    move_list = ['Fire Slash', 'Needle Strike']
    super().__init__('Nano Sword', dmg, crit, move_list)

  def attack(self, hero, attack_name):
    def fire_slash(dmg, crit):  
      return 'Fire Slash', dmg + (2 * int(np.random.choice([1, 2], p=[1-crit, crit])))

    def needle_strike(dmg, crit):  
      new_crit = crit+0.3 
      return 'Needle Strike', dmg + (1 * int(np.random.choice([1, 2], p=[1-new_crit, new_crit])))

    return dict(zip(self.move_list, [fire_slash, needle_strike]))[attack_name](hero.dmg + self.dmg, hero.crit + self.crit)

class LaserGun(Weapon): 
  def __init__(self, floor, kill_count):
    dmg = math.ceil(LASERGUN_BASE_DMG*0.75*floor) + int(np.random.choice(range(floor-1, (kill_count // 4)+1)))
    crit = min(WEAPON_CRIT_MAX, LASERGUN_BASE_CRIT + (0.02*floor) + (0.02 * int(np.random.choice(range(floor-1, (kill_count // 4)+1))))) # Random Poisson Instead? 
    move_list = ['Gunshot', 'Laser Beam']
    super().__init__('Laser Gun', dmg, crit, move_list) 

  def attack(self, hero, attack_name):
    def gunshot(dmg, crit): 
      return 'Gunshot', dmg + 2 

    def laser_beam(dmg, crit): 
      new_crit = crit+0.1 
      return 'Laser Beam', dmg + (1 * int(np.random.choice([1, 2], p=[1-new_crit, new_crit])))

    return dict(zip(self.move_list, [gunshot, laser_beam]))[attack_name](hero.dmg + self.dmg, hero.crit + self.crit)

class Hammer(Weapon): 
  def __init__(self, floor, kill_count):
    dmg = math.ceil(HAMMER_BASE_DMG*0.75*floor) + int(np.random.choice(range(floor-1, (kill_count // 4)+1)))
    crit = min(WEAPON_CRIT_MAX, HAMMER_BASE_CRIT + (0.03*floor) + (0.04 * int(np.random.choice(range(floor-1, (kill_count // 4)+1))))) # Random Poisson Instead? 
    move_list = ['Hammer Rush', 'Nail Strike']
    super().__init__('Hammer', dmg, crit, move_list)

  def attack(self, hero, attack_name):
    def hammer_rush(dmg, crit):
      return 'Hammer Rush', dmg + (1 * int(np.random.choice([1, 2], p=[1-crit, crit])) * int(np.random.choice([1, 2], 1, p=[1-crit, crit])))

    def nail_strike(dmg, crit): 
      new_crit = crit+0.25 
      return 'Nail Strike', dmg + (2 * int(np.random.choice([1, 2], p=[1-new_crit, new_crit])))
    
    return dict(zip(self.move_list, [hammer_rush, nail_strike]))[attack_name](hero.dmg + self.dmg, hero.crit + self.crit)

# TODO Road Plan: This Class 
# class BioGun(Weapon): 
#   def __init__(self, floor, kill_count):
#     dmg = None
#     crit = None 
#     move_list = []
#     super().__init__('Bio-Gun', dmg, crit, move_list)

#   # Create Move 