# Creating Dungeon Crawler Python Test Game 

# Imports 

import numpy as np 
import math 
import pyinputplus as pyip 

MAX_FLOOR = 1
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
NANOSWORD_BASE_DMG = 2
NANOSWORD_BASE_CRIT = 0.04
LASERGUN_BASE_DMG = 3 
LASERGUN_BASE_CRIT = 0.05 
HAMMER_BASE_DMG = 3 
HAMMER_BASE_CRIT = 0.08 
WEAPON_CRIT_MAX = 0.75

# Organisms 

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

# Weapons 

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

class Room: 
  def __init__(self, floor): 
    self.connections = {} 
    self.north = None 
    self.east = None 
    self.south = None 
    self.west = None 
    self.floor = floor 
    self.hero = None 
    self.generated = False 
    self.enemy = None 
    self.items = {} 

  def connect(self, north, east, south, west): 
    self.connections['north'] = north 
    self.connections['east'] = east 
    self.connections['south'] = south 
    self.connections['west'] = west 

  
  def chips_calc(self, floor, kill_count): 
    return int(np.random.choice(range(1* floor, 3*floor))) + int((np.random.choice(range(0, (kill_count // 4)+1))))
    # Max luck: 3 * floor + kill_count // 4 
    # Min luck: 1 * floor + 0 

  def organ_calc(self, floor, kill_count): 
    return  int(np.random.choice(range(math.ceil(1.5*floor), math.ceil(2.75*floor))))
    # Max luck: math.ceil(2.75 * floor) 
    # Min luck: math.ceil(1.5*floor) 

  def enter(self, hero, furnish_num=0): 
    print("A door. You enter another room. How many more can you take?")
    self.hero = hero 
    self.furnish(self.floor, hero.kill_count, furnish_num) 
    self.generated = True 

  def furnish(self, floor, kill_count, num_items): 
    shop_items = np.random.choice([NanoSword, LaserGun, Hammer, self.organ_calc], num_items, False)
    for item in shop_items: 
      new_item = item(floor, kill_count) 
      if isinstance(new_item, int): 
        self.items['Organ'] = new_item 
      else: 
        self.items[new_item.name] = new_item

  def upgrade(self, prices={}): 
    weapons_strings = [weapon.__name__ for weapon in Weapon.__subclasses__()]  # TODO Better Place to Put This? 
    all_items = list(self.items.keys())
    
    for item_name, item in self.items.items():
      if item_name == 'Organ':
        print("There is a metal {0} that will give you {1} more health".format(item_name.lower(), item))
      elif item_name == 'Chips':
        if item == 1: item_name = 'chip'
        print("You see {0} {1} for the taking".format(item, item_name.lower()))
      elif item_name.replace(' ', '') in weapons_strings:
        print("There is a {} lying unattended".format(item_name))
        print(item.stats)
      
      if prices: print("It costs {}".format(prices[item_name])) # Doesn't run with chips

    if len(all_items) == 1: 
      if pyip.inputYesNo(prompt='Are you going to take the {}?'.format(all_items[0])) == 'yes':
        upgrade_path = all_items[0]
      else:
        upgrade_path = ''
        print('A shame to waste what little resources are left.')
    else:
      upgrade_path = pyip.inputMenu(list(self.items.keys()), "Don't be greedy. Pick one from the remaining ash. Who knows who else may need it.\n", numbered=True)     

    price = prices.get(upgrade_path, 0)
    if price > self.hero.chips:
      print("You can't afford this. Buy something else.")
      upgrade_path = ''
    else:
      if upgrade_path == 'Organ': 
        self.hero.increase_health(self.items[upgrade_path]) 
      elif upgrade_path == 'Chips': 
        self.hero.increase_chips(self.items[upgrade_path]) 
      elif upgrade_path.replace(' ', '') in weapons_strings:
        self.hero.add_item(self.items[upgrade_path]) 
      
      if price: self.hero.increase_chips(price * -1) # Decrease Amount by Price if Shopping 

    return upgrade_path 

  def exit(self): 
    direction = None 
    while not direction:
      direction = self.connections[pyip.inputMenu(['north', 'east', 'south', 'west'], 'You have to keep going! Which direction do head in next?\n', numbered=True)]
      print()
      if not direction: 
        no_exit_option_1 = "There's only a wall smeared with blood and oil. This isn't a way out."
        no_exit_option_2 = "You approach the darkness. From the black void, calls ask you to go further. Your body begs you to not go in. You listen."
        no_exit_option_3 = "From the windows of Semson, the efforts you made seem to have no effect on the world outside you're losing. You have to go further, there must be a door somewhere here."
        print(np.random.choice([no_exit_option_1, no_exit_option_2, no_exit_option_3]))

    direction.enter(self.hero) 

class Battle(Room): 
  def __init__(self, floor):
    super().__init__(floor)

  def enter(self, hero): 
    if not self.generated: 
      super().enter(hero) 
      self.battle(hero, self.enemy) 
      self.upgrade() 
    else:
      print("You've already been in this room. You don't hear a thing.")
    self.exit()

  def furnish(self, floor, kill_count, num_enemies): # Do Room Generation Function 
    # super.furnish(self.floor, self.hero.kill_count, 0) # TODO Check If Works 
    self.enemy = np.random.choice([Agent, LabBeast, Mutant])(floor, kill_count) 
    weapon = np.random.choice([NanoSword, LaserGun, Hammer])(floor, kill_count) 
    self.items[weapon.name] = weapon 
    self.items['Chips'] = self.chips_calc(floor, kill_count) 
    self.items['Organ'] = self.organ_calc(floor, kill_count) 

  def battle(self, hero, enemy): 
    print("Scraping comes from the vents. You can tell it's moving. Be prepared.")
    print("YOU   ARE  NOT   ALONE")
    while hero.hp > 0: 
      right_hand_moves = hero.right_hand.move_list 
      if not hero.left_hand: 
        left_hand_moves = [] 
      else: 
        left_hand_moves = hero.left_hand.move_list 

      print()
      hero.attack(enemy, pyip.inputMenu(left_hand_moves + right_hand_moves, 'How are you going to fight it?!\n', numbered=True))

      if enemy.hp > 0: 
        enemy.attack(hero) 
      else: 
        print("The {} perishes in front of you.".format(enemy.name))
        self.enemy = None
        hero.kill_count += 1
        print("You live another day.")
        print()
        return 

    print("This was a mistake. It cost your life and everyone else.")
    # if pyip.inputStr(prompt="Would you like to try again?") == 'yes': # TODO Ask to Try Again, If Yes Clear and Run main() again 
    #    main()
    # else:
    print("Maybe in another life.")
    print('++++++++++++++++++++++++++++++++++++++++++++++')
    print('+++++++++++++++++  GOODBYE.  +++++++++++++++++')
    print('++++++++++++++++++++++++++++++++++++++++++++++')
    raise SystemExit(0) # Kill Switch


class BossRoom(Battle): 
  def __init__(self, floor):
    super().__init__(floor)
    self.stairs = None

  def enter(self, hero): 
    if not self.generated: 
      self.hero = hero
      self.furnish(self.floor, hero.kill_count, 0) 
      self.battle(hero, self.enemy)
      self.generated = True
    else:
      print("You've already been in this room. You don't hear a thing.")
    self.exit()

  def furnish(self, floor, kill_count, num_enemies): # No Reward, Just Final Boss 
    self.enemy = EvilScientist() 
    print("The lights flicker faster than you can track. All you hear is laughing. Laughing and laughing.")

  def exit(self): 
    print("The mad scientist falls to the ground laughing and bleeding. His screeching fills the hall even after he's dead.")
    if self.floor == MAX_FLOOR: # If Ending
      return 
    else:
      self.stairs.enter(self.hero) # Go to next floor

class Rest(Room): 
  def __init__(self, floor):
    super().__init__(floor)

  def enter(self, hero): 
    if not self.generated: 
      self.hero = hero 
      print("The room is empty except for a fridge full of blood bags ready to be taken.")
      self.hero.restore_health(self.hero.max_hp) 
      self.generated = True 
    else: 
      print("You've already been in this room. The fridge is open. All that's left is one blood bag half gone and bleeding onto the floor.")
    self.exit()

class Treasure(Room): 
  def __init__(self, floor):
    super().__init__(floor)

  def enter(self, hero): 
    if not self.generated: 
      super().enter(hero, 1) 
      self.generated = True 
      print("There's no one here. All you hear is the metal hum in every direction. You're in an R&D Lab.")
      self.upgrade() 
    else: 
      print("You've already been in this room. There's nothing else to take. You'll have to live with what you have.")
    self.exit()

class Shop(Room): 
  def __init__(self, floor):
    super().__init__(floor)
    self.empty = False 
    self.costs = {} 

  def shop(self, continuing=''): 
    shop_path = pyip.inputYesNo("Alright, c'mon. You gonna help me out and buy something{}?".format(continuing)) 
    if shop_path == 'yes': 
      if self.hero.chips < max(self.costs.values()): 
        print("Jeez, I think you have less money than me. That's just sad. Come back when you have more chips or else I might cry.")
      else: 
        bought = self.upgrade(self.costs) 
        self.items.pop(bought, None) 
        self.costs.pop(bought, None) 
        if len(self.items.keys()) > 0: 
            self.shop(' else') 
        else: 
          self.empty = True 
          print("You bought it all. You cleaned me out. You're a lifesaver man. Now to find something else to sell.")
          print("WAIT! Actually, could donate me some chips?")
    else: 
      print("Aww man, don't leave me hanging man. I really need a new car.") 

  def furnish(self, floor, kill_count, furnish_num): 
    super().furnish(floor, kill_count, 3) 
    for item in list(self.items.keys()): 
      if item == 'Organ': 
        cost = 9 
      else: 
        cost = 20 
      self.costs[item] = cost 

  def enter(self, hero): 
    if not self.generated: 
      super().enter(hero) 

      # Shop Keeper Dialogue
      print("Wait! Please I'm unarmed!")
      print("Can you believe all this is happening? It's a nightmare, my worst nightmare.")
      print("I came here to work in Semson Tower cause it was safe and stable, and everyone said I could work here for the rest of my life and take it easy with good pay, even for a janitor!")
      print("Now the towers shooting a beam into the sky and I'm stuck here... WITHOUT A JOB!")
      print("Look man, I NEEEEEEED some money. Please, I stole these from the R&D Department, before the Tower shot a beam into the sky or after, who knows.")
      print("Anywaaaaays please buy something. I'll trade you whatever I got for those chips you're stashing.")
    if not self.empty: 
      self.shop()
    else:
      print("You've already been in this room. The man desparate for money is nowhere to be.")
    self.exit()
    # self.exit(pyip.inputMenu(['north', 'east', 'south', 'west'], '')) 

# Guess a number to finish Boss Super attack move? 

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