import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line, Pie, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import './App.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const API_URL = 'http://localhost:5000/api';

function App() {
  const [overview, setOverview] = useState(null);
  const [sentiment, setSentiment] = useState(null);
  const [trending, setTrending] = useState([]);
  const [engagement, setEngagement] = useState([]);
  const [loading, setLoading] = useState(true);
  const [analyzeText, setAnalyzeText] = useState('');
  const [analyzeResult, setAnalyzeResult] = useState(null);
  const [xquikJson, setXquikJson] = useState('[{"tweet_id":"1889000000000000001","text":"Launch feedback is great today","author_username":"product_lead","likeCount":184,"retweetCount":42,"replyCount":17,"viewCount":9210}]');
  const [xquikResult, setXquikResult] = useState(null);
  const [xquikError, setXquikError] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [overviewRes, sentimentRes, trendingRes, engagementRes] = await Promise.all([
        axios.get(`${API_URL}/analytics/overview`),
        axios.get(`${API_URL}/analytics/sentiment`),
        axios.get(`${API_URL}/analytics/trending`),
        axios.get(`${API_URL}/analytics/engagement`)
      ]);

      setOverview(overviewRes.data.data);
      setSentiment(sentimentRes.data.data);
      setTrending(trendingRes.data.data);
      setEngagement(engagementRes.data.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!analyzeText.trim()) return;

    try {
      const response = await axios.post(`${API_URL}/analytics/analyze`, {
        text: analyzeText
      });
      setAnalyzeResult(response.data.data);
    } catch (error) {
      console.error('Error analyzing text:', error);
    }
  };

  const handleXquikImport = async () => {
    try {
      setXquikError('');
      const parsed = JSON.parse(xquikJson);
      const posts = Array.isArray(parsed) ? parsed : parsed.posts;

      if (!Array.isArray(posts) || posts.length === 0) {
        setXquikError('Paste a JSON array or an object with a posts array.');
        return;
      }

      const response = await axios.post(`${API_URL}/analytics/xquik-import`, {
        posts
      });
      setXquikResult(response.data.data);
    } catch (error) {
      setXquikError(error.response?.data?.error || error.message);
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading Analytics...</p>
      </div>
    );
  }

  const sentimentPieData = {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [{
      data: [
        overview?.sentiment_distribution.positive || 0,
        overview?.sentiment_distribution.negative || 0,
        overview?.sentiment_distribution.neutral || 0
      ],
      backgroundColor: ['#10b981', '#ef4444', '#6b7280'],
      borderWidth: 2
    }]
  };

  const engagementLineData = {
    labels: engagement.slice(0, 10).reverse().map(e => e.date),
    datasets: [
      {
        label: 'Likes',
        data: engagement.slice(0, 10).reverse().map(e => e.likes),
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4
      },
      {
        label: 'Shares',
        data: engagement.slice(0, 10).reverse().map(e => e.shares),
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.4
      },
      {
        label: 'Comments',
        data: engagement.slice(0, 10).reverse().map(e => e.comments),
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        tension: 0.4
      }
    ]
  };

  const trendingBarData = {
    labels: trending.slice(0, 8).map(t => t.tag),
    datasets: [{
      label: 'Mentions',
      data: trending.slice(0, 8).map(t => t.count),
      backgroundColor: '#8b5cf6',
      borderRadius: 8
    }]
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>📊 Social Media Analytics Dashboard</h1>
        <p>Real-time insights with AI-powered sentiment analysis</p>
      </header>

      <div className="container">
        {/* Overview Cards */}
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Posts</h3>
            <p className="stat-value">{overview?.total_posts || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Total Engagement</h3>
            <p className="stat-value">{overview?.total_engagement?.toLocaleString() || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Avg Sentiment</h3>
            <p className="stat-value">{overview?.avg_sentiment_score || 0}</p>
          </div>
          <div className="stat-card">
            <h3>Platforms</h3>
            <p className="stat-value">4</p>
          </div>
        </div>

        {/* Charts Section */}
        <div className="charts-grid">
          <div className="chart-card">
            <h2>Sentiment Distribution</h2>
            <Pie data={sentimentPieData} options={{ maintainAspectRatio: true }} />
          </div>

          <div className="chart-card large">
            <h2>Engagement Over Time</h2>
            <Line data={engagementLineData} options={{ maintainAspectRatio: true }} />
          </div>

          <div className="chart-card large">
            <h2>Trending Hashtags</h2>
            <Bar data={trendingBarData} options={{ maintainAspectRatio: true }} />
          </div>
        </div>

        {/* AI Analyzer Section */}
        <div className="analyzer-section">
          <h2>🤖 AI Sentiment Analyzer</h2>
          <div className="analyzer-card">
            <textarea
              value={analyzeText}
              onChange={(e) => setAnalyzeText(e.target.value)}
              placeholder="Enter text to analyze sentiment..."
              rows="4"
            />
            <button onClick={handleAnalyze} className="analyze-btn">
              Analyze Sentiment
            </button>

            {analyzeResult && (
              <div className="result-card">
                <h3>Analysis Result:</h3>
                <div className={`sentiment-badge ${analyzeResult.sentiment}`}>
                  {analyzeResult.sentiment.toUpperCase()}
                </div>
                <p>Score: {analyzeResult.score}</p>
                <p>Confidence: {analyzeResult.confidence}%</p>
              </div>
            )}
          </div>
        </div>

        {/* Xquik Import Section */}
        <div className="analyzer-section">
          <h2>📥 Xquik Export Import</h2>
          <div className="analyzer-card">
            <textarea
              value={xquikJson}
              onChange={(e) => setXquikJson(e.target.value)}
              placeholder="Paste Xquik export JSON..."
              rows="6"
            />
            <button onClick={handleXquikImport} className="analyze-btn">
              Import Xquik Export
            </button>

            {xquikError && (
              <div className="result-card error-card">
                {xquikError}
              </div>
            )}

            {xquikResult && (
              <div className="result-card">
                <h3>Xquik Import Summary:</h3>
                <p>Total Posts: {xquikResult.overview.total_posts}</p>
                <p>Total Engagement: {xquikResult.overview.total_engagement.toLocaleString()}</p>
                <p>Average Sentiment: {xquikResult.overview.avg_sentiment_score}</p>
              </div>
            )}
          </div>
        </div>

        {/* Platform Stats */}
        <div className="platform-stats">
          <h2>Platform Performance</h2>
          <div className="platform-grid">
            {Object.entries(overview?.platform_stats || {}).map(([platform, stats]) => (
              <div key={platform} className="platform-card">
                <h3>{platform}</h3>
                <p>Posts: {stats.posts}</p>
                <p>Engagement: {stats.engagement.toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
