import anthropic
from generate_voice import generate_voice
from elevenlabs import play
import os

def get_summary(documents, name):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    print("THESE ARE THE DOCUMENTS: ", documents)
    context_category = "News documents and Stock documents"
    # documents = """"""
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=5000,
        temperature=0.5,
        # system="You are a world-class poet. Respond only with short poems.",
        system=f"You are curating a 1-min long summary of the following documents. ONLY GENERATE BASED ON THE CONTEXT. THIS IS THE CONTEXT: {documents}. Use the documents to make a 1 minute news summary of the documents in an easily digestible and informational way. Make it sound like you are basically reading off the news. Do so in an easy way to understand and in full-text.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Use the documents to make a 1 minute news summary of the documents in an easily digestible and informational way.
                        At the beginning of the text you are generating, say: "Hello there, {name}."
                        Make it sound like you are basically reading off the news. 
                        DO THIS BASED ON THE DOCUMENTS BELOW AND ONLY ON THE DOCUMENTS. 
                        These are documents: 
                        {documents}
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


# def main(documents):
#     summary_text = get_summary(documents)
# #     audio = generate_voice(summary_text)
# #     play(audio)    
# # tet = "HeLLO, can you plesae alksdjflakjdflaskdjf work!"
# # main(tet)
