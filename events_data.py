

GENDER_OPTIONS = [
    {"id": "male", "text": "Male"},
    {"id": "female", "text": "Female"},
]

FAMILY_OPTIONS = [
    {
        "id": "wealthy",
        "text": "Extremely wealthy family",
        "desc": "You grew up in luxury. Money was never a problem.",
        "effects": {"Wealth": 30, "Happiness": 10},
    },
    {
        "id": "middle",
        "text": "Middle-class family",
        "desc": "A normal, stable upbringing. Nothing fancy, nothing lacking.",
        "effects": {},
    },
    {
        "id": "poor",
        "text": "Poor household",
        "desc": "Life was a struggle. But hardship builds character.",
        "effects": {"Wealth": -30, "Intelligence": 10, "Health": 5},
    },
    {
        "id": "orphan",
        "text": "Orphan",
        "desc": "You grew up without parents. The world was your teacher.",
        "effects": {"Wealth": -20, "Happiness": -20, "Intelligence": 10, "Social": -10},
    },
]

APPEARANCE_OPTIONS = [
    {
        "id": "attractive",
        "text": "Very attractive",
        "desc": "People are naturally drawn to you.",
        "effects": {"Social": 15, "Happiness": 5},
    },
    {
        "id": "average",
        "text": "Average-looking",
        "desc": "Nothing stands out, but nothing holds you back.",
        "effects": {},
    },
    {
        "id": "below_avg",
        "text": "Below average",
        "desc": "Looks aren't everything. You learned to rely on other strengths.",
        "effects": {"Social": -10, "Intelligence": 5, "Happiness": -5},
    },
]

PERSONALITY_OPTIONS = [
    {
        "id": "outgoing",
        "text": "Outgoing",
        "desc": "You love being around people. Life of the party.",
        "effects": {"Social": 10, "Happiness": 5},
    },
    {
        "id": "introvert",
        "text": "Introvert",
        "desc": "You prefer solitude and deep thinking.",
        "effects": {"Intelligence": 10, "Social": -5},
    },
    {
        "id": "ambitious",
        "text": "Ambitious",
        "desc": "You always want more. Success drives you.",
        "effects": {"Intelligence": 10, "Wealth": 5},
    },
    {
        "id": "laidback",
        "text": "Laid-back",
        "desc": "You go with the flow. Stress is for other people.",
        "effects": {"Happiness": 10, "Intelligence": -5},
    },
]


def build_events(player):
    """Build event list based on player traits and history."""
    events = [
        # ── CHILDHOOD ──
        {
            "year": 3,
            "scene": "kindergarten",
            "text": "It's your first day of preschool. You immediately eat a crayon. It tastes like purple. The teacher sighs so hard she ages 5 years.",
            "choices": [
                {"text": "Eat another crayon to assert dominance", "effects": {"Health": -5, "Happiness": 10, "Social": 5}, "tag": "crayon_eater"},
                {"text": "Share your crayons with the kid crying in the corner", "effects": {"Social": 10, "Happiness": 5}, "tag": "crayon_sharer"},
                {"text": "Build a crayon fortress and declare yourself king", "effects": {"Intelligence": 5, "Happiness": 10}, "tag": "crayon_king"},
            ],
        },
        {
            "year": 6,
            "scene": "playground",
            "text": "An older kid steals your lunch money. You cry. The bully also cries. Everyone on the playground cries. A bird cries. It's a whole crying situation.",
            "choices": [
                {"text": "Fight back with a dramatic anime punch", "effects": {"Social": 10, "Health": -10, "Happiness": 5}, "tag": "anime_punch"},
                {"text": "Tell the teacher, who gives a 45-minute lecture on kindness", "effects": {"Intelligence": 5, "Happiness": -5}, "tag": "snitch"},
                {"text": "Befriend the bully by sharing your snack", "effects": {"Social": 15, "Happiness": 5}, "tag": "befriend_bully"},
            ],
        },
        {
            "year": 10,
            "scene": "school",
            "text": "Your school is holding a talent show. Your friend dares you to sign up. You can't sing, dance, or juggle. This is going to be great.",
            "choices": [
                {"text": "Perform a dramatic reading of your math textbook", "effects": {"Intelligence": 10, "Social": 5, "Happiness": 5}, "tag": "math_reading"},
                {"text": "Do a magic trick that goes horribly wrong", "effects": {"Social": 10, "Happiness": 10, "Intelligence": -5}, "tag": "bad_magic"},
                {"text": "Fake a stomachache and hide in the nurse's office", "effects": {"Happiness": -5, "Intelligence": 5}, "tag": "fake_sick"},
            ],
        },
        {
            "year": 13,
            "scene": "gym",
            "text": "A group of kids behind the gym offers you a cigarette. You take it. It's actually a stick of celery. They've been pranking people all week. You kind of respect the hustle.",
            "choices": [
                {"text": "Join their celery prank gang", "effects": {"Social": 15, "Happiness": 10, "Health": 5}, "tag": "celery_gang"},
                {"text": "Report them to the principal for celery-related crimes", "effects": {"Intelligence": 5, "Social": -10}, "tag": "celery_snitch"},
                {"text": "Eat the celery. It's a vegetable. You need the nutrients.", "effects": {"Health": 10, "Happiness": 5}, "tag": "eat_celery"},
            ],
        },
        {
            "year": 15,
            "scene": "school-crush",
            "text": "You spot your crush across the cafeteria. Your heart does a backflip. Your friend says they think the feeling is mutual. Your palms are sweaty. Mom's spaghetti.",
            "choices": [
                {"text": "Confess your love with a dramatic speech from a movie", "effects": {"Happiness": 15, "Social": 10, "Intelligence": -5}, "tag": "early_romance"},
                {"text": "Write them a love letter and accidentally give it to the teacher", "effects": {"Happiness": -10, "Social": -5, "Intelligence": 5}, "tag": "love_letter_fail"},
                {
                    "text": "Your crush says yes! You're now officially dating!",
                    "effects": {"Happiness": 25, "Social": 15, "Intelligence": -10},
                    "requires": {"Social": 70},
                    "tag": "crush_yes"
                },
                {
                    "text": "Your crush friendzones you. 'You're like a brother/sister to me.'",
                    "effects": {"Happiness": -15, "Social": -5},
                    "requires": {"Social": 40},
                    "tag": "friendzone"
                },
                {"text": "Keep it to yourself. Love is temporary. Homework is forever.", "effects": {"Intelligence": 10, "Happiness": -5}, "tag": "no_romance"},
            ],
        },
        {
            "year": 16,
            "scene": "street",
            "text": "Your friend offers to help you get a job at a local shop. The manager asks 'What's your greatest weakness?' You say 'Kryptonite.' You don't get the job.",
            "choices": [
                {"text": "Try again at a different shop. This time say 'perfectionism' like a normal person", "effects": {"Wealth": 15, "Intelligence": 5}, "tag": "part_time_job"},
                {"text": "Start a lemonade stand empire in your garage", "effects": {"Wealth": 10, "Intelligence": 10, "Happiness": 5}, "tag": "lemonade_stand"},
                {"text": "Spend the summer speedrunning video games", "effects": {"Happiness": 15, "Health": -5, "Wealth": -5}, "tag": "video_games"},
                {
                    "text": "Your dad's friend offers you a high-paying internship",
                    "effects": {"Wealth": 25, "Intelligence": 5},
                    "requires": {"Wealth": 70},
                    "tag": "nepotism"
                },
            ],
        },
    ]

    # ── CONSEQUENCE: ROMANCE AT 15 ──
    if player.has_history("early_romance") or player.has_history("crush_yes"):
        events.append({
            "year": 17,
            "scene": "prom",
            "text": "Your teacher found out about your relationship. She calls your parents. Your mom is more excited than angry. Your dad asks if they're 'the one.' This is so embarrassing.",
            "choices": [
                {"text": "Accept the lecture and cool things off", "effects": {"Intelligence": 10, "Happiness": -5}, "tag": "accept_scolding"},
                {"text": "Ignore them — love conquers all, including homework", "effects": {"Happiness": 5, "Intelligence": -10, "Social": 5}, "tag": "ignore_scolding"},
                {"text": "Break up via text. Like a coward. A modern coward.", "effects": {"Happiness": -15, "Social": -5}, "tag": "break_up"},
            ],
        })
    else:
        events.append({
            "year": 17,
            "scene": "prom",
            "text": "It's junior year. Everyone's talking about prom. You see couples everywhere. You're starting to wonder if you'll die alone with your cat. You don't even have a cat.",
            "choices": [
                {"text": "Ask your crush to prom with a flash mob that goes viral", "effects": {"Social": 15, "Happiness": 15}, "tag": "prom_flash_mob"},
                {"text": "Go with a group of friends and have the best night ever", "effects": {"Social": 10, "Happiness": 10}, "tag": "prom_friends"},
                {"text": "Skip prom and watch Netflix. No regrets. Okay, some regrets.", "effects": {"Intelligence": 5, "Happiness": -5}, "tag": "no_prom"},
            ],
        })

    # ── CONSEQUENCE: CELERY GANG ──
    if player.has_history("celery_gang"):
        events.append({
            "year": 17,
            "scene": "street",
            "text": "The celery gang has evolved. They now run an underground vegetable smuggling ring. They want you to be the getaway driver. You don't have a license.",
            "choices": [
                {"text": "Join them. Vegetables never hurt anyone. Except that one time.", "effects": {"Social": 10, "Happiness": 10, "Intelligence": -5}, "tag": "veggie_crime"},
                {"text": "Report them to the FDA. Yes, the actual FDA.", "effects": {"Intelligence": 10, "Social": -15}, "tag": "fda_snitch"},
            ],
        })

    # ── CONTINUE EVENTS ──
    events.extend([
        {
            "year": 18,
            "scene": "school",
            "text": "High school is over! You throw your cap in the air. It hits someone. They're not happy. But YOU'RE happy. Time for the next chapter.",
            "choices": [
                {"text": "Go to university and major in something useless like Philosophy", "effects": {"Intelligence": 20, "Wealth": -15, "Social": 10}, "tag": "university"},
                {"text": "Go to community college. It's basically the same thing but cheaper", "effects": {"Intelligence": 10, "Wealth": -5, "Happiness": 5}, "tag": "community_college"},
                {"text": "Skip college and start working. School is for nerds anyway", "effects": {"Wealth": 20, "Intelligence": -5, "Happiness": 5}, "tag": "work_immediately"},
                {
                    "text": "Your parents send you to an Ivy League school. Thanks, trust fund!",
                    "effects": {"Intelligence": 25, "Social": 15, "Wealth": -5},
                    "requires": {"Wealth": 80},
                    "tag": "ivy_league"
                },
            ],
        },
        {
            "year": 20,
            "scene": "party",
            "text": "It's Friday night. Your roommates drag you to a house party. You spend 3 hours talking to a cat in the corner. The cat is a better conversationalist than most humans.",
            "choices": [
                {"text": "Party hard! You wake up on a lawn. Whose lawn? Nobody knows.", "effects": {"Social": 15, "Happiness": 10, "Health": -10, "Intelligence": -5}, "tag": "party_hard"},
                {"text": "Stay in and study. Your GPA thanks you. Your social life doesn't.", "effects": {"Intelligence": 15, "Happiness": -5}, "tag": "study_hard"},
                {"text": "Go for a bit, make friends with the cat, then leave early", "effects": {"Social": 5, "Happiness": 10}, "tag": "cat_party"},
                {
                    "text": "You become the life of the party. Everyone knows your name!",
                    "effects": {"Social": 25, "Happiness": 15},
                    "requires": {"Social": 70},
                    "tag": "party_legend"
                },
            ],
        },
        {
            "year": 22,
            "scene": "office",
            "text": "You've graduated! Time to adult. Two job offers are on the table. One is at a startup that might change the world. The other is at a company that definitely won't but pays well.",
            "choices": [
                {"text": "Join the startup. Free snacks and existential dread!", "effects": {"Wealth": 10, "Happiness": -10, "Intelligence": 15}, "tag": "startup"},
                {"text": "Take the corporate job. Your soul leaves your body on day one.", "effects": {"Wealth": 20, "Happiness": -5, "Health": 5}, "tag": "corporate"},
                {"text": "Backpack across Europe and 'find yourself'", "effects": {"Happiness": 20, "Wealth": -20, "Social": 15}, "tag": "travel"},
                {
                    "text": "Ace the interview at Google. Your algorithm skills pay off!",
                    "effects": {"Wealth": 30, "Intelligence": 10, "Social": 5},
                    "requires": {"Intelligence": 80},
                    "tag": "google"
                },
                {
                    "text": "Your dad's friend hooks you up with a cushy office job",
                    "effects": {"Wealth": 25, "Happiness": 5},
                    "requires": {"Wealth": 70},
                    "tag": "nepotism_job"
                },
            ],
        },
        {
            "year": 25,
            "scene": "home",
            "text": "You've been dating someone for two years. They suggest moving in together. You're excited but also terrified. What if they discover your secret anime collection?",
            "choices": [
                {"text": "Move in together. Time to merge your Netflix accounts", "effects": {"Happiness": 15, "Social": 10, "Wealth": -5}, "tag": "move_in"},
                {"text": "You're not ready. Your anime collection needs its own room.", "effects": {"Happiness": -5, "Intelligence": 5}, "tag": "not_ready"},
                {"text": "Break up. You choose anime over love. A true weeb.", "effects": {"Happiness": -10, "Social": -5, "Intelligence": 5}, "tag": "break_up_25"},
                {
                    "text": "Your crush says they've always loved you. It's a fairy tale!",
                    "effects": {"Happiness": 25, "Social": 15},
                    "requires": {"Social": 70},
                    "tag": "fairy_tale_love"
                },
            ],
        },
        {
            "year": 30,
            "scene": "promotion",
            "text": "Your boss offers you a promotion. More money, but you'd work 80 hours a week. Your desk plant is already dead. Your social life is next.",
            "choices": [
                {"text": "Take the promotion. Sleep is for the weak!", "effects": {"Wealth": 25, "Happiness": -15, "Health": -10}, "tag": "promotion"},
                {"text": "Decline. Your desk plant needs you. And your sanity.", "effects": {"Happiness": 15, "Health": 10}, "tag": "decline_promotion"},
                {"text": "Negotiate: more money AND a nap pod in your office", "effects": {"Wealth": 10, "Happiness": 10, "Intelligence": 10}, "tag": "negotiate"},
                {
                    "text": "Your charisma wins the boss over. Corner office, baby!",
                    "effects": {"Wealth": 20, "Happiness": 10, "Social": 10},
                    "requires": {"Social": 70},
                    "tag": "charisma_promotion"
                },
            ],
        },
        {
            "year": 40,
            "scene": "midlife",
            "text": "You're turning 40. You buy a sports car. Your back hurts getting out of it. Your knees make sounds when you stand up. Welcome to your midlife crisis.",
            "choices": [
                {"text": "Quit your job and become a professional skydiver", "effects": {"Happiness": 20, "Wealth": -25, "Health": -5}, "tag": "skydiver"},
                {"text": "Buy a motorcycle. Your spouse is NOT happy.", "effects": {"Happiness": 10, "Health": -10, "Social": -5}, "tag": "motorcycle"},
                {"text": "Accept aging gracefully. Buy sensible shoes.", "effects": {"Wealth": 10, "Happiness": -5, "Health": 5}, "tag": "graceful_aging"},
                {
                    "text": "Start a tech company that actually succeeds!",
                    "effects": {"Wealth": 30, "Intelligence": 10, "Happiness": 5},
                    "requires": {"Intelligence": 80},
                    "tag": "tech_success"
                },
            ],
        },
        {
            "year": 50,
            "scene": "hospital",
            "text": "Your doctor says your health numbers aren't great. 'You need to exercise,' she says. You think about the stairs you avoided this morning. She knows. They always know.",
            "choices": [
                {"text": "Become a gym rat. You're the oldest person in the spin class.", "effects": {"Health": 25, "Happiness": 5, "Wealth": -5}, "tag": "gym_rat"},
                {"text": "Start walking 10,000 steps a day. Your Fitbit is so proud.", "effects": {"Health": 10, "Happiness": 5}, "tag": "walking"},
                {"text": "Ignore the doctor. You've survived this long on pizza and coffee.", "effects": {"Health": -20, "Happiness": 5}, "tag": "ignore_doctor"},
            ],
        },
        {
            "year": 60,
            "scene": "retirement",
            "text": "You're retiring! Your coworkers throw you a party. The cake says 'Happy Retirement' but someone crossed out 'Retirement' and wrote 'Finally Leaving.' You'll miss them.",
            "choices": [
                {"text": "Travel the world. You've earned those Instagram photos.", "effects": {"Happiness": 20, "Social": 10, "Wealth": -15}, "tag": "retire_travel"},
                {"text": "Volunteer at a animal shelter. Puppies cure everything.", "effects": {"Happiness": 15, "Social": 15, "Health": 5}, "tag": "retire_volunteer"},
                {"text": "Become a professional couch potato. Netflix awaits.", "effects": {"Happiness": 10, "Health": -5}, "tag": "retire_relax"},
                {
                    "text": "Climb Mount Everest. Age is just a number!",
                    "effects": {"Health": 15, "Happiness": 20, "Social": 10},
                    "requires": {"Health": 70},
                    "tag": "everest"
                },
            ],
        },
        {
            "year": 70,
            "scene": "grandkids",
            "text": "Your kids have kids now. You're a grandparent. Your grandkids ask you to play Fortnite. You accidentally delete their save file. They don't talk to you for a week.",
            "choices": [
                {"text": "Spoil them rotten. Buy them everything. Revenge is sweet.", "effects": {"Happiness": 20, "Wealth": -15, "Social": 10}, "tag": "spoil_grandkids"},
                {"text": "Teach them life lessons. They roll their eyes. A lot.", "effects": {"Intelligence": 10, "Happiness": 10, "Social": 5}, "tag": "wise_grandparent"},
                {"text": "Learn Fortnite. You're now a gaming grandparent.", "effects": {"Happiness": 15, "Intelligence": 5, "Social": 5}, "tag": "gaming_grandparent"},
            ],
        },
        {
            "year": 80,
            "scene": "reflection",
            "text": "An old friend visits. 'If you could do it all over again, what would you change?' they ask. You think about the crayon incident. It all started there.",
            "choices": [
                {"text": "Nothing. Every mistake was a plot twist in my story.", "effects": {"Happiness": 20, "Intelligence": 5}, "tag": "no_regrets"},
                {"text": "I'd eat MORE crayons. Those were the days.", "effects": {"Happiness": 15, "Social": 5}, "tag": "more_crayons"},
                {"text": "I'd spend more time with the people I love.", "effects": {"Happiness": 15, "Social": 15}, "tag": "more_love"},
            ],
        },
        {
            "year": 90,
            "scene": "journalist",
            "text": "A young journalist wants to write your life story. 'So it all began with a crayon?' they ask. 'Yes,' you say. 'The best stories always start with something ridiculous.'",
            "choices": [
                {"text": "Share everything. Your story deserves to be told.", "effects": {"Social": 20, "Happiness": 15}, "tag": "share_story"},
                {"text": "Write your own memoir. Title: 'The Crayon Chronicles'", "effects": {"Intelligence": 15, "Happiness": 15}, "tag": "write_memoir"},
                {"text": "Keep it private. Some legends are better left untold.", "effects": {"Happiness": 10}, "tag": "keep_private"},
            ],
        },
        {
            "year": 100,
            "scene": "graveyard",
            "text": "You've lived a full century. Your family gathers around you. The room is filled with love. Someone whispers, 'Remember the crayon incident?' You smile. What a life.",
            "choices": [
                {"text": "Smile. It was a good life. A weird life. But a good one.", "effects": {"Happiness": 25}, "tag": "good_life"},
                {"text": "Whisper your final words: 'The crayons... they were delicious...'", "effects": {"Happiness": 20, "Social": 10}, "tag": "final_crayon"},
            ],
        },
    ])

    # ── TRAIT-BASED EXTRA CHOICES ──
    for event in events:
        if event["year"] == 16 and player.family == "wealthy":
            event["choices"].append({
                "text": "Why work? Your trust fund covers everything. Duh.",
                "effects": {"Wealth": 10, "Intelligence": -5}, "tag": "trust_fund"
            })
        if event["year"] == 22 and player.appearance == "attractive":
            event["choices"].append({
                "text": "Become an influencer. Your face is your resume.",
                "effects": {"Wealth": 20, "Social": 15, "Intelligence": -5}, "tag": "influencer"
            })
        if event["year"] == 25 and player.personality == "introvert":
            event["choices"].append({
                "text": "You prefer being alone. Adopt 7 cats instead.",
                "effects": {"Happiness": 15, "Social": -15}, "tag": "cat_lady"
            })

    return events