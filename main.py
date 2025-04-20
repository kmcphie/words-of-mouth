from get_news import get_news, get_news_text, scrape_news
from stocks import prepare_morning_content
from get_summary import get_summary
from get_ritual import get_ritual
from get_wise import get_wise
from generate_voice import generate_voice
import concurrent.futures
from elevenlabs import play

# We are going to put everything into a main function now
def run_pipeline(user_data=None):
    # Extracting the information from the user data
    name = user_data.get('name')
    pronouns = user_data.get('pronouns')
    reflection = user_data.get('reflection')
    age = user_data.get('age')
    timestamp = user_data.get('timestamp')

    # Extract nested morning routine info
    morning = user_data.get('morning', {})
    ritual = morning.get('ritual')
    reminders = morning.get('reminders')
    stocks = morning.get('stocks', '').split(',') if morning.get('stocks') else []
    stock_detail = morning.get('stock_detail')
    news = morning.get('news')
    news_detail = morning.get('news_detail')
    tone = morning.get('tone')
    wisdom = morning.get('wisdom')

    # Run news and stocks in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        stocks_future = executor.submit(lambda: prepare_morning_content(stocks))
        news_future = executor.submit(lambda: get_news_text(news))
        ritual_future = executor.submit(lambda: get_ritual(ritual))
        wise_future = executor.submit(lambda: get_wise(reflection, wisdom))

        news_result = news_future.result()
        stocks_result = stocks_future.result()
        ritual_result = ritual_future.result()
        wise_result = wise_future.result()
        
    # Combine the results
    # combined_text = f"{news_result}\n\n{stocks_result} \n\n {ritual_future.result()} \n\n {wise_future.result()}"
    # print(combined_text)
    # print("Stocks result:", stocks_result)
    # Generate summary
    print(news_result)
    summary = get_summary(news_result, name=name)
    # print(summary)
    full_text = summary + "\n\n" + stocks_result + "\n\n" + ritual_result + "\n\n" + wise_result

    # Generate voice
    audio_path = generate_voice(full_text, tone)
    play(audio_path)

    # return audio_path, summary

if __name__ == "__main__":
    audio, summary = run_pipeline()
    print("Summary:")
    print(summary)
    print(f"\nVoice file saved to: {audio}")
