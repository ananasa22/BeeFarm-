'''Good luck reading the spaghetti code :) '''

import customtkinter as ctk
from PIL import Image
import numpy as np
import tkinter as tk
from backend import on_canvas_click,add_random_flowers,update_loop,Flower,add_bee
import json
import build_info_frame
import build_main_frame
import build_settings_frame

app = ctk.CTk()
app.title("Bee Simulator")
app.geometry("1100x720")
app.minsize(980, 640)
app.configure(fg_color='#121316')

changed_dark=False
changed_light=False

mutevfx=False
mutemusic=False

honey_mult=1

bold_font = ctk.CTkFont(family="Impact", size=48, weight="bold")
subtitle_font = ctk.CTkFont(family="Arial", size=10, weight="bold")

def get_honey():
  with open('Bee_pj/player_data.json') as f:
    data=json.load(f)
  return f"{data.get('honey'):.2f}"


def mute_vfx():
  global mute_vfx
  sound_img=ctk.CTkImage(dark_image=Image.open("Bee_pj/volume-2.png"),size=(20,20))
  sound_lbl=ctk.CTkLabel(Sound_but, image=sound_img, text='', fg_color="#2b2a2e")

  mute_img=ctk.CTkImage(dark_image=Image.open("Bee_pj/volume-off.png"),size=(20,20))
  mute_lbl=ctk.CTkLabel(Sound_but,image=mute_img, text='', fg_color="#111113")

  if not mute_vfx:
    Sound_but.configure(
      fg_color='#2b2a2e',
      border_color='#F3B300'
    )
    sound_lbl.place(relx=.5, rely=0.5, anchor="center")
    mute_lbl.destroy()

    mute_vfx=True

  else:
    Sound_but.configure(
      border_color="#363636",
      fg_color="#111113",
    )
    mute_lbl.place(relx=.5, rely=0.5, anchor="center")
    sound_lbl.destroy()
    
    mute_vfx=False


def mute_music():
  global mute_music
  music_img=ctk.CTkImage(dark_image=Image.open("Bee_pj/headphones.png"),size=(20,20))
  music_lbl=ctk.CTkLabel(music_but, image=music_img, text='', fg_color="#2b2a2e")

  mutemusic_img=ctk.CTkImage(dark_image=Image.open("Bee_pj/headphone-off.png"),size=(20,20))
  mutemusic_lbl=ctk.CTkLabel(music_but,image=mutemusic_img, text='', fg_color="#111113")

  if not mute_music:
    music_but.configure(
      fg_color='#2b2a2e',
      border_color='#F3B300'
    )
    music_lbl.place(relx=.5, rely=0.5, anchor="center")
    mutemusic_lbl.destroy()

    mute_music=True

  else:
    music_but.configure(
      border_color="#363636",
      fg_color="#111113",
    )
    mutemusic_lbl.place(relx=.5, rely=0.5, anchor="center")
    music_lbl.destroy()
    
    mute_music=False


def switch_to_dark():
  global changed_dark
  global changed_light

  if not changed_dark:
    ctk.set_appearance_mode('dark')
    DarkMode_but.configure(
      fg_color='#2b2a2e',
      text_color='#F3B300',
      border_color='#F3B300'
    )
    if changed_light:
      LightMode_but.configure(
        border_color="#363636",
        fg_color="#111113",
        text_color="grey",
      )
      changed_light=False
    changed_dark=True

def switch_to_light():
  global changed_dark
  global changed_light
  if not changed_light:
    ctk.set_appearance_mode('light')
    LightMode_but.configure(
      fg_color='#2b2a2e',
      text_color='#F3B300',
      border_color='#F3B300'
    )
    if changed_dark:
      DarkMode_but.configure(
        border_color="#363636",
        fg_color="#111113",
        text_color="grey",
      )
      changed_dark=False
    changed_light=True      

def open_settings():
  global LightMode_but
  global DarkMode_but
  global main_frame
  global settingsFrame
  global Sound_but
  global music_but
  
  main_frame.destroy()

  settingsFrame=ctk.CTkFrame(
      master=app,
      fg_color="#1A1A1B",
      corner_radius=30,
      width=400,
      height=500,
      border_color='#363636',
      border_width=1,
  )
  settingsFrame.place(relx=0.5, rely=0.5, anchor="center")

  close=ctk.CTkButton(
    settingsFrame,
    text='✖',
    width=20,
    height=20,
    text_color='white',
    fg_color="#1A1A1B",
    command=close_settings,
    font=ctk.CTkFont(size=25),
    hover_color='#2b2a2e',
    corner_radius=10,
    
  )
  close.place(relx=0.9, rely=0.1, anchor="center")

  title_frame=ctk.CTkFrame(
      master=settingsFrame,
      fg_color="#1A1A1B",
      width=100,
      height=50,
  )
  title_frame.place(relx=0.27, rely=0.1, anchor="center")

  settings_img=ctk.CTkImage(dark_image=Image.open('Bee_pj/sliders-vertical.png'),size=(30,30))

  settings_lbl=ctk.CTkLabel(title_frame,image=settings_img, text='')
  settings_lbl.pack(side="left",padx=(3,0))

  settings_label = ctk.CTkLabel(
    title_frame,
    text="SETTINGS",
    font=ctk.CTkFont(family="Impact", size=28, weight="bold"),
    text_color="#F3B300"  
  )
  settings_label.pack(side="left", padx=(8, 0))

  sub_tlt=ctk.CTkLabel(
    settingsFrame,
    text="APPEARANVE MODE",
    width=100,
    font=ctk.CTkFont(family="Arial", size=14),
    text_color="grey"
  )
  sub_tlt.place(relx=0.25, rely=0.22, anchor="center")

  appearance_frame=ctk.CTkFrame(
    master=settingsFrame,
    fg_color="#1A1A1B",
  )

  appearance_frame.place(relx=0.48, rely=0.3, anchor="center")

  DarkMode_but=ctk.CTkButton(
    master=appearance_frame,
    width=180,
    height=45,
    text="☾   Dark Mode",
    font=subtitle_font,
    corner_radius=15,
    fg_color="#111113",
    text_color="grey",
    hover=False,
    command=switch_to_dark,
    border_color="#363636",
    border_width=2
  )

  DarkMode_but.pack(side="left", padx=(10,10))

  LightMode_but=ctk.CTkButton(
    master=appearance_frame,
    width=180,
    height=45,
    text="𖤓   Light Mode",
    font=subtitle_font,
    corner_radius=15,
    fg_color="#111113",
    text_color="grey",
    hover=False,
    command=switch_to_light,
    border_color="#363636",
    border_width=2
  )

  LightMode_but.pack(side="left", padx=(3,0))

  vfx_frame=ctk.CTkFrame(
    master=settingsFrame,
    width=380,
    height=70,
    corner_radius=15,
    fg_color="#111113",
    border_color="#363636",
    border_width=2
  )

  vfx_frame.place(relx=0.5, rely=0.45, anchor="center")

  vfx_label = ctk.CTkLabel(
      vfx_frame,
      width=50,
      height=30,
      text="AUDIO SOUND FX",
      font=ctk.CTkFont(family="Impact", size=15),
      text_color="#FFFFFF",
      anchor='center'
  )
  vfx_label.place(relx=0.2, rely=0.33, anchor="center")

  Sound_but=ctk.CTkButton(
    master=vfx_frame,
    width=50,
    height=50,
    corner_radius=15,
    text="",
    fg_color="#111113",
    hover=False,
    command=mute_vfx,
    border_color="#F3B300",
    border_width=2,
  )

  Sound_but.place(relx=0.9, rely=0.5, anchor="center")

  sound_img=ctk.CTkImage(dark_image=Image.open("Bee_pj/volume-2.png"),size=(20,20))
  sound_lbl=ctk.CTkLabel(Sound_but, image=sound_img, text='', fg_color="#111113")

  sound_lbl.place(relx=.5, rely=0.5, anchor="center")

  vfx_sub_tlt=ctk.CTkLabel(
    vfx_frame,
    text="Audio Synthesizer",
    font=ctk.CTkFont(family="Arial", size=11),
    text_color="grey"
  )
  vfx_sub_tlt.place(relx=0.16, rely=0.62, anchor="center")




  music_frame=ctk.CTkFrame(
    master=settingsFrame,
    width=380,
    height=70,
    corner_radius=15,
    fg_color="#111113",
    border_color="#363636",
    border_width=2
  )

  music_frame.place(relx=0.5, rely=0.63, anchor="center")

  music_label = ctk.CTkLabel(
      music_frame,
      width=50,
      height=30,
      text="AUDIO SOUND FX",
      font=ctk.CTkFont(family="Impact", size=15),
      text_color="#FFFFFF",
      anchor='center'
  )
  music_label.place(relx=0.2, rely=0.33, anchor="center")

  music_but=ctk.CTkButton(
    master=music_frame,
    width=50,
    height=50,
    corner_radius=15,
    text="",
    fg_color="#111113",
    hover=False,
    command=mute_music,
    border_color="#F3B300",
    border_width=2,
  )

  music_but.place(relx=0.9, rely=0.5, anchor="center")

  music_img=ctk.CTkImage(dark_image=Image.open("Bee_pj/headphones.png"),size=(20,20))
  music_lbl=ctk.CTkLabel(music_but, image=sound_img, text='', fg_color="#111113")

  music_lbl.place(relx=.5, rely=0.5, anchor="center")

  music_sub_tlt=ctk.CTkLabel(
    music_frame,
    text="Audio Synthesizer",
    font=ctk.CTkFont(family="Arial", size=11),
    text_color="grey"
  )
  music_sub_tlt.place(relx=0.16, rely=0.62, anchor="center")

  
def start_game(): #this was a bad idea 8 hours just for the main menu 
  main_frame.destroy()

  left_frame=ctk.CTkFrame(
    master=app,
    fg_color="#181819",
    corner_radius=35,
    width=280,
    height=680,
    border_color='#363636',
    border_width=1,
  )

  left_frame.place(relx=0.14, rely=0.5, anchor="center")

  info_frame=ctk.CTkFrame(
    master=app,
    fg_color="#181819",
    corner_radius=25,
    width=480,
    height=80,
    border_color='#363636',
    border_width=1,
  )

  info_frame.place(relx=0.5, rely=0.09, anchor="center")
  info_frame.pack_propagate(False) 

  build_info_frame.build_dashboard_panel(info_frame)

  mid_frame=ctk.CTkFrame(
    master=app,
    fg_color="#181819",
    corner_radius=45,
    width=480,
    height=580,
    border_color='#363636',
    border_width=1,
  )

  canvas = tk.Canvas(mid_frame, bg="#181819", highlightthickness=0,width=440,height=540)
  canvas.place(relx=0.5, rely=0.5, anchor="center")

  output=build_main_frame.build_mid_frame_panel(mid_frame)
  hise_cord=output['hive_box_coords']
  start_cld=output['start_cooldown']

  update_loop(canvas,2,honey_mult)

  Flower.master=canvas
  canvas.bind("<Button-1>", on_canvas_click)

  mid_frame.place(relx=0.5, rely=0.57, anchor="center")

  field_frame=ctk.CTkFrame(
    master=app,
    fg_color="#181819",
    corner_radius=35,
    width=280,
    height=180,
    border_color='#363636',
    border_width=1,
  )

  field_frame.place(relx=0.86, rely=0.16, anchor="center")
  build_settings_frame.build_nest_control_panel(field_frame,mid_frame)
  

  loot_frame=ctk.CTkFrame(
    master=app,
    fg_color="#181819",
    corner_radius=35,
    width=280,
    height=480,
    border_color='#363636',
    border_width=1,
  )

  loot_frame.place(relx=0.86, rely=0.64, anchor="center")

  title_left=ctk.CTkLabel(
    left_frame,
    text="Upgrades",
    font=ctk.CTkFont(family="Impact", size=24, weight="bold"),
    text_color="#F3B300"
    )

  title_left.place(relx=0.25, rely=0.05, anchor="center")

  subtitle_left=ctk.CTkLabel(
  left_frame,
  text="ENHANCE YOUR SWARM",
  font=ctk.CTkFont(family="Aerial", size=15),
  text_color="#8E8E93"
  )

  subtitle_left.place(relx=0.365, rely=0.1, anchor="center")


  search_frame=ctk.CTkFrame(
    master=left_frame,
    fg_color="#181819",
    width=280,
    height=55,
    corner_radius=0,
    border_color='#363636',
    border_width=1,
  )

  search_frame.place(relx=0.5, rely=0.18, anchor="center")

  search_entry = ctk.CTkEntry(
    search_frame,
    placeholder_text="🔍 Search Upgrades...",
    width=260,
    height=30,
    border_width=1,
    corner_radius=11,
    border_color='#363636',
    fg_color="#1c1d20",  
    text_color="white",
    placeholder_text_color="#787B87",
    font=ctk.CTkFont(size=12)
  )

  search_entry.place(relx=0.5, rely=0.5, anchor="center")

  scrollable_frame = ctk.CTkScrollableFrame(
    left_frame,
    width=261,
    height=480,
    corner_radius=0,
    border_width=1,
    fg_color="#1A1A1B",
    border_color='#363636',
    scrollbar_button_color="#363636",     
    scrollbar_button_hover_color="#F3B300"  
  )

  scrollable_frame.place(relx=0.5, rely=0.57, anchor="center")

  def add_upgrade(text):

    frame=ctk.CTkFrame(
      scrollable_frame,
      width=250,
      height=90,
      border_width=1,
      corner_radius=10,
      border_color='#363636',
      fg_color="#1F1F21"
    )

    main_button=ctk.CTkButton(
    master=frame,
    width=180,
    height=75,
    text=text,
    font=ctk.CTkFont(family="Arial", size=17, weight="bold"),
    corner_radius=10,
    fg_color="#2b2b2e",
    text_color='white',
    hover_color='#616570',
    border_color='#363636',
    border_width=1,
    anchor='nw',
    command=lambda: add_bee(hise_cord[0],hise_cord[1])
  )
    
    main_button.place(relx=0.4, rely=0.5, anchor="center")

    level_lbl=ctk.CTkLabel(
      main_button,
      text="Lv.1",
      font=ctk.CTkFont(family="Impact", size=9, weight="bold"),
      text_color="#F3B300",
      fg_color='#202224',
      width=50,
      height=20,
      corner_radius=8
    )
    level_lbl.place(relx=0.84, rely=0.2, anchor="center")

    left_buts=ctk.CTkFrame(frame,fg_color="transparent",width=40,height=80)
    left_buts.place(relx=0.87, rely=0.5, anchor="center")

    auto_button=ctk.CTkButton(
      master=left_buts,
      width=40,
      height=35,
      text='A',
      font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
      corner_radius=5,
      fg_color="#222225",
      text_color='white',
      hover_color='#616570',
      border_color='#363636',
      border_width=1,
    )
    
    max_button=ctk.CTkButton(
      master=left_buts,
      width=40,
      height=35,
      text='M',
      font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
      corner_radius=5,
      fg_color="#222225",
      text_color='#01b2f5',
      hover_color='#616570',
      border_color='#363636',
      border_width=1,
    )

    auto_button.place(relx=0.5, rely=0.75, anchor="center")
    max_button.place(relx=0.5, rely=0.25, anchor="center")

    frame.pack(pady=(15,0))
  
  add_upgrade('+1 bee')
 
    
  




    
    

  





def close_settings():
  global settingsFrame

  settingsFrame.destroy()

  make_main_frame()



def add_tracking(text, space_count=2):
    return (" " * space_count).join(text)


def make_main_frame():
  global main_frame
  main_frame=ctk.CTkFrame(
      master=app,
      fg_color="#1A1A1B",
      corner_radius=30,
      width=500,
      height=600,
      border_color='#363636',
      border_width=1,
  )
  main_frame.place(relx=0.5, rely=0.5, anchor="center")

  logo=ctk.CTkImage(dark_image=Image.open("Bee_pj/logo.png"), size=(130,130))

  logo_lbl=ctk.CTkLabel(main_frame,image=logo, text='')
  logo_lbl.place(relx=0.5, rely=0.15, anchor="center")

  logo_frame = ctk.CTkFrame(main_frame, fg_color="#1A1A1B")
  logo_frame.place(relx=0.5, rely=0.32, anchor="center")

  
  bee_label = ctk.CTkLabel(
      logo_frame,
      text="BEE",
      font=bold_font,
      text_color="#FFFFFF"
  )
  bee_label.pack(side="left", padx=(0, 0))  

  simulator_label = ctk.CTkLabel(
      logo_frame,
      text="SIMULATOR",
      font=bold_font,
      text_color="#F3B300"  
  )
  simulator_label.pack(side="left", padx=(0, 0))

  subtitle_font = ctk.CTkFont(family="Arial", size=10, weight="bold")

  raw_text = "ULTIMATE HIVE MANAGEMENT"
  tracked_text = add_tracking(raw_text, space_count=2)

  subtitle_label = ctk.CTkLabel(
      main_frame,
      text=tracked_text,
      font=subtitle_font,
      width=50,
      text_color="#8E8E93",
      bg_color="#1A1A1B"
  )
  subtitle_label.place(relx=0.5, rely=0.39, anchor="center")

  play_but=ctk.CTkButton(
    master=main_frame,
    width=450,
    height=60,
    text="➤   ENTER THE HIVE!",
    font=ctk.CTkFont(family="Arial", size=17, weight="bold"),
    corner_radius=15,
    fg_color="#F3B300",
    text_color='black',
    hover_color='#ffc42a',
    command=start_game
  )
  play_but.place(relx=0.5, rely=0.5, anchor="center")

  settings_but=ctk.CTkButton(
    master=main_frame,
    width=450,
    height=60,
    text="⚙  Settings",
    font=ctk.CTkFont(family="Arial", size=17, weight="bold"),
    corner_radius=15,
    fg_color="#1a1a1b",
    text_color='white',
    hover_color='#2a2b2e',
    border_color='#363636',
    border_width=1,
    command=open_settings
  )
  settings_but.place(relx=0.5, rely=0.62, anchor="center")

  credits_but=ctk.CTkButton(
    master=main_frame,
    width=450,
    height=60,
    text="🎖  Credits",
    font=ctk.CTkFont(family="Arial", size=17, weight="bold"),
    corner_radius=15,
    fg_color="#1a1a1b",
    text_color='white',
    hover_color='#2a2b2e',
    border_color='#363636',
    border_width=1,
  )
  credits_but.place(relx=0.5, rely=0.74 ,anchor="center")

  line=ctk.CTkFrame(main_frame,height=3,width=400,fg_color='#363636',corner_radius=100)
  line.place(relx=0.5, rely=0.9 ,anchor="center")

  info=ctk.CTkFrame(
    master=main_frame,
    width=150,
    height=40,
    fg_color="#1a1a1b"
  )
  info.place(relx=0.5, rely=0.93 ,anchor="center")

  mono_font = ctk.CTkFont(family="Consolas", size=10)

  def add_info(text):
    color_map = {
      '🟢': '#4CAF50',  
      '🟡': '#FFC107',  
      '🟣': '#9C27B0'   
  }

    if text in ['🟢','🟡','🟣']:
      new=ctk.CTkLabel(
      master=info,
      text=text,
      font=subtitle_font,
      fg_color="#1a1a1b",
      text_color=color_map[text]
      )
    else:
      new=ctk.CTkLabel(
      master=info,
      text=text,
      font=mono_font,
      fg_color="#1a1a1b",
      text_color='grey'
      )

    new.pack(side='left',padx=(3,0))

  add_info('🟢')
  add_info('5s Flower Cooldown')
  add_info('🟡')
  add_info('1% Gold Chance')
  add_info('🟣')
  add_info('0.1% Raimbow Chance')

make_main_frame()
app.mainloop()