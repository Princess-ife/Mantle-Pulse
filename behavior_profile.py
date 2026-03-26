import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

behavior_profile = {
        "most_active_hour": 8,
        "favorite_day": "Sunday",
        "avg_hours_between_trades": 245.25,
        "max_value_zscore": 3.51,
        "max_trades_per_day": 2,
        "error_rate": 0.0,
        "most_common_defi_action": "transfer(address recipient, uint256 amount)"

    }
    
prompt = f"""
Based on the following behavior profile of a crypto wallet, provide insights into the wallet's trading patterns and potential strategies for engagement on Mantle Blockchain:

Behavior Profile:
- Most Active Hour: {behavior_profile['most_active_hour']} (UTC)
- Favorite Day: {behavior_profile['favorite_day']}
- Average Hours Between Trades: {behavior_profile['avg_hours_between_trades']}
- Maximum Value Z-Score: {behavior_profile['max_value_zscore']}
- Maximum Trades Per Day: {behavior_profile['max_trades_per_day']}
- Error Rate: {behavior_profile['error_rate']}
- Most Common DeFi Action: {behavior_profile['most_common_defi_action']}

Please analyze these metrics to identify any notable trends or behaviors that could inform how we might engage with this wallet on the Mantle Blockchain. Consider factors such as optimal times for interaction, potential trading strategies, and any risks associated with the wallet's activity patterns.

Insights:
- 🟢 CLEAN SIGNAL: Normal behavior, safe to transact
- 🟡 CAUTION: Some unusual patterns detected
- 🔴 EMOTIONAL PATTERN: High risk behavior detected

Respond with the verdict and a short 2-3 sentence explanation.
"""

chat_completion = client.chat.completions.create(
    messages=[
        {"role": "user", "content": prompt}
    ],
    model="llama-3.3-70b-versatile"
)

print(chat_completion.choices[0].message.content)