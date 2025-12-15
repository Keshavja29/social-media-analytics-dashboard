from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random
from utils.sentiment_analyzer import SentimentAnalyzer

app = Flask(__name__)
CORS(app)

# Initialize sentiment analyzer
sentiment_analyzer = SentimentAnalyzer()

# Sample data generator
def generate_sample_data():
    platforms = ['Twitter', 'Instagram', 'LinkedIn', 'Facebook']
    sample_posts = [
        "Amazing product! Highly recommend to everyone!",
        "Not satisfied with the service. Very disappointed.",
        "Just okay, nothing special about it.",
        "Absolutely love this! Best purchase ever!",
        "Terrible experience. Would not recommend.",
        "Great quality and fast delivery!",
        "Could be better. Average experience.",
        "Fantastic! Exceeded my expectations!",
        "Waste of money. Very poor quality.",
        "Decent product for the price."
    ]
    
    data = []
    for i in range(50):
        post = random.choice(sample_posts)
        sentiment = sentiment_analyzer.analyze(post)
        data.append({
            'id': i + 1,
            'platform': random.choice(platforms),
            'content': post,
            'sentiment': sentiment['sentiment'],
            'score': sentiment['score'],
            'likes': random.randint(10, 1000),
            'shares': random.randint(5, 500),
            'comments': random.randint(2, 200),
            'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 72))).isoformat()
        })
    return data

@app.route('/api/analytics/overview', methods=['GET'])
def get_overview():
    """Get overall analytics overview"""
    data = generate_sample_data()
    
    total_posts = len(data)
    total_engagement = sum(post['likes'] + post['shares'] + post['comments'] for post in data)
    avg_sentiment = sum(post['score'] for post in data) / total_posts
    
    sentiment_distribution = {
        'positive': len([p for p in data if p['sentiment'] == 'positive']),
        'negative': len([p for p in data if p['sentiment'] == 'negative']),
        'neutral': len([p for p in data if p['sentiment'] == 'neutral'])
    }
    
    platform_stats = {}
    for platform in ['Twitter', 'Instagram', 'LinkedIn', 'Facebook']:
        platform_posts = [p for p in data if p['platform'] == platform]
        platform_stats[platform] = {
            'posts': len(platform_posts),
            'engagement': sum(p['likes'] + p['shares'] + p['comments'] for p in platform_posts)
        }
    
    return jsonify({
        'success': True,
        'data': {
            'total_posts': total_posts,
            'total_engagement': total_engagement,
            'avg_sentiment_score': round(avg_sentiment, 2),
            'sentiment_distribution': sentiment_distribution,
            'platform_stats': platform_stats
        }
    })

@app.route('/api/analytics/sentiment', methods=['GET'])
def get_sentiment_analysis():
    """Get detailed sentiment analysis"""
    data = generate_sample_data()
    
    sentiment_timeline = []
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        day_posts = [p for p in data if datetime.fromisoformat(p['timestamp']).date() == date.date()]
        
        sentiment_timeline.append({
            'date': date.strftime('%Y-%m-%d'),
            'positive': len([p for p in day_posts if p['sentiment'] == 'positive']),
            'negative': len([p for p in day_posts if p['sentiment'] == 'negative']),
            'neutral': len([p for p in day_posts if p['sentiment'] == 'neutral'])
        })
    
    return jsonify({
        'success': True,
        'data': {
            'timeline': sentiment_timeline,
            'recent_posts': data[:10]
        }
    })

@app.route('/api/analytics/trending', methods=['GET'])
def get_trending_hashtags():
    """Get trending hashtags"""
    hashtags = [
        {'tag': '#AI', 'count': 1250, 'growth': 15.5},
        {'tag': '#MachineLearning', 'count': 980, 'growth': 12.3},
        {'tag': '#DataScience', 'count': 875, 'growth': 8.7},
        {'tag': '#Python', 'count': 756, 'growth': 10.2},
        {'tag': '#React', 'count': 654, 'growth': 7.8},
        {'tag': '#WebDev', 'count': 543, 'growth': 6.5},
        {'tag': '#JavaScript', 'count': 498, 'growth': 5.9},
        {'tag': '#TechNews', 'count': 432, 'growth': 4.2},
        {'tag': '#Coding', 'count': 387, 'growth': 3.8},
        {'tag': '#Programming', 'count': 321, 'growth': 2.5}
    ]
    
    return jsonify({
        'success': True,
        'data': hashtags
    })

@app.route('/api/analytics/analyze', methods=['POST'])
def analyze_post():
    """Analyze a new post"""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'success': False, 'error': 'No text provided'}), 400
    
    result = sentiment_analyzer.analyze(text)
    
    return jsonify({
        'success': True,
        'data': result
    })

@app.route('/api/analytics/engagement', methods=['GET'])
def get_engagement_metrics():
    """Get engagement metrics over time"""
    engagement_data = []
    
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        engagement_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'likes': random.randint(500, 2000),
            'shares': random.randint(100, 800),
            'comments': random.randint(50, 500),
            'reach': random.randint(5000, 20000)
        })
    
    return jsonify({
        'success': True,
        'data': engagement_data
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
