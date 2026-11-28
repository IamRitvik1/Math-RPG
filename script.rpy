# Initialize Persistent Global Progression (Carries over beyond individual saves)
default persistent.has_completed_good_run = False 
default persistent.owns_ledger_of_absolute_value = False 

# Initialize Player Identity & Base Stats
default player_name = ""
default initial_stress_set = 20
default current_stress = 20
default current_cash = 500.00
default active_day = 1

# Updated Core Attributes (Now split and dynamically scaled)
default stat_intellect = 0
default stat_stamina = 0
default stat_charisma = 0

# Hidden Dynamic Growth Multipliers (Default is 1.0, choices add +0.05)
default growth_intellect = 1.0
default growth_stamina = 1.0
default growth_charisma = 1.0

# The 4 Dynamic Narrative Life Pillars
default pillar_romance = 0
default pillar_social = 0
default pillar_passion = 0
default pillar_career_score = 50  # Out of 100

# Career Tiers & Global Trait Flags
default current_tier = "Unemployed" 
default career_progress_modifier = 1.0
default hobby_cash_discount = 0.0
default path_chosen = "None"
default has_started_emergency_business = False
default active_burnout_debuff = False
default active_isolation_debuff = False
default fortune_visits_counter = 0

# Define NPCs
define sam = Character("Unknown")
define emilie = Character("Emilie")
define luca = Character("Luca")
define therapist = Character("The Therapist")
define fortune = Character("Fortune Teller")
define player = Character("[player_name]")

default unlocked_freelance = False
default unlocked_own_business = False

default job_strike_counter = 0      
default promotion_streak_counter = 0

# Core Evening Phase State Flags
default is_evening_consumed = False
default course_days_remaining = 0
default study_days_remaining = 0
default current_business_streak = 0
default business_breaks_taken = 0
default scheduled_meetup_active = False

# Local menu navigation state
default current_phone_screen = "main"

# Gym Membership & Cost Tracking Variables
default gym_membership_active = False
default gym_days_until_billing = 0

# Fortune Teller State & Pass Sub-system Tracking
default fortune_passes_remaining = 0
default fortune_sessions_attended = 0
default has_received_golden_roses = False
default golden_roses_count = 0

# Test configuration values (Adjust these as needed during your tests)
default test_unlocked_own_business = False

# --- Defaults that were used in the code but never declared ---
default job_level_rank = 1
default consecutive_days_negative = 0
default shift_score = 0              # per-shift score (pillar_career_score is now untouched by shifts)
default shift_failed = False
default current_shift_questions = []
default sam_hangout_2_choice = "none"
default emilie_hangout_1_mood = "none"
default has_active_relationship = False
default emilie_hangouts_completed = 0
default luca_hangouts_completed = 0
default sibling_collision_failed = False
default freelance_revenue_multiplier = 1.0
default affinity_phase_1_cleared = False
default luca_intro_generosity_chosen = False
default stat_carry = {}
default terminated_jobs = []
default sibling_meetup_tomorrow = ""
default sibling_meet_target = ""
default second_sibling_day = 0
default day_6_done = False
default day_2_done = False
default sibling_double_header_pending = False

init python:
    import os

    # Scans all folders inside game/images/
    for path in renpy.list_files():
        if path.startswith("images/") and path.endswith((".png", ".jpg", ".webp")):
            # Breaks "images/Sam/normal.png" into ["images", "Sam", "normal.png"]
            parts = path.split("/")
            
            # Checks if the file is inside a subfolder
            if len(parts) == 3:
                tag = parts[1].lower()
                attribute = os.path.splitext(parts[2])[0].lower()
                
                # Registers it so "show sam normal" works automatically
                scaled_image = Transform(path, zoom=0.4)
                renpy.image((tag, attribute), scaled_image)


init python:
    def get_max_strikes():
        # 2 strikes by default, 3 above 30 charisma, 4 above 60
        return 2 + (1 if stat_charisma > 30 else 0) + (1 if stat_charisma > 60 else 0)

    def scaled_gain(key, base, mult):
        # Applies a growth multiplier without losing the fractional part (int(3*1.1) is 3)
        total = base * mult + stat_carry.get(key, 0.0)
        gain = int(total + 1e-9)
        stat_carry[key] = total - gain
        return gain

    def meetup_booked():
        return bool(sam_meetup_scheduled_tomorrow or sibling_meetup_tomorrow != "" or sibling_double_header_pending)

# WIP placeholder backgrounds: only created if the image file is missing from images/
init 10 python:
    for bgname in ("fortune_tent"):
        if not renpy.has_image("bg " + bgname):
            renpy.image("bg " + bgname, Fixed(Solid("#2b2b3a"), Text("WIP background: " + bgname, xalign=0.5, yalign=0.5, size=32, color="#ffffff")))

image bg apartment_night = "bedroom_night.png"
image bg apartment_morning = "livingroom_day.png"
image bg educator_place = "classroom_day.png"
image bg analyst_place = "analyst_day.png"
image bg researcher_place = "researcher_day.png"
image bg cafe_interior = "cafeteria_day.png"
image bg city_exploration = "backstreet_summer_day.png"
image bg emilie_office = "emilie_office.jpg"
image bg restaurant = "restaurant.png"

image phone = "phone.png"

label start:
    jump introductory_phone_sequence

label introductory_phone_sequence:
    scene bg apartment_night with fade
    "You sit down on your couch in your new apartment. Your phone buzzes."
    show phone
    sam "Hey! Welcome to the city. I'm your guide to the city for the first few days. I'm so sorry, I totally forgot your name, I feel terrible! What was it again?"

    menu phone_choices:
        # Option A: Focused on The Happy Couple (Romance / Rizz Focus)
        "Tell them you're looking for a partner and a content life.":
            $ player_name = renpy.input("Enter your name:", length=20, exclude="[]{}").strip()
            if not player_name:
                $ player_name = "Alex"
                
            "You text back: 'Yeah no worries, I completely understand. My name is [player_name] and honestly, I just came here to live a happy and content life and get a partner to do that with.'"
            
            # Apply Stat Adjustments
            $ stat_charisma = 5
            $ initial_stress_set = 10
            $ current_stress = 10
            $ sam = Character("Sam")
            sam "Oh I remember you, [player_name]! Remember me, Sam from school? We should really catch up. Anyway, glad you made it here safely."
            jump sequence_complete

        # Option B: Focused on The Successful Businessman (Intellect Focus)
        "Tell them you're here strictly for business.":
            $ player_name = renpy.input("Enter your name:", length=20, exclude="[]{}").strip()
            if not player_name:
                $ player_name = "Alex"
                
            "You text back: 'Hello, I am [player_name]. Let us skip all of these introductions and just talk business.'"
            
            # Apply Stat Adjustments
            $ stat_intellect = 5
            $ growth_stamina = 1.1
            $ initial_stress_set = 40
            $ current_stress = 40
            
            $ sam = Character("Sam")
            sam "Ok, wait, I remember a [player_name] from school, is that you? I remember how business-minded you were. Anyway, I am Sam from school, nice to see you made it here. We should catch up and talk about business opportunities here soon."
            jump sequence_complete

        # Option C: Focused on The Hobby Follower (Stamina Focus)
        "Tell them you are searching for a passion or hobby.":            
            $ player_name = renpy.input("Enter your name:", length=20, exclude="[]{}").strip()
            if not player_name:
                $ player_name = "Alex"
                
            "You text back: 'Hi, I'm [player_name], I just want to explore the city and find my passion.'"
            
            # Apply Stat Adjustments
            $ stat_stamina = 5
            $ growth_intellect = 1.1
            $ initial_stress_set = 20
            $ current_stress = 20
            
            $ sam = Character("Sam")
            sam "Nice meeting you. Wait I remember a [player_name] from school! Is that really you? Remember me, Sam from school."
            "You text back: 'I remember a Sam from school, is that you? Also, can you help me set up?'"
            sam "Yeah, that's me, [player_name]! And sure, I will help since I remember how much you liked following your passions. We should catch up sometime."
            jump sequence_complete

        # Option D: Focused on The Community Network (Platonic Charisma Focus)
        "Tell them your name and ask to be friends.":
            $ player_name = renpy.input("Enter your name:", length=20, exclude="[]{}").strip()
            if not player_name:
                $ player_name = "Alex"

            # Apply Stat Adjustments
            $ growth_charisma = 1.1
            $ initial_stress_set = 30
            $ current_stress = 30
            
            $ sam = Character("Sam")
            "You text back: 'Hi, I'm [player_name]. We should be friends, what's your name?'"
            sam "Nice meeting you. Wait I remember a [player_name] from school! Is that really you? Remember me, Sam from school."
            
            "You text back: 'Wait, Sam, is that really you!!! Oh, I missed you so much. We should catch up sometime. Also I really need some money, can I borrow some?'"
            sam "Yeah, we really should. I missed you too and sure since you are an old friend. Come sometime to the cafe to catch up. Message me."
            jump sequence_complete

        # Option E: Focused on The Allrounder (NG+ Secret: Balanced Growth) if unlocked
        "Tell them you're here to balance everything." if persistent.has_completed_good_run:
            $ player_name = renpy.input("Enter your name:", length=20, exclude="[]{}").strip()
            if not player_name:
                $ player_name = "Alex"
                
            "You text back: 'Yeah sure! I'm [player_name] and I'm here to balance it all.'"
            "You text back: 'I want to experience everything this city has to offer, from work to hobbies to relationships.'"
            
            # Apply Stat Adjustments (1 Point to ALL stats)
            $ stat_intellect = 5
            $ stat_stamina = 5
            $ stat_charisma = 5
            $ initial_stress_set = 20
            $ current_stress = 20
            
            $ sam = Character("Sam")
            sam "Oh I remember you, [player_name]! Remember me, Sam from school? We should really catch up. Anyway, glad you made it here safely. Message me later to hangout."
            jump sequence_complete

label sequence_complete:
    hide phone
    $ sam_storyline_started = True   # Sam is now in your contacts
    # Advance to the first morning loop...
    jump morning_phase
