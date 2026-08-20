import math
import random
import tkinter as tk
import customtkinter as ctk
from PIL import Image
import time

last_time=0
Cooldown=5

def get_chance():
    chance=random.randint(1,1000)
    if chance==1:
        rarity='rainbow'
    elif 11>= chance:
        rarity='gold'
    else:
        rarity='red'
    return rarity

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, v):
        return Vector2D(self.x + v.x, self.y + v.y)

    def sub(self, v):
        return Vector2D(self.x - v.x, self.y - v.y)

    def mult(self, n):
        return Vector2D(self.x * n, self.y * n)

    def magnitude(self):
        return math.hypot(self.x, self.y)

    def normalize(self):
        m = self.magnitude()
        if m != 0:
            return Vector2D(self.x / m, self.y / m)
        return Vector2D(0, 0)

class Bee:
    def __init__(self, x, y):
        self.pos = Vector2D(x, y)
        self.vel = Vector2D(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acc = Vector2D(0, 0)
        self.max_speed = 3.0
        self.max_force = 0.3
        self.label=None
        
        self.nectar = 0
        self.max_nectar = 10
        self.state = "SEARCHING" 
        self.unload_timer = 0  # Pause timer for hive stop

    def seek(self, target_pos):
        desired = target_pos.sub(self.pos).normalize().mult(self.max_speed)
        steer = desired.sub(self.vel)

        if steer.magnitude() > self.max_force:
            steer = steer.normalize().mult(self.max_force)
        return steer

    def update(self, hive_pos, flowers, app):
        if self.nectar >= self.max_nectar and self.state != "UNLOADING":
            self.state = "RETURNING"

        if self.state == "RETURNING":
            dist_to_hive = self.pos.sub(hive_pos).magnitude()
            if dist_to_hive < 15:
                self.state = "UNLOADING"
                self.unload_timer = 15  
                self.nectar = 0
                self.vel = Vector2D(0, 0)
                self.acc = Vector2D(0, 0)
            else:
                force = self.seek(hive_pos)
                self.acc = self.acc.add(force)

        elif self.state == "UNLOADING":
            self.unload_timer -= 1
            if self.unload_timer <= 0:
                self.state = "SEARCHING"
                angle = random.uniform(0, 2 * math.pi)
                self.vel = Vector2D(math.cos(angle), math.sin(angle)).mult(self.max_speed)

        elif self.state == "SEARCHING":
            closest_flower = None
            min_dist = float('inf')
            for f in flowers:
                if f.nectar > 0:
                    d = self.pos.sub(f.pos).magnitude()
                    if d < min_dist:
                        min_dist = d
                        closest_flower = f
            
            if closest_flower and min_dist < 150: 
                if min_dist < 10:
                    self.state = "HARVESTING"
                    self.acc = Vector2D(0, 0)
                    self.vel = Vector2D(0, 0)
                    self.target_flower = closest_flower
                else:
                    force = self.seek(closest_flower.pos)
                    self.acc = self.acc.add(force)
            else:
                wander = Vector2D(random.uniform(-1, 1), random.uniform(-1, 1)).normalize().mult(0.5)
                self.acc = self.acc.add(wander)

        elif self.state == "HARVESTING":
            if hasattr(self, 'target_flower') and self.target_flower.nectar > 0:
                self.nectar += 0.1
                self.target_flower.nectar -= 0.1
                self.acc = Vector2D(0, 0)
                self.vel = Vector2D(0, 0)
            else:
                self.state = "SEARCHING"

        if self.state not in ["HARVESTING", "UNLOADING"]:
            self.vel = self.vel.add(self.acc)
            if self.vel.magnitude() > self.max_speed:
                self.vel = self.vel.normalize().mult(self.max_speed)
            self.pos = self.pos.add(self.vel)
            self.acc = Vector2D(0, 0)

flowers=[]
bees=[]

def add_bee():
    bee= Bee(350,90)
    bees.append(bee)


def on_canvas_click(event):
    global last_time
    rarity=get_chance()

    current=time.time()
    passed=current-last_time

    if passed < Cooldown:
        return

    last_time=current

    frame_x = event.x +330
    frame_y = event.y +140

    new_flower = Flower(event.x, event.y,rarity)
    new_flower.label.place(x=frame_x,y=frame_y,anchor='center')
    flowers.append(new_flower)

def add_random_flowers():
    for _ in range(5):
        rarity=get_chance()
        x = random.randint(330, 770)
        y = random.randint(140, 680)
        f = Flower(x, y, rarity)
        f.label.place(x=x,y=y)
        flowers.append(f)

def update_loop(master,speed_val):
    
    for i, bee in enumerate(bees):
        bee.max_speed = speed_val

        bee.update(Vector2D(350,90), flowers,master)

        x, y = bee.pos.x, bee.pos.y
        if bee.label:
            bee.label.place(x=x,y=y)
        else:
            bee_img=ctk.CTkImage(dark_image=Image.open('Bee_pj/bee.png'),size=(30,30))
            bee_lbl=ctk.CTkLabel(master,image=bee_img,text='',fg_color='transparent')
            
            bee.label=bee_lbl

    for f in flowers:
        if f.nectar <= 0:
            f.label.destroy()
            flowers.remove(f)

    master.after(33, update_loop,master,speed_val)

class Flower:
    def __init__(self, x, y,rarity):
        self.master=None
        self.pos = Vector2D(x, y)
        self.nectar = 20
        if rarity=='red':
            flower_img=ctk.CTkImage(dark_image=Image.open('Bee_pj/red.png'),size=(20,20))
        elif rarity=='gold':
            flower_img=ctk.CTkImage(dark_image=Image.open('Bee_pj/gold.png'),size=(20,20))
        else:
            flower_img=ctk.CTkImage(dark_image=Image.open('Bee_pj/rainbow.png'),size=(20,20))

        flower_lbl=ctk.CTkLabel(self.master,image=flower_img,text='',fg_color='#181819')
        self.label=flower_lbl
