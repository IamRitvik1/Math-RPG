default sam_storyline_started = False
default sam_hangouts_completed = 0
default sam_storyline_complete = False
default sam_loan_active = False
default sam_debt_balance = 0.00
default sam_debt_due_day = 0
default sam_hangout_1_track = "none" # Tracks your dynamic cross-meeting requirements
default sam_meetup_scheduled_tomorrow = False
default sam_affinity_skip_active = False
default sam_affinity_rejected_once = False


label text_sam_interface_loop:
    menu text_sam_menu_dashboard:
        "Borrow Emergency Cash" if sam_storyline_started and not sam_loan_active:
            jump sam_phone_loan_request_action
            
        "Pay Back Active Debt" if sam_loan_active and current_cash >= sam_debt_balance:
            jump sam_phone_loan_repayment_action
            
        "Schedule Casual Hangout" if sam_storyline_started and not sam_storyline_complete and not is_evening_consumed and not sam_meetup_scheduled_tomorrow:
            jump sam_phone_hangout_scheduling_action

        "[[ Back ]":
            jump label_do_something_hub
# ---------------------------------------------------------
# BANKING LEDGER HANDLERS & PHONE MEETING CLOCKS
# ---------------------------------------------------------
label sam_phone_loan_request_action:
    if sam_hangouts_completed < 2:
        player "Sam, could I please borrow some money, I am short on cash."
        sam "Ok, I will send 50 dollars but please pay me back before next week and don't make this a habit."
        $ current_cash += 50.00
        $ sam_debt_balance = 50.00
        $ sam_debt_due_day = active_day + 3 + stat_charisma//30
        $ sam_loan_active = True
        "50 dollars was added to your account. You must repay Sam by Day [sam_debt_due_day]."
    else:
        player "Sam, could I please borrow some money, I am short on cash."
        sam "Sure, here is 75 dollars. Pls pay me back whenever you have enough."
        $ current_cash += 75.00
        $ sam_debt_balance = 75.00
        $ sam_debt_due_day = active_day + 4
        $ sam_loan_active = True
        "75 dollars was added to your account. You must repay Sam by Day [sam_debt_due_day]."
        
    jump text_sam_interface_loop

label sam_phone_loan_repayment_action:
    $ current_cash -= sam_debt_balance
    "You repaid $[sam_debt_balance:.2f] to Sam. Your debt is now cleared."
    $ sam_debt_balance = 0.00
    $ sam_loan_active = False
    $ sam_debt_due_day = 0
    jump text_sam_interface_loop

label sam_phone_hangout_scheduling_action:
    if sam_meetup_scheduled_tomorrow:
        "You have already asked Sam to hangout, he said to come tomorrow to the cafe."
        jump text_sam_interface_loop
    if meetup_booked():
        "You already have plans for tomorrow evening."
        jump text_sam_interface_loop
    if job_level_rank >= 3:
        "Your daily workload is simply too overwhelming to schedule any casual hangouts right now."
        jump text_sam_interface_loop

    if sam_hangouts_completed < 2:
        player "Hi Sam, we should really hangout soon."
        sam "Yeah sure, I will book a reservation at the cafe after my shift."
        $ sam_meetup_scheduled_tomorrow = True
        "You sent the text. Sam booked a table for tomorrow evening."
        jump text_sam_interface_loop
    elif sam_hangouts_completed == 2:
        player "Hi Sam, we should really hangout."
        sam "Yeah sure, Come to the cafe now since my shift just got over."
        jump sam_casual_hangout_3
    elif sam_hangouts_completed == 3 and not sam_affinity_skip_active and not sam_affinity_rejected_once:
        player "Hi Sam, we should really hangout. Can we meet at the cafe whenever you're free?"
        sam "I took up that night job I told you about. It started 3 hours ago and I am on my break right now, but I have to go back after 5 minutes, and I will not be free after this. If you want to hangout you can come tomorrow morning but i understand if you can't because of your job."
        menu:
            "Yeah no worries, I will come tomorrow morning.":
                $ sam_meetup_scheduled_tomorrow = True
                $ sam_affinity_skip_active = True
                jump text_sam_interface_loop
            "I am busy tomorrow so I cannot come, I'm sorry.":
                sam "It's fine text me whenever you want to hangout but I will only be available in the mornings from now on."
                $ sam_affinity_rejected_once = True
                jump text_sam_interface_loop
    elif sam_hangouts_completed == 3 and not sam_affinity_skip_active and sam_affinity_rejected_once:
        player "Can we hangout tomorrow morning?"
        sam "Yeah sure, come to the cafe in the morning. But are you sure you are fine missing work?"
        player "Yeah I am fine missing it tomorrow."
        $ sam_meetup_scheduled_tomorrow = True
        $ sam_affinity_skip_active = True
        jump text_sam_interface_loop
    elif sam_hangouts_completed == 4:
        player "Can we hangout tomorrow morning?"
        sam "Yeah sure, come to the cafe in the morning. But you already got 1 strike earlier, are you sure you want to risk your job for me."
        player "Yeah you are one of my best friends ever so I think it is worth it."
        $ sam_meetup_scheduled_tomorrow = True
        jump text_sam_interface_loop
    else:
        sam "I'm swamped with work right now, text me again later."
        jump text_sam_interface_loop
# ---------------------------------------------------------
# CORE NARRATIVE SCENE INTERACTIONS & DIALOGUE ENCOUNTERS
# ---------------------------------------------------------
label day_2_doorbell_intercept:
    show sam normal
    "You hear a doorbell. It is Sam."
    sam "Hey! I wanted to stop by and help you set up like I promised."
    "Together you finished setting up your supplies."
    player "Thank you so much, Sam."
    show sam smirk
    sam "No problem at all! Glad I could help. See you around!"
    "Sam waves goodbye and leaves."
    hide sam with dissolve
    jump evening_ticks

label sam_casual_hangout_1:
    scene bg cafe_interior with fade
    $ is_evening_consumed = True
    
    show sam normal
    sam "Hi [player_name], how is the city? Hope you like it. It has been so long since I could talk to you like this. Remember the time when we..."
    menu:
        "Romantic History":
            player "...used to go on dates in school and then broke up since you were moving out of town. I was so sad and heartbroken, you know I never dated anyone after you."
            sam "Oh yeah right, I am so sorry for leaving you like that, we can continue now."
            menu:
                "Start dating again":
                    player "Yeah sure. We should start dating again, it was some of the best times I had in school."
                    sam "Yeah, I agree, we will just remain casual and go on dates to not jeopardize our friendship."
                    "REST OF THIS TRACK IS WIP FROM HERE, ALL TEXTS FROM NOW ON WILL ASSUME YOU SAID NO."
                    $ sam_hangout_1_track = "platonic_links"
                "Stay friends":
                    player "Nah, I loved you and all but I must move on and I dont want to jeopardize our friendship now."
                    sam "Yeah sure, we can remain just friends."
                    $ sam_hangout_1_track = "platonic_links" # Roots directly into Hangout 2 Option B
        "Prank History":
            player "...used to prank each other. Yeah it was so fun. I loved thinking of a way to one up your pranks. I think that is how I am so passionate."
            sam "Yeah, I remember all the creative pranks we made. Remember the slime prank I did. You were crying for a whole week and got me back with the bug prank. It is nice to talk like this with my old best friend."
            $ sam_hangout_1_track = "prank_link" # Roots directly into Hangout 2 Option A
        "Hangout History":
            player "...used to go to the movies together. You always paid for the tickets and I always bought the snacks. But now both are so expensive. But it was nice watching a movie with a good friend like you."
            sam "Yeah it was so fun watching the movies with my best friend. We always used to yap together about headcanons and things. It is nice to talk like this with my old best friend."
            $ sam_hangout_1_track = "platonic_links" # Roots directly into Hangout 2 Option B
    $ sam_hangouts_completed = 1
    hide sam
    jump evening_ticks

label sam_casual_hangout_2:
    
    show sam normal
    scene bg cafe_interior with fade
    $ is_evening_consumed = True
    sam "Hi [player_name], how is your job going? Hope it is going great. For me I like this job here but I really want to switch jobs since it does not give enough money. Anyways, how is life going?"
    
    # Enforces your exact dynamic pathing links natively
    if sam_hangout_1_track == "prank_link":
        # Forced Option A selection sequence (Triggered uniquely by Option B previously)
        show sam confident
        player "It is going fine. I do not like my job also that much but like it is what it is. I really want to start my own business and explore my passion more."
        sam "Yeah, here you can start your own business pretty easily, and with your passion I think going freelance is good. But like I recommend doing some phone study since it really helps with freelance. Anyways, hope everything else is going great."
        player "Yeah it is. Thank you so much. So, I have to buy some supplies so bye!!!"
        hide sam
        $ current_cash -= max(0.00, min(15.00, current_cash))
        $ sam_hangout_2_choice = "supplies"
    else:
        # Forced Option B selection sequence (Triggered uniquely by Option A.2 or Option C previously)
        player "Ehh! I don't really care about jobs that much, I just want to chill and hangout with my old best friend. So like I know you like strawberries so how about I buy you a strawberry latte?"
        show sam smirk
        sam "You would do that for me. I know finances are tight for you right now so you don't really have to. But thank you."
        player "I must do it since you have been my friend for so long and you were the one who kept me going in school."
        $ current_cash -= max(0.00, min(15.00, current_cash))
        $ sam_hangout_2_choice = "latte"
    hide sam
    $ sam_hangouts_completed = 2
    jump evening_ticks

label sam_casual_hangout_3:
    scene bg cafe_interior with fade
    $ is_evening_consumed = True
    show sam normal
    if sam_hangout_2_choice == "latte":
        show sam smirk
        sam "Hi [player_name]. I remember you liked coffees a lot so i bought you one."
        player "Thank you so much!!! And I still do like coffees. Yumm!! It tastes so good."
        sam "Also i got the coffee to thank you for the latte last time."
        player "It is an incredibly nice gesture, thank you so much. So, I want to explore the city with a friend and since you are a tour guide you know all the best places, right?"
        show sam normal
        sam "Yeah I do, there is this really great zoo. How about we go now?"
        player "Yeah sure, come let's go."
    else:
        sam "Hi [player_name]. I remember you liked coffees a lot so I bought you one."
        player "Thank you so much!!! And I still do like coffees. Yumm!! It tastes so good."
        sam "Yeah, remember when we used to buy each other our drinks and rate them out of 10? I really had to think hard about which drink to buy. Also it is so nice to have such a nice friend in the city, it is more fun with you here."
        player "Yeah I like this city. Also thanks for showing me around the other day. Without you, i dont know what I would have done."
        sam "Did you get all the supplies? If you need anymore we can go now."
        player "No not really, but thanks for asking. But I want to explore the city more and see what is there."
        sam "Oh that's nice, we can go now."
    scene bg city_exploration with fade
    "You and Sam go out and explore the city and have a lot of fun seeing new places like the zoo and the aquarium."
    "After three hours, you decide to go back to the café after a nice time exploring."
    scene bg cafe_interior with fade
    sam "That was really fun, we should go again sometime. It really took out all the stress I have professionally."
    player "Yeah I agree. So, why do you have so much stress, I thought you loved your tour guide job."
    sam "I do but I recently got an opportunity to shift to a company but it is night shift, so I cannot talk to you that much anymore, and I have done a sample shift and it is really stressful, but the amount of money it earns is too much for me to ignore, it will make me set for life even if I work only for a year or two."
    if has_received_golden_roses and golden_roses_count > 0:
        menu:
            "Comfort Sam (Give Golden Rose)":
                player "Here is a golden rose, I heard it helps with situations like this."
                show sam smirk
                sam "Wait, you are giving me this golden rose!!! You know how rare this is right? And seeing into it I feel that I should not move because it will ruin my friendship with you."
                player "It is yours to keep and I will support you no matter what decision you take."
                $ golden_roses_count -= 1
                $ sam_storyline_complete = True
                hide sam
                jump evening_ticks
            "Encourage Sam (Do not give golden rose)":
                jump label_sam_automatic_encourage
    else:
        jump label_sam_automatic_encourage

label label_sam_automatic_encourage:
    player "You really should take this job if you really think it will help you."
    sam "It 100% will so I think I will take it so I never have to worry about money again."
    $ sam_hangouts_completed = 3
    hide sam
    jump evening_ticks

label sam_affinity_morning_scene_1:
    if current_tier in ["Educator","Analyst", "Researcher"]:
        $ job_strike_counter += 1
        "Because you skipped your scheduled shift to hangout with Sam, you have automatically received 1 corporate strike."
        if job_strike_counter >= get_max_strikes():
            call job_termination_logic(True)

    scene bg cafe_interior with fade
    show sam mad
    player "How you doing sam? Are you better now or do you need anything?"
    sam "It is so stressful and it is so difficult and I am struggling so much. But the amount of money I am earning is crazy. BTW it is 500 dollar per day, that is like 5 day rent per day. It is a crazy amount. Even the highest researchers only earn about 300 dollars per day. I really don't know what to do."
    player "I understand completely and 500 dollars is a huge amount. But if it is so stressful and difficult you should quit or quit after some time. But no matter your decision I stand by you."
    sam "I think I will keep the job for few more days because the money is too much to ignore. Anyways, we should stop talking about my job and start having fun."
    player "Sure lets go."
    scene bg city_exploration with fade
    show sam smirk
    "You and Sam have so much fun going to different places, seeing different things, and just talking about life near the beach."
    "When Sam's shift was about to start, you and Sam went back to the cafe to finish the hangout."
    scene bg cafe_interior with fade
    show sam confident3
    sam "These past few hours really made me forget about my stress. Thanks man. Seeing and visiting all these places with you really reminded me of the good times as a tour guide."
    player "Yeah I had fun too. I really like hanging out with you. But looks like you have to go right now for your job. We should hangout again sometime."
    $ sam_hangouts_completed = 4
    hide sam
    jump afternoon_phase

label sam_affinity_morning_scene_2:
    if current_tier in ["Educator","Analyst", "Researcher"]:
        $ job_strike_counter += 1
        "Because you skipped your scheduled shift to hangout with Sam, you have automatically received 1 corporate strike."
        if job_strike_counter >= get_max_strikes():
            call job_termination_logic(True)
    scene bg cafe_interior with fade
    player "How you doing sam? Are you better now or do you need anything?"
    sam "This job is so stressful but right after our hangout, I became extra focused because of your help and I got promoted on the spot to 1k per day and got 1k that day itself. The new job class is more stressful but even if I endure for a week it will be good."
    player "Yeah I understand. But you should value your mental health, with 1k per day you can have loads of extra money and go back to your old tour guide job since that still pays ok."
    sam "Yeah that makes more sense and thank you for being with me for this journey. Wait, I completely forgot that you missed work twice. I hope you are fine financially."
    player "I can endure and manage on my own pretty well. But some money would be nice."
    sam "Here is 100 dollars right now, take it pls."
    $ current_cash += 100.00
    player "Seriously, that is too much. Thank you so much Sam. I can never repay you."
    sam "You already have repaid me by your presence and your advice. So no thank you [player_name]. Anyways, we should go get icecream and go out and have some fun."
    scene bg city_exploration with fade
    "You and Sam spend 5 hours having fun. You go get icecream, go to the movies, play at the beach, and many other things. After that you decide to go back to the cafe."
    scene bg cafe_interior with fade
    player "1 coffee and 1 strawberry latte pls on me."
    sam "Seriously are you sure, we can always split yk, I have the money."
    player "Sam it is not always about the money, also you are one of my best friends and you just gave me 100 dollars so like I think I need to repay you a little."
    sam "Fine. Also after this hangout I realized that you really sacrificed your career for me. So I will go back to my old job just to hangout with you from tomorrow. Guess I will get that last 1k now huh? Got to go bye!!!"
    player "Bye Sam!! Thank you so much for everything."
    $ sam_storyline_complete = True
    jump afternoon_phase
# ---------------------------------------------------------
# DAY 6 MUTUAL EXCLUSIVITY MEETING ROUTER
# ---------------------------------------------------------
default emilie_unlocked = False
default luca_unlocked = False
default emilie_main_choice = "none"
default luca_main_choice = "none"
default emilie_sub_choice = "none"
default luca_sub_choice = "none"

label day_6_afternoon_check:
    # Triggers right during your afternoon transition phase calculations
    if current_tier in ["Analyst", "Researcher"]:
        jump emilie_day_6_introduction
    else:
        # Triggers for Educators, Unemployed, Business Owners, or Freelancers
        jump luca_day_6_introduction

# ---------------------------------------------------------
# ROUTE A: MANAGING DIRECTOR EMILIE PERFORMANCE REVIEW
# ---------------------------------------------------------
label emilie_day_6_introduction:
    scene bg emilie_office with fade
    "After you finish your work, you are suddenly called by your managing director Emilie."
    "You wonder why and rush to her office, worried if you are in trouble."
    show Emilie default
    player "H-hi Emilie, ma'am... am I in any trouble?"
    emilie "No calm down, don't sweat it. You are in no trouble; it is just that i check my new employees myself and do a review myself."
    
    # SYSTEM GATING ARCHITECTURE: Evaluates Rank Level and Active Warning Tickers
    if job_level_rank >= 2 and job_strike_counter <= 0:
        # Path A.1
        emilie "You are a star employee you know, nobody has been promoted so fast especially starting all the way from Level 1. Good job. And I see you have 0 strikes right now, that is an amazing accomplishment. So don't be scared."
        jump emilie_review_choices_path_a
        
    elif job_level_rank >= 2 and job_strike_counter >= 1:
        # Path A.2
        emilie "You are a very good employee you know, nobody has been promoted so fast especially starting from Level 1. I see you have a strike so be careful since if you get another you will be demoted back to Level 1 but I see you are working very hard so it most likely won't happen. So don't be scared"
        jump emilie_review_choices_path_a
        
    elif job_level_rank == 1 and job_strike_counter <= 0:
        # Path B.1
        emilie "You are a good employee as I see, you have no strikes and you work very hard, good job and if you keep up a streak you will be promoted so strive to do that. But still good job and do not be scared."
        jump emilie_review_choices_path_a
        
    elif job_level_rank == 1 and job_strike_counter >= 1:
        # Path B.2 (Struggling Level 1 Probation)
        emilie "I see you have a strike so be careful since company policy says you will be terminated immediately, so be careful but your strike can be removed from your record if you get promoted so please strive to do that. Don't be scared and I know that you can do good."
        jump emilie_review_choices_path_b2

# CHOICE GATE ROUTER PATH A (Paths A.1, A.2, and B.1 Sharing Universal Dialogue Pools)
label emilie_review_choices_path_a:
    menu:
        "Thank her for her feedback":
            player "Thank you so much for your feedback. I want to excel here."
            emilie "You are already excelling. I like your character, I am giving you a negative strike so if you already have a strike or get a strike in the future, it will not count, also here is my number if you want help in anything outside or in work."
            player "Thank you so much Ms. Emilie. I really appreciate having a director who supports my career growth. I'd love to stay in touch outside of shift hours."
            emilie "Thanks for the praise, but I am not the 'best boss ever', I always want to improve. And sure, let us hangout in a mutually convenient time. Regardless, we have finished the review, so you can head home."
            player "Thank you Ms. Emilie. Goodbye."
            
        "Ask her about how to do better":
            player "I want to do better in my job, how to excel?"
            emilie "Just be yourself and focus on your work in work hours. Also enjoy your work and be passionate about it. And try to not have too much stress since that is detrimental to your mental health."
            player "Thank you so much Ms. Emilie, I will try my best to excel."
            emilie "I like your efficiency and mindset so here is a negative strike so when you get a strike or if you already have a strike, it will not count. Also here is my number if you need any more help or tips."
            player "Thank you so much Ms.Emilie."
            emilie "You are welcome. Regardless, your performance review is over, so please head home."
            player "Goodbye Ms.Emilie"
    hide Emilie
    $ job_strike_counter -= 1
    $ emilie_unlocked = True
    jump evening_phase

# CHOICE GATE ROUTER PATH B.2
label emilie_review_choices_path_b2:
    menu:
        "Accept her feedback":
            player "I am sorry, I will try to do better."
            emilie "No need to apologize, I understand people make mistakes and I know that you will do better, just focus on your work and try to reduce your stress. If you need any help here is my phone number and I will also remove your strike so you can have a clean slate and try again."
            player "Thank you so much for your help and support."
            emilie "You're welcome. Regardless, the performance review is over, please head home."
            player "Yeah sure, goodbye!!!"
            $ job_strike_counter = 0
            
        "Ask her about how to do better":
            player "I want to do better in my job, so how do I excel?"
            emilie "You should be focused and try to enjoy your work, and try to manage stress. I like your attitude though so I am giving you a negative strike removing your current strike and I am giving you my number if you need any more tips."
            player "Thank you so much Ms.Emilie, I will try to excel as much as I can."
            emilie "You are welcome. Regardless, your performance review is over so please head home."
            player "Ok, goodbye!!!"
            $ job_strike_counter -= 1
    hide Emilie
    $ emilie_unlocked = True
    jump evening_phase
label emilie_casual_hangout_2:
    scene bg restaurant with fade
    show Emilie sad_smile
    $ is_evening_consumed = True
    
    player "Hi Emilie, you look tired."
    emilie "Yeah, my workload tripled since the last time we met that is the reason I could not hangout anytime with you."
    player "Wait what seriously?!! Ok come then, let us order and then let us relax for sometime."
    emilie "Yeah that is what I really need now."

    # ENFORCES DYNAMIC CHANCE BASED ON HANGOUT 1 OUTING
    show Emilie default with dissolve
    if emilie_hangout_1_mood == "relaxation":
        "You and Emilie order the food and the website it will take 30 minutes due to rush hour. After placing your order,you and her go and relax by walking around the city and resting at the park. You buy some snacks for her."
    else:
        "You and Emilie order the food and the website it will take 30 minutes due to rush hour. After placing your order,you and her go and have some fun around the city stores."
    if current_cash > 0:
        $ spent_cash = min(25.00, current_cash)
        $ current_cash -= spent_cash
        "You spent [spent_cash] dollars."

    "After, you both went back to the restaurant and your food was due to come in 3 minutes."
    emilie "That is just what I needed, thank you so much."
    player "It is fine. So, different thing, I met Luca and he told me about the other side of the story. Trust me the whole situation is just a big misunderstanding."
    
    emilie "Yeah I realize I made a big mistake by telling him freelance was 'not a real job', after doing some research I realized that some freelancers earn alot, but it is risky so I was correct in a way and I just wanted to look out for him, but I most likely came as harsh and annoying, tell him I am sorry."
    player "How about you tell him yourself, I am planning a meeting between you two so you can just share your feelings about the thing and let go of this feud."
    emilie "If you feel this is the right call, I will stand by it. Regardless, looks like the food came."
    
    "You both ate heartily and really enjoyed the food."
    emilie "Hm, I feel way better. Being around you makes me a better version of myself..."
    emilie "Thank you [player_name]."

    menu emilie_hangout_2_splits:
        # Option 1: Romance Track
        "Ask her to be your girlfriend" if not has_active_relationship and stat_charisma >= 10:
            player "Emilie, I feel the same way around you, would you like to be my girlfriend."
            emilie "Yess, I would love to. But for now let us keep it casual until after the meeting with Luca. Regardless, looks like I have to go now, goodbye.!!"
            player "Goodbye!!!"
            
        # Default Splits (Option 2)
        "Support her through thick and thin":
            player "Thank you Emilie, I feel a lot better around you too, we must support each other through thick and thin."
            
            menu emilie_friendship_vs_mentorship:
                "Corporate mentorship":
                    emilie "I agree so I would be very happy to take you under my wing and to teach you more tips and tricks, and how to become successful."
                    player "I would love that Emilie, thank you."
                    emilie "No thank you. Looks like I have to go now, goodbye.!!"
                    player "Goodbye!!"
                    
                "True friendship":
                    emilie "I agree so let us become good friends [player_name]. You know my complete story, now I want to learn more about yours."
                    player "Well my story is way less interesting, I just came here for my goals and before in my old city, I had a best friend named Sam, he shifted here at the end of school and I missed him alot, so it is nice seeing him again."
                    emilie "Yeah I understand, I felt the same way about Luca when he came here for the University of Arts, he came 2 years after me probably because of the whole 'not a real job' thing that broke his confidence, but I did not feel bad for him at all while he was still in Japan I just missed him as a brother, now I realize the error in my ways, thank you [player_name]. But looks like I have to go now, goodbye.!!"
                    player "Goodbye!!!"
    hide Emilie
    $ emilie_hangouts_completed = 2
    jump evening_ticks
label sibling_joint_hangout_3:
    scene bg restaurant with fade
    $ is_evening_consumed = True
    show Emilie mad at left
    show Luca disagree at right
    player "Hi Emilie and Luca, now let us calm down and have a nice chat to get all your feelings out."
    emilie "Ok thank you [player_name]. Luca I am sorry for telling you freelance is not a 'real job', I realized that it is a valid way of living, and I was just trying to protect you because of how risky it is."
    luca "Risky? Seriously, that just shows you never believed in me and my skill. But anyway I am sorry for always telling you to be so 'chill', I was just trying to help you calm down and reduce your stress."
    emilie "The problem was not what you meant or what you said it is the problem that you always told that whenever I am very happy, very sad,very angry and it felt like ignoring my emotions."
    show Luca provoke with fade
    luca "You ignored my skill, I ignored your 'emotions' wowww, great way of deflecting blame. Also btw I earn 7 million per year so I never wanted or needed grandpa's money, you telling me to take it since my job is not real is the whole reason I was so mad, I was anyway going to give you the money but you acting so smug and so much better than me really caused me to boil. And I am still mad since I still did not get an apology."
    emilie "Fine,fine 'sorry Luca, I am so sorry and your dear sister is always wrong and you are always right Luca.'Is that what you wanted me to say? HuH? It was a mistake talking to you again."
    show Luca disagree with fade
    player "Wait everyone calm down please. Let us have a calm discussion...."
    luca "Are you mocking me? You always do this when you are angry. Ugghhhhhh, please shut up."
    emilie "You want me to shut up, huh. I also earn 6 million a year and I agree I underestimated you but you still earn less than me probably, 7 million is probably your sales."
    luca "Actually 10 million is my sales, I have made a 70% profit margin using my skill and connection with my friends. You obviously are just a suck up to a corporate company."
    emilie "Absolutely absurd, I should never have come here, I am leaving. I am sorry [player_name] I know how hard it was to convince my idiot brother to come here. Goodbye. [player_name] and I hope I never see you again Luca."
    
    luca "You think I am absurd..."
    emilie "Yes I do."
    luca "I also should not have come here. I can never trust my overbearing sister, I am sorry [player_name] but this was a mistake. Ciao [player_name] and I hope I never see you too Emilie"
    
    "Both of them ran out of the door, you were left alone in the restaurant and decided to leave."
    hide Luca
    hide Emilie
    $ sibling_collision_failed = True
    jump evening_ticks
label sibling_affinity_phase_1_double_header:
    "You skip work and arrive to the restaurant, you see just Emilie there."
    show Emilie default
    
    if current_tier in ["Educator","Analyst", "Researcher"]:
        $ job_strike_counter += 1
        "Because you skipped your scheduled shift to resolve this family emergency, you have automatically received 1 corporate strike."
        if job_strike_counter >= get_max_strikes():
            call job_termination_logic(True)

    player "So Emilie, why did you storm out? What exactly happened and what do you want from Luca?"
    emilie "I stormed out because of his smug attitude and his annoying personality. I was angry that he completely ignored my feelings and just talked about his own things, he literally only cared about himself and I gave him an apology and he refused to accept it."
    player "Do you think you could have done anything better?"
    emilie "NO NOT AT ALL. I did my best to talk to him and he messed it up."
    player "But Emilie just think, he has a lot of skill and charisma and it felt like you were ignoring him. I am not denying the fact that he also made mistakes then but you must accept you did too."
    emilie "No he doesn't he was just bragging. He earns way less than me. He is way less valuable than me."
    player "It looks like you are in denial, and that is fine come let us go."

    # ENFORCES DYNAMIC WALLET COST PROTECTION CHECK
    if current_cash > 0:
        $ spent_cash = min(25.00, current_cash)
        $ current_cash -= spent_cash
        "You spent [spent_cash] dollars on the outing loop."

    "After you spent some time out, you came back to the restaurant and Emilie seemed way more calm and relaxed. Also the food you ordered arrived."

    emilie "Hm that was something, and I have been thinking about the disaster of a conversation we had and I realized I have been in denial. He is equally skilled as me and he is a very good painter. But it is too late, he must hate me."
    player "Do not worry Emilie, I will convince Luca to do a do-over but this time pls remain calm and collected."
    emilie "I agree, I miss him so much. Ok time to eat."
    
    "You both ate everything on the table in 10 minutes flat. It tasted amazing."
    player "Wow I really liked the food, I just can't believe how good the food is and it never gets boring."
    emilie "That is why it is my favourite restaurant."
    
    emilie "Regardless, since you are my student and I am your mentor here are few more tips. Always be focused on your goals, never give up and always be as kind but stern as possible."
    player "Thank you for your tips. I really appreciate it."
    emilie "Good job, but looks like it is time for that meeting."
    
    player "So, goodbye!"
    emilie "Goodbye., until we meet again."
    
    $ stat_charisma += scaled_gain("charisma", 15, growth_charisma)
    hide Emilie
    jump luca_afternoon_affinity_intercept

label luca_afternoon_affinity_intercept:
    show Luca smilie2
    "Emilie left the restaurant and 10 minutes later Luca walks in."
    
    player "Hi Luca! I have already ordered some food for you so let us focus on what happened in that disastrous conversation."
    luca "I have been thinking about that the whole time from then, and I really need a do-over, I escalated and completely ignored Emilie and her feelings and I feel like I easily could have improved that conversation. She just irritated me so much and her 'real' apology at the start felt extremely fake. But I accept I made mistakes too."
    player "I have already planned a do-over for both of you, and Emilie agrees that you both really need it. So, enough about that."
    luca "I concur."
    show Luca smile

    menu:
        "Talk about jobs and tips":
            luca "Since you are passionate like me, here are some tips -> Always follow your dream, do not over work yourself, work smart, and use your connections like me."
            
            if current_tier == "Freelance":
                luca "Since you already are a freelancer, I will do a free advertisement for you and that will 100% boost your revenue by 50%."
                $ freelance_revenue_multiplier = 1.5
                "Luca launched a global ad campaign for your services! Freelance payout multiplier is now 1.5x."
            else:
                luca "If you ever become a freelancer, just contact me and I will do a free advert for you and that will boost your revenue by 50%."
                $ freelance_revenue_multiplier = 1.5
                
            "While you were talking, the food arrived."
            luca "Enough of talking about jobs and business, let us feast."
            "You both finish your food very quickly since it was so good."
            
            luca "The food was absolutely amazing, I did not think I could like food that I have basically every day."
            player "I agree. With both of you, I have come here so many times. But this food, it never gets old."
            luca "Anyway I just hope the Emilie meeting goes good though, unlike last time. I will make sure to keep my cool."
            
            "You spent 25 dollars on your tab for all the food you had over the last few days that you forgot to pay."
            
            if luca_intro_generosity_chosen:
                luca "I must repay you for your kindness earlier so here is the full 25 dollar pls 25 extra."
                $ current_cash += 50.00
            else:
                luca "I must repay you for your efforts to reunite me and Emilie so here is 25 dollars."
                $ current_cash += 25.00
                
            player "Thank you so much, you and Emilie really are the best friends I can ask for."
            luca "I still really hope it goes well. Now looks like I have to finish another one of my projects, ciao!"
            player "Goodbye!"

        "Chill and go out":
            luca "Anyway since you are my friend, want to chill and go out."
            player "Yeah sure, let us take a walk and just have fun and relax. I will also cancel the order."
            luca "Yeah sure, I am not really hungry."
            
            "You both go out and just have fun. You pay 25 dollars."
            
            if luca_intro_generosity_chosen:
                luca "I must repay you for your kindness earlier so here is the full 25 dollar pls 25 extra."
                $ current_cash += 50.00
            else:
                luca "I must repay you for your efforts to reunite me and Emilie so here is 25 dollars."
                $ current_cash += 25.00
                
            player "Thank you so much, you and Emilie really are the best friends I can ask for."
            luca "I hope the do-over goes good,anyway I have to finish a job now so ciao!"
            player "Goodbye!"

    $ affinity_phase_1_cleared = True
    $ stat_charisma += scaled_gain("charisma", 15, growth_charisma)
    jump afternoon_phase

label luca_casual_hangout_1:
    show Luca smile
    scene bg cafe_interior with fade
    $ is_evening_consumed = True
    
    luca "Hey! Glad you could make it. I love this Japanese restaurant—I eat here basically every day. So, what's on your mind while we wait for the food?"

    menu luca_hangout_1_choices:
        "Talk about his past.":
            player "I am wondering about your backstory - how you came here, and how you became so successful."
            luca "Well umm, I came from Japan to go to the University of Arts here which is the top university of arts in the world. It is an amazing city, and it would be better if my belligerent twin sister Emilie wasn't here."
            luca "She just continues about how freelancing is not a 'real job' and offering services and my works to people will not 'earn money' and she is just so irritating."
            luca "Recently we had a whole fight because our grandparents passed away and they gave 50% of the inheritance to our parents and 50% for us to share."
            luca "She told me that since I don't have a real job and that I barely earn money (Even though I earned and still earn more than her at that time which I did not mention) to take her money since she is well-off, well ofcourse I refused and offered her my money instead which I was anyway going to do because I had too much and I still have too much money."
            luca "I can afford like 3 mansions and 2 Porsches with my liquid money but I do my job for fun rather than money. So that is why we are like this. She thinks just because she got a director job in her company my job is worthless."
            
            if emilie_unlocked:
                player "Woww. I knew that there would be more to it than Emilie told, and I am so sorry about your grandparents."
            else:
                player "Woww, that's crazy. I am so sorry about your grandparents, and she does sound really annoying."
                
            luca "She is, anyway after passing university, I called my coder friend who set up a website for me (inexchange I gave him 5% royalties for like server management and gratitude so he is rich now too) and then after my advertising and using my connections to advertise, in 1 year I made 2 million in sales, and then it just took off, I got orders for months but I created a slot system with the coder friend and we still earn about 10million per year and we get a lot of high end clients and my workload is not that much."
            player "WOWWW!!! That is so good, how profitable is it may I ask?"
            luca "Very profitable, about 70% of that goes directly to me, 10% for supplies, 10% for that friend (I upped his pay) and 10% for taxes."
            player "So you earn about 7 million a year, that is crazy amount, and since you dont spend that much as I see you basically are a multimillionaire."
            luca "Yes I am, that is why I did not want the money (about 50k for me and 50k for emilie) since I have way more than her."
            luca "So yeah, that is my story. And just in time for the food."
            
            "You and Luca ate all of the dishes and enjoyed them a lot."
            luca "Wow that was amazing, I cannot believe that I can underestimate how good that was everytime."
            player "I agree, it really was amazing."

        "Go out and explore the city for 15 minutes.":
            "You both go on a walk and head on over to the park, there you both just chilled and talked about your hobbies for sometime, bought some lemonade that Luca paid for and started your walk back. You both reached the restaurant with 2 minutes left for the food to come."
            luca "Wow that felt so good, I cannot believe it was only 13 minutes."
            player "Me too... That was such a relaxing time."
            luca "Anyway I want to talk to you about something and let my anger about something out."
            
            if emilie_unlocked:
                player "Let me guess, you want to talk about Emilie."
                luca "Yeah, Emilie and what she did to me."
            else:
                player "What do you want to talk about?"
                luca "My sister Emilie, and what she did to me."
                
            luca "She was my main hurdle, she continuously said that 'freelance and passion projects are not real jobs', that concept is so irritating, and recently my grandparents died and we got some inheritance right, she offered to give her money to me which would have been a nice gesture and I was going to do the same anyway but her reason was since I was working in freelance and probably only earned very small amounts. It made me really angry and we got into a fight. I always used to tell her to cool off and chill also about work and studies which made her angry even though I was just trying to help her. Uggh.. anyway let us move on about that now and talk about something else while we wait for the food."
            player "I am so sorry about your grandparents and your fight with Emilie. So, how about we talk about the new game that came out like a month ago. It is really fun."
            luca "I agree, it is really fun but it is not that new also. I love rpg's.... Oh looks like the food is here, great."
            
            "You and luca ate the food and enjoyed it alot."
            luca "Wow that was amazing, I cannot believe that I can underestimate how good that was everytime."
            player "I agree, it really was amazing."

    # UNIFIED OUTRO BLOCK
    luca "It also reminds me of the times me and my sister would come here and eat a lot, I really miss those times before she got so focused on her studies and never had any chill. [player_name], can you please help me by making her chill, and stop focusing so much about her job and accepting freelance is real? Here is her number"
    player "Sure I will help you."
    luca "Ok then, let us head back home. Ciao!"
    player "Ok goodbye!"
    
    $ luca_hangouts_completed = 1
    if not emilie_unlocked:
        $ second_sibling_day = active_day + 1
    $ stat_charisma += scaled_gain("charisma", 8, growth_charisma)
    hide Luca
    jump evening_ticks
label emilie_casual_hangout_1:
    scene bg restaurant with fade
    show Emilie default
    $ is_evening_consumed = True
    
    player "Hi Ms. Emilie. How are you?"
    emilie "You do not have to call me miss, Emilie is fine. I am good. Regardless, what would you like to eat?"
    player "Everything is going fine..."
    player "This restaurant has so complicated menu names and everything is japanese, I guess I should have known that since it is a japanese restaurant."
    emilie "Ha, you know you can use the qr code on the table to get the english menu right?"
    player "Yeah I definitely 100% knew that..."
    player "I think I will order one tonkotsu ramen for me. What about you? Also what do you want as appetizer? Because I think I want some gyoza."
    emilie "Yeah I would love gyoza and I would love some sashimi and rolls please."
    player "Ok sure. I will place the order on the website the qr code pointed to since I am way too lazy to call a waiter."
    emilie "Ha. So like what do you want to talk about."

    menu emilie_hangout_1_branch_select:
        "Ask her about her backstory":
            # Dynamic corporate text swaps evaluation block
            if current_tier in ["Analyst", "Researcher"]:
                player "I want to know more about your past Emilie, and how you rose this far in our company."
            else:
                player "I want to know more about your past Emilie, and how you rose this far in your company."
                
            emilie "Oh ok, so I am actually from Japan. I came here to join the prestigious university in this town, it is an amazing town. It would be more amazing if Luca was not there."
            player "Who is Luca?"
            emilie "Luca is my irritating twin brother who always 'goes with the flow' and never works too hard. He always tells me to 'chill' and it is so irritating. We recently got into a huge fight after our grandparents passed away on who keeps their money."
            emilie "They just put on their will that my parents will get a 25% cut each and we will get the rest, and I wanted to give all the remaining 50% to him since he did not yet have a job and I was well off after I got promoted, but he said that he does not want the money and we got into a huge fight."
            player "I am so sorry about your grandparents, and he sounds irritating, like who won't take the free money, especially since it is coming from your grandparents as a gift"
            emilie "Yes he is very irritating and always irritated me when I lived with him. Let me continue with the story. So I came here for university and finished it with straight A's, then I applied for the job..."
            
            if current_tier in ["Analyst", "Researcher"]:
                emilie "...the job you are currently in and I just worked hard and got to the place I am today."
            else:
                emilie "...the job you were in and I just worked hard and got to the place I am today."
                
            player "Wow that certainly is an amazing story. It really inspires me."
            
            # --- TERMINATION/JOBLESS FINANCES MATRIX ---
            if current_tier in ["Unemployed", "Educator", "Freelance", "Entrepreneur"]:
                emilie "Regardless, I heard you recently left/was terminated from the company. Are you ok, do you need any financial help."
                menu emilie_loan_lifeline:
                    "Yes: Borrow cash":
                        player "Yeah, finances are tight, so could I please borrow some money."
                        emilie "Yeah sure, here is 50 dollars. But don't make this a habit and from next time you will have to pay me back."
                        $ current_cash += 50.00
                    "No: Decline help":
                        player "No, I am fine. But thanks anyway."
            $ emilie_main_choice = "A"

        "Ask her for tips about work":
            player "I wanted to ask you for tips about work."
            emilie "In any profession, you must have intellect, focus and most importantly interest or passion for that profession. Intellect lets you do things easier, focus or stamina lets you figure out things in less time and most importantly interest or passion keeps you going, trains you and gives you focus."
            emilie "Even if you are not that smart or dont have too much focus, you can do anything and everything if you have enough interest and passion for that thing. Like for example I had interest in economics even though I was not too smart or too good in anything but now I am a managing director in one of the biggest companies in the world. So try to be passionate about your job and work hard and eventually you will be the best."
            player "Thank you so much for your tip. I will definitely work on this."
            
            # Dynamic class based response parameters
            if current_tier == "Analyst":
                emilie "Since you are an analyst, I recommend going to the gym since it helps boost your stamina. And also I know you must be thinking why to go to the gym and how it helps but trust it does help with your health and stamina. Also good on you for sticking to the company, and if you were ever to quit don't go to freelance, it is only for the lazy people who don't want to work hard in a real job."
            elif current_tier == "Researcher":
                emilie "Since you are a researcher, I recommend taking courses and phone study to learn more so you can boost your intellect, also I recommend to take breaks from time to time to reduce stress since being a researcher is very stressful. Also good on you for sticking to the company, and if you were ever to quit don't go to freelance, it is only for the lazy people who don't want to work hard in a real job."
            elif current_tier == "Educator":
                emilie "Since you are an educator now, I recommend to follow your instincts and try your best, and be passionate about it, and if you dont feel any passion in it just switch over to an analyst/researcher or even start your own business, it really helps. But I recommend not to do freelance for a long time since it is just for people who are too lazy to actually work."
            elif current_tier == "Entrepreneur":
                emilie "Since you have started your own business, I recommend to not work too hard and to try to be calm and collected, and a business earns a lot of money if you manage it right so good luck. And good on you for not going to the easy option of 'freelance'. It is just for the lazy of this world."
            elif current_tier == "Unemployed":
                emilie "And do not worry if you currently do not have a job, I know you can get one eventually or start your own business and become successful. But I recommend not to do freelance for a long time since it is just for people who are too lazy to actually work."
            elif current_tier == "Freelance":
                emilie "Since you are a 'freelancer', I recommend getting a real job or starting your own business, freelance is for people who just are too lazy. So if you actually want to become successful get a business."
            $ emilie_main_choice = "B"

    "After your chat, the food came and you and Emilie ate everything. Both of you enjoyed the food a lot."
    emilie "Hm, I forgot how good their food was. What do you want to do?"
    player "Yeah their food was amazing. So, I want to go somewhere...."

    menu emilie_hangout_1_outings:
        "Go to the park to relax":
            $ emilie_hangout_1_mood = "relaxation"
            "You both took a walk to the park and sat there, you and her talked about the food at the restaurant, about work and office life and many other things. After some time, you both decide to go around the city."
            if current_cash > 0:
                $ spent_cash = max(0.00, min(15.00, current_cash))
                $ current_cash -= spent_cash
                if spent_cash > 0:
                    "You spent [spent_cash] dollars."
                    
            emilie "Hm that was something. We should do that again."
            player "I agree."
            
        "Go to the mall to have fun":
            $ emilie_hangout_1_mood = "fun"
            "You both go to the mall and do a full shopping spree and some window shopping. After you both took some snacks and rested for some time and talked about work and office life. Then you went back to exploring the mall."
            if current_cash > 0:
                $ spent_cash = max(0.00, min(15.00, current_cash))
                $ current_cash -= spent_cash
                if spent_cash > 0:
                    "You spent a total of [spent_cash] dollars."
                    
            emilie "Hm that was something. We should do that again."
            player "I agree."
            
    if emilie_main_choice == "A":
        emilie "It reminded me of the times with my brother Luca where we used to hangout and talk and play. But now we are in this whole grandparent situation, and he became a 'freelancer' and refuses to get a real job. It is so frustrating"
    else:
        emilie "It reminded me of the times with my twin brother Luca where we used to hangout and talk and play. But then he became a 'freelancer' and refused to get a real job and a whole situation about our grandparents occured."
    # UNIFIED SYSTEM CLOSING HOOKS
    if not luca_unlocked: 
        emilie "[player_name], can you help me by talking to my brother, here is his phone number. I miss him but he is just so annoying in my opinion. Talk some sense in him and make him accept the money and get a real job."
    else:
        emilie "[player_name], you already know my brother so can you talk to him please. I miss him but he is just so annoying in my opinion. Talk some sense in him and make him accept the money and get a real job."
    player "Sure I will talk to him."
    
    $ emilie_hangouts_completed = 1
    if not luca_unlocked:
        $ second_sibling_day = active_day + 1
    hide Emilie
    $ luca_unlocked = True
    $ stat_charisma += scaled_gain("charisma", 8, growth_charisma)
    jump evening_ticks

label luca_day_6_introduction:
    scene bg apartment_morning with fade
    
    "After coming back to your house, you hear a knock on your door, you open the door and find a man holding a basket with food, a lot of necessities and 100 dollars."
    "The 100 dollars in the basket covers your rent, food and basic necessities for today."
    show Luca smile
    $ current_cash += 100.00
    
    luca "Hi I am Luca, I see that you are my new neighbour and I thought to arrange for you this care basket."
    player "Thank you so much for this basket, it really helps. Come inside."
    luca "Thanks. So what brings you to town?"

    menu luca_intro_focus_architecture:
        "Say you came to explore your passions":
            player "I came here to explore my passions, and if it goes well maybe even become rich who knows?"
            luca "Haha, I also came here 6 years ago to find my passion and I found that I really loved painting and became a freelancer and sold my paintings, and that is how I could afford the basket with no difficulty. So just stay passionate and enjoy doing your passions and you will succeed."
            player "Wow, I feel more motivated by your story. Thank you so much for everything."
            
            menu luca_path_a_outing:
                "Go to the mall to have some fun.":
                    "You both go to the mall and go shop for art supplies for Luca, tools for you, and go enjoy in their arcade. It was really fun. You spent 15 dollars. You both come back to your apartment."
                    if current_cash >= 15.00:
                        $ current_cash -= 15.00
                    jump label_luca_path_a_climax_ledger
                    
                "Go to the park to relax":
                    "You both go to the park to relax and just talk some more, Luca explains more about his business and you both get some snacks and just relax and talk. And then you both just walk around and explore the city. You spent 15 dollars. Both of you head back to your apartment."
                    if current_cash >= 15.00:
                        $ current_cash -= 15.00
                    jump label_luca_path_a_climax_ledger

        "Say you came to make friends and find a partner":
            player "I came here to find some friends and maybe find a partner."
            luca "That's nice, I came here to find my passions."
            player "Thank you so much for your gift basket though. How do I repay you?"
            luca "Don't mention it, I have enough finances to afford a million of those baskets."
            player "I don't care if you are a millionaire or broke, how about I repay you with your favourite food at your favourite restaurant?"
            luca "You don't have to you know, but I would really like that but I am paying for half of it, I am not letting you pay for me."
            player "Then let us go."
            
            scene bg restaurant with fade
            "You and Luca go to a japanese restaurant and have a lot of sushi and 2 bowls of ramen each. You are about to pay when Luca swipes his credit card and gave the waiter a 5 dollar tip."
            player "Bro I was going to pay, why did you pay."
            luca "Since that was some amazing food and you took me here."
            player "The food was amazing I agree,..."

            menu luca_path_b_payment_routers:
                "Pay him back for the food ($15)" if current_cash >= 15.00:
                    player "but I cannot let you pay for it so here is 15 dollars to cover the bill."
                    luca "No I cannot possibly accept this."
                    player "I insist please take it."
                    luca "Fine if you insist. Thank you. I really am grateful, and I would love to be friends and stay in touch here is my number."
                    player "You are most certainly welcome and I would love to be friends with you here is my number too."
                    $ current_cash -= 15.00
                    $ luca_intro_generosity_chosen = True
                    jump label_luca_path_b_climax_intercept
                    
                "Thank him for paying":
                    player "and thank you so much for paying."
                    luca "No problem, you just taking me out here is enough for me to become friends with you, so let us stay in touch here is my number."
                    player "You are most certainly welcome and I would love to be friends with you here is my number too."
                    $ luca_intro_generosity_chosen = False
                    jump label_luca_path_b_climax_intercept

label label_luca_path_a_climax_ledger:
    luca "Wow that was fun. I would love to do it again. Anyway I saw that you spent 15 dollars for everything. So here is the same amount to cover the cost."
    menu luca_path_a_repayments:
        "No I refuse to accept this":
            player "No I refuse to accept this, it was my choice to spend it. So, just hanging out with you was good enough."
            $ luca_intro_generosity_chosen = False
        "Thank him for covering costs" if current_cash >= 0.00:
            player "What seriously? Thank you so much. Even though I planned to spend it on you, getting the money back is nice since finances are tight right now."
            $ current_cash += 15.00
            $ luca_intro_generosity_chosen = True
            
    if emilie_unlocked:
        player "Wait , I already have this number. Do you have a sister Emilie by chance?"
        luca "Yeah how do you know her name?"
        player "She is my boss, and my friend. She wanted to reconnect with you."
        luca "You must be pranking me, she was my main obstacle to fully explore my dream with her annoying 'It is not a real job' talk, that killed my confidence and made me almost give up my dream. I do not believe that she said that, so I would like not to talk about her now."
        player "It is okay, and I am sorry for bringing her up."
        luca "Anyway, I will get out of your hair. Ciao!"
        player "Goodbye, hope to hangout soon."
        $ luca_unlocked = True
        jump label_luca_intro_exit_block
    else:
        luca "Ok then, let us stay in touch, I would love to hangout again with another passionate person which is rare in this city."
        player "Yeah sure I would love to hangout, here is my number."
        luca "Here is mine, anyway I will get out of your hair. Ciao!"
        player "Goodbye, hope to hangout soon."
        $ luca_unlocked = True
        jump label_luca_intro_exit_block

label label_luca_path_b_climax_intercept:
    if emilie_unlocked:
        player "Wait , I already have this number. Do you have a sister Emilie by chance?"
        luca "Yeah how did you know?"
        player "She is my boss, and she is my friend. She wanted to reconnect with you."
        luca "You must be pranking me, she was my main blockage to fully explore my dream with her annoying 'It is not a real job' talk, I do not believe that she said that, so I would like not to talk about her now."
        player "It is okay, and I am sorry for bringing her up."
        luca "Thanks again, ciao!"
        player "Goodbye!"
        $ luca_unlocked = True
        jump label_luca_intro_exit_block
    else:
        luca "Thanks again, ciao!"
        player "Goodbye!"
        
        $ luca_unlocked = True
        jump label_luca_intro_exit_block

label label_luca_intro_exit_block:
    hide Luca
    "You head back home."
    $ stat_charisma += scaled_gain("charisma", 3, growth_charisma)
    # Corrected: Does NOT consume evening block parameters, course modules immediately trigger next
    jump evening_phase

label emilie_after_luca_meeting:
    show Emilie worry2
    if current_tier == "Unemployed":
        "You went out for some groceries and while walking back home you suddenly bump into someone on the way. She drops all her papers and you slip and fall"
    else:
        "You were walking back home when you suddenly bump into someone on the way. She drops all her papers and you slip and fall."
    show Emilie default with fade
    emilie "I am so sorry, I was so focused on going back to work after my break. Regardless, my name is Emilie, you look like you are new to town, what is your name?"
    player "My name is [player_name], and I am sorry too. Let me help you by picking up these papers."
    "Emilie helps you up and you help get her all her papers."
    emilie "Thank you. You seem like a nice person, can we be friends? Here is my number."
    player "Yeah sure, we can be friends. Wait, I recognize this number, do you have a brother Luca by chance?"
    emilie "Yes, how do you know my annoying brother's name?"
    player "Luca is my neighbour and friend, he wanted to reconnect with you."
    emilie "What? No way, he is so stupid and lazy. I would never want to reconnect with him."
    player "Fine, I will not talk about it anymore but can we still be friends?"
    emilie "Yeah sure, ok looks like I am little late, goodbye."
    player"Bye!"
    $ emilie_unlocked = True
    hide Emilie
    jump evening_phase

# ---------------------------------------------------------
# SIBLING MESSAGING (from Do Something -> Text Emilie / Text Luca)
# ---------------------------------------------------------
label emilie_phone_hangout_scheduling_action:
    if meetup_booked():
        "You already have plans for tomorrow evening."
        jump label_do_something_hub
    if affinity_phase_1_cleared:
        jump sibling_affinity_phase_2
    if sibling_collision_failed:
        jump sibling_aftermath_scheduling_action
    if emilie_hangouts_completed >= 2 and luca_hangouts_completed >= 2:
        jump sibling_group_scheduling_action
    if emilie_hangouts_completed > luca_hangouts_completed:
        emilie "Sorry, my workload is crazy right now. I will text you when I am free."
        jump label_do_something_hub
    player "Hi Emilie, you want to meet soon."
    emilie "Sure, I will make a reservation for the Japanese restaurant down the street for tomorrow evening."
    player "Sure, see you then."
    $ sibling_meetup_tomorrow = "emilie"
    jump label_do_something_hub

label luca_phone_hangout_scheduling_action:
    if meetup_booked():
        "You already have plans for tomorrow evening."
        jump label_do_something_hub
    if affinity_phase_1_cleared:
        jump sibling_affinity_phase_2
    if sibling_collision_failed:
        jump sibling_aftermath_scheduling_action
    if emilie_hangouts_completed >= 2 and luca_hangouts_completed >= 2:
        jump sibling_group_scheduling_action
    if luca_hangouts_completed > emilie_hangouts_completed:
        luca "Sorry, I am in the middle of a big project right now. I will text you when I am free."
        jump label_do_something_hub
    player "Hi Luca, you want to hangout?"
    if luca_hangouts_completed == 0:
        luca "Yeah sure, come to the Japanese restaurant tomorrow evening."
        player "Sure, see you then."
    else:
        luca "Yeah sure, come to the Japanese restaurant again tomorrow evening, I am craving sushi again."
        player "Sure, see you then and I am excited for the amazing food."
    $ sibling_meetup_tomorrow = "luca"
    jump label_do_something_hub

label sibling_group_scheduling_action:
    # WIP: placeholder group message for hangout 3, not written by you yet
    player "Hi Emilie and Luca, can we all meet at the Japanese restaurant tomorrow evening?"
    emilie "Sure, I will be there."
    luca "Fine, I will come too."
    player "Great, see you both tomorrow."
    $ sibling_meetup_tomorrow = "joint"
    jump label_do_something_hub

# ---------------------------------------------------------
# WIP PLACEHOLDER LABELS
# ---------------------------------------------------------
label luca_casual_hangout_2:
    scene bg restaurant with fade
    show Luca smilie
    $ is_evening_consumed = True

    luca "Hey [player_name]! I am craving sushi so badly today, I could not even focus on my painting."
    player "Haha, same, I have been thinking about the food since you texted me. Let us order, I will use the QR code on the table."
    luca "Haha, look at you, you actually know about the QR code now. I am proud of you."

    "You and Luca order a lot of sushi and two bowls of ramen each. The website says it will take 30 minutes due to rush hour."
    luca "30 minutes? Then let us go for a walk, I need to clear my head anyway."
    "You both walk around the city and end up at the park. Luca sketches the pond on a napkin while you rest on a bench and get some snacks."

    if current_cash > 0:
        $ spent_cash = min(25.00, current_cash)
        $ current_cash -= spent_cash
        "You spent [spent_cash] dollars."

    "After some time, you both went back to the restaurant and the food was due to come in 5 minutes."
    luca "Wow that was exactly what I needed, thank you so much."
    player "It is fine. So, different thing, I met Emilie and she told me her side of the story. Trust me, the whole situation is just a big misunderstanding."
    luca "Wowww, you actually did it. Let me guess, she told you again that freelance is not a 'real job'."
    player "Nope, she said she did some research and realized that some freelancers earn a lot. She was just scared because it is risky. Also she misses you."
    luca "She said that? Hmm, that is not the Emilie I remember. Fine, maybe I also made it worse, I kept telling her to 'chill' even when she was actually upset."
    player "Exactly! How about you tell her yourself, I am planning a meeting between you two so you can share your feelings and let go of this feud."
    luca "I concur, if you think it is the right call then I am in. Anyway looks like the food came."

    "You both ate everything on the table and really enjoyed the food."
    luca "Wow, I feel so much better now. Hanging out with you makes my day way more fun."
    luca "Thank you [player_name]."

    menu luca_hangout_2_splits:
        "Ask him to teach you about his work":
            player "Luca, you are really good at what you do. Could you teach me some of it, like tips about passion projects and freelancing?"
            luca "Of course! Honestly nobody ever asks about my work and actually means it. First tip, put your work out there before you feel ready, and never underprice yourself."
            player "Thank you so much Luca, I will remember that."
            luca "No thank you. Anyway I have a project due, so I have to go now, ciao!"
            player "Goodbye!"

        "Tell him about your own story":
            player "Well my story is way less interesting, I just came here for my goals and before in my old city I had a best friend named Sam. He moved here at the end of school and I missed him a lot."
            luca "Yeah I understand, I felt the same when Emilie left for university before me. I was angry at her, but mostly I just missed her. Anyway, thanks for listening, I really needed that."
            player "Anytime. That is what friends are for."
            luca "Haha, true. Anyway I have a project due, so I have to go now, ciao!"
            player "Goodbye!"

    $ luca_hangouts_completed = 2
    $ stat_charisma += scaled_gain("charisma", 8, growth_charisma)
    hide Luca
    jump evening_ticks

label micro_burnout_wip:
    "WIP: Micro-Burnout (80% stress) locks social and romance growth."
    jump evening_dashboard_loop

label rock_bottom_wip:
    "WIP: Rock Bottom (100% stress) locks work for 3 days and forces therapist sessions."
    jump evening_dashboard_loop

label therapist_session_wip:
    "WIP: Therapist session. Running out of cash here is the hard Game Over."
    jump evening_dashboard_loop

label dating_app_wip:
    "WIP: Dating app."
    jump evening_dashboard_loop

# ---------------------------------------------------------
# AFTERMATH MESSAGE (after the disastrous joint meeting). Emilie and Luca are merged here.
# ---------------------------------------------------------
label sibling_aftermath_scheduling_action:
    "You message Emilie and Luca so you can try to go over the aftermath. You have decided to finish both of them on the same day so there may be a chance you can get them to talk calmly."
    player "Hi Emilie, I want to talk to you alone without Luca after the disastrous meeting."
    emilie "Yeah sure, come tomorrow to the Japanese restaurant but you have to skip work since I have a meeting at 6 o'clock due to international time zones."
    menu:
        "Agree to skip work":
            player "Yeah sure."
        "Say you cannot skip work":
            player "Sorry, I cannot skip work tomorrow."
            emilie "I understand. Text me when you are free."
            jump label_do_something_hub
    player "Hi Luca, I want to talk to you alone without Emilie after the disastrous meeting."
    luca "Yeah sure, come tomorrow to the Japanese restaurant but you have to come in the afternoon since I have taken an international client."
    player "Yeah sure."
    $ sibling_double_header_pending = True
    jump label_do_something_hub

# ---------------------------------------------------------
# SIBLING AFFINITY 2
# ---------------------------------------------------------
label sibling_affinity_phase_2:
    "WIP: Sibling Affinity 2 goes here."
    jump label_do_something_hub
