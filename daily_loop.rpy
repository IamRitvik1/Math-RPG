label morning_phase:
    if active_isolation_debuff:
        jump cognitive_isolation_morning

    # Sam's morning meetups (hangouts 3 and 4 are "come tomorrow morning")
    if sam_meetup_scheduled_tomorrow and sam_hangouts_completed == 3:
        $ sam_meetup_scheduled_tomorrow = False
        jump sam_affinity_morning_scene_1
    elif sam_meetup_scheduled_tomorrow and sam_hangouts_completed == 4:
        $ sam_meetup_scheduled_tomorrow = False
        jump sam_affinity_morning_scene_2

    if sibling_double_header_pending:
        $ sibling_double_header_pending = False
        jump sibling_affinity_phase_1_double_header
        
    scene bg apartment_morning with fade
    "Day [active_day]: The morning sun wakes you up."
    
    # Check for your unique introductory state
    if current_tier == "Unemployed":
        "You remember that you do not have a job anymore and check your phone for jobs."
        jump unemployment_menu
        
    else:
        jump initialize_work_shift
    
    jump afternoon_phase
# ---------------------------------------------------------
# THE AFTERNOON TRANSITION PHASE (RUNS POST-WORK, PRE-EVENING)
# ---------------------------------------------------------
label afternoon_phase:
    $ current_cash -= 100.00
    "You came back home. You spent 100 dollars for rent, groceries and basic necessities."

    # 2. Financial Overdraft Evaluation Logic
    if current_cash < 0.00:
        $ consecutive_days_negative += 1
        "Warning: You are in debt. Balance: $[current_cash:.2f]."
        if consecutive_days_negative > 3:
            jump systemic_insolvency_failed_ending
    else:
        # Reset the overdraft counter if they climbed back into the black
        $ consecutive_days_negative = 0

    # 3. Dynamic Automated Loan Deadline Verification Tickers
    if sam_loan_active:
        if active_day >= sam_debt_due_day:
            if current_cash >= sam_debt_balance:
                # Absolute safety net auto-clear payout execution
                $ current_cash -= sam_debt_balance
                $ sam_debt_balance = 0.00
                $ sam_loan_active = False
                "You paid your debt to Sam."
            else:
                # Debt default condition triggered
                jump systemic_insolvency_failed_ending
    
    if sam_meetup_scheduled_tomorrow:
        if sam_hangouts_completed == 1:
            $ sam_meetup_scheduled_tomorrow = False
            jump sam_casual_hangout_2
        elif sam_hangouts_completed == 0:
            $ sam_meetup_scheduled_tomorrow = False
            jump sam_casual_hangout_1

    # Day 6: meet the siblings (Emilie as your boss, or Luca as your neighbour)
    if active_day >= 6 and not day_6_done:
        $ day_6_done = True
        jump day_6_afternoon_check

    # The day after hangout 1 with the first sibling, you meet the other one
    if second_sibling_day > 0 and active_day >= second_sibling_day:
        $ second_sibling_day = 0
        if emilie_unlocked and not luca_unlocked:
            jump luca_day_6_introduction
        elif luca_unlocked and not emilie_unlocked:
            jump emilie_after_luca_meeting

    # Booked sibling meetups
    if sibling_meetup_tomorrow != "":
        $ sibling_meet_target = sibling_meetup_tomorrow
        $ sibling_meetup_tomorrow = ""
        if sibling_meet_target == "emilie":
            if emilie_hangouts_completed == 0:
                jump emilie_casual_hangout_1
            else:
                jump emilie_casual_hangout_2
        elif sibling_meet_target == "luca":
            if luca_hangouts_completed == 0:
                jump luca_casual_hangout_1
            else:
                jump luca_casual_hangout_2
        else:
            jump sibling_joint_hangout_3

    # Advance cleanly directly into the main apartment dashboard layout
    jump evening_phase


label unemployment_menu:
    "You open up your phone's career application page to see your current options."

    menu career_options:
        # Standard Corporate Options (Always Available)
        "Apply for School Tutor (Educator Tier)" if "Educator" not in terminated_jobs:
            "You fill out the application form for the local tutoring center."
            $ current_tier = "Educator"
            $ job_level_rank = 1
            jump initialize_work_shift

        "Apply for Corporate Analyst (Analyst Tier)" if "Analyst" not in terminated_jobs:
            "You submit your resume to the financial logistics firm."
            $ current_tier = "Analyst"
            $ job_level_rank = 1
            jump initialize_work_shift

        "Apply for Research Laboratory (Researcher Tier)" if "Researcher" not in terminated_jobs:
            "You apply for the technical grant lab assistant role."
            $ current_tier = "Researcher"
            $ job_level_rank = 1
            jump initialize_work_shift

        # Unlocked Path: Freelance (Only appears if condition is met)
        "Look for Freelance Work" if unlocked_freelance:
            # Placeholder for future design work
            "You look at open contract boards..."
            $ current_tier = "Freelance"
            jump freelance_work_shift

        # Unlocked Path: Start a Company (Only appears if condition is met)
        "Start a New Business" if unlocked_own_business:
            # Placeholder for future design work
            "You process your business license registration paperwork..."
            $ current_tier = "Entrepreneur"
            jump entrepreneur_shift
        "Stay Jobless":
            "You decide to stay without a job..."
            jump afternoon_phase
label entrepreneur_shift:
    "WIP, setting work back to unemployed"
    $ current_tier = "Unemployed"
    jump unemployment_menu

label freelance_work_shift:
    "WIP, setting work back to unemployed"
    $ current_tier = "Unemployed"
    jump unemployment_menu

label evening_phase:
    scene bg apartment_night with fade
    $ is_evening_consumed = False
    if active_day == 2 and not day_2_done:
        $ day_2_done = True
        jump day_2_doorbell_intercept
    jump evening_ticks

# Runs every evening, including evenings that start with a hangout
label evening_ticks:
    show bg apartment_night
    $ current_phone_screen = "main"

    if current_business_streak >= 3:
        "You spent the whole evening working on your business."
        jump evening_sleep_maintenance

    if course_days_remaining > 0:
        $ course_days_remaining -= 1
        "You attend your night course."
        $ is_evening_consumed = True
        if course_days_remaining == 0:
            $ unlocked_own_business = True
            "You finished your course. You can now start your own business."

    if study_days_remaining > 0:
        $ study_days_remaining -= 1
        "You study on your phone and finish a chapter."
        $ is_evening_consumed = True
        if study_days_remaining == 0:
            $ unlocked_freelance = True
            "You finished your studies. You can now look for freelance work."

    jump evening_dashboard_loop

# ---------------------------------------------------------
# CHIEF EVENING MENU CONTROLLER
# ---------------------------------------------------------
label evening_dashboard_loop:
    # Refresh the UI dashboard overlay canvas screen
    call screen main_evening_dashboard_ui
    
    # Process return values from buttons
    if _return == "do_something":
        jump label_do_something_hub
    elif _return == "check_phone":
        jump label_check_phone_hub
    elif _return == "sleep":
        jump evening_sleep_with_warning

# ---------------------------------------------------------
# [DO SOMETHING] NAVIGATION ENGINE & ACTIVITIES
# ---------------------------------------------------------
label label_do_something_hub:
    call screen submenu_do_something_ui
    
    if _return == "back":
        jump evening_dashboard_loop
    elif _return == "gym_visit":
        jump activity_gym_execution
    elif _return == "fortune_visit":
        jump activity_fortune_execution
    elif _return == "sam_hangout":
        jump text_sam_interface_loop
    elif _return == "emilie_hangout":
        jump emilie_phone_hangout_scheduling_action
    elif _return == "luca_hangout":
        jump luca_phone_hangout_scheduling_action

# A. Gym Access Calculation Loop
label activity_gym_execution:
    $ is_evening_consumed = True
    
    if gym_membership_active:
        "You scan your membership card and hit the weights."
        $ stamina_gain = scaled_gain("stamina", 5, growth_stamina)
        $ stat_stamina = min(100, stat_stamina + stamina_gain)
        "Your Stamina increases by [stamina_gain] to [stat_stamina]."
    else:
        "You do not have a membership, so you pay $20 for a day pass."
        $ current_cash -= 20.00
        $ stamina_gain = scaled_gain("stamina", 3, growth_stamina)
        $ stat_stamina = min(100, stat_stamina + stamina_gain)
        "Your Stamina increases by [stamina_gain] to [stat_stamina]."
        
    jump evening_dashboard_loop

# B. Fortune Teller Analytics & Golden Rose NG+ Matrix
label activity_fortune_execution:
    $ is_evening_consumed = True
    $ fortune_sessions_attended += 1
    
    # Process pass balances if they bought prepaid cards
    if fortune_passes_remaining > 0:
        $ fortune_passes_remaining -= 1
        "You present one of your prepaid passes to the Fortune Teller."
    else:
        "You pay the out-of-pocket single session fee of $99.00."
        $ current_cash -= 99.00

    scene bg fortune_tent with fade
    fortune "Welcome back to the tent, traveler. Sit down and peer into the absolute values of your current reality."
    
    # EXCLUSIVE METHOD: The only window exposed to raw 100-point traits
    "The Fortune Teller lays down cards revealing your absolute inner parameters:"
    "Intellect: [stat_intellect] | Stamina: [stat_stamina]"
    "Charisma : [stat_charisma]"
    
    # --- NEW GAME PLUS SECRET ROSES MATRIX ---
    if persistent.has_completed_good_run and not has_received_golden_roses:
        
        # PATH B: Guided Carry-Over Run via Ledger
        if persistent.owns_ledger_of_absolute_value:
            "You gently pull the Ledger of Absolute Value out from your bag and set it on the table."
            fortune "Hmm... that's why you look so familiar."
            fortune "Take this box. It contains 6 Golden Roses. Use their affinity carefully to bypass your daily professional sacrifices."
            fortune "And please, take your money back for this session. The ledger records that your debts are already cleared."
            $ current_cash += 99.00
            $ has_received_golden_roses = True
            $ golden_roses_count = 6
            
        # PATH A: Blind Replay Run on the 3rd Session
        elif fortune_sessions_attended >= 3:
            fortune "You look familiar... yes, I remember your spirit timeline patterns now."
            fortune "Take this box. Inside are 6 Golden Roses. Gift them to your companions to maximize their development parameters instantly."
            $ has_received_golden_roses = True
            $ golden_roses_count = 6

    fortune "Go forth safely. Your current cosmic alignment is recorded."
    jump evening_dashboard_loop

# C. Instant Cafe Meetup Integration Hook
label activity_cafe_instant_execution:
    # WIP: not wired to any menu yet
    $ is_evening_consumed = True
    "You step out of your apartment to meet up with your companion tonight."
    # High-affinity character date choices will jump from here during our script sessions
    jump evening_dashboard_loop

# ---------------------------------------------------------
# [CHECK YOUR PHONE] SUBMENU HOOKS (Framework Interface)
# ---------------------------------------------------------
label label_check_phone_hub:
    call screen submenu_check_phone_ui_master
    
    if _return == "back":
        jump evening_dashboard_loop
    elif _return == "buy_pass_1":
        $ current_cash -= 99.00
        $ fortune_passes_remaining += 1
        "You purchased 1 Fortune Teller Pass ($99.00)."
    elif _return == "buy_pass_2":
        $ current_cash -= 189.00
        $ fortune_passes_remaining += 2
        "You purchased 2 Fortune Teller Passes ($189.00)."
    elif _return == "buy_pass_3":
        $ current_cash -= 219.00
        $ fortune_passes_remaining += 3
        "You purchased 3 Fortune Teller Passes ($449.00)."
    elif _return == "toggle_gym_sub":
        if gym_membership_active:
            $ gym_membership_active = False
            "Membership cancelled. You will not be billed again."
        else:
            if current_cash >= 60.00:
                $ current_cash -= 60.00
                $ gym_membership_active = True
                $ gym_days_until_billing = 5
                "You paid $60 for a membership. You have access for 5 days."
            else:
                "Insufficient card balance to authorize membership initialization ($60.00)."
    $ renpy.restart_interaction()
    jump label_check_phone_hub

# ---------------------------------------------------------
# RELAXATION, BREAKS, & CALENDAR MAINTENANCE PROCESSING
# ---------------------------------------------------------
label trigger_business_break_logic:
    if current_business_streak == 0:
        "You aren't actively running a streak. No business break needed right now."
        jump evening_dashboard_loop
        
    $ current_business_streak = 0
    $ business_breaks_taken += 1
    
    if business_breaks_taken == 1:
        "You decide to take a short break from your business operations tonight to manage your schedule."
    elif business_breaks_taken == 2:
        "Warning: This is your second business break. Taking one more break will cause your company to collapse completely."
    elif business_breaks_taken >= 3:
        "You neglected your business for too long."
        "Your business went bankrupt."
        "It is gone for good."
        $ current_tier = "Unemployed"
        
    jump evening_phase

label evening_sleep_with_warning:
    if not is_evening_consumed:
        "You decide to head straight to bed early tonight without performing any major activities."
    jump evening_sleep_maintenance

label evening_sleep_maintenance:    
    if gym_membership_active:
        $ gym_days_until_billing -= 1
        if gym_days_until_billing <= 0:
            if current_cash >= 60.00:
                $ current_cash -= 60.00
                $ gym_days_until_billing = 5
                "Your recurring 5-day membership auto-renewed (-$60.00)."
            else:
                $ gym_membership_active = False
                "Auto-billing failed due to insufficient funds. Your membership has expired."
                
    $ active_day += 1
    jump morning_phase

# ---------------------------------------------------------
# PLACEHOLDER LABELS (were jumped to but did not exist)
# ---------------------------------------------------------
label systemic_insolvency_failed_ending:
    scene black with fade
    if sam_loan_active and current_cash < sam_debt_balance:
        "You could not pay Sam back in time. Things between you are never the same."
    else:
        "Too many days in debt. You cannot keep up with rent and bills anymore."
    "GAME OVER (placeholder ending, WIP)"
    return

label cognitive_isolation_morning:
    "WIP: isolation debuff morning."
    $ active_isolation_debuff = False
    jump morning_phase
