from  Generation import Map, Wall, Environmental, Exit, Level_map, Level_Node

#from Character import Character_class
#from Character import Monster
from Character import Node
from Character import C
import pygame
import random

class Line(pygame.sprite.Sprite):
    def __init__(self, text, x, y, colour,background, size):
        '''
        It takes the parameters and renders the text with the colours and the text and size due to the parameters given with the font castellar and then the rect/hitbox is created and the position of the text is set according to the parameters
        :param text:
        :param x:
        :param y:
        :param colour:
        :param background:
        :param size:
        '''
        super().__init__()

        self.__font = pygame.font.SysFont('castellar', size)
        self.__text = self.__font.render(text, True, colour, background)
        self.__text_rect = self.__text.get_rect()
        self.__text_rect.x = x
        self.__text_rect.y = y

    def collide(self):
        '''
        Checks whether the mouse has colldied/ is inside of the rect/hitbox of the text
        :return:
        '''
        mouse = pygame.mouse.get_pos()
        if self.__text_rect.collidepoint(mouse[0],mouse[1]):
            return True
        else:
            return False
    def give_text(self):
        '''
        Returns the string variable text
        :return:
        '''
        return self.__text
    def give_rect(self):
        '''
        returns the rect of the text
        :return:
        '''
        return self.__text_rect

class Rest_Screen:
    def __init__(self,screen):
        '''
        Assigns the parameter screen to screen and then creates the text for the screen aswell as loads the images they are then added to a pygame group
        and all the variables needed for the class is assigned a variable count is set to 1
        :param screen:
        '''
        self.__screen = screen
        #pygame stuff
        self.__writing = []
        self.__writing.append(Line('Welcome to the camp !', 100,100,'black','light grey', 60))
        self.__writing.append(Line('Rest',650,310,'black','light grey',60))
        self.__writing.append(Line('Shop', 150, 310, 'black', 'light grey', 60))
        self.__group = pygame.sprite.Group()
        self.__rest_button= button(600,200, 'images/rest point button.png')
        self.__shop_button = button(100,200, 'images/shop_button.png')
        self.__group.add(self.__rest_button)
        self.__group.add(self.__shop_button)
        self.__over = False
        self.__shop = False
        self.__shop_object = Shop(self.__screen)
        self.__count = 1


    def run_rest(self,click,C):
        '''
        If the count is not 0 it checks wether it is 20 if it is then count is 0 if not 1 is added
        if the count is 0 then it checks for wether the shop is true if it is then functions update_gold, update_health, update_damage and run_shop are ran
        If the string return from run_shop is quit then the shop is False otherwise the string is returned.
        Or the function button.colision for the rest button  is ran if that return is True and click is True then over is set to True
        The function button.colision for the shop button is ran and if they is a click from the mouse then shop is set to True
        :param click:
        :param C:
        :return:
        '''
        if self.__count != 0:
            if self.__count == 20:
                self.__count = 0
            else:
                self.__count += 1
        if self.__count == 0:
            if self.__shop == True:
                self.__shop_object.update_gold(C.player.return_gold())
                self.__shop_object.update_health(C.player.return_health())
                self.__shop_object.update_damage(C.player.return_damage())
                string = self.__shop_object.run_shop(click)
                if string == 'quit':
                    self.__shop = False
                else:
                    return string

            else:
                if self.__rest_button.collision():
                    if click:
                        self.__over = True
                if self.__shop_button.collision():
                    if click:
                        self.__shop = True


            self.__screen.fill('light grey')
            for i in self.__writing:
                self.__screen.blit(i.give_text(), i.give_rect())
            self.__group.draw(self.__screen)
            self.__group.update(self.__screen)
            pygame.display.update()

    def return_over(self):
        '''
        Returns the bollean variable __over
        :return:
        '''
        return self.__over

    def reset_over(self):
        '''
        Boolean variable over is set to False
        :return:
        '''
        self.__over = False

    def return_cost(self):
        cost = self.__shop_object.return_cost()
        return cost

class button(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        '''
        Runs the initializer of the pygame.sprite.Sprite and then loads the image of the string and creates a rect/hitbox for that image and sets the x and y to those integer parameters
        :param x:
        :param y:
        :param image:
        '''
        super().__init__()
        self.image = pygame.image.load(image)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def collision(self):
        '''
        detects wether the mouse is over the button if it is it returns True if not then it returns False
        :return:
        '''
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            return True
        else:
            return False

class Shop:
    def __init__(self,screen):
        '''
        It creates the text of the shop with the Line class
        Loads the images that are used on this screen
        sets up the variables that the class uses
        :param screen:
        '''
        self.__screen = screen
        self.__cost = 5
        self.__gold = 0
        self.__count = 1
        self.__writing = []
        self.__writing.append(Line('''"WelCome to my StOre''',410,5,'white',(112,146,190),40))
        self.__writing.append(Line('''WhIch potion wOUld''', 410, 45, 'white', (112,146,190), 40))
        self.__writing.append(Line('''you like:''', 410, 85, 'white', (112,146,190), 40))
        self.__writing.append(Line('''The Potion of HeAlth''', 410, 125, 'white', (112,146,190), 40))
        self.__writing.append(Line('''The pOtion of Damage''', 410, 165, 'white', (112,146,190), 40))
        self.__writing.append(Line('''THey can be yours''', 410, 205, 'white', (112,146,190), 40))
        self.__writing.append(Line('''with the right gold"''', 410, 245, 'white', (112,146,190), 40))

        self.__writing.append(Line('Health + 1',100, 700,'black','light grey',40))
        self.__writing.append(Line('Cost: '+str(self.__cost), 100,740,'black','light grey',40))

        self.__writing.append(Line('Damage + 1', 400, 700, 'black', 'light grey', 40))
        self.__writing.append(Line('Cost: ' + str(self.__cost), 400, 740, 'black', 'light grey', 40))

        self.__writing.append(Line('Gold: ',400,400,'black','light grey', 40))
        self.__writing.append(Line('Health: ',100,355,'black','light grey', 40))
        self.__writing.append(Line('Damage: ',400,355,'black','light grey', 40))
        self.__group = pygame.sprite.Group()
        self.__shop_keep = button(0,0,'images/shop_keep.png')
        self.__text_background = button(405,0,'images/text background shopkeep.png')
        self.__Health_bottle = button(100,500,'images/Health Potion.png')
        self.__damage_potion = button(400, 500,'images/Damage Potion.png')
        self.__go_back = button(700,500,'images/Go Back Sign.png')
        self.__group.add(self.__shop_keep)
        self.__group.add(self.__text_background)
        self.__group.add(self.__Health_bottle)
        self.__group.add(self.__damage_potion)
        self.__group.add(self.__go_back)

    def run_shop(self,click):
        '''
        The main code for this class where to make sure no colision issues occor doesnt let the player input anything until the code is ran 100 times which is done quickly
        this happens every time an icon is clicked so that it is only activated once. It checks whether the icons have been clicked and returns a string according to the icon clicked
        it then updates and draws on the screen.

        :param click:
        :return:
        '''
        if self.__count != 0:
            if self.__count == 400:
                self.__count = 0
            else:
                self.__count += 1

        if self.__count == 0:

            if self.__Health_bottle.collision():
                if click and self.__gold - self.__cost > 0 :
                    self.__count += 1
                    self.cost_up()
                    return 'health'

            if self.__damage_potion.collision():
                if click and self.__gold - self.__cost > 0:
                    self.__count += 1
                    self.cost_up()
                    return 'damage'

            if self.__go_back.collision():
                if click:
                    self.__count += 1
                    return 'quit'

        self.__screen.fill('light grey')
        self.__group.draw(self.__screen)
        self.__group.update()
        for i in self.__writing:
            self.__screen.blit(i.give_text(),i.give_rect())
        pygame.display.update()

    def cost_up(self):
        '''
        Increases the class variable cost and updates the text in the class variable __writing according to the new cost
        :return:
        '''
        self.__cost += 5
        self.__writing[8] = Line('Cost: '+str(self.__cost), 100,740,'black','light grey',40)
        self.__writing[10] = Line('Cost: ' + str(self.__cost), 400, 740, 'black', 'light grey', 40)

    def update_gold(self,gold):
        '''
        Updates the class variable gold with the parameter and updates the text in the shop accordingly
        :param gold:
        :return:
        '''
        self.__gold = gold
        self.__writing[11] = Line(('Gold: '+str(gold)),410,300,'black','light grey',40)

    def update_health(self,health):
        '''
        Takes the parameter and updates the text in the shop for the health of the player
        :param health:
        :return:
        '''
        self.__writing[12] = Line(('Health: '+str(health)),100,440,'black','light grey', 40)

    def update_damage(self,damage):
        '''
        Takes the parameter and updates the text in the shop for the damage of the player
        :param damage:
        :return:
        '''
        self.__writing[13] = Line(('Damage: '+str(damage)),400,440,'black','light grey', 40)

    def return_cost(self):
        return self.__cost

class Start_menu:
    def __init__(self,screen):
        '''
        Creates all the writing using the Line class for the main menu aswell as a seperate list for the controls screen
        :param screen:
        '''
        self.__screen = screen
        self.__start = True #NEEDS TO BE SET TO TRUE
        self.__quit = False
        self.__controls = False
        #MAIN MENU
        self.__writing_main = []
        self.__writing_main.append(Line('Monster Hunter', 200, 150, 'black', 'light grey', 60))
        self.__writing_main.append(Line('Start Game', 350, 300, 'black', 'light grey', 40))
        self.__writing_main.append(Line('Controls', 350, 400, 'black', 'light grey', 40))
        self.__writing_main.append(Line('Quit', 350, 500, 'black', 'light grey', 40))
        #CONTROL MENU
        self.__writing_control = []
        self.__writing_control.append(Line('GO BACK', 200,100,'black','light grey', 40))
        self.__writing_control.append(Line('Use the WASD keys to move', 200, 200, 'black', 'light grey', 30))
        self.__writing_control.append(Line('Press R to attack', 200, 300, 'black', 'light grey', 30))
        self.__writing_control.append(Line('Press CTRL to dash towards', 200, 400, 'black', 'light grey', 30))
        self.__writing_control.append(Line('the location of the mouse', 200, 430, 'black', 'light grey', 30))
        self.__writing_control.append(Line('Press SHIFT to slow walk', 200, 530 , 'black', 'light grey', 30))


    def startup_menu(self, mouse_click):
        '''
        Updates and draws the text onto the screen as well as making the background light grey it then checks for if any colisions have happend if they has a variable is set to True depending on which one it was
        :param mouse_click:
        :return:
        '''
        self.__screen.fill('light grey')

        for i in self.__writing_main:
            self.__screen.blit(i.give_text(), i.give_rect())

        if self.__writing_main[1].collide() and mouse_click:
            self.__start = False

        elif self.__writing_main[2].collide() and mouse_click:
            self.__controls = True
            self.__start = False

        elif self.__writing_main[3].collide() and mouse_click:
            self.__quit = True

        pygame.display.update()

    def controls_menu(self, click):
        '''
        Makes the bnackground of the screen light grey and then puts the text onto the screen and checks for wether the text go back has had a collision if so then sets the Boolean variables
        to say that the controls menu is false and the start menu is true
        :param click:
        :return:
        '''
        self.__screen.fill('light grey')
        for i in self.__writing_control:
            self.__screen.blit(i.give_text(), i.give_rect())

        if self.__writing_control[0].collide() and click:
            self.__controls = False
            self.__start = True

        pygame.display.update()


    def run_menu(self, click):
        '''
        checks if the variable quit,controls and start is true if quit is true program ends if controls is true it runs the function Controls_menu and if start is true it runs the startup_menu function
        :param click:
        :return:
        '''
        if self.__quit == True:
            quit()
        elif self.__controls == True:
            self.controls_menu(click)

        elif self.__start == True:
            self.startup_menu(click)


    def check(self):
        '''
        If controls is false return start or return True this is used to check wether the start menu is in use
        :return:
        '''
        if self.__controls == False:
            return self.__start
        else:
            return True

    def reset_main_menu(self):
        self.__start = True

class Level_map_creator:
    def __init__(self,screen):
        '''
        Creates the variables the class uses and assigns the pygame screen to a variable
        :param screen:
        '''
        self.__level = 1
        self.__screen = screen
        self.__level_buttons = None
        self.__choice = None

    def create(self):
        '''
       Resets the buttons and deletes the previous ones and then creates a new level map class and adds the buttons of that class to pygame group level buttons. Then the difficulty variable is increased by 1.
        :return:
        '''
        self.__level_buttons = pygame.sprite.Group()
        self.__map = Level_map(self.__level, self.__screen)
        map = self.__map.give_map()
        for i in map:
            for x in i:
                self.__level_buttons.add(x)
        self.__level += 1

    def reset_choice(self):
        '''
        assings the class variable of chioce to None/nothing
        :return:
        '''
        self.__choice = None

    def running(self):
        '''
        Loops through every level node in the level map and checks if they return a choice if so that choice is assigned to the class variable choice
        It then runs the function send_level and makes teh screen white and puts the buttons onto the screen and thgebn updates the display
        :return:
        '''
        for i in self.__map.give_map():
            for x in i:
                choice = x.run()
                if  choice != None:
                    self.__choice =  choice

        self.__map.send_level()
        self.__screen.fill('white')
        self.__level_buttons.draw(self.__screen)
        self.__level_buttons.update()
        pygame.display.update()

    def return_choice(self):
        '''
        Returns the class variable choice
        :return:
        '''
        return self.__choice

class Chest_screen:
    def __init__(self,screen):
        '''
        Creates the text and image needed for the chest screen it also creates all the variables the class uses
        :param screen:
        '''
        self.__screen = screen
        self.__contents = None
        self.__string_contents = ''
        self.__writing = []
        self.__writing.append(Line('You have Found a Chest', 200, 200, 'black', 'light grey', 40))
        self.__writing.append(Line(('Inside the chest there is'+self.__string_contents), 200,300, 'black', 'light grey', 30))
        self.__writing.append(Line('Take the Gold',200,700, 'black', 'grey', 30))
        self.__group = pygame.sprite.Group()
        self.__image = Chest_image()
        self.__group.add(self.__image)
        self.__count = 0
        self.__spin = True


    def chest(self,click):
        '''
        This is the main code for the chest screen it creates a new value for the chest 200 times then stops this creates the illusion that the amount in the text is spining to select an amount
        it then checks for if a clolision and the mouse has clicked and then returns the value (amount of gold the chest has) and restocks the chest.
        :param click:
        :return:
        '''
        self.__screen.fill('light grey')
        if self.__spin == True:
            self.__restock()
            self.__count += 1
        if self.__count == 200:
            self.__spin = False

        if self.__writing[2].collide() and click:
            self.__count = 0
            self.__spin = True
            value = self.__contents
            self.__restock()
            return value

        for i in self.__writing:
            self.__screen.blit(i.give_text(), i.give_rect())
        self.__group.draw(self.__screen)
        self.__group.update()

        pygame.display.update()

    def __restock(self):
        '''
        Creates a random number (0,100) this new value is now the new contents it then modifies the text according to the new amount of gold the chest has
        :return:
        '''
        num = random.randint(0, 100)
        self.__contents = num
        self.__string_contents = " "+str(num)+' Gold'
        self.__writing[1] = Line(('Inside the chest there is'+self.__string_contents), 200,300, 'black', 'light grey', 30)

class Chest_image(pygame.sprite.Sprite):
    def __init__(self):
        '''
        Loads the image chest and creates the rect/hitbox for the image and sets the coordinates of where the image is placed
        '''
        super().__init__()
        self.image = pygame.image.load('images/chest.png')
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 400


class Main_game():
    def __init__(self):
        '''
        This function sets up everything that stays constant in the game and creates all the variables this class uses
        '''
        self.__Map = None
        self.__map_list = []
        self.__node_map = []
        self.__exit_map = None
        self.__C = C()
        self.__player_placement = []
        self.__screen = pygame.display.set_mode((1000,800))
        self.__level_selection_map = Level_map_creator(self.__screen)

        self.__walls = pygame.sprite.Group()
        self.__objects = pygame.sprite.Group()
        self.__players = pygame.sprite.Group()
        self.__players.add(self.__C.player)
        self.__weapon_hitboxes = pygame.sprite.Group()
        for i in self.__C.player.give_weapon():
            self.__weapon_hitboxes.add(i)

        self.__start_menu = Start_menu(self.__screen)
        self.__rest_screen = Rest_Screen(self.__screen)
        self.__level_selection = True
        self.__Main = False
        self.__rest = False
        self.__chest = False
        self.__chest_screen = Chest_screen(self.__screen)
        self.__run = True
        self.__restart = False

    def bootup(self):
        '''
        This resets the game this includes the level selection screen as well as the main game levels
        :return:
        '''
        self.reset_main_game()
        self.__level_selection_map.create()

    def reset_main_game(self):
        self.__Map = Map()
        self.__player_placement = self.__Map.return_player_placement()
        self.__C.player.set_coords(self.__player_placement)
        self.__Map.place_enemy(self.__C)
        self.__walls = pygame.sprite.Group()
        self.__objects = pygame.sprite.Group()
        self.__map_list = self.__Map.give_map()
        for i in range(len(self.__map_list)):
            for x in range(len(self.__map_list[0])):
                if self.__map_list[i][x] == 1:
                    # slot = self.__map_list[i][x]
                    x_cord = x * 20
                    y_cord = i * 15
                    wall = Wall(x_cord, y_cord)
                    self.__walls.add(wall)

                elif self.__map_list[i][x] == 2:
                    # slot = self.__map_list[i][x]
                    x_cord = x * 20
                    y_cord = i * 15
                    object = Environmental(False, x_cord, y_cord)
                    self.__objects.add(object)

                elif self.__map_list[i][x] == 3:
                    # slot = self.__map_list[i][x]
                    x_cord = x * 20
                    y_cord = i * 15
                    object = Environmental(True, x_cord, y_cord)
                    self.__objects.add(object)

                elif self.__map_list[i][x] == 4:
                    # slot = self.__map_list[i][x]
                    x_cord = x * 20
                    y_cord = i * 15
                    self.__exit_map = Exit(x_cord, y_cord, self.__players)
                    self.__objects.add(self.__exit_map)

        for i in range(len(self.__map_list)):
            self.__node_map.append([])
            for x in range(len(self.__map_list[0])):
                self.__node_map[i].append(Node([i, x], [0, 0], 1, self.__map_list, self.__node_map, None))
                self.__node_map[i][x].create_neighbours()

        for monster in self.__C.monsters:
            self.__players.add(monster)
            monster.recieve_map(self.__node_map)
            monster.recieve_weapon_hitbox(self.__weapon_hitboxes)
            monster.wallsetter(self.__walls)

        self.__C.player.wall_setter(self.__walls)

    def run_game(self):
        '''
        This function is the main loop of the game and where everything runs from
        :return:
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__run = False


        M_inputs = pygame.mouse.get_pressed()
        if M_inputs[0]:
            click = True

        else:
            click = False
        if self.__start_menu.check():

            self.__start_menu.run_menu(click)

        elif self.__rest == True:
            print('runs')
            string = self.__rest_screen.run_rest(click,self.__C)
            if string == 'health':
                self.__C.player.give_health()
                self.__C.player.take_gold(self.__rest_screen.return_cost())
            if string == 'damage':
                self.__C.player.give_damage()
                self.__C.player.take_gold(self.__rest_screen.return_cost())

            if self.__rest_screen.return_over():
                self.__rest = False
                self.__level_selection = True
                self.__level_selection_map.reset_choice()
                self.__rest_screen.reset_over()

        elif self.__chest == True:
            contents = self.__chest_screen.chest(click)
            if contents != None:
                self.__C.player.give_gold(contents)
                self.__chest = False
                self.__level_selection = True
                self.__level_selection_map.reset_choice()

        elif self.__level_selection == True:
            self.__level_selection_map.running()
            self.__choice = self.__level_selection_map.return_choice()
            if self.__choice != None:
                if self.__choice == 'dungeon':
                    print('going to a dungeon')
                    self.__level_selection = False
                    self.__chest = False
                    self.__rest = False
                    self.__Main = True

                elif self.__choice == 'chest':
                    print('going to a chest')
                    self.__level_selection = False
                    self.__chest = True
                    self.__rest = False
                    self.__Main = False

                elif self.__choice == 'rest':
                    print('rest on')
                    self.__level_selection = False
                    self.__chest = False
                    self.__rest = True
                    self.__Main = False

                elif self.__choice == 'end':
                    print('new level')
                    self.__level_selection = False
                    self.__chest = False
                    self.__rest = False
                    self.__Main = False
                    self.__restart = True
                    print('restarting')

        elif self.__restart == True:
            self.__restart = False
            self.__level_selection_map.reset_choice()
            self.bootup()
            self.__level_selection = True

        elif self.__Main == True:
            self.__main()
            self.__exit_map.update_exit_clause(self.__players)
            if self.__exit_map.entering() == True:
                self.__Main = False
                self.__level_selection = True
                self.__level_selection_map.reset_choice()
                self.reset_main_game()

        else:
            # screen.fill('white')
            font = pygame.font.Font('Comic sans', 32)
            text = font.render('loading', True, 'green', 'blue')
            text_rect = text.get_rect()
            text_rect.center(400, 300)
            self.__screen.blit(text, text_rect)
            pygame.display.update()

    def __main(self):
        '''
        This function is used when in a main level of the game and updates and draws all pygame groups needed.
        It also updates the display and runs the functions C.C.coords_recieve() C.coords_give() C.weapon_hitbox_recieve() C.damage_bits().
        :return:
        '''
        if self.__Main == True:
            # collisions(C.player, objects)
            self.__screen.fill('light grey')
            self.__objects.draw(self.__screen)
            self.__objects.update()
            self.__walls.draw(self.__screen)
            self.__walls.update()
            self.__players.draw(self.__screen)
            self.__weapon_hitboxes.draw(self.__screen)
            self.__weapon_hitboxes.update()
            self.__players.update()
            pygame.display.update()

            self.__C.coords_recieve()
            self.__C.coords_give()
            self.__C.weapon_hitbox_recieve()
            self.__C.damage_bits(self.__players)
            self.__Map.check_room(self.__C)

            for i in self.__C.monsters:
                if i.player_colision(self.__C.player.rect):
                    damage = i.return_damage()
                    if self.__C.player.take_damage(damage):
                        quit()




    def return_run(self):
        '''
        Returns the class variable __run
        :return: Boolean
        '''
        return self.__run



pygame.font.init()
pygame.display.init()
main_game = Main_game()
main_game.bootup()

run = True
while run:
    main_game.run_game()
    run = main_game.return_run()

pygame.quit()