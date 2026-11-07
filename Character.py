import pygame
#from Main import Weapon_hitboxes
import time

class Node:
    def __init__(self, coords, target, cost, map, Node_map, parent):
        '''
        Assigns everything a variable and then checks whether it is traversable and it also splits up the
        1st parameter: coords into and x and y integer it then runs the self.__Heuristics function
        Calculates the total distance and creates a variable to store it (movement_cost+heuristics)
        creates a variable with a list and a variable to check when it has been traversed.
        :param coords:
        :param target:
        :param cost:
        :param map:
        :param Node_map:
        :param parent:
        '''
        self.__coords = coords
        self.__parent = parent
        self.__map = map
        self.__Node_map = Node_map
        if map[coords[0]][coords[1]] == 0: # checks if the space is traversable if 1 it is not
            self.__traversable = True
        else:
            self.__traversable = False

        self.__target = target
        self.__y = self.__coords[0] # [y,x] because in the map the y direction is the first index
        self.__x = self.__coords[1]
        self.__movement_cost = cost
        self.__Heuristics()
        self.__Total_distance = self.__movement_cost + self.__heuristics

        self.__Nieghbours = []
        self.__traversed = False

    def __Heuristics(self):
        '''
        Does the Heuristics equation which is (x + y) + ((2**0.5) * x or y) depending on which one
        is smaller this is saved as one of the classes variables.
        :return:
        '''
        distance_x = abs(self.__x - self.__target[1])
        distance_y = abs(self.__y - self.__target[0])
        if distance_x < distance_y:
            self.__heuristics = (distance_x + distance_y) + ((2 ** 0.5) * distance_x)
        else:
            self.__heuristics = (distance_x + distance_y) + ((2 ** 0.5) * distance_y)

    def create_neighbours(self):
        '''
        Creates a list of the coords of the neigbhours next to it
        :return:
        '''
        Nieghbours = []


        directions = [(1, 0, 1), (1,-1, 2**0.5), (0, 1, 1),  (1,1, 2**0.5),(-1, 0, 1), (-1,-1, 2**0.5),(0, -1, 1), (-1,1, 2**0.5)]
        checks = []
        for i in directions:
            if self.__y + i[0] > -1 and self.__y + i[0] < len(self.__map) and self.__x + i[1] > -1 and self.__x + i[1] < len(self.__map[1]):
                checks.append(True)
            else:
                checks.append(False)
        for i in range(len(directions)):
            if checks[i]:
                Nieghbours.append([self.__y + directions[i][0], self.__x + directions[i][1], directions[i][2]])

        self.__Nieghbours = Nieghbours




    def check_neighbours(self):
        '''
        This is the A* algorithm. It first checks if it is the target if not it looks through its
        neighbours. It then checks if it can be traversed if it can it checks that it gives a smaller distance to the target
        if it does it runs the function update node map appends its coords to the a list and then returns that list the list
        is the return of a check neighbours function of the neigbhour with a smaller distance.
        :param travelled_distance:
        :param new_distance:
        :return:
        '''
        if self.__traversable:
            self.Traveled()
            new_distance = self.give_distance()# The new distance to find a smaller distance of

            if self.__coords == self.__target:
                self.__traversed = False
                return [self.__coords] # send back a list of all the moves

            for neighbour in self.__Nieghbours:

                neighbour_Node = self.__Node_map[neighbour[0]][neighbour[1]] # gets the Node class ascosiated with those coords
                #if neighbour_Node.check_traverse(): # checks it can be traversed
                #sets variables
                neighbour_Node.set_parent(self.__coords)
                neighbour_Node.update_movement_cost(neighbour[2])
                neighbour_Node.update_target(self.__target)



                if neighbour_Node.give_distance() < self.__Total_distance and not neighbour_Node.check_traveled():
                    #This if statment checks if the distance is smaller between them and the target than this node
                    #if they have been traversed yet

                    next_current = neighbour # sets next current to nighbour
                    self.__Node_map[neighbour[0]][neighbour[1]] = neighbour_Node # makes sure that map has the updated node
                    for Node_line in self.__Node_map:
                        for Node in Node_line:
                            Node.update_Node_map(self.__Node_map) # sends out updadted node list to other nodes
                    list = self.__Node_map[next_current[0]][next_current[1]].check_neighbours()
                    if list == None:
                        list = []
                    self.__traversed = False # resets traversal
                    list.append(self.__coords) # puts their coords onto the list
                    return list


    def set_parent(self, parent):
        '''
        Takes parameter and assigns it to a class variable
        :param parent:
        :return:
        '''
        self.__parent = parent

    def update_target(self, target):
        '''
        Takes parameter and assigns it to a class (target) variable it then runs the __Heuristics function
        and then recalculates the class variable "total distance"
        :param target:
        :return:
        '''
        self.__target = target
        self.__Heuristics()
        self.__Total_distance = self.__movement_cost + self.__heuristics

    def update_movement_cost(self, cost):
        '''
        Takes parameter and assigns it to class variable "Movement cost"
        :param cost:
        :return:
        '''
        self.__movement_cost = cost


    def update_Node_map(self, map):
        '''
        Takes parameter and assigns it to the class variable "Node map"
        :param map:
        :return:
        '''
        self.__Node_map = map

    def give_coords(self):
        '''
        return class variable "coords"
        :return:
        '''
        return self.__coords

    def give_neighbours(self):
        '''
        return class variable "Neighbours"
        :return:
        '''
        return self.__Nieghbours

    def check_traverse(self):
        '''
        Return class variable "traversable"
        :return:
        '''
        return self.__traversable

    def give_distance(self):
        '''
        returns class variable "total distance"
        :return:
        '''
        return self.__Total_distance

    def check_traveled(self):
        '''
        Returns class variable "traversed"
        :return:
        '''
        return self.__traversed

    def Traveled(self):
        '''
        Assigns True to class variable "traversed"
        :return:
        '''
        self.__traversed =True


class C: # Connection
    def __init__(self):
        '''
        Creates class Variables:
        "coords" : None
        "player" : object of character class
        "map" : list
        It then runs the function coords recieve and weapon hitbox recieve
        '''
        self.coords = None
        self.player = Character_class()
        self.monsters = []
        self.map = []


        self.coords_recieve()
        self.weapon_hitbox_recieve()

    def create_monsters(self, monsters_n, placement_coords, room):
        '''
        loops number of times for the 1st parameter and appends the class variable "monsters" with an
        instance of the monster class for so many times it loops for
        :param monsters_n:
        :param placement_coords:
        :param room:
        :return:
        '''
        for i in range(monsters_n):
            self.monsters.append(Monster(self.coords, placement_coords, room))


    def coords_recieve(self):
        '''
        sets the class variable "coords" to the return value of the object player`s return of give cord.
        :return:
        '''
        self.coords = self.player.give_coord()

    def player_room_active(self, room):
        for i in self.monsters:
            i.get_active_room(room)

    def weapon_hitbox_recieve(self):
        '''
        sets the class variable "weapon hitbox" to the objects player return of give weapon group
        :return:
        '''
        self.weapon_hitbox = self.player.give_weapon_group() # function returns pygame group that is used as a hitbox with the collide sprite function
    def coords_give(self):
        '''
        loops through class variable list of monsters and each loop it gives that monster the coords
        via the function recieve coords from the monster class
        :return:
        '''
        for i in self.monsters:
            i.recieve_coords(self.coords)


    def map_get(self, map):
        '''
        Sets parameter to class variable "map"
        :param map:
        :return:
        '''
        self.map = map


    def map_give(self):
        '''
        loops through every monster in its list and gives them all a map via the recieve map function
        from the monster class.
        :return:
        '''
        for i in self.monsters:
            i.recieve_map(self.map)

    def damage_bits(self,players):
        '''
        gets 2 variables form the player class function give damage bits. It then loops through
        monster list and runs function from monster class set damage bits and if they died it removes them from the game.
        :return:
        '''
        damage,attacking = self.player.give_damage_bits()
        for i in self.monsters:
            i.set_damage_bits(attacking,damage)
            if i.dying():
                self.monsters.remove(i)
                players.remove(i)


class Character_class(pygame.sprite.Sprite):
    def __init__(self):
        '''
        This sets up the character class`s Varaibles and loads the image
        that is a sprite sheet it also inizilises the weapon class as a variable
        '''
        super().__init__()
        self.__Health = 50
        self.__gold = 0
        self.__weapon_type = 'sword'
        self.__dashing = False
        self.__dash_counter = 0
        self.__invunrebility = False
        self.__colour = (255, 255, 255)
        self.__sheet = pygame.image.load('images/sprite_sheet.png')#.convert_alpha()
        pygame.draw.rect(self.__sheet, self.__colour, self.__sheet.get_rect(),1)  # display of rect to be taken out only used for testing
        self.__width = 25
        self.__height = 25
        self.__frame = 0
        self.__walking = False
        self.image = pygame.Surface([self.__width,self.__height])
        self.image.fill((1,0,0))
        self.image.blit(self.__sheet, (0, 0), (0, 0, self.__width, self.__height))
        self.image.set_colorkey((1,0,0))

        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 200
        self.__walls = None

        #set up collisions
        self.last_move = []
        pygame.draw.rect(self.__sheet, self.__colour, self.rect,1)  # display of rect to be taken out only used for testing

        #WEAPON
        self.__weapon = Weapon(1, self.__weapon_type, 1)
        self.__weapon_group = pygame.sprite.Group()
        self.__weapon_group.add(self.__weapon.give_hit_boxes()[0])
        self.__weapon_group.add(self.__weapon.give_hit_boxes()[1])

    def wall_setter(self, walls):
        '''
        Sets parameter to class variable "walls"
        :param walls:
        :return:
        '''
        self.__walls = walls
    def give_coord(self):
        '''
        returns a list of its y coord and x coord
        :return:
        '''
        return [self.rect.y,self.rect.x]
    def set_coords(self, coords):
        '''
        sets the parameter[0] to the y coord and parameter [1] to the x coord
        It also mutliplies the y coord by 15 and x coord by 20 so that it is the
        coords of specific pixles.
        :param coords:
        :return:
        '''
        self.rect.y = coords[0] * 15
        self.rect.x = coords[1] * 20
    def give_weapon_group(self):
        '''
        Returns class variable "weapon group"
        :return:
        '''
        return self.__weapon_group
    def give_damage_bits(self):
        '''
        This returns the damage of the weapon from weapon.give damage
        and returns if the player is attacking from weapon. attacking
        :return: damage , attacking
        '''
        damage = self.__weapon.give_damage()
        attacking = self.__weapon.attacking()
        return damage,attacking
    def __collisions(self):
        '''
        checks if a collision is made with the player and the wall
        If it has it uses the class variable "last move" to determine which
        direction the players icon is moved so that it is no longer coliding with the wall

        :return:
        '''
        if pygame.sprite.spritecollide(self, self.__walls, False):
            self.__colour = (0, 255, 0)
            for i in self.last_move:
                if i == 'w':
                    self.rect.y += 1

                if i == 's':
                    self.rect.y -= 1

                if i == 'a':
                    self.rect.x += 1

                if i == 'd':
                    self.rect.x -= 1
    def __movement(self):
        '''
        creates a varibale of a boolean list of all inputs
        it gets the position of the mouse
        sets class variable invunrability to false
        checks if player is dashing if it is dash counter goes up 1 and if dash counter is 100 then dashing is false dash counter is set to 0
        then it checks if player is holding left control if so then the player dashes 30 pixles towards the mouse
        after this it checks for every input of W A S or D and then moves the player in that respective direction (0.5 pixles if holding shift or 1 if not)
        :return:
        '''
        inputs = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pos()
        self.__invunrebility = False
        if self.__dashing:
            self.__dash_counter += 1
            if self.__dash_counter == 1000:
                self.__dashing = False
                self.__dash_counter = 0


        if inputs[pygame.K_LCTRL] and self.__dashing == False:
            if self.rect.x < mouse[0]:
                amount = mouse[0] - self.rect.x
                if amount > 30:
                    self.rect.x += 30
                else:
                    self.rect.x += amount

            elif self.rect.x > mouse[0]:
                amount =self.rect.x - mouse[0]
                if amount > 30:
                    self.rect.x -= 30
                else:
                    self.rect.x -= amount

            if self.rect.y < mouse[1]:
                amount = mouse[1] - self.rect.y
                if amount > 30:
                    self.rect.y += 30
                else:
                    self.rect.y += amount

            elif self.rect.y > mouse[1]:
                amount =self.rect.y - mouse[1]
                if amount > 30:
                    self.rect.y -= 30
                else:
                    self.rect.y -= amount

            self.__dashing = True
            self.__invunrebility = True


        if inputs[pygame.K_LSHIFT]:
            if inputs[pygame.K_w]:
                self.last_move.append('w')
                self.rect.y -= 0.5
                self.__walking = True

            if inputs[pygame.K_s]:
                self.last_move.append('s')
                self.rect.y += 0.5
                self.__walking = True


            if inputs[pygame.K_a]:
                self.last_move.append('a')
                self.rect.x -= 0.5
                self.__walking = True


            if inputs[pygame.K_d]:
                self.last_move.append('d')
                self.rect.x += 0.5
                self.__walking = True


        elif not inputs[pygame.K_LSHIFT]:
            if inputs[pygame.K_w]:
                self.last_move.append('w')
                self.rect.y -= 1
                self.__walking = True



            if inputs[pygame.K_s]:
                self.last_move.append('s')
                self.rect.y += 1
                self.__walking = True


            if inputs[pygame.K_a]:
                self.last_move.append('a')
                self.rect.x -= 1
                self.__walking = True

            if inputs[pygame.K_d]:
                self.last_move.append('d')
                self.rect.x += 1
                self.__walking = True


        else:
            self.__walking = False

        if len(self.last_move) > 15:
            self.last_move = []
    def __animation(self):
        '''
        A function that swaps between pictures on the sprite sheet to make it look like the character is walking
        :return:
        '''
        if self.__walking == True:
            self.image = self.__get_image(self.__frame)
            self.__frame += 1
            if self.__frame == 5:
                self.__frame = 0
    def update(self):
        '''
        Where every function that runs every loop is ran from thatare to do with the character class
        :return:
        '''
        self.__movement()
        self.__collisions()
        self.__weapon.coords([self.rect.y,self.rect.x])
        self.__weapon.input()

    def give_gold(self, gold):
        '''
        takes the variable and adds it the character class variable "gold".
        :param gold:
        :return:
        '''
        self.__gold += gold

    def take_gold(self, gold):
        '''
        takes the parameter and takes it away from the vaaribale gold
        :param gold:
        :return:
        '''
        self.__gold -= gold

    def return_gold(self):
        return self.__gold

    def return_health(self):
        return self.__Health

    def give_health(self):
        self.__Health +=5

    def give_damage(self):
        self.__weapon.increase_damage()

    def return_damage(self):
        damage = self.__weapon.give_damage()
        return damage

    def __get_image(self,frame):
        '''
        selects the image of the sprite sheet of the specific frame is needed in that animation and puts it on as the one that is being used
        :param frame:
        :return:
        '''
        image = pygame.Surface((self.__width, self.__height)).convert_alpha()
        image.fill((1,0,0))
        image.blit(self.__sheet, (0, 0), ((frame * self.__width), 0, self.__width, self.__height))
        image.set_colorkey((1,0,0))
        return image

    def give_weapon(self):
        '''
        Returns the sprites of the hitboxes of the weapon
        :return:
        '''
        return self.__weapon.give_hit_boxes()

    def take_damage(self, damage):
        self.__Health -= damage
        if self.__Health <= 0:
            return True
        else:
            return False


class Weapon():
    def __init__(self, damage, type, size):
        '''
        Sets up all the variables of the weapon class and initilises to instances of the weapon sprite class
        :param damage:
        :param type:
        :param size:
        '''
        # variables
        self.__size = size
        self.__damage = damage
        self.__type = type
        self.__Attacking = False
        self.__count = 0

        #pygame
        self.__Side_hitbox = Weapon_sprite(self.__size, (0,0), True)
        self.__Top_Bottom_hitbox = Weapon_sprite(self.__size, (0, 0), False)

    def input(self):
        '''
        Checks if the R key has been pressed and if "count" is 0
        if it has it sets "attacking" to true
        and "count" is set to 100
        while Attacking is False and "count" is not 0
        1 is taken away from "count"
        :return:
        '''
        inputs = pygame.key.get_pressed()
        if inputs[pygame.K_r] and self.__count == 0:
            self.__Attacking = True
            self.__count = 100
        else:
            self.__Attacking = False
            if self.__count !=0:
                self.__count -= 1

    def coords(self, coords):
        '''
        Sets the coords of the 2 weapon sprite classes inside of weapon by running
        the .coords function of the weapon sprite class
        :param coords:
        :return:
        '''
        self.__Side_hitbox.coords(coords)
        self.__Top_Bottom_hitbox.coords(coords)

    def give_hit_boxes(self):
        '''
        Returns the 2 instances of the class weapon sprites
        :return:
        '''
        return [self.__Side_hitbox, self.__Top_Bottom_hitbox]

    def give_damage(self):
        '''
        return the damage of the weapon
        :return:
        '''
        return self.__damage

    def attacking(self):
        '''
        If "attacking" is true then the weapon sprtie function attacking is run
        If count is 0 the hitboxes reset with the reset function of weapon sprite
        Then "attack" is returned
        :return:
        '''
        if self.__Attacking:
            self.__Side_hitbox.attacking()
            self.__Top_Bottom_hitbox.attacking()
        elif self.__count == 0:
            self.__Side_hitbox.reset()
            self.__Top_Bottom_hitbox.reset()
        return self.__Attacking

    def increase_damage(self):
        self.__damage += 1


class Weapon_sprite(pygame.sprite.Sprite):
    def __init__(self, size, coords, side):
        '''
        It sets the weapon Sprites classes variables then it checks the Boolean parameter "side"
        if it is True or False it will take a different surface of the inverse of eachother
        This creates the two hitboxes
        :param size:
        :param coords:
        :param side:
        '''
        super().__init__()
        #Variables
        self.__size = size
        self.__coords = coords
        self.__side = side
        #pygame bits
        if self.__side:
            self.image = pygame.Surface([60 * size, 20 * size])

        else:
            self.image = pygame.Surface([20 * size, 60 * size])

        self.image.fill(('lightgrey'))

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def coords(self, coords):
        '''
        It checks where the mouse is on the screen
        It sets the list parameter "coords" to the coordinates of the rect
        It then changes the coords of the Sprite to face to where the mouse is.
        :param coords:
        :return:
        '''
        mouse_pos = pygame.mouse.get_pos()
        if self.__side: # if it is the vertical hitboxes
            if mouse_pos[1] < coords[0]:
                self.rect.x = coords[1] - 20 * self.__size
                self.rect.y = coords[0] - 15 * self.__size

            elif mouse_pos[1] > coords[0]:
                self.rect.x = coords[1] - 20 * self.__size
                self.rect.y = coords[0] + 25 * self.__size

        else:
            if mouse_pos[0] < coords[1]:
                self.rect.x = coords[1] - 25
                self.rect.y = coords[0] - 20 * self.__size

            elif mouse_pos[0] > coords[1]:
                self.rect.x = coords[1] + 25
                self.rect.y = coords[0] - 20 * self.__size

    def attacking(self):
        '''
        Depending on the "side" boolean varibale it cheanges the colour of the rect to
        red or yellow.
        :return:
        '''
        if self.__side:
            pygame.draw.rect(self.image, (255, 0, 0), self.image.get_rect())

        else:
            pygame.draw.rect(self.image, 'yellow', self.image.get_rect())

    def reset(self):
        '''
        Fills the image with the colour light grey
        :return:
        '''
        self.image.fill(('lightgrey'))

class Monster (pygame.sprite.Sprite):
    def __init__(self, target, coords, room):
        '''
        Sets up the varibales of the Monster Class
        :param target:
        :param coords:
        :param room:
        '''
        super().__init__()
        self._multiplier = 1
        self.__health = self._multiplier * 10
        self.__Damage = 1 * self._multiplier
        self.image = pygame.image.load('images/monster.png')
        self.rect = self.image.get_rect()
        self.rect.x = coords[1]
        self.rect.y = coords[0]
        self.__player_coord = [0,0]
        self.__target_x = None
        self.__target = target
        self.__target_y = None
        self.__t_y_node = 0
        self.__t_x_node = 0
        self.__count = 0
        self.__Same_target = False
        self.__taking_damage = False
        self.__player_damage = 0
        self.__weapon_hitboxes = None
        self.__room = room
        self.__active_room = 0
        self.__walls = None
        self.__last_move = []
        self.__movement_list = []
        self.__damage_count = 0

    def update(self):
        '''
        Where all the function of the monster class are ran from each loop
        :return:
        '''
        if self.__room_check():
            self.__detection()
            self.__movement()
            self.__collision()
            self.__take_damage()

    def recieve_coords(self, coords):
        '''
        it takes the "coords" list paremeter and checks if coords are the same
        if they are a boolean variable "Same Target" is set as True
        if not "target coords" are aset as coords and "Same Target" is set to False
        and integer variable "count" is set to 0
        :param coords:
        :return:
        '''
        if coords == self.__target:
            self.__Same_target = True
        else:
            self.__target = coords
            self.__Same_target = False
            self.__count = 0

    def recieve_map(self,map):
        '''
        Sets 2d list parameter "map" to the class varibale "map"
        :param map:
        :return:
        '''
        self.__map = map

    def recieve_weapon_hitbox(self, group):
        '''
        Assiigns the object parameter "group" to the class variable "weapon hitboxes"
        :param group:
        :return:
        '''
        self.__weapon_hitboxes = group

    def __detection(self):
        '''
        It checks if it has the same target if not it runs the check neighbour function of the class node to detect where the player is.
        :return:
        '''


        starting_x = self.rect.x // 100  # 20
        starting_y = self.rect.y // 100  # 15
        #Discover patha

        #set nodes
        #new_t_y_node = self.__target[0] // 100
        #new_t_x_node = self.__target[1] // 100

        self.__t_y_node = self.__target[0] // 100
        self.__t_x_node = self.__target[1] // 100

        target = [self.__t_y_node, self.__t_x_node]

        current = self.__map[starting_y][starting_x]

        current.update_target(target)

        if current.give_coords() == target:
           self.__target_x = self.__target[1]
           self.__target_y = self.__target[0]

           if self.rect.x > self.__target_x:
               self.__target_x += 15

           else:
               self.__target_x -= 15

           if self.rect.y > self.__target_y:
               self.__target_y += 15

           else:
                self.__target_y += 15

        elif self.__Same_target == False:
            movement_list = current.check_neighbours()
            if movement_list != None:
                self.__movement_list = movement_list
                self.__movement_list.reverse()

            self.__target_x = self.__movement_list[0][1] * 100# give coords of first node to travel too
            self.__target_y = self.__movement_list[0][0] * 100

        else:
            self.__target_x = self.__movement_list[self.__count][1] * 100  # give coords of first node to travel too
            self.__target_y = self.__movement_list[self.__count][0] * 100

            if starting_x == self.__target_x // 100 and starting_y == self.__target_y // 100 and self.__count != len(self.__movement_list) - 1:
                self.__count += 1

    def __room_check(self):
        '''
        Make a variable that tells the monster what room it is in (self variable)
        Make a variable that tells what rooms the player is in (self variable of a player variable)
        if this number is the same then they are in the same room therefore detection function should start
        :return:
        '''
        if self.__active_room == self.__room:
            return True
        else:
            return False

    def get_active_room(self,room):
        self.__active_room = room

    def __take_damage(self):
        '''
        It checks if a collision has occured and if so then it checks wether
        it should be taking damage if so it takes damage up to the damage of the characters damage
        :return:
        '''
        if pygame.sprite.spritecollide(self,self.__weapon_hitboxes,False):
            if self.__taking_damage:
                self.__health -= self.__player_damage

    def set_damage_bits(self,taking,damage):
        '''
        Assigns the parameters to "taking damage" a Boolean varibale to check
        wether the monster should be taking damage
        and "player damage" and integer varibale that stores how much damage the player does
        :param taking:
        :param damage:
        :return:
        '''
        self.__taking_damage = taking
        self.__player_damage = damage

    def dying(self):
        '''
        If health drops bellow 0 the monster has died so it returns True
        This will then start the monster to be deleted from the game so that it has died
        :return:
        '''
        if self.__health <= 0:
            return True
        else:
            return False

    def __movement(self):
        '''
        Moves the monster toward the target coordinates by adding or subtracting its y and x values
        :return:
        '''
        if self.__map[self.__target_y//100][self.__target_x//100].check_traverse:
            if self.rect.x < self.__target_x:
                self.rect.x += 1
                self.__last_move.append('d')

            else:
                self.rect.x -= 1
                self.__last_move.append('a')

            if self.rect.y < self.__target_y:
                self.rect.y +=1
                self.__last_move.append('s')
            else:
                self.rect.y -= 1
                self.__last_move.append('w')

        if len(self.__last_move) > 7:
            self.__last_move = []

    def __collision(self):
        if self.__walls != None:
            if pygame.sprite.spritecollide(self, self.__walls, False):
                for i in self.__last_move:
                    if i == 'w':
                        self.rect.y += 1

                    if i == 's':
                        self.rect.y -= 1

                    if i == 'a':
                        self.rect.x += 1

                    if i == 'd':
                        self.rect.x -= 1

    def wallsetter(self, walls):
        self.__walls = walls

    def player_colision(self, player):
        if self.__damage_count == 0:
            if self.rect.colliderect(player):
                self.__damage_count += 1
                return True
            else:
                return False
        else:
            self.__damage_count += 1
            if self.__damage_count == 90:
                self.__damage_count = 0

    def return_damage(self):
        return self.__Damage
