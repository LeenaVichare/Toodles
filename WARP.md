# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Toodless is a calendar-focused task management application built with a Python Flask backend and vanilla JavaScript frontend. The app combines task management with a focus timer (Pomodoro technique) and features a modern purple-themed UI.

## Development Environment Setup

### Initial Setup
```bash
python setup.py
```
This automated setup script will:
- Check Python 3.7+ compatibility
- Install Flask dependencies from requirements.txt
- Create sample data for demonstration

### Start Development Server
```bash
python app.py
```
- Runs on http://localhost:5000
- Debug mode enabled by default
- Auto-reloads on file changes

### Dependencies
- **Backend**: Flask 2.3.3, Flask-CORS 4.0.0, python-dateutil 2.8.2
- **Frontend**: Vanilla JavaScript, no build process required

## Architecture Overview

### Backend (Flask)
- **Entry Point**: `app.py` - Main Flask application and API server
- **Data Storage**: JSON files in `data/` directory (tasks.json, sessions.json)
- **API Pattern**: RESTful endpoints with `/api/` prefix
- **CORS**: Enabled for frontend-backend communication

### Frontend Structure
- **Single Page Application**: Pure vanilla JavaScript, no framework
- **Main Files**:
  - `index.html` - Complete UI structure with all views
  - `js/app.js` - ToodlessApp class with calendar, timer, and task management
  - `css/styles.css` - Modern purple-themed styling with gradients

### Data Architecture
- **Tasks**: Stored with UUID, timestamps, project categories, priorities
- **Timer Sessions**: Pomodoro-style focus sessions linked to tasks
- **Projects**: Color-coded categories (personal, work, health)
- **Calendar Integration**: Tasks mapped to dates with time slots

## API Endpoints

### Core Task Operations
- `GET /api/tasks` - List tasks with optional filters (date, project, status)
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update task
- `DELETE /api/tasks/<id>` - Delete task

### Calendar & Timer
- `GET /api/calendar/<year>/<month>` - Monthly calendar data
- `POST /api/timer/start` - Start focus session
- `POST /api/timer/complete/<id>` - Complete session
- `GET /api/timer/sessions` - Timer history

### Analytics & Search
- `GET /api/analytics/productivity` - Productivity metrics
- `GET /api/search?q=<query>` - Search across tasks

## Frontend Architecture

### Main Class: ToodlessApp
- **State Management**: Centralized in constructor (currentDate, selectedDate, tasks, timer)
- **View System**: Single-page with view switching via data attributes
- **API Integration**: Centralized apiCall method with error handling

### Key Components
- **Calendar Engine**: Monthly grid generation with task visualization
- **Timer System**: Pomodoro technique with presets (25/5/15 minutes)
- **Task Management**: CRUD operations with real-time UI updates
- **Search**: Live filtering across all task fields

### UI Views
- **Dashboard**: Monthly calendar + task creation panel + kanban board
- **Timer**: Focus timer with session tracking
- **Calendar**: Detailed calendar view
- **Tasks**: Task list management

## Development Patterns

### Adding New Features
1. **Backend**: Add API endpoint to `app.py`, update data structure if needed
2. **Frontend**: Add UI elements to `index.html`, implement logic in `app.js`
3. **Styling**: Extend purple theme in `styles.css` following existing patterns

### Task Data Structure
```javascript
{
  id: "uuid",
  title: "string",
  description: "string", 
  project: "personal|work|health",
  priority: "high|medium|low",
  status: "todo|in_progress|completed",
  due_date: "YYYY-MM-DD",
  start_time: "HH:MM",
  end_time: "HH:MM",
  location: "string",
  created_at: "ISO timestamp",
  updated_at: "ISO timestamp",
  completed: boolean,
  completed_at: "ISO timestamp or null"
}
```

### Color Coding System
- **Personal**: Light blue (#3b82f6)
- **Work**: Orange (#f59e0b)  
- **Health**: Green (#10b981)
- **Primary Purple**: #8b5cf6 (main brand color)

## Testing

### Manual Testing
- Use sample data created by setup.py
- Test calendar navigation across months
- Verify timer functionality with different presets
- Test task CRUD operations across all views
- Validate responsive design on different screen sizes

### Browser Compatibility
- Modern browsers supporting ES6+ features
- Uses vanilla JavaScript (no transpilation needed)
- Responsive CSS Grid/Flexbox layout

## File Structure Context

```
Toodless/
├── app.py              # Flask server & API endpoints
├── index.html          # Complete UI (all views in one file)
├── js/app.js          # Frontend application logic
├── css/styles.css     # Purple-themed styling
├── data/              # JSON data storage (auto-created)
├── setup.py           # Automated setup script
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Common Development Tasks

### Adding a New Task Field
1. Update task creation in `create_task()` API endpoint (app.py)
2. Add form field to task modal (index.html)
3. Update `saveTask()` method in ToodlessApp (app.js)
4. Style new field following existing form patterns (styles.css)

### Modifying Timer Behavior
- Timer logic in `ToodlessApp.timer` object (app.js)
- API endpoints in `/api/timer/` section (app.py)
- Timer UI in `#timerView` section (index.html)

### Changing Color Scheme
- Main brand colors defined in CSS variables at top of styles.css
- Project colors in `.project-color` classes
- Gradient backgrounds in `.sidebar` and `body` elements

## Production Considerations

- Replace JSON storage with proper database (PostgreSQL/SQLite)
- Add user authentication system
- Implement proper error handling and validation
- Add environment-based configuration
- Consider adding build process for CSS/JS optimization
