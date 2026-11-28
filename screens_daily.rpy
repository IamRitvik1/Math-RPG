screen main_evening_dashboard_ui():
    frame:
        xalign 0.5 yalign 0.4 xpadding 40 ypadding 40 xminimum 450
        vbox:
            spacing 25
            text "Apartment Dashboard - Evening of Day [active_day]" xalign 0.5 size 24 color "#fff"
            
            # Displays if an auto-anchor task or shift already took your evening time
            if is_evening_consumed:
                text "Night: no activities left today" xalign 0.5 size 16 color "#ef4444"
            else:
                text "Evening: you have time for one activity" xalign 0.5 size 16 color "#22c55e"
                
            null height 10
            
            # BRANCH 1: DO SOMETHING (Dynamically locked out if time is already spent tonight)
            textbutton "Do Something" action [SensitiveIf(not is_evening_consumed), Return("do_something")] xalign 0.5 xminimum 300
            
            # BRANCH 2: CHECK YOUR PHONE (Always open for player scheduling)
            textbutton "Check Your Phone" action Return("check_phone") xalign 0.5 xminimum 300
            
            # DEVELOPMENT HOOK: Take a business break option (Only shows if player is running a business streak)
            if current_business_streak > 0 and unlocked_own_business:
                textbutton "Take a Business Break" action Jump("trigger_business_break_logic") xalign 0.5 xminimum 300
                
            null height 10
            
            # BRANCH 3: SLEEP (Advance the day loop parameters cleanly)
            textbutton "Go to Sleep (End Day)" action Return("sleep") xalign 0.5 xminimum 300

screen submenu_do_something_ui():
    frame:
        xalign 0.5 yalign 0.4 xpadding 40 ypadding 40 xminimum 450
        vbox:
            spacing 20
            text "Do Something" xalign 0.5 size 24
            null height 10
            
            # Gym Selection: click opens pass if poor, or free if member is active
            if gym_membership_active:
                textbutton "Visit Gym (Membership Active)" action Return("gym_visit") xalign 0.5 xminimum 320
            else:
                textbutton "Visit Gym (Single Day Pass: $20)" action [SensitiveIf(current_cash >= 20.00), Return("gym_visit")] xalign 0.5 xminimum 320
                
            # Fortune Teller Tent: Enforces absolute Day 5 Lockout parameter boundaries
            if active_day >= 5:
                if fortune_passes_remaining > 0:
                    textbutton "Visit Fortune Teller ([fortune_passes_remaining] Pass Card Left)" action Return("fortune_visit") xalign 0.5 xminimum 320
                else:
                    textbutton "Visit Fortune Teller (Session: $99)" action [SensitiveIf(current_cash >= 99.00), Return("fortune_visit")] xalign 0.5 xminimum 320
                
            # Instant Cafe: Hook placeholder for high-affinity companion meetings
            textbutton "Text Sam" action [SensitiveIf(sam_storyline_started), Return("sam_hangout")] xalign 0.5 xminimum 320
            textbutton "Text Emilie" action [SensitiveIf(emilie_unlocked), Return("emilie_hangout")] xalign 0.5 xminimum 320
            textbutton "Text Luca" action [SensitiveIf(luca_unlocked), Return("luca_hangout")] xalign 0.5 xminimum 320
            
            null height 15
            textbutton "[[ Return to Main Menu ]" action Return("back") xalign 0.5

screen submenu_check_phone_ui_master():
    if current_phone_screen == "main":
        use submenu_check_phone_ui
    elif current_phone_screen == "banking":
        use phone_subscreen_banking
    elif current_phone_screen == "gym_app":
        use phone_subscreen_gym
    elif current_phone_screen == "fortune_store":
        use phone_subscreen_fortune_store
    elif current_phone_screen == "dating_app_hub":
        use phone_subscreen_dating_hub
    elif current_phone_screen == "digital_textbook":
        use phone_subscreen_textbook
    elif current_phone_screen == "social_scheduler":
        use phone_subscreen_social
screen submenu_check_phone_ui():
    frame:
        xalign 0.5 yalign 0.4 xpadding 40 ypadding 40 xminimum 450
        vbox:
            spacing 15
            text "Phone" xalign 0.5 size 24
            text "Cash Balance: $[current_cash:.2f]" xalign 0.5 size 16 color "#22c55e"
            null height 5
            
            # --- APPLICATION TILES / MAIN SELECTIONS ---
            
            # 🏢 App 1: Banking & Wallet Profile (New structural inspection addition)
            textbutton "Bank App" action [SetVariable("current_phone_screen", "banking"),Return("refresh")] xalign 0.5 xminimum 340
            
            # 💳 App 2: Gym Membership Manager (Pre-programmed membership toggle from last session)
            textbutton "Gym App" action [SetVariable("current_phone_screen", "gym_app"),Return("refresh")] xalign 0.5 xminimum 340
            
            # 🔮 App 3: Fortune Teller Prepaid Store Bundle Cards
            textbutton "Fortune Pass Card Ticket Store" action [SetVariable("current_phone_screen", "fortune_store"),Return("refresh")] xalign 0.5 xminimum 340
            
            # 💬 App 4: The Online Dating App Profile Hub (Placeholder Button - System Coded Next Session)
            textbutton "Online Dating Messaging Feed" action [SetVariable("current_phone_screen", "dating_app_hub"),Return("refresh")] xalign 0.5 xminimum 340
            
            # 📅 App 5: The Social Schedule Calendar (Placeholder Button - Coded in Character Phase)
            textbutton "Social Scheduler" action [SetVariable("current_phone_screen", "social_scheduler"),Return("refresh")] xalign 0.5 xminimum 340
            
            # 📖 App 6: Non-Canon Digital Textbook Module (Placeholder Button - Coded in Business Phase)
            textbutton "Algebra & Stats Revision Textbook" action [SetVariable("current_phone_screen", "digital_textbook"),Return("refresh")] xalign 0.5 xminimum 340
            
            null height 15
            textbutton "[[ Close Phone ]" action Return("back") xalign 0.5

# ---------------------------------------------------------
# SMARTPHONE APPLICATION SUB-SCREEN ROUTINGS
# ---------------------------------------------------------

# SCREEN A: THE INDEPENDENT WALLET & IDENTITY SCREEN
screen phone_subscreen_banking():
    frame:
        xalign 0.5 yalign 0.4 xpadding 40 ypadding 40 xminimum 450
        vbox:
            spacing 20
            text "Your Bank Account" xalign 0.5 size 24 color "#22c55e"
            null height 5
            text "Registered Account Name: [player_name]" size 18
            text "Active Job: [current_tier]" size 18
            if current_tier in ("Educator", "Analyst", "Researcher"):
                text "Current Corporate Rank: Level [job_level_rank]" size 18
            text "Cash Balance: $[current_cash:.2f]" size 18 color "#22c55e"
            text "Strikes: [job_strike_counter] / [get_max_strikes()]" size 18 color ("#ef4444" if job_strike_counter >= 1 else "#fff")
            null height 15
            textbutton "[[ Back to Main Menu ]" action SetVariable("current_phone_screen", "main") xalign 0.5

# SCREEN B: THE RECURRING MEMBER MANAGEMENT WIDGET
screen phone_subscreen_gym():
    frame:
        xalign 0.5 yalign 0.4 xpadding 40 ypadding 40 xminimum 450
        vbox:
            spacing 20
            text "Gym Membership" xalign 0.5 size 24
            null height 5
            if gym_membership_active:
                text "Subscription Status: ACTIVE" size 18 color "#22c55e"
                text "Days Until Recurring $60 Billing Cycle: [gym_days_until_billing] Days" size 18
                null height 10
                textbutton "Cancel Recurring Auto-Renew" action Return("toggle_gym_sub") xalign 0.5 xminimum 300
            else:
                text "Subscription Status: INACTIVE (Day Pass Fee Required)" size 18 color "#ef4444"
                null height 10
                textbutton "Initialize 5-Day Member Sub ($60.00)" action Return("toggle_gym_sub") xalign 0.5 xminimum 300
            null height 15
            textbutton "[[ Back to Apps List ]" action SetVariable("current_phone_screen", "main") xalign 0.5

# SCREEN C: THE PREPAID FORTUNE BUNDLE PASS CHECKOUT CARDS
screen phone_subscreen_fortune_store():
    frame:
        xalign 0.5 yalign 0.4 xpadding 40 ypadding 40 xminimum 450
        vbox:
            spacing 15
            text "Fortune Tent Pass Checkout" xalign 0.5 size 24
            text "Available Prepaid Passes in Wallet: [fortune_passes_remaining]" xalign 0.5 size 16 color "#f59e0b"
            null height 5
            textbutton "Buy 1 session ($99)" action [SensitiveIf(current_cash >= 99.00), Return("buy_pass_1")] xalign 0.5 xminimum 340
            textbutton "Buy 2 sessions ($189)" action [SensitiveIf(current_cash >= 189.00), Return("buy_pass_2")] xalign 0.5 xminimum 340
            textbutton "Buy 3 sessions ($219)" action [SensitiveIf(current_cash >= 219.00), Return("buy_pass_3")] xalign 0.5 xminimum 340
            null height 15
            textbutton "[[ Back to Apps List ]" action SetVariable("current_phone_screen", "main") xalign 0.5

# SCREEN D: DATING APP SYSTEM SUB-MENU CANVAS (Placeholder - Unlocked Next Coding Session)
screen phone_subscreen_dating_hub():
    frame:
        xalign 0.5 yalign 0.4 xpadding 40 ypadding 40 xminimum 450
        vbox:
            spacing 20
            text "Dating App" xalign 0.5 size 24
            null height 10
            text "WIP." xalign 0.5 text_align 0.5 size 16
            null height 15
            textbutton "[[ Back to Apps List ]" action SetVariable("current_phone_screen", "main") xalign 0.5


# SCREEN F: NON-CANON REVISION GUIDE CANVAS (Placeholder - Unlocked in Business Phase)
screen phone_subscreen_textbook():
    frame:
        xalign 0.5 yalign 0.4 xpadding 40 ypadding 40 xminimum 450
        vbox:
            spacing 20
            text "Study App" xalign 0.5 size 24
            null height 10
            text "WIP" xalign 0.5 text_align 0.5 size 16
            null height 15
            textbutton "[[ Back to Apps List ]" action SetVariable("current_phone_screen", "main") xalign 0.5
# ---------------------------------------------------------
# MINECRAFT STORY MODE STYLE NOTIFICATION OVERLAY
# ---------------------------------------------------------
screen narrative_change_alert(message="The storyline has changed."):
    # Restricts user interaction blocks from accidentally breaking the screen timer
    zorder 100
    
    # Visual positioning block: Centers text near the upper-middle of the screen
    frame:
        xalign 0.5
        yalign 0.15
        background "#1a1a1acc"  # Semi-transparent dark slate block background
        padding (25, 12, 25, 12)
        
        # Soft visual animation: Slides in gently, lingers, then fades out completely
        at transform:
            alpha 0.0 yoffset -20
            easein 0.4 alpha 1.0 yoffset 0
            pause 2.5
            easeout 0.5 alpha 0.0 yoffset -10
            
        text "[message]":
            color "#ffff00"      # Classic high-contrast Story Mode Yellow text
            size 26
            bold True
            font "DejaVuSans.ttf" # Uses standard safe Ren'Py built-in font rendering
            xalign 0.5
            yalign 0.5

    # Automatically kills the screen overlay after 3.5 total seconds have cleared
    timer 3.5 action Hide("narrative_change_alert")

# SCREEN E: SOCIAL SCHEDULER (placeholder so the button no longer soft-locks)
screen phone_subscreen_social():
    frame:
        xalign 0.5 yalign 0.4 xpadding 40 ypadding 40 xminimum 450
        vbox:
            spacing 20
            text "Social Scheduler" xalign 0.5 size 24
            null height 10
            text "WIP." xalign 0.5 text_align 0.5 size 16
            null height 15
            textbutton "[[ Back to Apps List ]" action SetVariable("current_phone_screen", "main") xalign 0.5
