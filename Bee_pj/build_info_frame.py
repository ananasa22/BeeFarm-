import customtkinter as ctk

def build_dashboard_panel(parent_frame):
    # Lock the parent frame to its defined width (480) and height (80)
    parent_frame.pack_propagate(False)

    def create_stat_block(parent, title, value, val_color, unit, left_pad):
        block_frame = ctk.CTkFrame(parent, fg_color="transparent")
        block_frame.pack(side="left", padx=left_pad, pady=12)
        
        title_lbl = ctk.CTkLabel(
            block_frame, 
            text=title, 
            font=ctk.CTkFont(family="Arial", size=9, weight="bold"), 
            text_color="#636366"
        )
        title_lbl.pack(anchor="w", pady=(0, 0))
        
        val_frame = ctk.CTkFrame(block_frame, fg_color="transparent")
        val_frame.pack(anchor="w")
        
        val_lbl = ctk.CTkLabel(
            val_frame, 
            text=value, 
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"), 
            text_color=val_color
        )
        val_lbl.pack(side="left")
        
        unit_lbl = ctk.CTkLabel(
            val_frame, 
            text=unit, 
            font=ctk.CTkFont(family="Arial", size=10), 
            text_color="#636366"
        )
        unit_lbl.pack(side="left", anchor="s", padx=(3, 0), pady=(0, 2))

    def create_separator(parent):
        sep = ctk.CTkFrame(parent, width=1, fg_color="#2C2C2E")
        sep.pack(side="left", fill="y", pady=18)

    def create_rate_box(parent, title, title_color, value, left_pad):
        box_frame = ctk.CTkFrame(
            parent, 
            fg_color="#121214", 
            border_color="#2C2C2E", 
            border_width=1, 
            corner_radius=8
        )
        box_frame.pack(side="left", padx=left_pad, pady=14)
        
        title_lbl = ctk.CTkLabel(
            box_frame, 
            text=title, 
            font=ctk.CTkFont(family="Arial", size=8, weight="bold"), 
            text_color=title_color
        )
        title_lbl.pack(pady=(4, 0), padx=8)
        
        val_lbl = ctk.CTkLabel(
            box_frame, 
            text=value, 
            font=ctk.CTkFont(family="Arial", size=13, weight="bold"), 
            text_color="#FFFFFF"
        )
        val_lbl.pack(pady=(0, 4), padx=8)

    # --- Section Population ---
    create_stat_block(
        parent=parent_frame,
        title="NECTAR SUPPLY",
        value="460",
        val_color="#F3B300",
        unit="ml",
        left_pad=(15, 6)
    )
    
    create_separator(parent_frame)
    
    create_stat_block(
        parent=parent_frame,
        title="BEE POPULATION",
        value="2",
        val_color="#F3B300",
        unit="Active",
        left_pad=(6, 6)
    )
    
    create_separator(parent_frame)

    create_stat_block(
        parent=parent_frame,
        title="POLLEN CAPACITY",
        value="0 / 100",
        val_color="#FFFFFF",
        unit="units",
        left_pad=(6, 8)
    )
    
    create_rate_box(
        parent=parent_frame,
        title="GOLDEN RATE",
        title_color="#F3B300",
        value="1.0%",
        left_pad=(4, 3)
    )
    
    create_rate_box(
        parent=parent_frame,
        title="RAINBOW RATE",
        title_color="#D87BFF",
        value="0.1%",
        left_pad=(3, 10)
    )