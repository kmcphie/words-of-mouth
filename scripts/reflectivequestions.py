import random
from datetime import datetime

class ReflectiveQuestionGenerator:
    def __init__(self):
        self.categories = {
            "gratitude": [
                "Think about one thing you're grateful for today.",
                "Reflect on someone who made your day better and why.",
                "Consider a small pleasure you enjoyed today.",
                "What's something you have that many others don't?",
                "Think about an opportunity you had today that you appreciate.",
                "Reflect on a challenge that taught you something valuable.",
                "Consider a relationship in your life you're thankful for.",
                "What aspect of your health are you grateful for today?",
                "Think about a moment of beauty you noticed today.",
                "Reflect on a tool or resource that made your day easier."
            ],
            "learning": [
                "What's one thing you learned today?",
                "Think about a mistake that taught you something.",
                "Reflect on advice you received recently that proved useful today.",
                "Consider a skill you improved slightly today.",
                "What's something you realized about yourself today?",
                "Think about something you'd like to learn more about based on today's experiences.",
                "Reflect on how you solved a problem today.",
                "Consider a perspective different from yours that you encountered today.",
                "What surprised you today?",
                "Think about how you might approach tomorrow differently based on today's experiences."
            ],
            "achievement": [
                "What's one thing that went better than expected today?",
                "Think about something you accomplished today, however small.",
                "Reflect on a moment you felt proud of yourself today.",
                "Consider a situation you handled well today.",
                "What's a small win you had today?",
                "Think about progress you made toward a goal today.",
                "Reflect on a time you showed strength today.",
                "Consider a moment when you helped someone else today.",
                "What difficulty did you overcome today?",
                "Think about something you did today that your past self would be proud of."
            ],
            "wellbeing": [
                "How did you take care of yourself today?",
                "Think about a moment when you felt at peace today.",
                "Reflect on what gave you energy today.",
                "Consider what drained your energy today.",
                "What boundaries did you maintain or need to set?",
                "Think about a moment you felt fully present today.",
                "Reflect on how your body feels right now.",
                "Consider one thing you could do tomorrow to support your wellbeing.",
                "What emotions were most present for you today?",
                "Think about a moment when you showed yourself compassion today."
            ],
            "values": [
                "How did you express one of your core values today?",
                "Think about a choice you made today that reflected what matters to you.",
                "Reflect on a moment when you stood up for something important.",
                "Consider how your actions aligned with your priorities today.",
                "What did you say 'no' to today to protect what matters most?",
                "Think about a situation where you compromised or didn't compromise your values.",
                "Reflect on how you might better align your actions with your values tomorrow.",
                "Consider what your actions today say about what's important to you.",
                "When did you feel most like yourself today?",
                "Think about a situation where you wish you had acted differently based on your values."
            ]
        }

        self.used_questions = set()
        self.category_rotation = list(self.categories.keys())
        self.category_index = 0
        self.last_day = None

        self.weekly_questions = [
            "Looking back on your week, what theme seems to emerge?",
            "What's something you'd like to do differently next week?",
            "Consider one way you've grown this week.",
            "Think about your biggest accomplishment this week.",
            "Reflect on someone who made your week better."
        ]

    def get_next_category(self):
        category = self.category_rotation[self.category_index]
        self.category_index = (self.category_index + 1) % len(self.category_rotation)
        return category

    def reset_if_needed(self, category):
        questions = self.categories[category]
        available = [q for q in questions if f"{category}:{q}" not in self.used_questions]
        if not available:
            for q in questions:
                self.used_questions.discard(f"{category}:{q}")

    def check_new_day(self):
        today = datetime.now().strftime('%Y-%m-%d')
        if self.last_day != today:
            self.last_day = today
            return True
        return False

    def is_weekly_reflection_time(self):
        return datetime.now().weekday() == 6  # Sunday

    def get_weekly_question(self):
        return random.choice(self.weekly_questions)

    def generate_question(self):
        if self.check_new_day() and self.is_weekly_reflection_time():
            return self.get_weekly_question()

        category = self.get_next_category()
        self.reset_if_needed(category)

        questions = self.categories[category]
        available = [q for q in questions if f"{category}:{q}" not in self.used_questions]
        if not available:
            return "No available questions at the moment."

        question = random.choice(available)
        self.used_questions.add(f"{category}:{question}")
        return question

    def add_custom_question(self, category, question):
        if category in self.categories:
            self.categories[category].append(question)
            return True
        return False

    def add_category(self, category_name, initial_questions=None):
        if category_name not in self.categories:
            self.categories[category_name] = initial_questions or []
            self.category_rotation.append(category_name)
            return True
        return False
