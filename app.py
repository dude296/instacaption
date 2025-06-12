from flask import Flask, request, jsonify, render_template, redirect
import openai
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load API keys from environment variables

from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/caption', methods=['POST'])
def caption():
    data = request.json
    topic = data.get('topic', '')
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Write a catchy Instagram caption about: {topic}"}]
    )
    
    caption_text = response.choices[0].message.content.strip()
    return jsonify({'caption': caption_text})

@app.route('/subscribe')
def subscribe():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'InstaCaption Monthly Subscription',
                },
                'unit_amount': 900,
                'recurring': {
                    'interval': 'month',
                },
            },
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://yourdomain.com/success',
        cancel_url='https://yourdomain.com/cancel',
    )
    return redirect(session.url, code=303)

if __name__ == '__main__':
    app.run(debug=True)
