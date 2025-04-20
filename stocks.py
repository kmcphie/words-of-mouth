import requests
import os
import anthropic

detail={
            "detail_level": "brief",
            "interests": "price and daily change",
            "tone": "casual"
        }

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# This function fetches stock data 
def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=ALPHAVANTAGE_API_KEY"
    response = requests.get(url)
    return response.json()

def prepare_stock_data(stock_symbols):
    stock_data = []
    for symbol in stock_symbols:
        data = get_stock_data(symbol)
        if "Global Quote" in data:
            quote = data["Global Quote"]
            stock_data.append({
                "symbol": quote.get("01. symbol"),
                "price": quote.get("05. price"),
                "change_percent": quote.get("10. change percent")
            })
        # stock_data.append(data)
    return stock_data

# def generate_stock_summary(stock_data, user_preferences):
#     client = anthropic.Anthropic(api_key="ANTHROPIC_API_KEY")
    
#     # Create context with user preferences and stock data
#     stock_info = "\n".join([
#         f"Stock: {s['symbol']}, Price: ${s['price']}, Change: {s['change_percent']}" 
#         for s in stock_data
#     ])
    
#     prompt = f"""
#     You are a personal finance assistant providing a brief update on stocks.
#     The user follows these stocks with the following data:
    
#     {stock_info}
    
#     User preferences:
#     - Detail level: {user_preferences['detail_level']} (brief/detailed)
#     - Interest in: {user_preferences['interests']} (price and daily change)
#     - Tone: {user_preferences['tone']} (serious/casual)
    
#     Generate a concise (30-second) stock update suitable for listening while brushing teeth. Focus on the most significant changes or news. Use a {user_preferences['tone']} tone.
#     """
    
#     response = client.messages.create(
#         model="claude-3-opus-20240229",
#         max_tokens=300,
#         temperature=0.7,
#         system="You are a helpful financial assistant that creates brief, personalized stock updates.",
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
    
#     return response.content[0].text

def generate_stock_summary(stock_data, user_preferences=detail):
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        stock_info = "\n".join([
            f"Stock: {s['symbol']}, Price: ${s['price']}, Change: {s['change_percent']}" 
            for s in stock_data
        ])
        prompt = f"""
        You are a personal finance assistant providing a brief update on stocks. Start your sentence with: "These are your stock updates for the day."

        {stock_info}
        DO IT ONLY BASED ON THE STOCK DATA.
        
        Preferences:
        - Detail level: {user_preferences['detail_level']}
        - Interests: {user_preferences['interests']}
        - Tone: {user_preferences['tone']} 
        """

        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=300,
            temperature=0.7,
            system="You are a personal finance assistant providing a brief update on stocks. Start your sentence with: 'These are your stock updates for the day.' Talk about the stocks in a way that is easy to understand and that doesn't necessarily cite their tag but rather just the name of the company. Make sure that you make it sound natural, like a human would tell another human these news updates.",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    except Exception as e:
        print("Error from Claude:", e)
        return "Error generating stock summary."

def prepare_morning_content(stock_symbols, detail=detail):
    # Get user preferences from database
    user = get_user_data()
    # stock_symbols = user['followed_stocks']
    # preferences = user['stock_preferences']
    
    # Get and process stock data
    stock_data = prepare_stock_data(stock_symbols)
    
    # Generate natural language summary with Claude
    stock_summary = generate_stock_summary(stock_data, detail)
    
    # Add to morning content queue
    add_to_morning_briefing("stocks", stock_summary)
    
    return stock_summary

# This is where we add the preferences of the user 
# def get_user_data():
#     return {
#         # "followed_stocks": ["SPY", "AAPL", "GOOGL", "TSLA"],
#         "stock_preferences": {
#             "detail_level": "brief",
#             "interests": "price and daily change",
#             "tone": "casual"
#         }
#     }

def add_to_morning_briefing(section, content):
    print(f"[DEBUG] Added to morning briefing: {section} - {content}")