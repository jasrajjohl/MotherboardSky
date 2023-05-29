import numpy as np
import math
import pyinputplus as pyip
from room import Room, Battle, BossRoom, Rest, Treasure, Shop
from character import Corporate, Punk, Detective

MAX_FLOOR = 1

def generate_level_one(floor_level): 
  # Create all rooms 
  r_1_0 = Room(floor_level) 
  r_1_1 = Battle(floor_level) 
  r_1_2 = Battle(floor_level) 
  r_1_3 = Treasure(floor_level) 
  r_1_4 = Battle(floor_level) 
  r_1_5 = Battle(floor_level) 
  r_1_6 = Battle(floor_level) 
  r_1_7 = Rest(floor_level) 
  r_1_8 = Battle(floor_level) 
  r_1_9 = Treasure(floor_level) 
  r_1_10 = Battle(floor_level) 
  r_1_11 = Battle(floor_level) 
  r_1_12 = Rest(floor_level) 
  r_1_13 = Battle(floor_level) 
  r_1_14 = BossRoom(floor_level) # Boss Room 
  r_1_15 = Shop(floor_level) 
  r_1_16 = Treasure(floor_level) 
  r_1_17 = Battle(floor_level) 

  # Connect all rooms 
              # north, east, south, west 
  r_1_0.connect(r_1_1, r_1_1, r_1_1, r_1_1) 
  r_1_1.connect(r_1_2, r_1_10, None, None) 
  r_1_2.connect(None, None, r_1_1, r_1_3) 
  r_1_3.connect(None, r_1_2, r_1_4, None) 
  r_1_4.connect(r_1_3, None, None, r_1_5) 
  r_1_5.connect(r_1_6, r_1_4, None, None) 
  r_1_6.connect(r_1_8, r_1_9, r_1_5, r_1_7) 
  r_1_7.connect(None, r_1_6, None, None) 
  r_1_8.connect(None, None, r_1_6, None) 
  r_1_9.connect(None, None, None, r_1_6) 
  r_1_10.connect(r_1_11, r_1_17, None, r_1_1) 
  r_1_11.connect(r_1_12, r_1_16, r_1_10, None) 
  r_1_12.connect(r_1_15, None, r_1_11, r_1_13) 
  r_1_13.connect(r_1_14, r_1_12, None, None) 
  r_1_14.connect(None, None, None, None) # Boss Room 
  r_1_15.connect(None, None, r_1_12, None) 
  r_1_16.connect(None, None, None, r_1_11) 
  r_1_17.connect(None, None, None, r_1_10) 

  hero_classes = {'Corporate': Corporate, 'Punk': Punk, 'Detective': Detective}

  return r_1_0, hero_classes

def main(): 
  # Generate field 
  base, hero_class_dict = generate_level_one(MAX_FLOOR) 

  # Title
  print('++++++++++++++++++++++++++++++++++++++++++++++')
  print('++++++++++++++  MOTHERBOARD SKY ++++++++++++++')
  print('++++++++++++++++++++++++++++++++++++++++++++++')
  print()

  pyip.inputStr(prompt='Press "Enter" to begin', blank=True)

  # Opening Cutscene
  print("Out of Semson Tower, a light of black and white rises into the sky and is cracking plane above. With each second the the world distorts and tears apart. Conreet on sidewlaks beginning moving vertically, and all that isn't tied does will never be again.")
  print("But Semson Tower itself remains unscathed. The source of the problem and the source of the solution. If no one is going to do it, you will.")
  print()

  # Character Selection
  hero_class = pyip.inputMenu(['Corporate', 'Punk', 'Detective'], prompt='Which person are you?\n', numbered=True) 
  character_name = pyip.inputStr(prompt="Please enter your character's name") 
  hero = hero_class_dict[hero_class](character_name, base.floor) # Create hero  
  base.hero = hero 
  print(hero.stats) # Gives Hero stats
  print()
  
  print('APPROACH   THE   BULDING')
  print('Enter a direction to start')
  base.exit() 

  # Ending Cutscene
  print("You destroy the generator he guarded and the begin folds in on itself until the world that once was can be remembered again.")
  print("Semson Tower felt alive, but is now the graveyard of so many. It's time to let the dead rest and return to the world.")
  print("You leave Semson Tower and enter a world of beauty.")
  print()
  print('++++++++++++++++++++++++++++++++++++++++++++++')
  print('++++++++++++++++++ THE  END ++++++++++++++++++')
  print('++++++++++++++++++++++++++++++++++++++++++++++')
  print()
  print("Thank you for playing.")

  return  'fin'

main()