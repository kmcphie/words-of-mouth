from elevenlabs.client import ElevenLabs
from elevenlabs import play

# summary_text = """
# Books loved anyone who opened them, they gave you security and friendship and didn't ask for anything in return; they never went away, never, not even when you treated them badly. Love, truth, beauty, wisdom and consolation against death. Who had said that? Someone else who loved books."""

voices = {
    "casual": "iP95p4xoKVk53GoZ742B",        # Chris (casual, conversational)
    "professional": "onwK4e9ZLuTAKqWW03F9",   # Daniel (authoritative, news)
    "poetic": "XrExE9yKIg1WjnnlVkGX",         # Matilda (friendly narration)
}

def generate_voice(summary_text, tone="casual"):
    client = ElevenLabs(
    api_key="sk_6de134175805bd8b881d471294be8cdaf1f8db73e874faef"  # Replace with your actual API key
    )

    voice_id = voices.get(tone, voices[tone])

    audio = client.text_to_speech.convert(
        text=summary_text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    
    play(audio)

    return audio

# generate_voice(summary_text)