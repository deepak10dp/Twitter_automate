from flask import Flask, render_template, jsonify
from scraper import TwitterScraper
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
scraper = TwitterScraper()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-scraper')
def run_scraper():
    try:
        # Try without proxy since we're using existing Chrome profile
        print("Attempting to scrape using existing Chrome profile...")
        result = scraper.get_trending_topics()
        
        if result:
            return jsonify(result)
        return jsonify({"error": "Failed to fetch trends"}), 500
    except Exception as e:
        print(f"Error in run_scraper: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
