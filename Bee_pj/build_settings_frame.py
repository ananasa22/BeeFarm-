import customtkinter as ctk
from backend import update_loop, add_random_flowers

def build_nest_control_panel(parent_frame, master):
    # Lock the frame to 280x180 dimensions
    parent_frame.pack_propagate(False)

    # Initial speed state
    max_speed = 3.0

    # ==========================================
    # HEADER ROW (NEST CONTROL + LIVE BADGE)
    # ==========================================
    header_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    header_frame.pack(fill="x", padx=16, pady=(12, 0))

    title_lbl = ctk.CTkLabel(
        header_frame,
        text="NEST CONTROL",
        font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
        text_color="#636366"
    )
    title_lbl.pack(side="left")

    live_badge = ctk.CTkFrame(
        header_frame,
        fg_color="#121214",
        border_color="#2C2C2E",
        border_width=1,
        corner_radius=8
    )
    live_badge.pack(side="right")

    live_lbl = ctk.CTkLabel(
        live_badge,
        text="LIVE",
        font=ctk.CTkFont(family="Arial", size=8, weight="bold"),
        text_color="#F3B300"
    )
    live_lbl.pack(padx=8, pady=2)

    # ==========================================
    # SPEED READOUT ROW
    # ==========================================
    speed_row = ctk.CTkFrame(parent_frame, fg_color="transparent")
    speed_row.pack(fill="x", padx=16, pady=(8, 0))

    speed_title_lbl = ctk.CTkLabel(
        speed_row,
        text="Bee Flight Speed",
        font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
        text_color="#E5E5EA"
    )
    speed_title_lbl.pack(side="left")

    speed_val_lbl = ctk.CTkLabel(
        speed_row,
        text=f"{max_speed:.1f} m/s",
        font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
        text_color="#F3B300"
    )
    speed_val_lbl.pack(side="right")

    # ==========================================
    # SLIDER & LABELS
    # ==========================================
    def on_slider_change(value):
        nonlocal max_speed
        max_speed = round(value, 1)
        speed_val_lbl.configure(text=f"{max_speed:.1f} m/s")
        update_loop(master, max_speed, 1)

    slider = ctk.CTkSlider(
        parent_frame,
        from_=1.0,
        to=8.0,
        number_of_steps=70,
        height=14,
        fg_color="#2C2C2E",
        progress_color="#2C2C2E",
        button_color="#F3B300",
        button_hover_color="#D19A00",
        command=on_slider_change
    )
    slider.set(max_speed)
    slider.pack(fill="x", padx=16, pady=(4, 0))

    sub_label_row = ctk.CTkFrame(parent_frame, fg_color="transparent")
    sub_label_row.pack(fill="x", padx=16, pady=(1, 0))

    left_sub = ctk.CTkLabel(
        sub_label_row,
        text="1.0x (Gentle)",
        font=ctk.CTkFont(family="Arial", size=8),
        text_color="#636366"
    )
    left_sub.pack(side="left")

    right_sub = ctk.CTkLabel(
        sub_label_row,
        text="8.0x (Hyper)",
        font=ctk.CTkFont(family="Arial", size=8),
        text_color="#636366"
    )
    right_sub.pack(side="right")

    # ==========================================
    # BUTTON: SPAWN 5 FLOWERS
    # ==========================================
    spawn_btn = ctk.CTkButton(
        parent_frame,
        text="✨  SPAWN 5 FLOWERS",
        font=ctk.CTkFont(family="Arial", size=11, weight="bold"),
        fg_color="#FFB82E",
        hover_color="#E0A025",
        text_color="#000000",
        corner_radius=18,
        height=34,
        command=add_random_flowers
    )
    spawn_btn.pack(fill="x", padx=16, pady=(10, 0))

    # Initialize loop with starting speed
    update_loop(master, max_speed, 1)

    return {
        "slider": slider,
        "spawn_button": spawn_btn,
        "get_max_speed": lambda: max_speed
    }