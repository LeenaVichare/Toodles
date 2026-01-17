# Toodless - Smart Task Management System

🎯 A beautiful, calendar-focused task management application with integrated focus timer, built with Python Flask backend and modern vanilla JavaScript frontend.

![Toodless Preview](https://via.placeholder.com/800x400/8b5cf6/ffffff?text=Toodless+Calendar+Interface)

## ✨ Features

### 📅 Calendar-Focused Task Management
- Beautiful monthly calendar view with task visualization
- Click any date to view/add tasks for that day
- Color-coded tasks by project (Personal, Work, Health)
- Mini calendar for quick date selection

### ⏱️ Focus Timer (Pomodoro Technique)
- Built-in focus timer with 25/5/15 minute presets
- Automatic session tracking and analytics
- Visual and audio notifications
- Timer persistence across page refreshes

### 🎨 Modern Purple-Themed UI
- Clean, professional design inspired by modern productivity apps
- Responsive design works on desktop, tablet, and mobile
- Smooth animations and micro-interactions
- Dark sidebar with beautiful gradient backgrounds

### 📊 Advanced Features
- Real-time search across all tasks
- Task analytics and productivity insights
- RESTful API for task management
- Data persistence with JSON storage
- Session tracking for focus time

### 🔍 Smart Functionality
- Live clock display in header
- Task creation with time slots and locations
- Project-based task organization
- Priority levels (High, Medium, Low)
- Completion tracking with timestamps

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd Toodless
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```
   This will:
   - Check Python version compatibility
   - Install required dependencies
   - Create sample data for demonstration

3. **Start the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 🏗️ Project Structure

```
Toodless/
├── 📱 Frontend
│   ├── index.html          # Main application interface
│   ├── css/
│   │   └── styles.css      # Modern purple-themed styles
│   └── js/
│       └── app.js          # Frontend JavaScript application
├── 🐍 Backend
│   ├── app.py              # Flask web server and API
│   ├── requirements.txt    # Python dependencies
│   └── setup.py           # Setup and installation script
├── 📊 Data
│   ├── data/
│   │   ├── tasks.json      # Task storage (auto-created)
│   │   └── sessions.json   # Timer sessions (auto-created)
└── 📚 Documentation
    └── README.md           # This file
```

## 🔗 API Endpoints

### Task Management
- `GET /api/tasks` - Get all tasks (with filtering)
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/<id>` - Update existing task
- `DELETE /api/tasks/<id>` - Delete task

### Calendar
- `GET /api/calendar/<year>/<month>` - Get calendar data

### Timer
- `POST /api/timer/start` - Start focus session
- `POST /api/timer/complete/<id>` - Complete session
- `GET /api/timer/sessions` - Get timer history

### Analytics
- `GET /api/analytics/productivity` - Get productivity insights

### Search
- `GET /api/search?q=<query>` - Search tasks

## 🛠️ Technologies Used

### Backend
- **Python 3.7+** - Server-side programming
- **Flask** - Lightweight web framework
- **Flask-CORS** - Cross-origin resource sharing
- **JSON** - Data storage (easily upgradeable to database)

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Grid/Flexbox
- **Vanilla JavaScript** - No frameworks, pure performance
- **Font Awesome** - Beautiful icons
- **Inter Font** - Clean, professional typography

### Features
- **RESTful API** - Clean API design
- **Responsive Design** - Works on all devices
- **Local Data Storage** - JSON-based persistence
- **Real-time Updates** - Dynamic UI updates

## 🎨 Design Philosophy

Toodless follows a calendar-first approach to task management, inspired by modern productivity applications. The purple color scheme creates a calming yet professional atmosphere, while the clean typography and generous whitespace ensure excellent readability.

Key design principles:
- **Simplicity** - Clean, uncluttered interface
- **Focus** - Calendar-centric task visualization
- **Productivity** - Built-in focus timer integration
- **Accessibility** - High contrast, clear typography
- **Responsiveness** - Seamless experience across devices

## 🔮 Future Enhancements

- [ ] Database integration (PostgreSQL/SQLite)
- [ ] User authentication and multi-user support
- [ ] Task templates and recurring tasks
- [ ] Email notifications and reminders
- [ ] Mobile app (React Native)
- [ ] Team collaboration features
- [ ] Advanced analytics and reporting
- [ ] Integration with calendar services (Google Calendar, Outlook)
- [ ] Dark/light theme toggle
- [ ] Drag-and-drop task organization

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

---

**Made with ❤️ for productivity enthusiasts**

*Toodless - Where tasks meet time management*
