# Initialize structural work variables
default correct_answers_count = 0
default player_math_input = ""
default total_shift_questions = 5
default shift_max_time = 30.0
default active_question_text = ""
default active_correct_answer = ""
default active_display_options = []
default current_question_index = 0

# Python Matrix Questions Array Configuration
init python:
    import random

    master_question_db = {
        "Educator": {
            1: [
                ("4 * 5 - 5", "15", ["10", "15", "20"]),
                ("12 / 3 + 8", "12", ["12", "14", "16"]),
                ("7 + 6 * 2", "19", ["19", "26", "20"]),
                ("9 - 2 * 3", "3", ["3", "21", "6"]),
                ("5 * 4 / 2", "10", ["8", "10", "12"]),
                ("14 + 6 - 3", "17", ["15", "17", "19"]),
                ("8 / 2 * 4", "16", ["1", "16", "4"]),
                ("10 - 5 + 3", "8", ["2", "8", "12"]),
                ("3 * 6 - 4", "14", ["10", "14", "18"]),
                ("15 / 5 + 9", "12", ["12", "15", "18"]),
                ("6 + 4 * 3", "18", ["30", "18", "24"]),
                ("20 - 4 * 2", "12", ["32", "12", "16"]),
                ("7 * 3 - 5", "16", ["16", "21", "26"]),
                ("18 / 2 + 3", "12", ["9", "12", "15"]),
                ("8 + 9 - 4", "13", ["11", "13", "15"])
            ],
            2: [
                ("Find x: 2x = 10", "5", ["3", "5", "7"]),
                ("Find x: x + 7 = 15", "8", ["6", "8", "10"]),
                ("Find x: 3x - 4 = 11", "5", ["4", "5", "6"]),
                ("What is 10% of 90?", "9", ["9", "10", "90"]),
                ("What is 50% of 60?", "30", ["20", "30", "40"]),
                ("Simplify: 1/2 + 1/4", "3/4", ["2/4", "3/4", "1/6"]),
                ("Find x: x - 9 = -3", "6", ["6", "-6", "12"]),
                ("Find x: 4x + 2 = 18", "4", ["3", "4", "5"]),
                ("What is 25% of 40?", "10", ["5", "10", "20"]),
                ("Find x: 2x - 8 = 0", "4", ["2", "4", "6"]),
                ("Simplify: 5x + 2x - 3x", "4x", ["4x", "7x", "3x"]),
                ("Find x: x / 2 = 7", "14", ["9", "14", "21"]),
                ("What is 20% of 80?", "16", ["10", "16", "20"]),
                ("Find x: 3x + 9 = 18", "3", ["2", "3", "4"]),
                ("Simplify: -5 + 12", "7", ["7", "-7", "17"])
            ],
            3: [
                ("Find x: 3x - 7 = 14", "7", ["5", "7", "9"]),
                ("Simplify expression: 4(x + 2) - 3x", "x+8", ["x+8", "x+2", "7x+8"]),
                ("Find degree of polynomial: 4x^3 + 2x - 1", "3", ["1", "2", "3"]),
                ("Add the expressions: (2x + 3) + (x - 5)", "3x-2", ["3x-2", "3x+8", "3x-8"]),
                ("Subtract the expressions: (2x - 5) - (x - 2)", "x-3", ["x-3", "x-7", "3x-7"]),
                ("Find x: 5x + 10 = 35", "5", ["4", "5", "6"]),
                ("Simplify expression: 2(3x - 1) - 4x", "2x-2", ["2x-2", "2x-1", "6x-2"]),
                ("Add the expressions: (3x - 4) + (2x + 1)", "5x-3", ["5x-3", "5x-5", "5x+3"]),
                ("Subtract the expressions: (4x + 2) - (x - 3)", "3x+5", ["3x+5", "3x-1", "5x+5"]),
                ("Find x: x / 3 + 4 = 7", "9", ["6", "9", "12"]),
                ("Simplify expression: 3(x - 3) + 2x", "5x-9", ["5x-9", "5x+9", "5x-3"]),
                ("Add the expressions: (x + 7) + (2x - 2)", "3x+5", ["3x+5", "3x+9", "3x-5"]),
                ("Subtract the expressions: (5x - 1) - (2x + 3)", "3x-4", ["3x-4", "3x+2", "7x-4"]),
                ("Find x: 2(x + 4) = 16", "4", ["4", "6", "8"]),
                ("Find degree of polynomial: 7x^2 - 5", "2", ["1", "2", "0"])
            ]
        },
        "Analyst": {
            1: [
                ("Find x: 3x - 7 = 14", "7"),
                ("Simplify expression: 4(x + 2) - 3x", "x+8"),
                ("Find degree of polynomial: 4x^3 + 2x - 1", "3"),
                ("Add the expressions: (2x + 3) + (x - 5)", "3x-2"),
                ("Subtract the expressions: (2x - 5) - (x - 2)", "x-3"),
                ("Find x: 5x + 10 = 35", "5"),
                ("Simplify expression: 2(3x - 1) - 4x", "2x-2"),
                ("Add the expressions: (3x - 4) + (2x + 1)", "5x-3"),
                ("Subtract the expressions: (4x + 2) - (x - 3)", "3x+5"),
                ("Find x: x / 3 + 4 = 7", "9"),
                ("Simplify expression: 3(x - 3) + 2x", "5x-9"),
                ("Add the expressions: (x + 7) + (2x - 2)", "3x+5"),
                ("Subtract the expressions: (5x - 1) - (2x + 3)", "3x-4"),
                ("Find x: 2(x + 4) = 16", "4"),
                ("Find degree of polynomial: 7x^2 - 5", "2")
            ],
            2: [
                ("Multiply the binomials: (x + 3)(x - 2)", "x^2+x-6"),
                ("Divide the polynomials: (x^2 + 5x + 6) / (x + 2)", "x+3"),
                ("Find the larger root of: x^2 - 5x + 6 = 0", "3"),
                ("Multiply the binomials: (x - 4)(x + 4)", "x^2-16"),
                ("Divide the polynomials: (x^2 - 9) / (x - 3)", "x+3"),
                ("Find the larger root of: x^2 - 7x + 12 = 0", "4"),
                ("Multiply the binomials: (x + 1)(x + 5)", "x^2+6x+5"),
                ("Divide the polynomials: (x^2 + 4x + 3) / (x + 1)", "x+3"),
                ("Find the larger root of: x^2 - 4x + 3 = 0", "3"),
                ("Multiply the binomials: (x - 2)(x - 3)", "x^2-5x+6"),
                ("Divide the polynomials: (x^2 - 4) / (x + 2)", "x-2"),
                ("Find the larger root of: x^2 - 6x + 8 = 0", "4"),
                ("Multiply the binomials: (x + 2)(x + 2)", "x^2+4x+4"),
                ("Divide the polynomials: (x^2 + x - 2) / (x - 1)", "x+2"),
                ("Find the larger root of: x^2 - 3x + 2 = 0", "2")
            ],
            3: [
                ("Solve system for x: x + y = 10 AND x - y = 2", "6"),
                ("Find slope (m) through coordinates (2, 3) and (5, 9)", "2"),
                ("Find vertex parameter h of parabola: y = (x - 3)^2 + 4", "3"),
                ("Solve system for y: 2x + y = 12 AND 2x - y = 8", "2"),
                ("Find slope (m) through coordinates (1, 2) and (3, 10)", "4"),
                ("Find vertex parameter h of parabola: y = (x + 5)^2 - 2", "-5"),
                ("Solve system for x: 2x + y = 7 AND x - y = 2", "3"),
                ("Find slope (m) through coordinates (0, 0) and (4, 12)", "3"),
                ("Find vertex parameter h of parabola: y = (x - 1)^2 + 7", "1"),
                ("Solve system for y: x + 2y = 8 AND x - 2y = 0", "2"),
                ("Find slope (m) through coordinates (2, 5) and (4, 11)", "3"),
                ("Find vertex parameter h of parabola: y = (x + 2)^2 + 1", "-2"),
                ("Solve system for x: 3x - y = 9 AND x + y = 3", "3"),
                ("Find slope (m) through coordinates (3, 1) and (6, 10)", "3"),
                ("Find vertex parameter h of parabola: y = (x - 4)^2 - 5", "4")
            ]
        },
        "Researcher": {
            1: [
                ("Solve system for x: x + y = 10 AND x - y = 2", "6"),
                ("Find slope (m) through coordinates (2, 3) and (5, 9)", "2"),
                ("Find vertex parameter h of parabola: y = (x - 3)^2 + 4", "3"),
                ("Solve system for y: 2x + y = 12 AND 2x - y = 8", "2"),
                ("Find slope (m) through coordinates (1, 2) and (3, 10)", "4"),
                ("Find vertex parameter h of parabola: y = (x + 5)^2 - 2", "-5"),
                ("Solve system for x: 2x + y = 7 AND x - y = 2", "3"),
                ("Find slope (m) through coordinates (0, 0) and (4, 12)", "3"),
                ("Find vertex parameter h of parabola: y = (x - 1)^2 + 7", "1"),
                ("Solve system for y: x + 2y = 8 AND x - 2y = 0", "2"),
                ("Find slope (m) through coordinates (2, 5) and (4, 11)", "3"),
                ("Find vertex parameter h of parabola: y = (x + 2)^2 + 1", "-2"),
                ("Solve system for x: 3x - y = 9 AND x + y = 3", "3"),
                ("Find slope (m) through coordinates (3, 1) and (6, 10)", "3"),
                ("Find vertex parameter h of parabola: y = (x - 4)^2 - 5", "4")
            ],
            2: [
                ("Evaluate: f(x, y) = 3x + 2y - 10 when x=4, y=3", "8"),
                ("Solve for x in rational linear equation: 12 / x = 3", "4"),
                ("Evaluate: f(x, y) = xy - 2x when x=5, y=4", "10"),
                ("Solve for x in rational linear equation: 24 / x = 6", "4"),
                ("Evaluate: f(x, y) = 2x^2 + y when x=3, y=5", "23"),
                ("Solve for x in rational linear equation: 30 / x = 5", "6"),
                ("Evaluate: f(x, y) = 4x - 3y when x=5, y=2", "14"),
                ("Solve for x in rational linear equation: 18 / x = 9", "2"),
                ("Evaluate: f(x, y) = x(y + 2) when x=3, y=4", "18"),
                ("Solve for x in rational linear equation: 40 / x = 4", "10"),
                ("Evaluate: f(x, y) = 2x - y + 4 when x=6, y=3", "13"),
                ("Solve for x in rational linear equation: 50 / x = 2", "25"),
                ("Evaluate: f(x, y) = x^2 - y^2 when x=5, y=3", "16"),
                ("Solve for x in rational linear equation: 100 / x = 10", "10"),
                ("Evaluate: f(x, y) = 3xy when x=2, y=5", "30")
            ],
            3: [
                ("Solve 3-variable system for z: x+y+z=15, x=4, y=5", "6"),
                ("Simplify expression value at x=2, y=2: (4x^2y) / (2xy^2)", "2"),
                ("Evaluate polynomial expression when x=2: (x + 1)(x^2 - x + 1)", "9"),
                ("Simplify fractional exponent: 27^(2/3)", "9"),
                ("Solve radical equation for x: sqrt(2x + 5) = 5", "10"),
                ("Determine discriminant value: 2x^2 + 4x + 5 = 0", "-24"),
                ("Solve exponential growth formula for x: 2^(x - 1) = 32", "6"),
                ("Simplify rational function value at x=2: (x / 2) + (4 / x)", "3"),
                ("Simplify fractional exponent: 16^(3/4)", "8"),
                ("Solve radical equation for x: sqrt(3x + 1) = 4", "5"),
                ("Determine discriminant value: x^2 - 6x + 9 = 0", "0"),
                ("Solve exponential growth formula for x: 3^(x + 1) = 27", "2"),
                ("Simplify rational function value at x=4: (x / 4) + (8 / x)", "3"),
                ("Simplify fractional exponent: 8^(2/3)", "4"),
                ("Solve radical equation for x: sqrt(x - 2) = 3", "11")
            ]
        }
    }

    def normalize_answer(s):
        # case/space-insensitive, accepts the superscript-2 character for ^2
        return str(s).lower().replace(" ", "").replace(u"\u00b2", "^2").replace(u"\u2212", "-")

    def setup_shift_questions(tier, rank, intellect):
        pool = list(master_question_db[tier][rank])
        renpy.random.shuffle(pool)
        max_q = 8 if tier == "Educator" else (6 if tier == "Analyst" else 4)
        # New 100-point adaptive scaling algorithm
        min_q = 1 if tier == "Researcher" else 2
        calculated_count = int(max(min_q, round((100.0 - intellect) / 100.0 * max_q)))
        return pool[:calculated_count]

label initialize_work_shift:
    $ current_shift_questions = setup_shift_questions(current_tier, job_level_rank, stat_intellect)
    $ total_shift_questions = len(current_shift_questions)
    $ correct_answers_count = 0
    $ shift_failed = False
    $ current_question_index = 0
    
    # Clocks scale at a precise +0.5s per Stamina point
    if current_tier == "Educator":
        scene bg educator_place with fade
        $ shift_max_time = 30.0 + (stat_stamina * 0.5)
    elif current_tier == "Analyst":
        scene bg analyst_place with fade
        $ shift_max_time = 45.0 + (stat_stamina * 0.5)
    elif current_tier == "Researcher":
        scene bg researcher_place with fade
        $ shift_max_time = 60.0 + (stat_stamina * 0.5)
    else:
        $ raise ValueError("Not valid tier.")
        
    jump work_question_router

label work_question_router:
    $ renpy.block_rollback()
    if current_question_index >= total_shift_questions:
        jump complete_shift_scoreboard
        
    $ active_question_data = current_shift_questions[current_question_index]
    $ active_question_text = active_question_data[0]
    $ active_correct_answer = active_question_data[1]
    
    if current_tier == "Educator":
        $ active_display_options = list(active_question_data[2])
        $ renpy.random.shuffle(active_display_options)
        show screen active_educator_ui_screen
    else:
        $ player_math_input = ""
        if current_tier == "Analyst":
            show screen active_analyst_ui_screen
        else:
            show screen active_researcher_ui_screen
            
    $ renpy.pause(shift_max_time, hard=True)
    jump workplace_deadline_failure

label process_submitted_choice:
    hide screen active_educator_ui_screen
    if player_math_input == active_correct_answer:
        $ correct_answers_count += 1
    else:
        $ current_stress = min(100, current_stress + 10)
    $ current_question_index += 1
    jump work_question_router

label process_submitted_input:
    hide screen active_analyst_ui_screen
    hide screen active_researcher_ui_screen
    if normalize_answer(player_math_input) == normalize_answer(active_correct_answer):
        $ correct_answers_count += 1
        $ current_question_index += 1
        jump work_question_router
    else:
        if current_tier == "Researcher":
            "One wrong step and the whole proof falls apart. Today's work is ruined."
            $ current_stress = min(100, current_stress + 20)
            $ shift_failed = True
            $ correct_answers_count = 0
            $ promotion_streak_counter = 0
            jump complete_shift_scoreboard
        else:
            $ current_stress = min(100, current_stress + 15)
            $ current_question_index += 1
            jump work_question_router

label workplace_deadline_failure:
    hide screen active_educator_ui_screen
    hide screen active_analyst_ui_screen
    hide screen active_researcher_ui_screen
    $ shift_failed = True
    $ promotion_streak_counter = 0
    "You ran out of time."
    $ current_stress = min(100, current_stress + 25)
    jump complete_shift_scoreboard

label complete_shift_scoreboard:
    if shift_failed:
        $ shift_score = 0
    else:
        $ shift_score = int((correct_answers_count / total_shift_questions) * 100)
    jump execute_career_evaluation_logic

label execute_career_evaluation_logic:
    if shift_score < 20:
        $ job_strike_counter += 1
        $ promotion_streak_counter = 0
        call screen shift_summary_scoreboard_screen
        if job_strike_counter >= get_max_strikes():
            jump job_termination_logic
    elif shift_score == 100:
        $ promotion_streak_counter += 1
        call screen shift_summary_scoreboard_screen
        if promotion_streak_counter >= 3:
            $ promotion_streak_counter = 0
            if job_level_rank < 3:
                $ job_level_rank += 1
                $ current_stress = max(0, current_stress - 10) 
                "You got promoted! You are now Level [job_level_rank]."
    else:
        $ promotion_streak_counter = 0
        call screen shift_summary_scoreboard_screen
    if current_tier == "Educator":
        $ payout = 80.00 + (job_level_rank * 30.00 - 30.00)
    elif current_tier == "Analyst":
        $ payout = 120.00 + (job_level_rank * 40.00 - 40.00)
    else:
        $ payout = 200.00 + (job_level_rank * 50.00 - 50.00)
        
    if shift_score >= 20:
        $ current_cash += payout
    jump afternoon_phase

label job_termination_logic(return_back=False):
    $ job_strike_counter = 0
    $ promotion_streak_counter = 0
    if job_level_rank > 1:
        $ job_level_rank = 1
        $ current_stress = min(100, current_stress + 20)
        "You were demoted to Level [job_level_rank] for poor performance."
        jump afternoon_phase
    else:
        if current_tier == "Educator":
            "You have been terminated. You cannot reapply to be an educator."
        else:
            "You have been terminated, you cannot reapply to be [current_tier]."
        $ terminated_jobs.append(current_tier)
        $ current_tier = "Unemployed"
        $ job_level_rank = 1
    if return_back:
        return
    else:
        jump afternoon_phase

screen active_educator_ui_screen():
    timer shift_max_time action Jump("workplace_deadline_failure")
    frame:
        xalign 0.5 yalign 0.4 xpadding 30 ypadding 30
        vbox:
            spacing 15
            text "Task [current_question_index+1] of [total_shift_questions]" xalign 0.5 size 22
            
            # VISUAL CLOCK: An animated bar that physically shrinks as time ticks away
            bar:
                value AnimatedValue(value=0.0, range=shift_max_time, delay=shift_max_time, old_value=shift_max_time)
                xmaximum 300
                xalign 0.5
                
            text "Grade: [active_question_text]" xalign 0.5 size 28 color "#fff"
            for opt in active_display_options:
                textbutton "[opt]" action [Hide("active_educator_ui_screen"),SetVariable("player_math_input", opt), Jump("process_submitted_choice")] xalign 0.5 xminimum 180

screen active_analyst_ui_screen():
    timer shift_max_time action Jump("workplace_deadline_failure")
    frame:
        xalign 0.5 yalign 0.4 xpadding 30 ypadding 30
        vbox:
            spacing 15
            text "Task [current_question_index+1] of [total_shift_questions]" xalign 0.5 size 22
            
            bar:
                value AnimatedValue(value=0.0, range=shift_max_time, delay=shift_max_time, old_value=shift_max_time)
                xmaximum 300
                xalign 0.5
                
            text "Solve:\n[active_question_text]" xalign 0.5 size 26 text_align 0.5
            text "Type your answer in simplest form, like x^2+3x-4 or 5" xalign 0.5 size 16 color "#9ca3af"
            
            input value VariableInputValue("player_math_input") length 20 xalign 0.5 size 26
            
            textbutton "Submit" action [Hide("active_analyst_ui_screen"), Jump("process_submitted_input")] xalign 0.5

screen active_researcher_ui_screen():
    timer shift_max_time action Jump("workplace_deadline_failure")
    frame:
        xalign 0.5 yalign 0.4 xpadding 30 ypadding 30
        vbox:
            spacing 15
            text "Proof [current_question_index+1] of [total_shift_questions]" xalign 0.5 size 22
            
            bar:
                value AnimatedValue(value=0.0, range=shift_max_time, delay=shift_max_time, old_value=shift_max_time)
                xmaximum 300
                xalign 0.5
                
            text "Verify Function:\n[active_question_text]" xalign 0.5 size 26 text_align 0.5
            text "Type your answer in simplest form, like x^2+3x-4 or 5" xalign 0.5 size 16 color "#9ca3af"
            
            input value VariableInputValue("player_math_input") length 20 xalign 0.5 size 26
            
            textbutton "Submit" action [Hide("active_researcher_ui_screen"), Jump("process_submitted_input")] xalign 0.5

screen shift_summary_scoreboard_screen():
    frame:
        xalign 0.5 yalign 0.4 xpadding 40 ypadding 40 xminimum 450
        vbox:
            spacing 20
            text "[current_tier] Rank [job_level_rank] Shift Over" xalign 0.5 size 24
            text "Correct answers: [correct_answers_count] / [total_shift_questions]" size 20
            text "Score: [shift_score]%" size 20 color ( "#22c55e" if shift_score >= 20 else "#ef4444" )
            text "Strikes: [job_strike_counter] / [get_max_strikes()]" size 16 color ("#ef4444" if job_strike_counter >= 1 else "#fff")
            text "Streak: [promotion_streak_counter] / 3 Flawless Days" size 16 color ("#22c55e" if promotion_streak_counter > 0 else "#fff")
            textbutton "Proceed" action Return() xalign 0.5