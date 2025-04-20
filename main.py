from get_news import get_news, get_news_text, scrape_news
from stocks import prepare_morning_content
from get_summary import get_summary
from generate_voice import generate_voice
import concurrent.futures
from elevenlabs import play

# We are going to put everything into a main function now
def run_pipeline():
    # Run news and stocks in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        stocks_future = executor.submit(prepare_morning_content)

        news_future = executor.submit(get_news_text('business'))

        news_result = news_future.result()
        stocks_result = stocks_future.result()

    # Combine the results
    combined_text = f"{news_result}\n\n{stocks_result}"
    print(combined_text)
    print("Stocks result:", stocks_result)
    # Generate summary
    
    summary = get_summary(news_result)
    print(summary)
    full_text = summary + "\n\n" + stocks_result

    # Generate voice
    audio_path = generate_voice(full_text)
    play(audio_path)

    # return audio_path, summary

if __name__ == "__main__":
    audio, summary = run_pipeline()
    print("Summary:")
    print(summary)
    print(f"\nVoice file saved to: {audio}")
