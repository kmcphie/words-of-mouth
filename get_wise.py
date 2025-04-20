import anthropic
import os

def get_wise(reflection, wisdom):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    context_category = "advice seeking"
    # documents = """"""
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1000,
        temperature=1,
        system="You are a wise guidance counselor. Speak in rhymes or poetry if you can. You are helping someone with what is on their {context_category} by telling them a very brief story or quote that is relevant.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Briefly offer thoughts on the reflection below, 1-2 sentences or a quote max. Sound like you are being {wisdom}.
                        DO THIS BASED ON THE REFLECTION BELOW AND ONLY ON THE REFLECTION. 
                        This is the reflection: 
                        {reflection}
                        """
                    }
                ]
            }
        ]
    )
    # print(message.content)
    # print(type(message.content))
    # print(message.content[0].text) # This prints the text without anything else. 
    # print(type(message.content[0].text))
    return message.content[0].text # Returns a string with the summary of the documents. 

# get_wise("I am feeling sad today", "wise")