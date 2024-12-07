#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up LEDE Encryption System...${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

# Check if python3-venv is installed
if ! dpkg -l | grep -q python3-venv; then
    echo -e "${BLUE}Installing python3-venv...${NC}"
    sudo apt-get update
    sudo apt-get install -y python3-venv python3-full
fi

# Create and activate virtual environment using python3 -m venv
echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install requirements
echo -e "${BLUE}Installing requirements...${NC}"
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Run the Flask application
echo -e "${GREEN}Starting Flask application...${NC}"
export FLASK_APP=app.py
export FLASK_ENV=development
python3 -m flask run