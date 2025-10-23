# Quiz System

A simple quiz system built with Flask, SQLAlchemy, and vanilla JavaScript.

## Features

- User registration system
- Interactive quiz interface
- Result storage in SQLite database
- Data export in CSV, JSON, and XML formats
- Responsive design

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Unix/MacOS:
     ```bash
     source .venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://localhost:5000`

## Database

The system uses SQLite with two main tables:
- Users: Stores user registration information
- QuizResults: Stores quiz attempts and scores

## Data Export

To export data, use the following endpoints:
- JSON: `/export/json`
- CSV: `/export/csv`
- XML: `/export/xml`

## Security Note

This is a basic implementation. For production use, you should:
- Hash passwords before storing
- Implement proper session management
- Add CSRF protection
- Use environment variables for sensitive data
- Add input validation and sanitization