#!/usr/bin/env python3
"""
MongoDB Setup Helper for RTSP Overlay App
"""

import os
import sys
import subprocess
from pathlib import Path

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def start_mongodb_docker():
    """Start MongoDB using Docker Compose"""
    if not Path('docker-compose.yml').exists():
        print("❌ docker-compose.yml not found")
        return False
    
    try:
        print("🚀 Starting MongoDB with Docker...")
        result = subprocess.run(['docker-compose', 'up', '-d', 'mongodb'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ MongoDB started successfully!")
            print("📊 MongoDB is running on: mongodb://localhost:27017")
            print("🌐 Optional: MongoDB Express UI available at: http://localhost:8081")
            print("   Username: admin, Password: admin123")
            return True
        else:
            print(f"❌ Failed to start MongoDB: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ docker-compose not found. Please install Docker Desktop.")
        return False

def check_env_file():
    """Check and create .env file if needed"""
    env_path = Path('server/.env')
    
    if not env_path.exists():
        print("📝 Creating .env file...")
        env_content = """# Database Configuration
USE_FILE_DB=true  # Use file database (no MongoDB required)

# MongoDB Connection (only needed if USE_FILE_DB=false)
MONGO_URI=mongodb://localhost:27017/rtsp_overlay_app
"""
        env_path.write_text(env_content)
        print("✅ Created server/.env file")
    else:
        print("✅ .env file already exists")

def main():
    print("🔧 RTSP Overlay App - MongoDB Setup")
    print("=" * 40)
    
    # Check .env file
    check_env_file()
    
    print("\nChoose your database setup option:")
    print("1. � UUse File Database (No setup required - Default)")
    print("2. 🐳 Use Docker MongoDB (Recommended for development)")
    print("3. ☁️  Use MongoDB Atlas (Cloud)")
    print("4. 💻 Use local MongoDB installation")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n📁 File Database Setup:")
        print("✅ No additional setup required!")
        print("📝 Overlay presets will be stored in server/overlays.json")
        print("🚀 You can start the app immediately:")
        print("   cd server && python app.py")
        print("   cd client && npm start")
    
    elif choice == "2":
        if not check_docker():
            print("❌ Docker not found. Please install Docker Desktop first:")
            print("   https://www.docker.com/products/docker-desktop")
            return
        
        if start_mongodb_docker():
            print("\n🎉 Setup complete! Update your .env file:")
            print("   Set USE_FILE_DB=false in server/.env")
            print("   Then run: cd server && python app.py")
    
    elif choice == "3":
        print("\n☁️  MongoDB Atlas Setup:")
        print("1. Go to https://www.mongodb.com/atlas")
        print("2. Create a free account and cluster")
        print("3. Get your connection string")
        print("4. Update server/.env file:")
        print("   - Set USE_FILE_DB=false")
        print("   - Set MONGO_URI=your-connection-string")
        print("\nExample connection string:")
        print