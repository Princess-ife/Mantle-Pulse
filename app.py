from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def simplify_defi_action(action):
    action = action.lower()
    if 'transfer' in action:
        return 'Token Transfer'
    elif 'swap' in action or 'exactinput' in action or 'exactoutput' in action:
        return 'Token Swap'
    elif 'addliquidity' in action or 'mint' in action:
        return 'Add Liquidity'
    elif 'removeliquidity' in action or 'burn' in action:
        return 'Remove Liquidity'
    elif 'deposit' in action:
        return 'Vault Deposit'
    elif 'withdraw' in action:
        return 'Vault Withdrawal'
    elif 'approve' in action:
        return 'Token Approval'
    elif 'claim' in action or 'harvest' in action:
        return 'Claim Rewards'
    else:
        return 'DeFi Interaction'
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        wallet_address = data.get('wallet_address')
        if not wallet_address:
            return jsonify({"error": "Missing wallet address"}), 400

        from fetch_wallet import fetch_wallet_transactions
        from risk_scorer import score_emotional_risk, get_verdict, evaluate_wallet

        df = fetch_wallet_transactions(wallet_address)

        if df is None or df.empty:
            return jsonify({"error": "Could not fetch wallet data or empty transaction history"}), 404

        import pandas as pd
        df['timeStamp'] = pd.to_datetime(df['timeStamp'].astype(int), unit='s')
        df['trade_hour'] = df['timeStamp'].dt.hour
        df['day_of_week'] = df['timeStamp'].dt.day_name()
        df['time_since_last_trade'] = df['timeStamp'].diff().abs().dt.total_seconds() / 3600
        df['value_mnt'] = df['value'].astype(float) / 10**18
        df['value_zscore'] = (df['value_mnt'] - df['value_mnt'].mean()) / df['value_mnt'].std()
        df['trades_per_day'] = df['timeStamp'].dt.date.map(df['timeStamp'].dt.date.value_counts())
        error_rate = (df['isError'] == '1').sum() / len(df) * 100
        df = df.fillna(0)

        behavior_profile = {
            "most_active_hour": int(df['trade_hour'].mode()[0]),
            "favorite_day": df['day_of_week'].mode()[0],
            "avg_hours_between_trades": float(df['time_since_last_trade'].mean()),
            "max_value_zscore": float(df['value_zscore'].max()),
            "max_trades_per_day": int(df['trades_per_day'].max()),
            "error_rate": float(error_rate),
            "most_common_defi_action": simplify_defi_action(df['functionName'].mode()[0])
        }

        evaluation = evaluate_wallet(behavior_profile)

        return jsonify({
            "behavior_profile": behavior_profile,
            "verdict": evaluation['verdict'],
            "risk_score": evaluation['risk_score'],
            "reasons": evaluation['reasons']
        })

    except Exception as e:
        app.logger.exception("Error analyzing wallet")
        return jsonify({"error": "Server error: %s" % str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
