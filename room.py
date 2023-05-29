import numpy as np
import math
import pyinputplus as pyip
from weapon import Weapon, NanoSword, LaserGun, Hammer
from character import Agent, LabBeast, Mutant, EvilScientist

MAX_FLOOR = 1

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