import tkinter as tk
import customtkinter as ctk
from backend import Flower, on_canvas_click, update_loop

honey_mult = 1

def build_mid_frame_panel(parent_frame):
    # Lock frame dimensions (480x580)
    parent_frame.pack_propagate(False)

    # ==========================================
    # TKINTER CANVAS
    # Clear space for drawing flowers
    # ==========================================
    canvas = tk.Canvas(
        parent_frame,
        bg="#181819", # Matches parent frame background
        highlightthickness=0,
        bd=0,
        width=440,
        height=540
    )
    canvas.place(x=20, y=20)

    # Assign canvas as master for backend Flower class
    Flower.master = canvas

    # ==========================================
    # TOP RIGHT: MAIN HIVE BUTTON (Absolute Coords)
    # ==========================================
    hive_x = 385
    hive_y = 20
    
    hive_box = ctk.CTkFrame(
        parent_frame,
        fg_color="#2A1B12", 
        border_color="#F3B300",
        border_width=1.5,
        corner_radius=15,
        width=75,
        height=75
    )
    hive_box.pack_propagate(False)
    hive_box.place(x=hive_x, y=hive_y)
    
    hive_icon = ctk.CTkLabel(hive_box, text="🍯", font=ctk.CTkFont(size=28))
    hive_icon.pack(pady=(10, 0))
    
    hive_lbl = ctk.CTkLabel(
        hive_box, 
        text="MAIN HIVE", 
        font=ctk.CTkFont(family="Arial", size=9, weight="bold"), 
        text_color="#F3B300"
    )
    hive_lbl.pack(pady=(0, 5))

    # ==========================================
    # BOTTOM: SPAWN READY PILL
    # ==========================================
    pill_box = ctk.CTkFrame(
        parent_frame,
        fg_color="#09090A",
        corner_radius=20,
        height=45
    )
    pill_box.place(relx=0.5, rely=0.88, anchor="center")
    
    dot = ctk.CTkFrame(pill_box, width=12, height=12, fg_color="#00E676", corner_radius=6)
    dot.pack(side="left", padx=(18, 12), pady=12)
    
    ready_lbl = ctk.CTkLabel(
        pill_box, 
        text="FLOWER SPAWN READY", 
        font=ctk.CTkFont(family="Arial", size=11, weight="bold"), 
        text_color="#FFFFFF"
    )
    ready_lbl.pack(side="left", padx=(0, 18))
    
    prog_bar = ctk.CTkProgressBar(
        pill_box, 
        width=100, 
        height=8, 
        progress_color="#F3B300", 
        fg_color="#2C2C2E"
    )
    prog_bar.set(1.0) # Starts fully ready
    prog_bar.pack(side="left", padx=(0, 18))

    # ==========================================
    # 5-SECOND COOLDOWN ANIMATION LOGIC
    # ==========================================
    cooldown_active = [False]

    def start_cooldown_animation(duration=5.0):
        if cooldown_active[0]:
            return
        cooldown_active[0] = True
        
        # Set red dot and updating status text
        dot.configure(fg_color="#FF3B30") 
        ready_lbl.configure(text="PLANTING COOLDOWN...")
        prog_bar.set(0.0)
        
        steps = 100
        step_time_ms = int((duration * 1000) / steps) # 50ms per step
        current_step = [0]

        def animate():
            current_step[0] += 1
            progress = current_step[0] / steps
            prog_bar.set(progress)
            
            if current_step[0] < steps:
                parent_frame.after(step_time_ms, animate)
            else:
                # Reset back to ready state when complete
                prog_bar.set(1.0)
                dot.configure(fg_color="#00E676")
                ready_lbl.configure(text="FLOWER SPAWN READY")
                cooldown_active[0] = False

        parent_frame.after(step_time_ms, animate)

    # Click handler: triggers backend event and starts cooldown animation
    def handle_canvas_click(event):
        if not cooldown_active[0]:
            on_canvas_click(event)
            start_cooldown_animation(5.0)

    # Bind click event
    canvas.bind("<Button-1>", handle_canvas_click)

    # Start update loop
    update_loop(canvas, 2, honey_mult)

    # ==========================================
    # RETURN DICTIONARY
    # ==========================================
    return {
        "canvas": canvas,
        "hive_box_frame": hive_box,
        "hive_box_coords": (hive_x, hive_y),
        "progress_bar": prog_bar,
        "ready_label": ready_lbl,
        "indicator_dot": dot,
        "start_cooldown": start_cooldown_animation
    }