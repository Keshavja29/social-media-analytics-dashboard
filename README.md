# Social Media Analytics Dashboard 📊

A powerful real-time social media analytics platform with AI-powered sentiment analysis, trending hashtags tracking, and comprehensive engagement metrics visualization.

## 🌟 Features

- **Real-time Data Visualization** - Interactive charts and graphs using Chart.js
- **AI Sentiment Analysis** - Analyze post sentiments (Positive, Negative, Neutral) using NLP
- **Trending Hashtags** - Track and visualize trending hashtags
- **Engagement Metrics** - Likes, shares, comments, and reach analytics
- **User Behavior Insights** - Understand audience patterns and preferences
- **Multi-Platform Support** - Analyze data from Twitter, Instagram, LinkedIn
- **Export Reports** - Download analytics as PDF/CSV

## 🛠️ Tech Stack

**Frontend:**
- React.js
- Chart.js / Recharts
- Axios
- TailwindCSS
- React Router

**Backend:**
- Python Flask
- Flask-CORS
- TextBlob (Sentiment Analysis)
- NLTK (Natural Language Processing)
- Pandas (Data Processing)

**Database:**
- MongoDB / SQLite

## 📋 Prerequisites

- Node.js (v14+)
- Python (3.8+)
- npm or yarn
- pip

## 🚀 Installation

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

## 📁 Project Structure

```
social-media-analytics-dashboard/
├── backend/
│   ├── app.py
│   ├── models/
│   ├── routes/
│   ├── utils/
│   │   └── sentiment_analyzer.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   └── package.json
└── README.md
```

## 🎯 Key Features Explained

### 1. Sentiment Analysis
Uses TextBlob and NLTK to analyze text sentiment with accuracy scores.

### 2. Real-time Updates
WebSocket integration for live data streaming.

### 3. Trending Algorithm
Custom algorithm to identify trending hashtags based on frequency and engagement.

## 📊 API Endpoints

- `GET /api/analytics/overview` - Get overall analytics
- `GET /api/analytics/sentiment` - Get sentiment analysis data
- `GET /api/analytics/trending` - Get trending hashtags
- `POST /api/analytics/analyze` - Analyze new post

## 🔧 Configuration

Create `.env` file in backend:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

## 📸 Screenshots

(Add screenshots here)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License

## 👨‍💻 Author

**Keshav Jadam**
- GitHub: [@Keshavja29](https://github.com/Keshavja29)
- LinkedIn: [Keshav Jadam](https://linkedin.com/in/keshav-jadam)

## 🙏 Acknowledgments

- TextBlob for sentiment analysis
- Chart.js for beautiful visualizations
- React community for amazing tools
