import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

def get_ai_insights(behavior_profile):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
    Analyze the following DeFi behavior profile from the Mantle Blockchain and return a high-fidelity risk assessment.

BEHAVIOR PROFILE:
- Most Active Hour: {behavior_profile['most_active_hour']} UTC
- Favorite Day: {behavior_profile['favorite_day']}
- Average Hours Between Trades: {behavior_profile['avg_hours_between_trades']}
- Max Value Z-Score: {behavior_profile['max_value_zscore']}
- Max Trades Per Day: {behavior_profile['max_trades_per_day']}
- Error Rate: {behavior_profile['error_rate']}%
- Most Common Action: {behavior_profile['most_common_defi_action']}

TASK:
Identify if this wallet exhibits "Emotional Trading" (revenge trading, FOMO, panic) or "Clean Patterns" (systematic, DCA, institutional).

OUTPUT FILTERS:
1. VERDICT: Must be exactly one of: "CLEAN SIGNAL", "CAUTION", or "EMOTIONAL PATTERN".
2. RISK_SCORE: An integer from 0 to 100.
3. REASONS: A list of 2-3 specific behavioral observations.

RESPONSE FORMAT:
You must respond ONLY with a valid JSON object. Do not include any prose or explanation outside the JSON.

EXAMPLE JSON:
{{
    "verdict": "EMOTIONAL PATTERN",
    "risk_score": 85,
    "reasons": ["High trade frequency during late-night hours suggests impulsive behavior", "Significant Z-Score spike indicates over-leveraged position sizing"]
}}

    """

    try:
      chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    ) 
      return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        raise Exception(f"Groq AI Error: {str(e)}")

