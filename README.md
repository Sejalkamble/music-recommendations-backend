# music-recommendations-backend
🎵 Music Recommendations Backend 
Backend service built using Django, PostgreSQL, Redis, Celery, Docker, and Spotify Web API to provide personalized music recommendations.  

🚀 Features  
User registration and profile management
Store user preferences (artists, genres, moods) 
Fetch music recommendations dynamically using Spotify Web API  
Caching using Redis  
Asynchronous tasks using Celery  
Fully containerized using Docker + docker-compose

📦 1. Setup & Run Instructions 
✅ Clone the repository git clone git@github.com:Sejalkamble/music-recommendations-backend.git
cd music-recommendations-backend

✅ Create .env file 
SPOTIFY_CLIENT_ID=your key
SPOTIFY_CLIENT_SECRET=your key
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/api/v1/spotify/callback/

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

1.pip install requirement.txt
2.python manage.py makemigration 
3.python manage.py migrate
2.python manage.py runserver


🐳 Run using Docker
Step 1 — Build & start all services
docker-compose up --build

Services started:
Service	        Purpose
Django	       API Server
PostgreSQL	   Database
Redis          Caching
Celery	Async  tasks
Celery Beat	   Scheduled tasks

▶ Access the app
Service	URL
API	  
http://127.0.0.1:8000/
admin/
api/v1/
api/v1/auth/

📌 3. Notes on Assumptions & Limitations
✔ Assumptions
Spotify API keys are valid and have access to the required endpoints
User must save preferences before requesting recommendations
The Spotify API returns at least 10 tracks for given inputs
Redis is available for caching tokens & responses

⚠ Limitations

Spotify access tokens expire every 1 hour, so the service refreshes automatically
Free tier API does not provide full audio features (danceability, valence, etc.)
Recommendation quality depends heavily on available Spotify data
Users with rare music tastes may get fewer recommendations
API rate limits may affect response times



