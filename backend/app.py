from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random
from utils.sentiment_analyzer import SentimentAnalyzer

app = Flask(__name__)
CORS(app)

sentiment_analyzer = SentimentAnalyzer()
MAX_IMPORT_POSTS = 500


def get_first_value(source, keys, default=None):
    for key in keys:
        value = source.get(key)
        if value not in (None, ''):
            return value
    return default


def parse_count(value):
    try:
        return max(int(value), 0)
    except (TypeError, ValueError):
        return 0


def build_overview(data):
    total_posts = len(data)
    total_engagement = sum(post['likes'] + post['shares'] + post['comments'] for post in data)
    avg_sentiment = sum(post['score'] for post in data) / total_posts if total_posts else 0

    sentiment_distribution = {
        'positive': len([p for p in data if p['sentiment'] == 'positive']),
        'negative': len([p for p in data if p['sentiment'] == 'negative']),
        'neutral': len([p for p in data if p['sentiment'] == 'neutral'])
    }

    platform_stats = {}
    for post in data:
        platform = post['platform']
        if platform not in platform_stats:
            platform_stats[platform] = {
                'posts': 0,
                'engagement': 0
            }
        platform_stats[platform]['posts'] += 1
        platform_stats[platform]['engagement'] += post['likes'] + post['shares'] + post['comments']

    return {
        'total_posts': total_posts,
        'total_engagement': total_engagement,
        'avg_sentiment_score': round(avg_sentiment, 2),
        'sentiment_distribution': sentiment_distribution,
        'platform_stats': platform_stats
    }


def normalize_xquik_post(post, index):
    text = get_first_value(post, ['text', 'full_text', 'tweet_text', 'content', 'body'])
    if not isinstance(text, str) or not text.strip():
        return None

    sentiment = sentiment_analyzer.analyze(text)

    return {
        'id': get_first_value(post, ['id', 'tweet_id', 'tweetId'], index + 1),
        'platform': 'X/Twitter',
        'content': text.strip(),
        'sentiment': sentiment['sentiment'],
        'score': sentiment['score'],
        'likes': parse_count(get_first_value(post, ['likes', 'like_count', 'likeCount'])),
        'shares': parse_count(get_first_value(post, ['shares', 'retweets', 'retweet_count', 'retweetCount'])),
        'comments': parse_count(get_first_value(post, ['comments', 'replies', 'reply_count', 'replyCount'])),
        'reach': parse_count(get_first_value(post, ['reach', 'views', 'view_count', 'viewCount'])),
        'timestamp': get_first_value(post, ['timestamp', 'created_at', 'createdAt'], datetime.now().isoformat())
    }

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

    return jsonify({
        'success': True,
        'data': build_overview(data)
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
    data = request.get_json(silent=True) or {}
    text = data.get('text', '')
    
    if not isinstance(text, str) or not text.strip():
        return jsonify({'success': False, 'error': 'No text provided'}), 400
    
    result = sentiment_analyzer.analyze(text.strip())
    
    return jsonify({
        'success': True,
        'data': result
    })

@app.route('/api/analytics/xquik-import', methods=['POST'])
def import_xquik_posts():
    """Normalize Xquik export rows into dashboard analytics."""
    data = request.get_json(silent=True) or {}
    posts = data.get('posts')

    if not isinstance(posts, list) or not posts:
        return jsonify({'success': False, 'error': 'Request body must include a non-empty posts array'}), 400

    normalized_posts = []
    for index, post in enumerate(posts[:MAX_IMPORT_POSTS]):
        if not isinstance(post, dict):
            continue
        normalized = normalize_xquik_post(post, index)
        if normalized:
            normalized_posts.append(normalized)

    if not normalized_posts:
        return jsonify({'success': False, 'error': 'No readable Xquik post text found'}), 400

    return jsonify({
        'success': True,
        'data': {
            'posts': normalized_posts,
            'overview': build_overview(normalized_posts),
            'row_limit': MAX_IMPORT_POSTS
        }
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
