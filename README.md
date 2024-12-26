# Twitter Trends Scraper

This project scrapes Twitter's trending topics using Selenium and ProxyMesh, stores the data in MongoDB, and displays it on a web page.

## Prerequisites

1. Python 3.8+
2. MongoDB installed and running locally
3. Chrome browser installed
4. Twitter account
5. ProxyMesh account

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
- Copy `.env.example` to `.env`
- Fill in your Twitter credentials
- Add your ProxyMesh credentials
- Update MongoDB URI if needed

3. Make sure MongoDB is running locally

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Click the button to run the scraper and view results

## Features

- Scrapes top 5 trending topics from Twitter
- Uses ProxyMesh for IP rotation
- Stores results in MongoDB
- Displays results in a clean web interface
- Shows JSON data extract

## Screenshots

### Web Interface
![Web Interface](screenshots/web_interface.png)
*The main web interface showing the scraper control and results display.*

### Trending Topics
![Trending Topics](screenshots/trending_topics.png)
*Example of scraped trending topics from Twitter.*

### MongoDB Data
![MongoDB Data](screenshots/mongodb_data.png)
*Stored data in MongoDB showing the trend records.*

## Project Structure

- `app.py`: Flask web application
- `scraper.py`: Twitter scraping logic
- `templates/`: HTML templates
- `requirements.txt`: Python dependencies
- `.env`: Configuration file
