#!/usr/bin/env python3
"""
Toodless Task Management Application
Run this script to start the server
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, load_data

if __name__ == '__main__':
    print("🎉 Starting Toodless Task Management System")
    print("=" * 50)
    print("📋 Features:")
    print("  ✅ Calendar-based Todo Management")
    print("  📅 Date-specific Task Lists")
    print("  🎯 Task Completion Tracking")
    print("  ⏱️  Focus Timer Integration")
    print("  📊 Task Analytics")
    print("  🔍 Search Functionality")
    print("=" * 50)
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Load existing data
    load_data()
    
    # Start the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
