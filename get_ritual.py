import anthropic
import os

def get_ritual(ritual):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    context_category = "leading someone through a ritual"
    # documents = """"""
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1000,
        temperature=1,
        system="You are a spiritual guru (but NOT specific to a religion).",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Say one sentence pertaining to the request below.
                        DO THIS BASED ON THE RITUAL BELOW AND ONLY ON THE RITUAL. 
                        This is the request: 
                        {ritual}

                        Here are some example for each of the four possible requets (gratitude, learning, wellbeing, values)

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
                        """
                    }
                ]
            }
        ]
    )
    # print(message.content)
    # print(type(message.content))
    print(message.content[0].text) # This prints the text without anything else. 

    return message.content[0].text # Returns a string with the summary of the documents. 


def main(documents):
    summary_text = get_summary(documents)
#     audio = generate_voice(summary_text)
#     play(audio)    
# tet = "HeLLO, can you plesae alksdjflakjdflaskdjf work!"
# main(tet)
