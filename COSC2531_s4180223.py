
"""
Pymon skeleton game
@Name: Raman pandey 
@student_id : s4180223
@highest_level_attempted (P/C/D/HD):HD 

- Reflection:
- Reference: 

"""

import random, csv ,sys ,time,datetime


# class for handling item objs 
class Item:
    def __init__(self,name,desc,pickable,consumable):
        self.name =  name 
        self.desc = desc 
        self.pickable =  pickable
        self.consumable =  consumable
    
    
    def __repr__(self):
        return f"Item(<{self.name}>)"
    
   
   
   
# class for handling location obj               
class Location:
    def __init__(self, name = "New room",desc=None, w = None, n = None , e = None, s = None):
        self.__name = name
        self.desc = desc 
        self.doors = {"west":w,"east":e,"north":n,"south":s}
        self.creatures = []
        self.items = []
        
    def add_creature(self, creature):
        self.creatures.append(creature)
    
    def __repr__(self):
        return f"Location(<{self.__name}>)"
    
    def add_item(self, item):
        self.items.append(item)
    
    def connect(self,direction,location):
        self.doors[direction] = location
        
        # connect back in opposite direction
        opposite = {"north": "south", "south": "north", "east": "west", "west": "east"}
        location.doors[opposite[direction]] = self
        
        # beach -> east : forrest then automatically vice versa 
        
        
    def connect_east(self, another_room):
        self.connect("east",another_room)
        
    def connect_west(self, another_room):
        self.connect("west",another_room)
        
    def connect_north(self, another_room):
        self.connect("north",another_room)
        
    def connect_south(self, another_room):
        self.connect("south",another_room)
      
    @property    # getter 
    def name(self):
        return self.__name
    
    @name.setter # setter 
    def name(self,new_name):
        self.__name = new_name
    
    
    def express_location(self):
        print(f"You are at {self.__name} , {self.desc} ")
    
    
    def express_creatures(self):
        for c in self.creatures:
            print(f"Hi player I am {c.name},{c.desc}")
    
    def add_item(self,itemObj: Item):
        
        self.items.append(itemObj)
    
    def express_items(self):
        for j in self.items:
            if j.pickable.strip() == "yes":
                print(f"Hi player , I am {j.name} ,{j.desc} ")
                
                
    def search_(self,list : list,name:  str ):
        itemObj = None
        for item in list:
            if item.name ==  name:
                itemObj =  item
                break 
        return itemObj
    
    def search_creature(self,name : str):
        return self.search_(self.creatures,name)
    
    def search_item(self,name : str):       
        return self.search_(self.items,name)

        
        
        
## class for a creature 
class Creature:
    def __init__(self,name,desc,location):
        self.__name = name
        self.desc =  desc
        self.__location  = location
        self.normal = False 
    
    @property
    def location(self):
        return self.__location
    
    @property 
    def name(self):
        return self.__name
    
    @location.setter
    def location(self,new_loc):
        self.__location = new_loc
    
  
# class for pymon   
class Pymon(Creature):
    def __init__(self, name = "Pymon name",desc= None , location=None):

        #location :  A Location Object not a str 

        super().__init__(name,desc,location=location)
        self._current_location = location
        self._energy_count  =  3 
        self.total_energy_count =  3 
        self._speed =  6  # Inital speed taken if not given 
        self.inventory = []
        self.min_luck_factor  = 20 
        self.max_luck_factor =  50 
        self.race_range = 30  # race of 100 metres 
        self.pogo_stick = False  # if used pogo stick 
        self.step_count  = 0
        self.stats = []
        self.status_opps ={"win":"lose","lose":"win","tie":"tie"}
    
    def move(self, direction):
        try :
             
            new_location  =  self._current_location.doors.get(direction)
            
            if isinstance(new_location,Location):  
                self.step_count += 1
                print(f"Moved from {self._current_location.name} TO {new_location.name}")
                self._current_location = new_location
                
                if self.step_count >= 2:
                    self._energy_count -= 1
                    self.step_count = 0          
                
            else:
                raise InvalidDirectionException(f"Invalid direction: {direction}")
            
        except InvalidDirectionException as e:
            print(e)
            
            
            
    def transfer_from(self, other):
        
        """Adopt inventory and location from another Pymon."""
        
        self.inventory.extend(other.inventory)
        self._current_location = other._current_location
     
    @property       
    def get_location(self):
        return self._current_location
    
    def __repr__(self):
        return f"Pymon(<{self.name}>)"
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self,new_value):
        self._speed =  new_value
    
    @property
    def energy(self):
        return self._energy_count
    
    @energy.setter
    def energy(self,new_count):
        self._energy_count =  new_count
    
    def express_urself(self):
        print(f"My name is {self.name}, I am a {self.desc} ,My energy level is  {self._energy_count}/{self.total_energy_count}")

    
    def calculate_speed(self,luck_factor: int ,pos="pos"):
        
        # luck factor : percentage 
        # pos : ["neg","pos"]
        instant_speed = 0 
        
        if self.min_luck_factor  <= luck_factor <= self.max_luck_factor: 
            if pos  == "pos":
                instant_speed = self._speed + (luck_factor /100)  * self._speed
            else:
                instant_speed = self._speed -  (luck_factor /100) * self._speed
        else:
            print("Luck factor must be in range 20-50% ")
        
        
        #pogo stick factor 
        instant_speed =  instant_speed * 2 if self.pogo_stick == True else instant_speed
        
        return instant_speed
    
    def get_luck(self):
        
        luck =  random.choice(["neg","pos"])
        luck_factor =  random.randint(self.min_luck_factor,self.max_luck_factor)
        instant_speed = self.calculate_speed(luck_factor,luck)
        return instant_speed
    
    def race(self,opp):
        
        
        print(f"\n🏁 Race started between {self.name} and {opp.name}!\n")
        if self.pogo_stick == True :
            print("Using Pogo stick !!!!")
        
        
        status_race=  None 
        
            
        
        distance_elapsed_own = 0.0 
        distance_elapsed_opp =  0.0
        
        
        start = time.time()
        last_time = start

        while True:
            time.sleep(1)
            now = time.time()
            delta = now - last_time
            last_time = now
            
            # get speed based on pos and neg 
            instant_speed = self.get_luck()
            instant_speed_opp = opp.get_luck()
            
            # multiply by time diff => speed * time  = distance 
            distance =   instant_speed * delta
            distance_opp = instant_speed_opp * delta

            distance_elapsed_own += distance
            distance_elapsed_opp += distance_opp
            
            
            # so that the distance dont become negative
            remaining_own = max(self.race_range - distance_elapsed_own, 0)
            remaining_opp = max(self.race_range - distance_elapsed_opp, 0)
            
        
            
            
            print(f"\n {self.name} (your Pymon) hopped {distance :.2f} meters. Distance remaining for {self.name}: {remaining_own :.2f}  meters")
            print(f"{opp.name} (your Pymon) hopped {distance_opp :.2f} meters. Distance remaining for {opp.name}: {remaining_opp:.2f}meters \n")
            
            
            if distance_elapsed_own >= self.race_range and distance_elapsed_opp >= self.race_range:
                print(" 🟰🟰 It's a tie! ")
                status_race  ="tie"        
                break
            
            
            elif distance_elapsed_own >= self.race_range:
                print(f"😎 😎 {self.name} wins the race!")
                print(f"{self.name} Finishes the race first  in {time.time() - start:.2f} seconds !!")
                status_race =  "win"
                break
            
            elif distance_elapsed_opp >= self.race_range:
                print(f"☹️ 😔 {opp.name} wins the race!")
                self._energy_count -= 1 
                print(f"{opp.name} finishes the race first  in {time.time() - start:.2f} seconds !! You lose ")
                status_race = "lose"
                break
        
        
        # append all the data to history 
        histroy_record  =  History(datetime.datetime.now().strftime("%d/%m/%Y %I:%M%p"),opp.name,status_race)
        histroy_record_opp =  History(datetime.datetime.now().strftime("%d/%m/%Y %I:%M%p"),self.name,self.status_opps[status_race])
        self.stats.append(histroy_record)
        opp.stats.append(histroy_record_opp)
        self.pogo_stick = False # pogo stick effect done 

        return status_race
    
    
    def express_inventory(self):
        
        items_connect =  ",".join([item.name for item in self.inventory])
        print("You are carrying :",items_connect)
        
        
    def search_inventory(self,name:str):
        
        itemObj = None
        for item in self.inventory:
            if item.name ==  name:
                itemObj =  item
                break 
        return itemObj

    def pick_item(self,obj : Item):
        self.inventory.append(obj)
    
    
    def use_apple(self):
        
        if self._energy_count <  3:
            self._energy_count +=  1
        
        print(" I ate apple, it is so delecious !!")
        
    def use_pogo_stick(self):
        self.pogo_stick = True 
        print("Pogo stick consumed !!")
        
    
    def use_binocular(self):
        
        direction  =  input("Which direction ?  :")
        
        try : 
                
            if self._current_location.doors.get(direction) == None :
                print("This direction leads nowhere")
            else:
                
                if direction == "current":
                    self._current_location.express_creatures()
                    self._current_location.express_items()
                    self._current_location.express_location()
                
                
                    
                loc =  self._current_location.doors.get(direction)
                
                if isinstance(loc,Location):
                        
                    loc.express_creatures()
                    loc.express_items()
                    loc.express_location()
                else:
                    raise InvalidDirectionException("this direction is not accessible !")
                  
        except InvalidDirectionException as e:
            print(e)
        

    def challenge_to_race(self,name :str ):
        
        status_race  = None 
        
        if len(self._current_location.creatures) > 0 :
            
            cObj =  self._current_location.search_creature(name)
            if cObj != None  and cObj.normal == False:
                print("Creature challenged !")
                status_race =  self.race(cObj)
                return status_race
            else:
                print(f"Cant challenge this creature : {name} !! ")
    
    def display_history(self):
        
        final_text =  f"Pymon Nickname :{self.name}\n "
        if self.stats:
            for idx , h in enumerate(self.stats):
                final_text += f"\nRace {idx +1 }, {h.time} Opponent : '{h.opp}', {h.status}"
            
            print(final_text)
            open("race_stats.txt","w").write(final_text)
            print("rac_stats.txt generated !!, view your history there ")
        else:
            print("You have Done No match yet ...")
               

class InvalidDirectionException(Exception):
    def __init__(self,msg ):
        super().__init__(msg)
        self.msg = msg 


class InvalidInputFileFormat(Exception):
    def __init__(self,msg ):
        super().__init__(msg)
        self.msg = msg 
        
        

# class for managing input files
class Filemanage:
    
    def __init__(self, loc_file="locations.csv", creat_file="creatures.csv", item_file="items.csv"):
        self.loc_file = loc_file
        self.creat_file = creat_file
        self.item_file = item_file
        self.load_from_args()

    def load_from_args(self):
        args = sys.argv[1:]
        if len(args) >= 1:
            self.loc_file = args[0]
        if len(args) >= 2:
            self.creat_file = args[1]
        if len(args) >= 3:
            self.item_file = args[2]
            
        self.location_csv =  self.file_loader(self.loc_file)
        self.creatures_csv =  self.file_loader(self.creat_file)
        self.items_csv =  self.file_loader(self.item_file)
    

    def file_loader(self,filename):
        """Loads a CSV file and returns its content (excluding header)."""
        try:
            file_csv = self.read_csv(filename)
            return file_csv

        except (FileNotFoundError, csv.Error) as e:
            raise InvalidInputFileFormat(f"File not found or invalid format: {filename}") from e


    def read_csv(self,filename):
        """Reads a CSV file and returns a list of rows (excluding header)."""
        with open(filename, "r", newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        return data[1:]  # skip header

        
    
    

class Record:
    def __init__(self):

        self.locations = []
        self.creatures = []
        self.item_list = []
     
    
    def load_files(self):
        
        fm = Filemanage()
        
        locations_csv  = fm.location_csv
        creatures_csv  = fm.creatures_csv
        items_csv =  fm.items_csv
        
        for location in locations_csv :
            self.locations.append(Location(*location))
    
            
        for creature in creatures_csv:
            name,desc,adoptable,speed =  creature
            normal =  True if adoptable.strip() == "no" else False
            pymon_ = Pymon(name,desc=desc,location=None)
            pymon_.speed = float(speed)
            pymon_.normal =  normal
            self.creatures.append(pymon_)

        
        for item in items_csv:
            self.item_list.append(Item(item[0],item[1],item[2],item[3]) )  

    
    
    # fx for connecting location to a direction 
    def connect_loc(self,loc1_,loc2_,direction):
        
        opposite = {"north": "south", "south": "north", "east": "west", "west": "east"}
        
        loc1 =  self.search_location(loc1_)
        loc2 =  self.search_location(loc2_)
        
        #print("LOCATION 1 :",loc1,"Location 2 :",loc2)
        
        try :
            if loc1 != None  and loc2 != None:
                loc1.connect(direction=direction,location=loc2)
                loc2.connect(direction=opposite[direction],location=loc1)
            else:
                raise InvalidDirectionException(f"Invalid direction: {direction}")
        except InvalidDirectionException as e:
            print(e)
    
    
    # fx for placing creature to a location 
    def place_creature(self,name,location):
        creature = self.search_creature(name)
        loc_obj = self.search_location(location)
        
        if creature!= None and loc_obj != None :
            creature.location = loc_obj  
            loc_obj.add_creature(creature)
        else:
            print(f"Either name : {name} ||  Location : {location} not found ")
    
    
    def place_item(self,loc_name,item_name):
        
        item_ = self.search_item(item_name)
        loc_ = self.search_location(loc_name)
        
        if item_ != None and loc_ != None :
            loc_.add_item(item_)
            
    def search_item(self,name:str):
        return self.search_(self.item_list,name)
    
    def search_creature(self,name : str ):
        return self.search_(self.creatures,name)
    
    def search_location(self,name : str):
        return self.search_(self.locations,name)
    
    def search_(self,list : list,name:  str ):
        itemObj = None
        for item in list:
            if item.name ==  name:
                itemObj =  item
                break 
        return itemObj
        
## for history 
    
class History:
    def __init__(self,time,opp,status):
        self.time = time 
        self.opp =  opp 
        self.status =  status    
        

        
class Operations:
    def __init__(self,Record_class : Record):
        
        self.R = Record_class
        self.curr_loc = random.choice(self.R.locations)
        self.current_pymon =  None 
        self.my_pymons = []
    
    def initial_setup(self):
        
        ## write code for randomized location which are logically  connected to each other 
        loc_names = [loc.name for loc in self.R.locations]
        directions = ["north", "south", "east", "west"]

        # Shuffle locations so the order is random
        shuffled = self.R.locations[:]
        random.shuffle(shuffled)

        # For each location, randomly connect to up to 2 other locations (ensuring no duplicates or self-loop)
        for loc in shuffled:
            others = [l for l in shuffled if l != loc]
            connected = set()
            for direction in random.sample(directions, k=min(2, len(others))):
                target = random.choice(others)
                if target not in connected:
                    loc.connect(direction, target)
                    connected.add(target)


        
        self.current_pymon  =  Pymon("Toromon","a white and yellow Pymon with a square face",self.curr_loc)
        self.my_pymons.append(self.current_pymon)
    
        
        
        # randomized location of creatures and items 
        for c in self.R.creatures:
            self.R.place_creature(c.name,random.choice(self.R.locations).name)
               
        for i in self.R.item_list:
            self.R.place_item(random.choice(self.R.locations).name,i.name)

    
    def check_energy_status(self):
        
        
        for c in self.my_pymons:
            
            # if energy out then 
            if c.energy == 0:
                
                self.my_pymons.remove(c)
                
                # move to a random location 
                random_loc =  random.choice(self.R.locations)
                random_loc.creatures.append(c)
                
                # hover over pet list and return the suitable pet 
                if self.my_pymons:
                    self.current_pymon = random.choice(self.my_pymons)   
                    self.current_pymon.transfer_from(c)
                else:
                    self.current_pymon = None       
                    print("No Pymons left in your team!")
                    print("GAME OVER !!")
                    sys.exit()
            
            if c.energy  == 1 and c.name == self.current_pymon.name :
                print(f"[INFO] your energy levels are low , consider eating an apple or changing the pymon !!")

    
    def use_item(self,item):
        
        items_fxs =  {
            "apple":self.current_pymon.use_apple,
            "pogo stick":self.current_pymon.use_pogo_stick,
            "binocular":self.current_pymon.use_binocular
        }
        name = item
        itemObj =  self.current_pymon.search_inventory(name)
        if itemObj != None and name in items_fxs.keys() :
            items_fxs[name]()
            self.current_pymon.inventory.remove(itemObj)
        else:
            print(f"No item of type : {name}")
    
    
    def inspect_pymon(self):
        
        print("1)  Inpect current pymon ")
        print("2)  List and select a benched Pymon to use.")
        
        user_input_inspect =  int(input("Enter what to inspect :"))
        
        try :
            
            if user_input_inspect ==  1:
                self.current_pymon.express_urself()
                
            elif user_input_inspect ==  2:
                
                
                print("You have available pymons :")
                for idx,c in enumerate(self.my_pymons):
                    print(f"{idx + 1})  {c.name}")
                
                py_input =  input("Enter name of pymon to use :").lower().capitalize()
                
                
                for idx,c in enumerate(self.my_pymons):
                    if c.name ==  py_input:
              
                        c.transfer_from(self.current_pymon) # tranfer data 
                        self.curr_loc = c._current_location  # keep world location in sync
                        self.current_pymon = c 
                        print(f"You current pymon is Now : {c.name}")
                        break 
        except ValueError:
            print("Please enter valid command !!")
    
    
    def admin_block(self):
        
        print("Admin Options :\n 1. Add Custom Creature \n 2. Add Custom Location ")
        print("Type cmd number for adding custom features !!")
        verify_input  =  input("Enter 'admin' to proceed further..")
        if verify_input == "admin":
            
            cmd =  int(input("(admin block) Enter your command : "))
            if cmd == 1:
                print("Creature format :  name, desc,adoptable(yes/no)")
                creature = input("Enter Creature details :").split(",")
                if len(creature) == 3:
                    new_creature =  Pymon(*creature)
                    self.R.creatures.append(new_creature)
                    new_creature.express_urself()
                
            
            elif cmd  ==  2:
                print("Location format : name,description,west,north,east,south ")
                location = input("Enter Location details :").split(",")
                if len(location) ==  6:
                    new_location  =  Location(*location)
                    self.R.locations.append(new_location)
                    new_location.express_location()
            else:
                pass
        else:
            print("You are not allowed to enter admin block")

    def save_game(self, filename="savegame.csv"):
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            
            # Save player's pymons
            for pymon in self.my_pymons:
                inv = "|".join([item.name for item in pymon.inventory])
                writer.writerow(["PYMON", pymon.name, pymon.desc, pymon.energy, pymon.speed, inv, pymon._current_location.name])
            
            # Save items
            for item in self.R.item_list:
                writer.writerow(["ITEM", item.name, item.desc, item.pickable, item.consumable])
            
            # Save locations and their creatures/items
            for loc in self.R.locations:
                loc_creatures = "|".join([c.name for c in loc.creatures])
                loc_items = "|".join([i.name for i in loc.items])
                writer.writerow(["LOCATION", loc.name, loc.desc, loc_creatures, loc_items])

            # Save race history
            for pymon in self.my_pymons:
                for hist in pymon.stats:
                    writer.writerow(["HISTORY", pymon.name, hist.time, hist.opp, hist.status])
            
            # Save current game state (current pymon, location, team)
            my_pymon_names = "|".join([p.name for p in self.my_pymons])
            writer.writerow(["CURRENT", self.current_pymon.name, self.curr_loc.name, my_pymon_names])
        
            
    def load_game(self, filename="savegame.csv"):
        
        
        with open(filename, "r", newline='') as f:
            reader = csv.reader(f)
            pymon_map = {}
            item_map = {}
            loc_map = {}
            self.my_pymons.clear()
            self.R.item_list.clear()
            self.R.locations.clear()
            
            for row in reader:
                prefix = row[0]
                if prefix == "PYMON":
                    name, desc, energy, speed, inv, loc_name = row[1:7]
                    pymon = Pymon(name, desc, None)
                    pymon.energy = int(energy)
                    pymon.speed = float(speed)
                    pymon.inventory = []
                    pymon_map[name] = pymon
                    pymon._current_location = Location(loc_name)
                    self.my_pymons.append(pymon)
                elif prefix == "ITEM":
                    item = Item(row[1], row[2], row[3], row[4])
                    item_map[item.name] = item
                    self.R.item_list.append(item)
                elif prefix == "LOCATION":
                    name, desc, creatures, items = row[1:5]
                    loc = Location(name, desc)
                    loc_map[name] = loc
                    self.R.locations.append(loc)
                elif prefix == "HISTORY":
                    pymon_name, time, opp, status = row[1:5]
                    hist = History(time, opp, status)
                    if pymon_name in pymon_map:
                        pymon_map[pymon_name].stats.append(hist)
                elif prefix == "CURRENT":
                    curr_pymon_name, curr_loc_name, my_pymon_names = row[1:4]
                    self.current_pymon = pymon_map.get(curr_pymon_name)
                    self.curr_loc = loc_map.get(curr_loc_name)
                    self.my_pymons = [pymon_map[n] for n in my_pymon_names.split("|") if n in pymon_map]
            
            # Set inventories and location objects for pymons
            for pymon in self.my_pymons:
                if hasattr(pymon, 'inventory'):
                    pymon.inventory = [item_map[name] for name in inv.split("|") if name in item_map]
                pymon._current_location = loc_map.get(pymon._current_location.name, pymon._current_location)

            # Set creatures and items for locations
            for loc in self.R.locations:
                if hasattr(loc, 'creatures'):
                    loc.creatures = [pymon_map[name] for name in creatures.split("|") if name in pymon_map]
                if hasattr(loc, 'items'):
                    loc.items = [item_map[name] for name in items.split("|") if name in item_map]
    
    
    def save_and_load_game(self):
        
        print("\n Options : \n 1. Save game state \n 2. Load game state ")
        cmd = int(input("(saver) Enter command : ").strip())
        options = {1: self.save_game, 2: self.load_game}
        options.get(cmd, lambda: None)()

    def start_game(self):
        print("\nWelcome to Pymon World !!\n")
        print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n")
        print("You started at ",self.curr_loc.name)
        
        user_manuals = [
            "Inspect Pymon",
            "Inspect Current Location",
            "Move",
            "Pick an item",
            "View Inventory",
            "Challenge a Creature ",
            "Generate Stats",
            "Admin Panel",
            "Save and Load game progress",
            "Exit the program "
        ]
        print("Please issue a command to your Pymon :")
        
        for idx, manual in enumerate(user_manuals):
            print(f"{idx + 1}) {manual}")
            
        while True:
            try :
                user_input  = int(input("Your command : "))
                
                if user_input ==  1:
                    self.inspect_pymon()
                
                elif user_input == 2:
                    self.curr_loc.express_location()
                    
                    for  c in self.curr_loc.creatures:
                        c.express_urself()
                    
                    
                elif user_input == 3:
                    new_direction =  input("Moving to which direction  ? ").lower().strip()
                    self.current_pymon.move(new_direction)
                    self.curr_loc =  self.current_pymon.get_location
                    self.check_energy_status()
                
                elif user_input == 4 :
                    
                    if len(self.curr_loc.items) > 0:
                        self.curr_loc.express_items()
                        
                        item_input =  input("Picking what :").lower()
                        itemObj =  self.R.search_item(item_input)
                        if itemObj != None:
                            self.current_pymon.pick_item(itemObj)
                            self.curr_loc.items.remove(itemObj)
                            print(f"You picked up {item_input} from the ground")
                    else:
                        print("No item left in the wild  !!")
                
                elif user_input ==  5:
                    self.current_pymon.express_inventory()
                    print("a. Select an Item to use ")
                    user_item_cmd =  input("(inventory) Enter command :")
                    if user_item_cmd == "a":  
                        item =   input("Which Item ?") 
                        self.use_item( item)
                    
                
                elif user_input == 6:
                    creature_name =  input("Challenge who ? ").lower().capitalize()
                    
                    if self.curr_loc.search_creature(creature_name) != None:
                        status_race  =  self.current_pymon.challenge_to_race(creature_name)
                        
                        if status_race == "win":

                            cObJ = self.curr_loc.search_creature(creature_name) # remove creature from location 
                            self.curr_loc.creatures.remove(cObJ) # and append it to our pet list 
                            self.my_pymons.append(cObJ)
                            print(f"You have Captured  {creature_name} !!")
                        self.check_energy_status()  
                
                elif user_input ==  7 :
                    self.current_pymon.display_history()
                
                elif user_input == 8 :
                    self.admin_block()
                
                elif user_input == 9:
                    self.save_and_load_game()
                    
                
                elif user_input == int(len(user_manuals)) :
                    print("Exiting the Game !!")
                    sys.exit()
            
            except ValueError:
                pass 
        
        
if __name__ == "__main__":


    record = Record()
    record.load_files()

    O = Operations(record)
    O.initial_setup()
    O.start_game()
    

    
    



