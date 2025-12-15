from textblob import TextBlob
import nltk

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analyzer"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/brown')
        except LookupError:
            nltk.download('brown')
    
    def analyze(self, text):
        """
        Analyze sentiment of given text
        Returns: dict with sentiment, score, and confidence
        """
        if not text or not isinstance(text, str):
            return {
                'sentiment': 'neutral',
                'score': 0.0,
                'confidence': 0.0
            }
        
        # Create TextBlob object
        blob = TextBlob(text)
        
        # Get polarity score (-1 to 1)
        polarity = blob.sentiment.polarity
        
        # Get subjectivity score (0 to 1)
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment category
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Calculate confidence based on absolute polarity
        confidence = min(abs(polarity) * 100, 100)
        
        return {
            'sentiment': sentiment,
            'score': round(polarity, 3),
            'confidence': round(confidence, 2),
            'subjectivity': round(subjectivity, 3)
        }
    
    def batch_analyze(self, texts):
        """
        Analyze multiple texts at once
        Returns: list of sentiment results
        """
        results = []
        for text in texts:
            results.append(self.analyze(text))
        return results
    
    def get_sentiment_summary(self, texts):
        """
        Get summary statistics for multiple texts
        Returns: dict with aggregated sentiment data
        """
        results = self.batch_analyze(texts)
        
        positive_count = sum(1 for r in results if r['sentiment'] == 'positive')
        negative_count = sum(1 for r in results if r['sentiment'] == 'negative')
        neutral_count = sum(1 for r in results if r['sentiment'] == 'neutral')
        
        avg_score = sum(r['score'] for r in results) / len(results) if results else 0
        avg_confidence = sum(r['confidence'] for r in results) / len(results) if results else 0
        
        return {
            'total_analyzed': len(texts),
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'average_score': round(avg_score, 3),
            'average_confidence': round(avg_confidence, 2),
            'positive_percentage': round((positive_count / len(texts)) * 100, 2) if texts else 0,
            'negative_percentage': round((negative_count / len(texts)) * 100, 2) if texts else 0,
            'neutral_percentage': round((neutral_count / len(texts)) * 100, 2) if texts else 0
        }
