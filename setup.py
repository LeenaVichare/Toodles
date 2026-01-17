#!/usr/bin/env python3
"""
Toodless Setup Script
Installs dependencies and provides setup instructions
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n🔧 Setting up Toodless...")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    commands = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install -r requirements.txt", "Installing Python dependencies")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def create_sample_data():
    """Create sample tasks for demonstration"""
    print("\n📝 Creating sample data...")
    
    sample_tasks = [
        {
            "title": "Review project proposal",
            "description": "Go through the Q4 project proposal and provide feedback",
            "project": "work",
            "priority": "high",
            "due_date": "2025-01-20"
        },
        {
            "title": "Morning workout",
            "description": "30-minute cardio session",
            "project": "health", 
            "priority": "medium",
            "due_date": "2025-01-17"
        },
        {
            "title": "Buy groceries",
            "description": "Weekly grocery shopping",
            "project": "personal",
            "priority": "low",
            "due_date": "2025-01-18"
        }
    ]
    
    try:
        os.makedirs('data', exist_ok=True)
        
        import json
        from datetime import datetime
        import uuid
        
        tasks_with_ids = []
        for task in sample_tasks:
            task['id'] = str(uuid.uuid4())
            task['created_at'] = datetime.now().isoformat()
            task['updated_at'] = datetime.now().isoformat()
            task['completed'] = False
            task['completed_at'] = None
            task['status'] = 'todo'
            tasks_with_ids.append(task)
        
        with open('data/tasks.json', 'w') as f:
            json.dump(tasks_with_ids, f, indent=2)
        
        with open('data/sessions.json', 'w') as f:
            json.dump([], f, indent=2)
            
        print("✅ Sample data created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
        return False

def main():
    """Main setup function"""
    print("🎉 Welcome to Toodless Setup!")
    print("=" * 50)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed. Please check the errors above.")
        return
    
    # Create sample data
    create_sample_data()
    
    print("\n🎊 Setup completed successfully!")
    print("\n🚀 How to run Toodless:")
    print("  1. Run: python app.py")
    print("  2. Open your browser to: http://localhost:5000")
    print("\n📚 Features available:")
    print("  ✅ Calendar-focused task management")
    print("  ⏱️  Focus timer with Pomodoro technique")
    print("  📊 Productivity analytics")
    print("  🔍 Search functionality")
    print("  📱 Beautiful modern UI")
    
    print("\n💡 Tips:")
    print("  • Click on calendar dates to add tasks")
    print("  • Use the timer to focus on your work")
    print("  • Search tasks using the top search bar")
    print("  • Track your productivity with analytics")

if __name__ == "__main__":
    main()
