# Leaderboard System Specification

## Project Overview
- **Project Name**: Multi-Leaderboard System
- **Type**: Web Application (Flask + MongoDB)
- **Core Functionality**: Three separate leaderboards with a combined main leaderboard, admin-managed teams and scoring
- **Target Users**: Admins managing team competitions

## Technical Stack
- Backend: Python Flask
- Database: MongoDB (via MONGO_DB_URI)
- Frontend: HTML, CSS, JavaScript

## Data Models

### Team Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "leaderboard1_score": "integer (default: 0)",
  "leaderboard2_score": "integer (default: 0)",
  "leaderboard3_score": "integer (default: 0)",
  "total_score": "integer (computed)",
  "created_at": "datetime"
}
```

## Pages & Routes

### 1. Main Leaderboard (`/`)
- Displays combined rankings of all teams
- Shows total scores (sum of all three leaderboard scores)
- Sorted by total score descending

### 2. Leaderboard 1 (`/leaderboard/1`)
- Shows scores from leaderboard 1 only

### 3. Leaderboard 2 (`/leaderboard/2`)
- Shows scores from leaderboard 2 only

### 4. Leaderboard 3 (`/leaderboard/3`)
- Shows scores from leaderboard 3 only

### 5. Admin Panel (`/admin`)
- Create new teams
- Add points to existing teams for any leaderboard

## UI/UX Specification

### Color Palette
- Background: `#0f0f1a` (dark navy)
- Card Background: `#1a1a2e` (dark purple-navy)
- Primary Accent: `#00d9ff` (cyan)
- Secondary Accent: `#ff6b6b` (coral red)
- Success: `#4ade80` (green)
- Text Primary: `#ffffff`
- Text Secondary: `#94a3b8`
- Border: `#2d2d44`

### Typography
- Font Family: 'Outfit', sans-serif (from Google Fonts)
- Heading sizes: h1: 2.5rem, h2: 1.75rem
- Body: 1rem

### Layout
- Max container width: 900px
- Card padding: 24px
- Border radius: 12px
- Responsive: mobile-friendly

### Leaderboard Table
- Rank column with medal icons (gold/silver/bronze for top 3)
- Team name
- Score column
- Alternating row backgrounds

### Animations
- Smooth fade-in on page load
- Hover effects on table rows

## Functionality Specification

### Admin Features
1. **Create Team**: Form with team name input
2. **Add Points**: Select team from dropdown, select leaderboard (1/2/3), enter points to add

### Data Handling
- Total score = leaderboard1_score + leaderboard2_score + leaderboard3_score
- Leaderboards sorted by respective scores
- Main leaderboard sorted by total_score

## Acceptance Criteria
1. Main page shows all teams sorted by total score
2. Each leaderboard page shows correct scores for that category
3. Admin can create new teams
4. Admin can add points to any team's specific leaderboard
5. Total score updates automatically when points are added
6. Top 3 teams show medal indicators
7. All pages are responsive and visually consistent
