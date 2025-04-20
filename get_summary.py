import anthropic
from generate_voice import generate_voice
from elevenlabs import play

def get_summary(context_category, documents):
    client = anthropic.Anthropic()

    context_category = "Nature"
    documents = """"""
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
                        "Context":f"""
                        <documents>
                        <document>
                            <title>{context_category}</title>
                            <content>{documents}</content>
                        </document>
                        
                        """,
                        "type": "text",
                        "text": "Use the context to make a 2 minute reading summary of the documents in an easily digestible and informational way."
                    }
                ]
            }
        ]
    )
    # print(message.content)
    # print(type(message.content))
    print(message.content[0].text) # This prints the text without anything else. 

    return message.content[0].text # Returns a string with the summary of the documents. 

def main(context_category, documents):
    summary_text = get_summary(context_category, documents)
    audio = generate_voice(summary_text)
    play(audio)    