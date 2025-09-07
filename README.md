
# Backend API

## Overview
This is the backend API for the test application, built with Python and FastApi.

## Features
- CRUD Note operations
- Endpoints
   - GET /notes → list user’s notes
   - POST /notes → create a note
   - PUT /notes/{id} → update a note
   - DELETE /notes/{id} → delete a note
- Firebase Authentication
- Firebase Database Integration

## Prerequisites
Minimum: Python 3.9
Recommended: Python 3.11 (as used in the Docker image)

## Installation

1. Clone the repository
```bash
git clone [repository-url]
cd backend
```

2. Install dependencies
Install dependencies inside requirements.txt file
After making sure the you have a python virtual enviroment you can go to step 3


3. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application
```bash
python3 run.py
```

## Environment Variables
See `.env.example` for required environment variables.

## API Documentation
- Base URL: `http://localhost:[PORT]`

## Project Structure
```
backend/
├── src/           # Source code
├── docs/          # Detailed documentation
├── tests/         # Test files
├── .env.example   # Environment variables template
└── README.md      # This file
```

