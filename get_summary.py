import anthropic
from generate_voice import generate_voice
from elevenlabs import play
import os

def get_summary(documents):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    context_category = "News documents and Stock documents"
    # documents = """"""
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1000,
        temperature=1,
        # system="You are a world-class poet. Respond only with short poems.",
        system="You are curating a 2-min long summary of the following documents about {context_category}. Do so in an easy way to understand and in full-text.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Use the context to make a 2 minute reading summary of the documents in an easily digestible and informational way. 
                        <documents>
                        <document>
                            <title>{context_category}</title>
                            <content>{documents}</content>
                        </document>
                        
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
