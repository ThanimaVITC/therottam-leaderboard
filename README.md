# Therottam Leaderboards

A multi-leaderboard system with three separate leaderboards and one main combined leaderboard. Built with Flask and MongoDB.

## Features

- **Main Leaderboard** - Combined rankings of all teams (total scores)
- **Three Individual Leaderboards** - Board 1, Board 2, Board 3
- **Admin Panel** - Create teams, add points, manage users
- **Mobile Responsive** - Works on all devices
- **Authentication** - Secure admin login

## Tech Stack

- Backend: Python Flask
- Database: MongoDB
- Frontend: HTML, CSS, JavaScript

## Prerequisites

- Python 3.8+
- MongoDB (local or Atlas)
- Node.js (optional, for Vercel CLI)

## Local Development

### 1. Clone and Install Dependencies

```bash
cd leaderboard
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file (or set these environment variables):

```env
MONGO_DB_URI=mongodb://localhost:27017/leaderboard
SECRET_KEY=your_secret_key_here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### 3. Seed Admin User

```bash
python seed_admin.py
```

This creates the default admin user:
- Username: `admin`
- Password: `admin123` (or whatever you set in ADMIN_PASSWORD)

### 4. Run the App

```bash
python -m flask --app api/index run
```

Or simply:

```bash
cd leaderboard
python api/index.py
```

The app will be available at `http://localhost:5000`

## Vercel Deployment

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/leaderboard.git
git push -u origin main
```

### 2. Deploy to Vercel

1. Go to [Vercel](https://vercel.com)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Add environment variables:
   - `MONGO_DB_URI` - Your MongoDB connection string (e.g., from MongoDB Atlas)
   - `SECRET_KEY` - A random secret key for sessions
5. Click "Deploy"

### 3. Seed Admin on Vercel

After deployment, run the seed script locally with your production MongoDB URI:

```bash
export MONGO_DB_URI=your_production_mongo_uri
python seed_admin.py
```

## Project Structure

```
leaderboard/
├── api/
│   ├── __init__.py
│   └── index.py          # Main Flask application
├── static/
│   ├── style.css
│   ├── script.js
│   ├── thanima_logo.webp
│   └── favicon.ico
├── templates/
│   ├── leaderboard.html
│   ├── admin_teams.html
│   ├── admin_points.html
│   ├── admin_management.html
│   └── login.html
├── vercel.json           # Vercel configuration
├── requirements.txt
├── seed_admin.py         # Admin user seeder
└── README.md
```

## Admin Routes

| Route | Description |
|-------|-------------|
| `/admin/login` | Admin login page |
| `/admin/teams` | Create and manage teams |
| `/admin/points` | Add points to teams |
| `/admin/management` | Manage admin users |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_DB_URI` | MongoDB connection string | `mongodb://localhost:27017/leaderboard` |
| `SECRET_KEY` | Flask secret key | `leaderboard_secret_key` |
| `ADMIN_USERNAME` | Default admin username | `admin` |
| `ADMIN_PASSWORD` | Default admin password | `admin123` |

## License

MIT
