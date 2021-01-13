"""Python escape room
This code creates a game using pyglet library. It consists of different scenes (instances of the class Scene).
Only the scene that is held in the active_scene variable is drawn.
Every scene consists of a background image and numerous clickable images (instances of the class ClickableItem).
When clicking on one of these items, active scene is changed to a new (e.g. detailed) scene.
Clicking on items can also change their position or make objects disappear.
Pressing keyboard keys (e.g. key arrows, backspace) also changes the active scene.
"""
import pyglet
window = pyglet.window.Window(width=1280, height=720)


class ClickableItem:
    """Every clickable object is represented by this class."""
    def __init__(self, name, image_name, x, y, batch, scale):
        """Inital method that constructs a clickable object:
            name - name of the object
            image_name - name of the PNG file
            x - draw on x coordinate
            y - draw on y coordinate
            batch - assigned batch to group items within the scene
            scale - a scale of the image
        """
        self.name = name
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load(image_name), x=x, y=y, batch=batch)
        self.sprite.scale = scale

    def __str__(self):
        """When clicked, the object name is showed."""
        return self.name

    def getx(self):
        """Return x coordinate of sprite."""
        return self.sprite.x

    def gety(self):
        """Return y coordinate of sprite."""
        return self.sprite.y

    def getheight(self):
        """Returns height of sprite."""
        return self.sprite.height

    def getwidth(self):
        """Returns width of sprite."""
        return self.sprite.width

    def getname(self):
        """Returns name of the object."""
        return self.name

    def delete(self):
        """Deletes sprite."""
        self.sprite.delete()


class Scene:
    """Every scene is represented by this class."""
    def __init__(self, name, background, items, batch, batch_key=""):
        """Inital method that constructs a scene:
            name - name of the scene
            background - background sprite
            items - list of clickable items
            batch - assigned batch to group items within the scene
            batch_key - assigned batch for a key item, makes key item draw last
        """
        self.name = name
        self.background = background
        self.items = items
        self.batch = batch
        self.batch_key = batch_key

    def draw(self):
        """Draws background of the scene and key items if there are any."""
        self.background.draw()
        self.batch.draw()
        if self.batch_key != "":    # if batch_key isn't empty
            self.batch_key.draw()

    def getitems(self):
        """Returns all clickable items of given scene."""
        return self.items

    def getitembyname(self, name):
        """Returns item named <name>."""
        for item in self.getitems():
            if item.getname() == name:
                return item

    def delete_key(self):
        """Deletes key from the scene"""
        key = self.getitembyname("key")
        key.delete()  # remove sprite
        self.items.remove(key)  # remove from items list


class Inventory:
    """Class to create an inventory"""
    def __init__(self):
        """Inital method that constructs an inventory"""
        self.batch = pyglet.graphics.Batch()    # assigned batch to group items within inventory
        self.image = pyglet.image.load("key.png")   # loads PNG file
        self.keys = []  # list that contains keys sprites that user clicked on
        self.base_x = 1160   # x position of the first key
        self.base_y = 633    # y position of the first key
        self.show = False   # set True to show
        self.background = pyglet.sprite.Sprite(pyglet.image.load("background_inventory.png"), x=1112, y=0)  # background sprite

    def draw(self):
        """Draws inventory (its background and its content), only when self.show is set to True"""
        if self.show is True:
            self.background.draw()
            self.batch.draw()

    def add_key(self):
        """Creates sprite (key), sets its scale and position and adds it to the list."""
        key = pyglet.sprite.Sprite(self.image, x=self.base_x, y=self.base_y - 64 * self.get_count(), batch=self.batch)
        key.scale = 0.1
        self.keys.append(key)

    def get_count(self):
        """Counts keys that are in the list self.keys"""
        return len(self.keys)

    def unshow(self):
        """Inventory isn't visible."""
        self.show = False

    def showit(self):
        """Inventory is visible."""
        self.show = True


"""Start screen:"""
batch_screen_start = pyglet.graphics.Batch()

image = pyglet.image.load('screen_start.png')
background = pyglet.sprite.Sprite(image)
background.scale = 1

button_howto = ClickableItem("button_howto", "button_howto.png", 280, 350, batch_screen_start, 0.5)     # creates clickable objects
button_start = ClickableItem("button_start", "button_start.png", 720, 350, batch_screen_start, 0.5)

sprites_screen_start = [button_howto, button_start]

screen_start = Scene("screen_start", background, sprites_screen_start, batch_screen_start)  # creates first scene (start screen)
active_scene = screen_start     # start screen is set as active scene, first scene when the program is opened

"""How to play screen:"""
batch_screen_howto = pyglet.graphics.Batch()

image = pyglet.image.load('screen_howto.png')
background = pyglet.sprite.Sprite(image)
background.scale = 1

button_arrow = ClickableItem("button_arrow", "button_arrow.png", 55, 610, batch_screen_howto, 0.5)  # loads clickable button

sprites_screen_howto = [button_arrow]
screen_howto = Scene("screen_howto", background, sprites_screen_howto, batch_screen_howto)

"""End screen:"""
batch_screen_end = pyglet.graphics.Batch()

image = pyglet.image.load('screen_end.png')
background = pyglet.sprite.Sprite(image)
background.scale = 1

sprites_screen_end = []
screen_end = Scene("screen_end", background, sprites_screen_end, batch_screen_end)      # last scene

"""Main scene1:"""
batch_main1 = pyglet.graphics.Batch()

image = pyglet.image.load('background.png')
background = pyglet.sprite.Sprite(image)
background.scale = 0.5

bed_whole = ClickableItem("bed_whole", "bed_whole.png", 731, 0, batch_main1, 0.5)
bookcase = ClickableItem("bookcase", "bookcase.png", 225, 110, batch_main1, 0.5)
bedside_table = ClickableItem("bedside_table", "bedside_table.png", 520, 110, batch_main1, 0.5)
painting = ClickableItem("painting", "painting.png", 780, 400, batch_main1, 0.5)


sprites_main1 = [bed_whole, bookcase, bedside_table, painting]

main_scene1 = Scene("main_scene1", background, sprites_main1, batch_main1)
inventory = Inventory()     # inventory is created

"""Main scene2:"""
batch_main2 = pyglet.graphics.Batch()

image = pyglet.image.load('background.png')
background = pyglet.sprite.Sprite(image)
background.scale = 0.5

table = ClickableItem("table", "table.png", 680, 100, batch_main2, 0.5)
sofa = ClickableItem("sofa", "sofa.png", 130, 113, batch_main2, 0.5)
shelf1 = ClickableItem("shelf1", "shelf1.png", 340, 350, batch_main2, 0.5)
shelf2 = ClickableItem("shelf2", "shelf2.png", 245, 450, batch_main2, 0.5)
plant2 = ClickableItem("plant2", "plant2.png", 540, 100, batch_main2, 0.5)

sprites_main2 = [table, sofa, shelf1, shelf2, plant2]

main_scene2 = Scene("main_scene2", background, sprites_main2, batch_main2)

"""Main scene3:"""
batch_main3 = pyglet.graphics.Batch()

image = pyglet.image.load('background.png')
background = pyglet.sprite.Sprite(image)
background.scale = 0.5

armchair = ClickableItem("armchair", "armchair.png", 70, 60, batch_main3, 0.5)
door = ClickableItem("door", "door.png", 740, 120, batch_main3, 0.5)
glass_window = ClickableItem("glass_window", "glass_window.png", 260, 300, batch_main3, 0.5)
plant = ClickableItem("plant", "plant.png", 550, 120, batch_main3, 0.5)

sprites_main3 = [armchair, door, glass_window, plant]
main_scene3 = Scene("main_scene3", background, sprites_main3, batch_main3)

"""Main scene4:"""
batch_main4 = pyglet.graphics.Batch()

image = pyglet.image.load('background.png')
background = pyglet.sprite.Sprite(image)
background.scale = 0.5

drawers = ClickableItem("drawers", "drawers.png", 700, 120, batch_main4, 0.4)
bed_side = ClickableItem("bed_side", "bed_side.png", 70, 65, batch_main4, 0.6)
glass_window2 = ClickableItem("glass_window2", "glass_window2.png", 230, 300, batch_main4, 0.5)

sprites_main4 = [drawers, bed_side, glass_window2]
main_scene4 = Scene("main_scene4", background, sprites_main4, batch_main4)

"""Ceiling scene:"""
batch_ceiling = pyglet.graphics.Batch()
batch_ceiling_key = pyglet.graphics.Batch()

image = pyglet.image.load('ceiling.png')
background = pyglet.sprite.Sprite(image)
background.scale = 0.5

key_rotated2 = ClickableItem("key", "key_rotated2.png", 543, 288, batch_ceiling_key, 0.08)

sprites_ceiling = [key_rotated2]
ceiling_scene = Scene("ceiling_scene", background, sprites_ceiling, batch_ceiling, batch_ceiling_key)

"""Bedside table scene (closer look to bedside table object, is accesible from main scene1
by clicking on bedside table object):"""
batch_bedside_table = pyglet.graphics.Batch()

image = pyglet.image.load('close_bedside_table.png')
close_bedside_table = pyglet.sprite.Sprite(image)
close_bedside_table.scale = 0.5

bedside_table = ClickableItem("bedside_table_new", "bedside_table.png", 450, 30, batch_bedside_table, 1)

sprites_bedside_table = [bedside_table]
bedside_table_scene = Scene("bedside_table_scene", close_bedside_table, sprites_bedside_table, batch_bedside_table)

"""Bookcase scene (closer look to bookcase object, is accesible from main scene1
by clicking on bookcase object):"""
batch_bookcase = pyglet.graphics.Batch()

image = pyglet.image.load('close_bookcase.png')
close_bookcase = pyglet.sprite.Sprite(image)
close_bookcase.scale = 0.5

bookcase = ClickableItem("bookcase_new", "bookcase.png", 300, 120, batch_bookcase, 1)

sprites_bookcase = [bookcase]
bookcase_scene = Scene("bookcase_scene", close_bookcase, sprites_bookcase, batch_bookcase)

"""Bed scene (closer look to bed object, is accesible from main scene1
by clicking on bed object):"""
batch_bed = pyglet.graphics.Batch()
image = pyglet.image.load('close_bed.png')
close_bed = pyglet.sprite.Sprite(image)
close_bed.scale = 0.5

pillows = ClickableItem("pillows", "pillows.png", 480, 365, batch_bed, 1)

sprites_bed = [pillows]
bed_scene = Scene("bed_scene", close_bed, sprites_bed, batch_bed)

"""Painting scene (closer look to painting object, is accesible from main scene1
by clicking on painting object):"""
batch_painting = pyglet.graphics.Batch()
image = pyglet.image.load('close_painting.png')
close_painting = pyglet.sprite.Sprite(image)
close_painting.scale = 0.5

sprites_painting = []
painting_scene = Scene("painting_scene", close_painting, sprites_painting, batch_painting)

"""Armchair scene (closer look to armchair object, is accesible from main scene3
by clicking on armchair object):"""
batch_armchair = pyglet.graphics.Batch()
image = pyglet.image.load('close_armchair.png')
close_armchair = pyglet.sprite.Sprite(image)
close_armchair.scale = 0.5

armchair = ClickableItem("armchair_new", "armchair.png", 170, 55, batch_armchair, 1)

sprites_armchair = [armchair]
armchair_scene = Scene("armchair_scene", close_armchair, sprites_armchair, batch_armchair)

"""Plant scene (closer look to plant object, is accesible from main scene3
by clicking on plant object):"""
batch_plant = pyglet.graphics.Batch()
image = pyglet.image.load('close_plant.png')
close_plant = pyglet.sprite.Sprite(image)
close_plant.scale = 0.5

plant = ClickableItem("plant_new", "plant.png", 450, 40, batch_plant, 1)

sprites_plant = [plant]
plant_scene = Scene("plant_scene", close_plant, sprites_plant, batch_plant)

"""Table scene (closer look to table object, is accesible from main scene2
by clicking on table object):"""
batch_table = pyglet.graphics.Batch()
image = pyglet.image.load('close_table.png')
close_table = pyglet.sprite.Sprite(image)
close_table.scale = 0.5

sprites_table = []
table_scene = Scene("table_scene", close_table, sprites_table, batch_table)

"""Drawers scene (closer look to drawers object, is accesible from main scene4
by clicking on drawers object):"""
batch_drawers = pyglet.graphics.Batch()
image = pyglet.image.load('close_drawers.png')
close_drawers = pyglet.sprite.Sprite(image)
close_drawers.scale = 0.5

drawers = ClickableItem("drawers_new", "drawers.png", 460, 30, batch_drawers, 0.7)

sprites_drawers = [drawers]
drawers_scene = Scene("drawers_scene", close_drawers, sprites_drawers, batch_drawers)

"""Shelf scene (closer look to shelf object, is accesible from main scene2
by clicking on shelf object):"""
batch_shelf = pyglet.graphics.Batch()
image = pyglet.image.load('close_shelf.png')
close_shelf = pyglet.sprite.Sprite(image)
close_shelf.scale = 0.5

shelf_book = ClickableItem("shelf_book", "shelf_book.png", 600, 344, batch_shelf, 0.5)

sprites_shelf = [shelf_book]
shelf_scene = Scene("shelf_scene", close_shelf, sprites_shelf, batch_shelf)

"""Cactus scene (closer look to cactus object, is accesible from main scene1
by clicking on cactus object):"""
batch_cactus = pyglet.graphics.Batch()
image = pyglet.image.load('close_cactus.png')
close_cactus = pyglet.sprite.Sprite(image)
close_cactus.scale = 0.5

cactus = ClickableItem("cactus", "cactus.png", 320, 240, batch_cactus, 1)

sprites_cactus = [cactus]
cactus_scene = Scene("cactus_scene", close_cactus, sprites_cactus, batch_cactus)

"""Sofa scene (closer look to sofa object, is accesible from main scene2
by clicking on sofa object):"""
batch_sofa = pyglet.graphics.Batch()
image = pyglet.image.load('close_sofa.png')
close_sofa = pyglet.sprite.Sprite(image)
close_sofa.scale = 0.5

sofa_pillow = ClickableItem("sofa_pillow", "sofa_pillow.png", 464, 240, batch_sofa, 1)

sprites_sofa = [sofa_pillow]
sofa_scene = Scene("sofa_scene", close_sofa, sprites_sofa, batch_sofa)

"""Open door scene (closer look to open door object, is accesible from main scene3
by clicking on door object after finding all keys):"""
batch_close_open_door = pyglet.graphics.Batch()
image = pyglet.image.load('close_open_door.png')
close_open_door = pyglet.sprite.Sprite(image)
close_open_door.scale = 0.5

open_door = ClickableItem("open_door", "open_door.png", 484, 6, batch_close_open_door, 0.85)

sprites_close_open_door = [open_door]
close_open_door_scene = Scene("close_open_door_scene", close_open_door, sprites_close_open_door, batch_close_open_door)


"""Open bedside table scene (closer look to open bedside table object, is accesible from bedside table scene
by clicking on bedside table object):"""
batch_open_bedside_table = pyglet.graphics.Batch()
batch_open_bedside_table_key = pyglet.graphics.Batch()

image = pyglet.image.load('close_bedside_table.png')
close_bedside_table = pyglet.sprite.Sprite(image)
close_bedside_table.scale = 0.5

open_bedside_table = ClickableItem("open_bedside_table", "open_bedside_table.png", 403, 31, batch_open_bedside_table, 1)
key = ClickableItem("key", "key.png", 570, 140, batch_open_bedside_table_key, 0.1)

sprites_open_bedside_table = [key, open_bedside_table]
open_bedside_table_scene = Scene("open_bedside_table_scene", close_bedside_table, sprites_open_bedside_table, batch_open_bedside_table, batch_open_bedside_table_key)

"""Open bookcase scene (closer look to open bookcase object, is accesible from bookcase scene
by clicking on bookcase object):"""
batch_open_bookcase = pyglet.graphics.Batch()
batch_open_bookcase_key = pyglet.graphics.Batch()

image = pyglet.image.load('close_bookcase.png')
close_bookcase = pyglet.sprite.Sprite(image)
close_bookcase.scale = 0.5

open_bookcase = ClickableItem("open_bookcase", "open_bookcase.png", 294, 120, batch_open_bookcase, 1)
key = ClickableItem("key", "key.png", 580, 250, batch_open_bookcase_key, 0.1)

sprites_open_bookcase = [key, open_bookcase]
open_bookcase_scene = Scene("open_bookcase_scene", close_bookcase, sprites_open_bookcase, batch_open_bookcase, batch_open_bookcase_key)

"""Pillows up bed scene (closer look to pillows object, is accesible from bed scene
by clicking on pillows object):"""
batch_pillows_up_bed = pyglet.graphics.Batch()
batch_pillows_up_bed_key = pyglet.graphics.Batch()

image = pyglet.image.load('close_bed.png')
close_bed = pyglet.sprite.Sprite(image)
close_bed.scale = 0.5

pillows = ClickableItem("pillows", "pillows.png", 480, 400, batch_pillows_up_bed, 1)
key = ClickableItem("key", "key.png", 755, 380, batch_pillows_up_bed_key, 0.1)

sprites_pillows_up_bed = [key, pillows]
bed_pillows_up_scene = Scene("bed_pillows_up_scene", close_bed, sprites_pillows_up_bed, batch_pillows_up_bed, batch_pillows_up_bed_key)

"""Shelf book moved scene (closer look to book/shelf object, is accesible from shelf scene
by clicking on shelf book object):"""
batch_shelf_book_moved = pyglet.graphics.Batch()
batch_shelf_book_moved_key = pyglet.graphics.Batch()

image = pyglet.image.load('close_shelf.png')
close_shelf = pyglet.sprite.Sprite(image)
close_shelf.scale = 0.5

shelf_book = ClickableItem("shelf_book", "shelf_book.png", 525, 343, batch_shelf_book_moved, 0.5)
key = ClickableItem("key", "key.png", 675, 345, batch_shelf_book_moved_key, 0.09)

sprites_shelf_book_moved = [shelf_book, key]
shelf_book_moved_scene = Scene("shelf_book_moved_scene", close_shelf, sprites_shelf_book_moved, batch_shelf_book_moved, batch_shelf_book_moved_key)

"""Armchair moved scene (closer look to armchair moved object, is accesible from armchair scene
by clicking on armchair object):"""
batch_armchair_moved = pyglet.graphics.Batch()
batch_armchair_moved_key = pyglet.graphics.Batch()

image = pyglet.image.load('close_armchair.png')
close_armchair = pyglet.sprite.Sprite(image)
close_armchair.scale = 0.5

armchair = ClickableItem("armchair", "armchair.png", 280, 55, batch_armchair_moved, 1)
key = ClickableItem("key", "key.png", 230, 160, batch_armchair_moved_key, 0.1)

sprites_armchair_moved = [key, armchair]
armchair_moved_scene = Scene("armchair_moved_scene", close_armchair, sprites_armchair_moved, batch_armchair_moved, batch_armchair_moved_key)

"""Cactus moved scene (closer look to cactus moved object, is accesible from cactus scene
by clicking on cactus object):"""
batch_cactus_moved = pyglet.graphics.Batch()
batch_cactus_moved_key = pyglet.graphics.Batch()

image = pyglet.image.load('close_cactus.png')
close_cactus = pyglet.sprite.Sprite(image)
close_cactus.scale = 0.5

key_rotated = ClickableItem("key", "key_rotated.png", 372, 332, batch_cactus_moved_key, 0.1)
cactus_half = ClickableItem("cactus_half", "cactus_half.png", 320, 241, batch_cactus_moved, 1)

sprites_cactus_moved = [key_rotated, cactus_half]
cactus_moved_scene = Scene("cactus_moved_scene", close_cactus, sprites_cactus_moved, batch_cactus_moved, batch_cactus_moved_key)

"""Open drawers scene (closer look to open drawers object, is accesible from drawers scene
by clicking on drawers object):"""
batch_open_drawers = pyglet.graphics.Batch()
batch_open_drawers_key = pyglet.graphics.Batch()

image = pyglet.image.load('close_drawers.png')
close_drawers = pyglet.sprite.Sprite(image)
close_drawers.scale = 0.5

open_drawers = ClickableItem("open_drawers", "open_drawers.png", 460, 30, batch_open_drawers, 0.7)
key = ClickableItem("key", "key.png", 623, 140, batch_open_drawers_key, 0.1)

sprites_open_drawers = [key, open_drawers]
open_drawers_scene = Scene("open_drawers_scene", close_drawers, sprites_open_drawers, batch_open_drawers, batch_open_drawers_key)

"""Sofa pillow up scene (closer look to sofa pillow object, is accesible from sofa scene
by clicking on sofa pillow object):"""
batch_sofa_pillow_up = pyglet.graphics.Batch()
batch_sofa_pillow_up_key = pyglet.graphics.Batch()

image = pyglet.image.load('close_sofa.png')
close_sofa = pyglet.sprite.Sprite(image)
close_sofa.scale = 0.5

sofa_pillow = ClickableItem("sofa_pillow", "sofa_pillow.png", 464, 300, batch_sofa_pillow_up, 1)
key = ClickableItem("key", "key.png", 550, 250, batch_sofa_pillow_up_key, 0.1)

sprites_sofa_pillow_up = [key, sofa_pillow]
sofa_pillow_up_scene = Scene("sofa_pillow_up_scene", close_sofa, sprites_sofa_pillow_up, batch_sofa_pillow_up, batch_sofa_pillow_up_key)

"""Plant moved scene (closer look to plant object, is accesible from plant scene
by clicking on plant object):"""
batch_plant_moved = pyglet.graphics.Batch()
batch_plant_moved_key = pyglet.graphics.Batch()

image = pyglet.image.load('close_plant.png')
close_plant = pyglet.sprite.Sprite(image)
close_plant.scale = 0.5

plant_moved = ClickableItem("plant_moved", "plant_moved.png", 443, 40, batch_plant_moved, 1)
key = ClickableItem("key", "key.png", 500, 280, batch_plant_moved_key, 0.1)

sprites_plant_moved = [key, plant_moved]
plant_moved_scene = Scene("plant_moved_scene", close_plant, sprites_plant_moved, batch_plant_moved_key, batch_plant_moved)


def click(x, y, button, mod):
    """Function that handles all mouse events.
    When clicking on an object from Clickable item class, active scene is changed """
    for object in active_scene.getitems():
        if isinstance(object, ClickableItem):   # is object from ClickableItem class
            if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < object.gety() + object.getheight():
                # when clicking on an object from Clickable item class, active scene is changed
                if object.getname() == "bed_whole":
                    change_scene(bed_scene)
                if object.getname() == "painting":
                    change_scene(painting_scene)
                if object.getname() == "armchair":
                    change_scene(armchair_scene)
                if object.getname() == "plant":
                    change_scene(plant_scene)
                if object.getname() == "table":
                    change_scene(table_scene)
                if object.getname() == "drawers":
                    change_scene(drawers_scene)
                if object.getname() == "shelf1" or object.getname() == "shelf2":
                    change_scene(shelf_scene)
                if object.getname() == "sofa":
                    change_scene(sofa_scene)
                if object.getname() == "bed_side":
                    change_scene(bed_scene)
                if object.getname() == "button_start":
                    change_scene(main_scene1)
                    inventory.showit()
                if object.getname() == "button_howto":
                    change_scene(screen_howto)
                if object.getname() == "button_arrow":
                    change_scene(screen_start)
                if object.getname() == "bookcase":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < 300:
                        change_scene(bookcase_scene)
                if object.getname() == "bedside_table":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < 270:
                        change_scene(bedside_table_scene)
                if object.getname() == "bookcase":
                    if object.getx() < x < object.getx() + object.getwidth() and 500 < y < 650:
                        change_scene(cactus_scene)
                if object.getname() == "key":   # when clicking on key object
                    active_scene.delete_key()   # the key is deleted from active scene
                    inventory.add_key()     # and one key is added to the inventory list
                    return
                if object.getname() == "door":  # when clicking on door object
                    if inventory.get_count() == 10:     # if all 10 keys are in inventory
                        change_scene(close_open_door_scene)    # active scene is changed to open door scene
                if object.getname() == "open_door":     # when clicking on open door
                    if inventory.get_count() == 10:     # if all 10 keys are in inventory
                        inventory.unshow()  # inventory isn't visible
                        change_scene(screen_end)    # active scene is changed to the last scene
                        return

            if active_scene == bedside_table_scene:     # "opens" bedside table when it's "closed"
                if object.getname() == "bedside_table_new":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < 270:
                        change_scene(open_bedside_table_scene)
            elif active_scene == open_bedside_table_scene:   # "closes" bedside table when it's "opened"
                if object.getname() == "open_bedside_table":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < 270:
                        change_scene(bedside_table_scene)

            if active_scene == bookcase_scene:  # "opens" bookcase when it's "closed"
                if object.getname() == "bookcase_new":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < 300:
                        change_scene(open_bookcase_scene)
            elif active_scene == open_bookcase_scene:   # "closes" bookcase when it's "opened"
                if object.getname() == "open_bookcase":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < 300:
                        change_scene(bookcase_scene)

            if active_scene == bed_scene:   # "lifts" pillows when they are down
                if object.getname() == "pillows":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < object.gety() + object.getheight():
                        change_scene(bed_pillows_up_scene)
            elif active_scene == bed_pillows_up_scene:  # puts pillows down when they are up
                if object.getname() == "pillows":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < object.gety() + object.getheight():
                        change_scene(bed_scene)

            if active_scene == shelf_scene:     # moves book to the left
                if object.getname() == "shelf_book":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < object.gety() + object.getheight():
                        change_scene(shelf_book_moved_scene)
            elif active_scene == shelf_book_moved_scene:    # moves book to the right
                if object.getname() == "shelf_book":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < object.gety() + object.getheight():
                        change_scene(shelf_scene)

            if active_scene == armchair_scene:  # moves armchair to the right
                if object.getname() == "armchair_new":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < object.gety() + object.getheight():
                        change_scene(armchair_moved_scene)
            elif active_scene == armchair_moved_scene:  # moves armchair to the left
                if object.getname() == "armchair_new":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < object.gety() + object.getheight():
                        change_scene(armchair_scene)

            if active_scene == cactus_scene:    # makes cactus disappear
                if object.getname() == "cactus":
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < object.gety() + object.getheight():
                        change_scene(cactus_moved_scene)
            elif active_scene == cactus_moved_scene:
                if object.getname() == "cactus_half":   # makes cactus appear
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < object.gety() + object.getheight():
                        change_scene(cactus_scene)

            if active_scene == drawers_scene:
                if object.getname() == "drawers_new":   # "opens" drawers when they are "closed"
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < 200:
                        change_scene(open_drawers_scene)
            elif active_scene == open_drawers_scene:
                if object.getname() == "open_drawers":  # "closes" drawers when they are "opened"
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < 200:
                        change_scene(drawers_scene)

            if active_scene == sofa_scene:
                if object.getname() == "sofa_pillow":   # lifts pillow when it's down
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < object.gety() + object.getheight():
                        change_scene(sofa_pillow_up_scene)
            elif active_scene == sofa_pillow_up_scene:
                if object.getname() == "sofa_pillow":   # puts pillow down when it's up
                    if object.getx() < x < object.getx() + object.getwidth() and object.gety() < y < object.gety() + object.getheight():
                        change_scene(sofa_scene)

            if active_scene == plant_scene:
                if object.getname() == "plant_new":     # "opens" plant leaves
                    if object.getx() < x < object.getx() + object.getwidth() and 180 < y < 400:
                        change_scene(plant_moved_scene)
            elif active_scene == plant_moved_scene:
                if object.getname() == "plant_moved":   # "closes" plant leaves
                    if object.getx() < x < object.getx() + object.getwidth() and 180 < y < 400:
                        change_scene(plant_scene)


def change_scene(scene):
    """Sets scene as active scene."""
    global active_scene
    active_scene = scene


def return_to_scene(symbol, mod):
    """If a certain key is pressed, active scene is changed. """
    global active_scene
    close_scenes_main1 = [bedside_table_scene, bookcase_scene, bed_scene, painting_scene, open_bedside_table_scene, open_bookcase_scene, bed_pillows_up_scene, cactus_scene, cactus_moved_scene]
    close_scenes_main2 = [table_scene, shelf_scene, shelf_book_moved_scene, sofa_scene, sofa_pillow_up_scene]
    close_scenes_main3 = [armchair_scene, plant_scene, armchair_moved_scene, plant_moved_scene]
    close_scenes_main4 = [drawers_scene, open_drawers_scene]
    if symbol == pyglet.window.key.BACKSPACE:   # if backspace is pressed (for returning to main scenes from close scenes)
        if active_scene in close_scenes_main1:
            change_scene(main_scene1)
        elif active_scene in close_scenes_main2:
            change_scene(main_scene2)
        elif active_scene in close_scenes_main3:
            change_scene(main_scene3)
        elif active_scene in close_scenes_main4:
            change_scene(main_scene4)
        elif active_scene == ceiling_scene:
            change_scene(main_scene1)
    elif symbol == pyglet.window.key.LEFT:  # if key left is pressed (for navigating around the room, changing main scenes)
        if active_scene == main_scene1:
            change_scene(main_scene2)
        elif active_scene == main_scene2:
            change_scene(main_scene3)
        elif active_scene == main_scene3:
            change_scene(main_scene4)
        elif active_scene == main_scene4:
            change_scene(main_scene1)
    elif symbol == pyglet.window.key.RIGHT:     # if key right is pressed (for navigating around the room, changing main scenes)
        if active_scene == main_scene2:
            change_scene(main_scene1)
        elif active_scene == main_scene3:
            change_scene(main_scene2)
        elif active_scene == main_scene4:
            change_scene(main_scene3)
        elif active_scene == main_scene1:
            change_scene(main_scene4)
    elif symbol == pyglet.window.key.UP:    # to "look up" (changing scene to ceiling scene)
        if active_scene == main_scene1 or active_scene == main_scene2 or active_scene == main_scene3 or active_scene == main_scene4:
            change_scene(ceiling_scene)
    elif symbol == pyglet.window.key.DOWN:  # to "look down" (going from ceiling scene to main scene1)
        if active_scene == ceiling_scene:
            change_scene(main_scene1)
    elif symbol == pyglet.window.key.SPACE:     # to go back to the start screen
        if active_scene != screen_end:
            inventory.unshow()  # inventory isn't visible when on start screen
            change_scene(screen_start)


def draw_current_scene():
    window.clear()
    active_scene.draw()
    inventory.draw()


window.push_handlers(
    on_draw=draw_current_scene,
    on_mouse_press=click,
    on_key_press=return_to_scene,
    )

pyglet.app.run()
