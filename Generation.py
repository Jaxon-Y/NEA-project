import pygame
import random
from Character import C
class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y):
        '''
        Loads the image of wall.png into the self.image class variable and sets the
        coordinates according to the integer parameters
        :param x:
        :param y:
        '''
        super().__init__()

        self.image = pygame.image.load('images/wall.png')
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Environmental(pygame.sprite.Sprite):
    def __init__(self, environment, x, y):
        '''
        Depending on the Boolean parameter it will load the image of either rock1 or rock2 .png
        it then sets the coords of these images according to the integer parameters
        :param environment:
        :param x:
        :param y:
        '''
        super().__init__()
        self.image = pygame.Surface([20, 15])
        self.image.fill((1,0,0))
        if environment:
            self.__sheet = pygame.image.load('images/rock_1.png')

        else:
            self.__sheet = pygame.image.load('images/rock_2.png')

        self.image.blit(self.__sheet, (0, 0), (0, 0, 20, 15))
        self.image.set_colorkey((1, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y, players):
        '''
        The inmage hatch is loaded and the rect/hitbox is created of the image and the coordinates are set using the parameters and the other variables thge class uses are created
        :param x:
        :param y:
        :param players:
        '''
        super().__init__()
        self.image = pygame.Surface([20, 15])
        self.__sheet = pygame.image.load('images/Hatch.png')
        self.image.fill((1,0,0))
        self.image.blit(self.__sheet, (0,0), (0,0, 20,15))
        self.image.set_colorkey((1,0,0))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.__players = players
        self.__Enter_clause_is_complete = False

    def entering(self):
        '''
        Checks for a colision between the player character and the rect/hiotbox of the image
        It then checks for if the enter clause is complete and if the etner key has been pressed
        if that is all True then it returns True if not then it returns false
        :return:
        '''
        inputs = pygame.key.get_pressed()
        colision = pygame.sprite.spritecollide(self, self.__players, False)
        if colision and inputs[pygame.K_RETURN] and self.__Enter_clause_is_complete:
            return True
        else:
            return False

    def update_exit_clause(self,players):
        '''
        It checks whether the length of the parameter object players is 1 which means only the player is now alive
        If that is true the enter clause is set to being True.
        :param players:
        :return:
        '''
        if len(players) == 1:
            self.__Enter_clause_is_complete = True



class Map:
    def __init__(self):
        '''
        It creates a 2d list of the size 70 by 70 by determining a random number 1 or 0 it selects which side the second room will come from
        the first room is created using the room class room 2 is then created with the starting coordinates either below or next to room 1
        room 3 is then created with the opposite direction to room 2 than room 2 was to room 1. The coords of each room are then assigned to variables.
        '''
        self._map = []
        for i in range(0, 70):
            self._map.append([])
            for x in range(0, 70):
                self._map[i].append(0)

        self.__dimensions = [0, 0]
        self.__rooms = []
        'random.randint(0,1)'
        if  random.randint(0,1) == 1:
            side1 = True
            side2 = False
        else:
            side1 = False
            side2 = True
        height = random.randint(10, 20)
        width = random.randint(13, 20)

        room1 = Room(width, height, [self.__dimensions[0] + 3, self.__dimensions[0] + 3], self._map, side2,1)
        self.__rooms.append(room1)
        self._map = room1.give_map_back()
        self.__dimensions = room1.give_dimensions_back()


        height = random.randint(10, 20)
        width = random.randint(13, 20)

        room2 = Room(width, height, self.__dimensions, self._map, side1,2)
        self.__rooms.append(room2)
        self._map = room2.give_map_back()
        self.__dimensions = room2.give_dimensions_back()

        room3 = Room(width, height, self.__dimensions, self._map, side2,3)
        self.__rooms.append(room3)
        self._map = room3.give_map_back()
        test = room3.give_map_back()
        self.__dimensions = room3.give_dimensions_back()
        self.__connections()
        self.__exit()

        self.__players_room = random.randint(0,2)
        self.__player_placement = self.__rooms[self.__players_room].player_placement()

        self.__room1_coords = room1.return_room_coords()
        self.__room2_coords = room2.return_room_coords()
        self.__room3_coords = room3.return_room_coords()


    def __connections(self):
        '''
        A hallway is created betwee 2 rooms in the direction that thery are next to eachother by this is done by
        changing the 1's and 0's to make the shape of a hallway onto the map that is one block wide which is enough room for the player.
        It also checks for if there are any indents and then changes the where the hallway is put.
        :return:
        '''
        for i in range(len(self.__rooms) - 1):
            print('running')
            room = self.__rooms[i]
            conneting = self.__rooms[i+1]
            gap = 3
            room_width0_height1 = room.give_width_height()
            zero_room = room.give_zero_width_height()
            zero_connecting = conneting.give_zero_width_height()
            connecting_width0_height1 = conneting.give_width_height()

            if room.give_side():

                #clear out space


                loop = True
                count = 1
                while loop:
                    if self._map[zero_room[1] + 4][zero_room[0] + room_width0_height1[0] + count] == 0:
                        count += 1
                    else:
                        loop = False

                if room_width0_height1[1] > connecting_width0_height1[1]:
                    half_height = connecting_width0_height1[1] // 2
                else:
                    half_height = room_width0_height1[1] // 2
                print(half_height)
                for i in range(gap):
                    self._map[zero_room[1] + half_height + i][zero_room[0] + room_width0_height1[0]] = 0

                    self._map[zero_connecting[1] + half_height + i][zero_connecting[0]] = 0

                #Upper
                for i in range(count):
                    self._map[zero_room[1] + half_height - 1][zero_room[0] + room_width0_height1[0] + i] = 1
                    #lower
                    self._map[zero_room[1] + half_height + gap][zero_room[0] + room_width0_height1[0] + i] = 1
                


            else:
                #checking for indent length
                room_B_working_room = room.give_B_working_room()
                if room_width0_height1[0] < connecting_width0_height1[0]:
                    half_width = room_width0_height1[0] // 2
                else:
                    half_width = connecting_width0_height1[0] // 2
                #geting the count
                count = 1
                loop = True
                while loop:
                    if self._map[zero_room[1] + room_width0_height1[1] + room_B_working_room + count][zero_room[0] + half_width] == 0:
                        count += 1
                    else:
                        loop = False

                count += room_B_working_room

                #clear out space
                for i in range(gap):
                    for x in range(count):
                        self._map[zero_room[1] + room_width0_height1[1] + x][zero_room[0] + half_width + i] = 0
                        self._map[zero_connecting[1] - x][zero_connecting[0] + half_width + i] = 0

                #Add in walls
                for i in range(count):
                    #left
                    self._map[zero_room[1] + room_width0_height1[1] + i][zero_room[0] + half_width - 1] = 1
                    #right
                    self._map[zero_connecting[1] - i][zero_connecting[0] + half_width + gap] = 1

    def __exit(self):
        '''
        It choses a room at random it then runs the function create exit on the room that was chosen
        :return:
        '''
        room = random.randint(0,len(self.__rooms) - 1)
        for i in range(len(self.__rooms)):
            if room == i:
                self.__rooms[i].create_exit()

    def place_enemy(self, C):
        '''
        It loops through all of the rooms if the player doesnt spawn in that room an enemy is placed by the place_enemy function
        :param C:
        :return:
        '''
        for i in range(len(self.__rooms)):
            if i != self.__players_room:
                self.__rooms[i].place_enemy(C)

    def check_room(self, C):
        '''
        Checks if the plkayer is in any of the rooms by looking at the coordinates of the player and looking at thye coordinates of which the rooms span
        This is then put into the function player_active_room
        :param C:
        :return:
        '''
        coords = C.player.give_coord()
        coords[0] = coords[0]//15
        coords[1] = coords[1]//20
        room = None
        #room 1
            #y coord check
        if coords[0] > self.__room1_coords[1] and coords[0] < (self.__room1_coords[1] + self.__room1_coords[3]):
            #x coord check
            if coords[1] > self.__room1_coords[0] and coords[1] < (self.__room1_coords[0] + self.__room1_coords[2]):
                room = 1
        # room 2
        # y coord check
        if coords[0] > self.__room2_coords[1] and coords[0] < (self.__room2_coords[1] + self.__room2_coords[3]):
            # x coord check
            if coords[1] > self.__room2_coords[0] and coords[1] < (self.__room2_coords[0] + self.__room2_coords[2]):
                room = 2
        # room 2
        # y coord check
        if coords[0] > self.__room3_coords[1] and coords[0] < (self.__room3_coords[1] + self.__room3_coords[3]):
            # x coord check
            if coords[1] > self.__room3_coords[0] and coords[1] < (self.__room3_coords[0] + self.__room3_coords[2]):
                room = 3

        C.player_room_active(room)

    def give_map(self):
        '''
        returns the list map
        :return:
        '''
        return self._map

    def return_player_placement(self):
        '''
        returns the integer player placement
        :return:
        '''
        return self.__player_placement

class Room:
    def __init__(self, width, height, zero, map, side, room_no):
        '''
        Creates a random height and width this is then put onto the map with the posistions having the starting coords added onto it
        Through a random number being generated a corner is chosen for each corner and then the orignal corner is removed and a new one is put onto the 2d list
        It then checks if there are space for indents and if there is space if they is it dcoes an indent to how much space it has after this calculates
        the starting coords of the next room.
        :param width:
        :param height:
        :param zero:
        :param map:
        :param side:
        :param room_no:
        '''
        self.__side = side
        self._map = map
        self.__height = height
        self.__width = width
        self.__zero_height = zero[1]
        self.__zero_width = zero[0]  # variable that will change for rooms where they start from
        self.__room_number = room_no
        # Set outline
        height_slot = self.__zero_height + self.__height
        width_slot = self.__zero_width + self.__width

        loop = True

        for i in range(self.__height):
            self._map[i + self.__zero_height][0 + self.__zero_width] = 1
            self._map[i + self.__zero_height][self.__width + self.__zero_width] = 1

        for i in range(self.__width):
            self._map[0 + self.__zero_height][i + self.__zero_width] = 1
            self._map[self.__height + self.__zero_height][i + self.__zero_width] = 1

        self._map[self.__height + self.__zero_height][self.__width + self.__zero_width] = 1
        # Make the corners curved
        '''
        start
        [1][1][1][1]
        [0][0][0][1]
        [0][0][0][1]
        [0][0][0][1]

        idea 1
        [1][1][0][0] remove 2 closet to corner
        [0][1][0][0]add one bellow remaining 1 and remove one at side
        [0][1][1][0]
        [0][0][1][1]

        idea 2
        [1][1][0][0]
        [0][1][1][0]
        [0][0][1][0]
        [0][0][1][1]

        idea 3
        [1][0][0][0]
        [0][1][0][0]
        [0][0][1][0]
        [0][0][0][1] does not look good
        '''

        # corner_type = 2
        # top left
        corner_type = random.randint(0, 1)
        if corner_type == 0:
            self._map[0 + self.__zero_height][0 + self.__zero_width] = 0
            self._map[0 + self.__zero_height][1 + self.__zero_width] = 0

            self._map[1 + self.__zero_height][2 + self.__zero_width] = 1
            self._map[1 + self.__zero_height][0 + self.__zero_width] = 0

            self._map[2 + self.__zero_height][0 + self.__zero_width] = 0
            self._map[2 + self.__zero_height][2 + self.__zero_width] = 1
            self._map[2 + self.__zero_height][1 + self.__zero_width] = 1

            self._map[3 + self.__zero_height][1 + self.__zero_width] = 1
        elif corner_type == 1:
            self._map[0 + self.__zero_height][0 + self.__zero_width] = 0
            self._map[0 + self.__zero_height][1 + self.__zero_width] = 0

            self._map[1 + self.__zero_height][2 + self.__zero_width] = 1
            self._map[1 + self.__zero_height][0 + self.__zero_width] = 0
            self._map[1 + self.__zero_height][1 + self.__zero_width] = 1

            self._map[2 + self.__zero_height][0 + self.__zero_width] = 0
            self._map[2 + self.__zero_height][1 + self.__zero_width] = 1

            self._map[3 + self.__zero_height][1 + self.__zero_width] = 1

        # bottom left
        corner_type = random.randint(0, 1)
        if corner_type == 0:
            self._map[self.__height + self.__zero_height][0 + self.__zero_width] = 0
            self._map[self.__height + self.__zero_height][1 + self.__zero_width] = 0

            self._map[self.__height - 1 + self.__zero_height][2 + self.__zero_width] = 1
            self._map[self.__height - 1 + self.__zero_height][0 + self.__zero_width] = 0

            self._map[self.__height - 2 + self.__zero_height][0 + self.__zero_width] = 0
            self._map[self.__height - 2 + self.__zero_height][2 + self.__zero_width] = 1
            self._map[self.__height - 2 + self.__zero_height][1 + self.__zero_width] = 1

            self._map[self.__height - 3 + self.__zero_height][1 + self.__zero_width] = 1

        elif corner_type == 1:
            self._map[self.__height + self.__zero_height][0 + self.__zero_width] = 0
            self._map[self.__height + self.__zero_height][1 + self.__zero_width] = 0

            self._map[self.__height - 1 + self.__zero_height][2 + self.__zero_width] = 1
            self._map[self.__height - 1 + self.__zero_height][0 + self.__zero_width] = 0
            self._map[self.__height - 1 + self.__zero_height][1 + self.__zero_width] = 1

            self._map[self.__height - 2 + self.__zero_height][0 + self.__zero_width] = 0
            self._map[self.__height - 2 + self.__zero_height][1 + self.__zero_width] = 1

            self._map[self.__height - 3 + self.__zero_height][1 + self.__zero_width] = 1

        # top right
        corner_type = random.randint(0, 1)
        if corner_type == 0:
            self._map[0 + self.__zero_height][self.__width + self.__zero_width] = 0
            self._map[0 + self.__zero_height][self.__width - 1 + self.__zero_width] = 0

            self._map[1 + self.__zero_height][self.__width - 2 + self.__zero_width] = 1
            self._map[1 + self.__zero_height][self.__width + self.__zero_width] = 0

            self._map[2 + self.__zero_height][self.__width + self.__zero_width] = 0
            self._map[2 + self.__zero_height][self.__width - 2 + self.__zero_width] = 1
            self._map[2 + self.__zero_height][self.__width - 1 + self.__zero_width] = 1

            self._map[3 + self.__zero_height][self.__width - 1 + self.__zero_width] = 1

        elif corner_type == 1:
            self._map[0 + self.__zero_height][self.__width + self.__zero_width] = 0
            self._map[0 + self.__zero_height][self.__width - 1 + self.__zero_width] = 0

            self._map[1 + self.__zero_height][self.__width - 2 + self.__zero_width] = 1
            self._map[1 + self.__zero_height][self.__width + self.__zero_width] = 0
            self._map[1 + self.__zero_height][self.__width - 1 + self.__zero_width] = 1

            self._map[2 + self.__zero_height][self.__width + self.__zero_width] = 0
            self._map[2 + self.__zero_height][self.__width - 1 + self.__zero_width] = 1

            self._map[3 + self.__zero_height][self.__width - 1 + self.__zero_width] = 1

        # bottom right
        corner_type = random.randint(0, 1)
        if corner_type == 0:
            self._map[self.__height + self.__zero_height][self.__width + self.__zero_width] = 0
            self._map[self.__height + self.__zero_height][self.__width - 1 + self.__zero_width] = 0

            self._map[self.__height - 1 + self.__zero_height][self.__width - 2 + self.__zero_width] = 1
            self._map[self.__height - 1 + self.__zero_height][self.__width + self.__zero_width] = 0

            self._map[self.__height - 2 + self.__zero_height][self.__width + self.__zero_width] = 0
            self._map[self.__height - 2 + self.__zero_height][self.__width - 2 + self.__zero_width] = 1
            self._map[self.__height - 2 + self.__zero_height][self.__width - 1 + self.__zero_width] = 1

            self._map[self.__height - 3 + self.__zero_height][self.__width - 1 + self.__zero_width] = 1
        elif corner_type == 1:
            self._map[self.__height + self.__zero_height][self.__width + self.__zero_width] = 0
            self._map[self.__height + self.__zero_height][self.__width - 1 + self.__zero_width] = 0

            self._map[self.__height - 1 + self.__zero_height][self.__width - 2 + self.__zero_width] = 1
            self._map[self.__height - 1 + self.__zero_height][self.__width + self.__zero_width] = 0
            self._map[self.__height - 1 + self.__zero_height][self.__width - 1 + self.__zero_width] = 1

            self._map[self.__height - 2 + self.__zero_height][self.__width + self.__zero_width] = 0
            self._map[self.__height - 2 + self.__zero_height][self.__width - 1 + self.__zero_width] = 1

            self._map[self.__height - 3 + self.__zero_height][self.__width - 1 + self.__zero_width] = 1

        # add indents

        # check for valid sides
        # checks for top
        if self.__zero_height != 0:
            top = True
        elif self._map[self.__zero_height - 1][self.__zero_width + 5] == 1:
            top = False
        else:
            top = False

        # checks for bottom
        if self.__zero_height + self.__height != 50:
            bottom = True
        elif self._map[self.__zero_height + self.__height + 1][self.__zero_width + 5] == 1:
            bottom = False
        else:
            bottom = False

        # top indent
        if top == True:

            width_start = 0
            start = self.__width // 8
            for i in range(self.__zero_width, len(self._map[0])):
                if self._map[self.__zero_height][i] == 1:
                    width_start = i
                    break
            self.__Top_working_room = 0
            i = 0
            while self.__Top_working_room < 3:
                if self._map[self.__zero_height - i][self.__zero_width + 4] == 0:
                    self.__Top_working_room += 1
                i += 1
                if self.__zero_height - i == -1:
                    self.__Top_working_room = 3

            # clear out space
            gap = self.__width // 2 + self.__Top_working_room - (self.__width // 8) * 2

            for i in range(gap):
                self._map[self.__zero_height][i + width_start + start] = 0

            # rise
            for i in range(self.__Top_working_room):
                self._map[self.__zero_height - i][width_start + i + start] = 1
                self._map[self.__zero_height - i][width_start + i + 1 + start] = 1

            # solid in middle
            wall = gap - (self.__Top_working_room * 2) + width_start + self.__Top_working_room

            for i in range((width_start + self.__Top_working_room), wall):
                self._map[self.__zero_height - self.__Top_working_room][i + start] = 1

            # fall
            for i in range(self.__Top_working_room):
                self._map[self.__zero_height - self.__Top_working_room + i][wall + i + start] = 1
                self._map[self.__zero_height - self.__Top_working_room + i][wall + i + 1 + start] = 1

        # bottom indent

        if bottom == True:
            width_start = 0
            start = self.__zero_width + self.__width - (self.__width // 8)
            for i in range(self.__zero_width, len(self._map[0])):
                if self._map[self.__zero_height][i] == 1:
                    width_start = i
                    break
            self.__Bottom_working_room = 0
            i = 0

            while self.__Bottom_working_room < 3:
                if self._map[height_slot + i][self.__width + 4] == 0:
                    self.__Bottom_working_room += 1
                i += 1
                if height_slot + i == 70:
                    self.__Bottom_working_room = 3

            # create the gap
            gap = self.__width // 2 + self.__Bottom_working_room - (self.__width // 8) * 2
            for i in range(gap):
                self._map[height_slot][start - i] = 0

            # rising
            for i in range(self.__Bottom_working_room):
                self._map[self.__zero_height + self.__height + i][start - i] = 1
                self._map[self.__zero_height + self.__height + i][start - i - 1] = 1

            # solid in middle
            wall = gap - (self.__Bottom_working_room * 2) + 2
            for i in range(wall):
                self._map[self.__zero_height + self.__height + self.__Bottom_working_room][start - self.__Bottom_working_room - i] = 1

            # fall
            for i in range(self.__Bottom_working_room):
                self._map[self.__zero_height + self.__height + self.__Bottom_working_room - i][start - wall - 1 - i] = 1
                self._map[self.__zero_height + self.__height + self.__Bottom_working_room - i][start - wall - 1 - i - 1] = 1


        if side == True:
            self.__dimensions = [width_slot + 4, self.__zero_height]
        else:
            self.__dimensions = [self.__zero_width, height_slot + self.__Bottom_working_room + 5]

        self.place_items(3)

    #extra generation after the inisialastion
    def place_items(self, amount):
        '''
        Loops amount of times as the parameter amount and randomly choses the coordinates of the object to be placed it then either places a 2 or a 3 on the 2d list
        :param amount:
        :return:
        '''
        amount -=1 # for loop starts at 0
        for i in range(amount):
            x_cord = 0
            y_cord = 0
            new_x = 0
            new_y = 0
            while new_x == x_cord or new_y == y_cord or new_x == x_cord - 1 or new_x == x_cord + 1 or new_y == y_cord - 1 or new_y == y_cord + 1:
                new_x = random.randint(self.__zero_width + 3, self.__zero_width + self.__width - 3)
                new_y = random.randint(self.__zero_height + 1, self.__zero_height + self.__height - 1)
            x_cord = new_x
            y_cord = new_y
            if random.randint(0,1) == 1:
                self._map[y_cord][x_cord] = 2
            else:
                self._map[y_cord][x_cord] = 3

    def create_exit(self):
        '''
        Loops until the coords chosen to place the exit is an empty slot and if it is then on the 2d list it is represented as a 4
        :return:
        '''
        loop = True
        while loop:
            new_x = random.randint(self.__zero_width + 3, self.__zero_width + self.__width - 3)
            new_y = random.randint(self.__zero_height + 1, self.__zero_height + self.__height - 1)
            if self._map[new_y][new_x] == 0:
                    loop = False

        self._map[new_y][new_x] = 4

    def place_enemy(self, C):
        '''
        places a monster in the middle of the room using Connection.create monsters
        :param C:
        :return:
        '''
        x_cord = (self.__zero_width + (self.__width//2)) * 20
        y_cord = (self.__zero_height + (self.__height//2)) * 15
        C.create_monsters(1, [y_cord, x_cord], self.__room_number)

    #returning items
    def give_map_back(self):
        '''
        Returns the 2d list map
        :return:
        '''
        return self._map

    def give_dimensions_back(self):
        '''
        returns the list of the dimesnions of the room
        :return:
        '''
        return self.__dimensions

    def return_room_coords(self):
        '''
        Returns a list of the starting width and height and the width and height of the room
        :return:
        '''
        return [self.__zero_width,self.__zero_height,self.__width,self.__height]

    def give_B_working_room(self):
        '''
        Returns the amount of space the room has underneath it
        :return:
        '''
        return self.__Bottom_working_room

    def give_T_working_room(self):
        '''
        Returns the amount of spoace the room has above it
        :return:
        '''
        return self.__Top_working_room

    def give_width_height(self):
        '''
        returns a list of the width and height
        :return:
        '''
        return [self.__width,self.__height]

    def give_zero_width_height(self):
        '''
        Returns a list of the starting width and height
        :return:
        '''
        return [self.__zero_width, self.__zero_height]

    def give_side(self):
        '''
        Returns the Boolean value side
        :return:
        '''
        return self.__side

    def player_placement(self):
        '''
        Returns a list of the coords of the middle of the room to place the player there
        :return:
        '''
        placementx = self.__zero_width + (self.__width//2)
        placementy = self.__zero_height + (self.__height // 2)
        return [placementy, placementx]

class Level_map:
    def __init__(self, difficulty,screen):
        '''
        creates all the variables the class uses then it loops for 4*difficulty and it starts by creating one node on each layer but it increases by 1 each time until the last node
        '''
        self.__level_map = [] # initialise map
        self.__dimensions = screen.get_size()
        #Node creation
        self.__difficulty = difficulty
        layers = 4*self.__difficulty
        self.__sectors_height = self.__dimensions[0]//layers
        self.__sectors_width = self.__dimensions[1]//layers
        self.__level_at = 1
        height_list = []
        for i in range(layers):
            height_list.append(i*self.__sectors_height)
        height_list.reverse()
        self.__level_map = []
        for i in range(1,layers): # not plus one so tyhat it leaves enough room for boss node to go
            self.__level_map.append([])
            num = i + 1
            for x in range(1,num):
                self.__level_map[i-1].append(Level_Node((height_list[i-1],(x*self.__sectors_width)), False, i, self, self.__difficulty))

        self.__level_map[0].append(Level_Node((0,400), True,layers , self, self.__difficulty))

    def give_map(self):
        '''
        returns the 2d list level map
        :return:
        '''
        return self.__level_map

    def send_level(self):
        '''
        it loops through every level node in level map and run the function level_at_recieve where the level at variable is the parameter
        :return:
        '''
        for i in self.__level_map:
            for x in i:
                x.level_at_recieve(self.__level_at)

    def recieve_new_level(self, level):
        '''
        assigns parameter to level at variable
        :param level:
        :return:
        '''
        self.__level_at = level

class Level_Node(pygame.sprite.Sprite):
    def __init__(self, pos, end, level, father, total_level):
        '''
        checks if it is the last node if it is the its type is end and its colour is balck with its width and height being 100 by 40 pixles
        if not then it is randomly assigned as either a dungeon, chest or rest node with the size always being 35 / total level halved squares
        if its a dungeon then its red, a chest then blue and a rest then yellow
        it then creates its rect/hitbox and assigns the position coordinates and creates other variables needed for the class
        :param pos:
        :param end:
        :param level:
        :param father:
        :param total_level:
        '''
        super().__init__()
        if end:
            self.image = pygame.Surface([100,40])
            self.__type ='end'
            self.__colour = 'black'
        else:
            #Node bits
            self.image = pygame.Surface([35//(total_level/2), 35//(total_level/2)])
            num = random.randint(1,3)
            if num == 1:
                self.__type = 'dungeon'
                self.__colour = 'red'
            elif num == 2:
                self.__type = 'chest'
                self.__colour = 'blue'

            elif num == 3:
                self.__type = 'rest'
                self.__colour = 'yellow'

        # Pygame bits
        self.__position = pos

        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, self.__colour,self.rect )
        self.__coords = (self.__position[0], self.__position[1])
        self.rect.x = self.__position[1]
        self.rect.y = self.__position[0]

        self.__level = level
        self.__current_level = 1
        self.__father = father

    def __colision(self):
        '''
        runs the __level_check function and if it returns True then it checks whether a colision is made between the mouse and the node
        if so its checks if a mouse click has happend if it has the __update_level method is ran and it returns True
        :return:
        '''
        if self.__level_check():
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if self.rect.collidepoint(mouse_pos):
                print('collision')
                if click[0]:
                    print('click')
                    self.__update_level()
                    self.__colour = 'purple'
                    return True

    def __update_level(self):
        '''
        new_level is assigned as the level + 1 and then runs the function recieve_new_level to the father object with the new_level as the parameter
        :return:
        '''
        new_level = self.__level + 1
        self.__father.recieve_new_level(new_level)

    def level_at_recieve(self,level):
        '''
        assigns the parameter to current_level
        :param level:
        :return:
        '''
        self.__current_level = level

    def __level_check(self):
        '''
        Checks if the level at is this nodes level if so then Return TRue if not Return False
        :return:
        '''
        if self.__level == self.__current_level:
            return True
        else:
            return False

    def run(self):
        '''
        Checks whether a collision has been made from the function __colisision and if it returns True then it returns the string of its type
        :return:
        '''
        if self.__colision():
            if self.__type == 'dungeon':
                return 'dungeon'

            elif self.__type == 'chest':
                return 'chest'

            elif self.__type == 'end':
                return 'end'

            elif self.__type == 'rest':
                return 'rest'

            else:
                return None


