from tkinter import END, Listbox, Scrollbar, Tk, Frame, Label, Button, W,S,E,N,SW,SE, BOTH
from PIL import Image
from PIL.ImageTk import PhotoImage


# files
import os
from typing import Dict, List
HERE = os.path.abspath(os.path.dirname(__file__))
IMAGE_FOLDER = os.path.join(HERE, "Images")
SCENES_FOLDER = os.path.join(IMAGE_FOLDER, "Scenes")
DEFAULT_IMAGE = os.path.join(SCENES_FOLDER, "default.png")
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 600

# GAME DATA
TOTAL_INVENTORY = ["Rope", "Bottle", "Newspaper", "Book", "Coins"]
CURRENT_INVENTORY = ["Rope", "Bottle"]
SCENES = ["Boxing", "Hallway", "HallwayWest", "Office"]
ACTIVE_SCENE = "default"
current_image: PhotoImage 

def load_scenes(directory:str = SCENES_FOLDER)->Dict[str, PhotoImage]:
    image_dict = {}
    for (dir_path, _, file_names) in os.walk(directory):
        print((dir_path, _, file_names))
        for file in file_names:
            name, _ = file.split(".")
            current_image = Image.open(os.path.join(dir_path, file))
            current_image = current_image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
            image_dict[name] = (current_image)
    return image_dict

def on_select(event):
    widget = event.widget
    index = int(widget.curselection()[0])
    value = widget.get(index)
    print(f" Scene number {index} was selected and is called {value}")
    global ACTIVE_SCENE
    ACTIVE_SCENE = value


def draw_scene_list(parent:Frame)-> Frame:
    default_scenes = load_scenes()
    scenes_frame = Frame(parent, name="scene_frame", height=100, width=120)
    scene_box = Listbox(scenes_frame, height=4, width=60)
    for item in default_scenes:
        scene_box.insert(END, item)
    scene_box.grid(row=0, column=0, sticky=E, pady=2)
    scene_scrollbar = Scrollbar(scenes_frame)
    scene_scrollbar.grid(row=0, column=1, sticky=W, pady=2)
    scene_box.config(yscrollcommand =scene_scrollbar.set)
    scene_scrollbar.config(command=scene_box.yview)
    scene_box.bind('<<ListboxSelect>>', on_select)
    return scenes_frame


def draw_main_window(edit_mode:bool = True):
    # init values
    scene_index = 0
    scene_title = "untitled"

    root_edit = Tk()
    root_edit.resizable(False, False)
    IMAGES_DICT = load_scenes()
    play_frame = Frame(root_edit, height=IMAGE_WIDTH, width=IMAGE_HEIGHT+100)
    if edit_mode:
        root_edit.title("Edit Window")
        root_edit.geometry("1200x900")
        play_frame.grid(row=1, column=1, sticky=SE, pady=2, rowspan=2, columnspan=2) 
    else:
        root_edit.title("Play Window")
        root_edit.geometry(f"{IMAGE_WIDTH}x{IMAGE_HEIGHT+100}")
        play_frame.grid(row=0, column=0) 


    play_window = draw_play_window(parent=play_frame, image_dict=IMAGES_DICT)

    play_window.grid(row=0, column=0, sticky=SE, pady=2)


    if edit_mode:
        details_frame = Frame(root_edit, height=200)
        label_scene_index = Label(details_frame, text=f"current index:{scene_index}")
        label_scene_title = Label(details_frame, text=f"current title:{scene_title}")
        label_scene_index.grid(row=0, column=0, sticky=W, pady=2) 
        label_scene_title.grid(row=0, column=1, sticky=W, pady=2) 
        scene_listbox = draw_scene_list(details_frame)
        scene_listbox.grid(row=0, column=2, sticky=W, pady=2) 
        details_frame.grid(row=0, column=1, columnspan=2)

        buttons_frame = Frame(root_edit, width=400)
        button_define_click_region = Button(buttons_frame, text="define click region")
        button_define_action = Button(buttons_frame, text="define action")
        button_define_combination = Button(buttons_frame, text="define combination")
        button_define_click_region.grid(row=0, column=0, sticky=W, pady=2) 
        button_define_action.grid(row=1, column=0, sticky=W, pady=2) 
        button_define_combination.grid(row=2, column=0, sticky=W, pady=2)
        buttons_frame.grid(row=1, column=0, rowspan=2)

        beeg_buttons_frame = Frame(root_edit, width=400, height=200)
        button_define_test = Button(beeg_buttons_frame, text="TEST", height=13, width = 25, bg="red")
        button_define_play = Button(beeg_buttons_frame, text="PLAY", height=13, width = 25, state="disabled")
        button_define_test.grid(row=0, column=0)
        button_define_play.grid(row=0, column=1)

        beeg_buttons_frame.grid(row=0, column=0)

    root_edit.mainloop()
    



def draw_play_window(parent: Frame = None, image_dict: Dict[str, PhotoImage] = None) -> Frame:
    # relabel for convenience
    root_play = parent

    # define frame for dimensions
    play_frame = Frame(root_play, width=800, height=700)
    play_frame.grid(row=0, column=0)
    # get current image  TODO
    global ACTIVE_SCENE
    global current_image
    current_image = PhotoImage(image_dict[ACTIVE_SCENE], master = parent)
    image_label = Label(play_frame, image=current_image)

    # define buttons
    button_labels = ["Use", "Pick Up", "Go", "Look", "Push", "Pull"]
    button_width=17
    buttons_frame = Frame(play_frame, name="buttons_frame", width=400, height=100)
    button_list = []
    for index in range(6):
        button_list.append(Button(buttons_frame,width=button_width, text=button_labels[index]))
    button_pad_y = 5
    button_pad_x = 2
    button_list[0].grid(row=0, column=0, pady=button_pad_y, padx=button_pad_x)
    button_list[1].grid(row=0, column=1, pady=button_pad_y, padx=button_pad_x)
    button_list[2].grid(row=0, column=2, pady=button_pad_y, padx=button_pad_x)
    button_list[3].grid(row=1, column=0, pady=button_pad_y, padx=button_pad_x)
    button_list[4].grid(row=1, column=1, pady=button_pad_y, padx=button_pad_x)
    button_list[5].grid(row=1, column=2, pady=button_pad_y, padx=button_pad_x)
    
    # define inventory box
    default_inventory_items = CURRENT_INVENTORY
    inventory_frame = Frame(play_frame, name="inventory_frame", height=100, width=120)
    inventory_box = Listbox(inventory_frame, height=4, width=60)
    for item in default_inventory_items:
        inventory_box.insert(END, item)
    inventory_box.grid(row=0, column=0, sticky=E, pady=2)
    scrollbar = Scrollbar(inventory_frame)
    scrollbar.grid(row=0, column=1, sticky=W, pady=2)
    inventory_box.config(yscrollcommand =scrollbar.set)
    scrollbar.config(command=inventory_box.yview)

    # place in frame
    image_label.place(x=0,y=0)
    buttons_frame.place(x=5,y=612)
    inventory_frame.place(x=410,y=612)

    return play_frame


if __name__ == "__main__":
    load_scenes()
    draw_main_window(edit_mode=True)

