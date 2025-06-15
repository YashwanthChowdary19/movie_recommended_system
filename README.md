# 🎬 Movie Recommender System

A content-based movie recommendation system built with Python and Streamlit that suggests similar movies based on genres, cast, crew, and movie overview.

## 🌟 Features

- Content-based movie recommendations
- Beautiful user interface with movie posters
- Real-time recommendations
- Movie details including:
  - Genres
  - Cast (Top 3 actors)
  - Director
  - Overview
  - Keywords
- Responsive design
- TMDB API integration for movie posters

## 🛠️ Prerequisites

- Python 3.8 or higher
- TMDB API Key (Get it from [TMDB](https://www.themoviedb.org/))
- Internet connection (for fetching movie posters)

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/movie_recommender_system.git
cd movie_recommender_system
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Download the dataset:
   - Download `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`
   - Place them in the project directory

5. Configure TMDB API:
   - Get your API key from [TMDB](https://www.themoviedb.org/)
   - Open `app.py`
   - Replace `YOUR_API_KEY` with your actual TMDB API key:
   ```python
   TMDB_API_KEY = "your_api_key_here"
   ```

## 🚀 Usage

1. Run the application:
```bash
streamlit run app.py
```

2. Open your web browser and go to:
```
http://localhost:8501
```

3. Using the application:
   - Select a movie from the dropdown menu
   - Click "Get Recommendations"
   - View the top 5 similar movies with their posters

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NLTK**: Natural Language Processing
- **Scikit-learn**: Machine Learning algorithms
- **Streamlit**: Web application framework
- **TMDB API**: Movie data and posters
- **Requests**: API communication

## 📝 Project Structure

```
movie_recommender_system/
│
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── tmdb_5000_movies.csv  # Movies dataset
└── tmdb_5000_credits.csv # Credits dataset
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [TMDB](https://www.themoviedb.org/) for providing the movie data and API
- [Streamlit](https://streamlit.io/) for the web framework
- [Kaggle](https://www.kaggle.com/) for the dataset



Project Link: [https://github.com/yourusername/movie_recommender_system](https://github.com/yourusername/movie_recommender_system) 