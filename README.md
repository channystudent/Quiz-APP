# Quiz Application 🎓

A full-featured web-based quiz application built with Flask and SQLite. This application provides separate interfaces for users to take quizzes and administrators to manage quiz content.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Admin Panel](#admin-panel)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)

## ✨ Features

### User Features
- **User Registration & Authentication**: Secure user registration and login system
- **Category-based Quizzes**: Take quizzes organized by different categories
- **Interactive Quiz Interface**: User-friendly quiz-taking experience
- **Score Tracking**: Automatic score calculation and result storage
- **Quiz History**: View past quiz attempts and scores

### Admin Features
- **Admin Dashboard**: Dedicated admin panel for content management
- **Category Management**: Create, view, and manage quiz categories
- **Question Management**: Add, edit, and delete quiz questions
- **Dynamic Question Creation**: Add multiple-choice questions with 4 options
- **Real-time Updates**: Changes reflect immediately in the user interface

### Data Export
- **Multiple Export Formats**: Export user and quiz data in JSON, CSV, or XML formats
- **Comprehensive Data**: Export includes user information and quiz results

## 🛠️ Technology Stack

### Backend
- **Flask 3.0.0**: Python web framework
- **Flask-SQLAlchemy 3.1.1**: ORM for database operations
- **Flask-Migrate 4.0.5**: Database migration management
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **SQLite**: Lightweight database engine

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript (ES6+)**: Interactive user interface
- **Fetch API**: Asynchronous HTTP requests

### Additional Libraries
- **Pandas 2.1.1**: Data manipulation and export
- **dicttoxml 1.7.16**: XML data conversion
- **python-dotenv 1.0.0**: Environment variable management

## 📁 Project Structure

```
Quiz-APP/
│
├── app.py                      # Main Flask application
├── reset_database.py           # Database reset utility
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── instance/
│   └── quiz.db                 # SQLite database file
│
├── static/
│   ├── css/
│   │   ├── style.css          # Main stylesheet
│   │   └── style_fixed.css    # Additional styles
│   └── js/
│       └── script.js          # Frontend JavaScript
│
└── templates/
    ├── base.html              # Base template
    ├── index.html             # User login page
    ├── register.html          # User registration page
    ├── quiz.html              # Quiz interface
    ├── admin_login.html       # Admin login page
    └── admin_dashboard.html   # Admin dashboard
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone or download the repository**
   ```bash
   cd Quiz-APP
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python app.py
   ```
   The database will be automatically created in the `instance/` folder.

5. **Access the application**
   - Open your browser and navigate to: `http://127.0.0.1:5000`

## 📖 Usage

### For Users

1. **Register an Account**
   - Navigate to `http://127.0.0.1:5000`
   - Click "Register here"
   - Fill in username, email, and password
   - Submit the registration form

2. **Login**
   - Enter your username and password
   - Click "Login"

3. **Take a Quiz**
   - Select a category from the available options
   - Click "Start Quiz"
   - Answer the questions
   - Submit to see your score

### For Administrators

1. **Admin Login**
   - Navigate to `http://127.0.0.1:5000/admin-login`
   - Default credentials:
     - **Username**: `admin`
     - **Password**: `1234`

2. **Manage Categories**
   - Click "Add Category"
   - Enter category name
   - Click "Add" to create

3. **Manage Questions**
   - Select a category
   - Click "Add Question"
   - Fill in:
     - Question text
     - Four options (A, B, C, D)
     - Correct answer
   - Click "Add Question"

4. **Delete Questions**
   - Click the "Delete" button next to any question
   - Confirm deletion

## 🗄️ Database Schema

### Tables

#### 1. **User**
Stores user account information.

| Column      | Type         | Description                    |
|-------------|--------------|--------------------------------|
| id          | INTEGER      | Primary key                    |
| username    | VARCHAR(80)  | Unique username                |
| email       | VARCHAR(120) | Unique email address           |
| password    | VARCHAR(120) | User password (plain text)     |
| created_at  | DATETIME     | Account creation timestamp     |

#### 2. **Category**
Stores quiz categories.

| Column | Type        | Description          |
|--------|-------------|----------------------|
| id     | INTEGER     | Primary key          |
| name   | VARCHAR(80) | Unique category name |

#### 3. **Question**
Stores quiz questions.

| Column      | Type         | Description                           |
|-------------|--------------|---------------------------------------|
| id          | INTEGER      | Primary key                           |
| question    | VARCHAR(255) | Question text                         |
| options     | VARCHAR(500) | Comma-separated options (A,B,C,D)     |
| correct     | VARCHAR(255) | Correct answer                        |
| category_id | INTEGER      | Foreign key to Category               |

#### 4. **QuizResult**
Stores quiz attempt results.

| Column       | Type     | Description                      |
|--------------|----------|----------------------------------|
| id           | INTEGER  | Primary key                      |
| user_id      | INTEGER  | Foreign key to User              |
| score        | INTEGER  | Quiz score                       |
| completed_at | DATETIME | Quiz completion timestamp        |
| answers      | TEXT     | JSON string of user answers      |

#### 5. **Admin**
Stores admin credentials (separate from SQLAlchemy).

| Column   | Type    | Description          |
|----------|---------|----------------------|
| id       | INTEGER | Primary key          |
| username | TEXT    | Admin username       |
| password | TEXT    | Admin password       |

## 🔌 API Endpoints

### Category Endpoints

#### GET `/api/categories`
Retrieve all categories.

**Response:**
```json
[
  {"id": 1, "name": "Science"},
  {"id": 2, "name": "History"}
]
```

#### POST `/api/categories`
Create a new category.

**Request Body:**
```json
{
  "name": "Mathematics"
}
```

**Response:**
```json
{
  "message": "Category added"
}
```

### Question Endpoints

#### GET `/api/questions/<category_id>`
Retrieve all questions for a specific category.

**Response:**
```json
[
  {
    "id": 1,
    "question": "What is 2+2?",
    "options": ["2", "3", "4", "5"],
    "correct": "4",
    "category_id": 1
  }
]
```

#### POST `/api/questions/<category_id>`
Add a new question to a category.

**Request Body:**
```json
{
  "question": "What is the capital of France?",
  "options": ["London", "Paris", "Berlin", "Madrid"],
  "correct": "Paris"
}
```

**Response:**
```json
{
  "message": "Question added"
}
```

#### DELETE `/api/questions/<category_id>?id=<question_id>`
Delete a specific question.

**Response:**
```json
{
  "message": "Question deleted"
}
```

### Export Endpoints

#### GET `/export/<format>`
Export user and quiz data.

**Formats:** `json`, `csv`, `xml`

**Example:** `http://127.0.0.1:5000/export/json`


## 🎛️ Admin Panel

### Accessing the Admin Panel

1. Navigate to: `http://127.0.0.1:5000/admin-login`
2. Login with admin credentials
3. You'll be redirected to the admin dashboard

### Admin Dashboard Features

- **Category Management Section**
  - View all categories
  - Add new categories
  - Select categories to manage questions

- **Question Management Section**
  - View all questions in selected category
  - Add new questions with multiple-choice options
  - Delete existing questions
  - Real-time question list updates

### Admin Session Management

- Admin sessions are stored securely
- Logout functionality available
- Automatic redirect to login if not authenticated

## 🔧 Troubleshooting

### Database Issues

#### Problem: "no such column" errors

**Solution:**
```bash
# Stop the Flask server (Ctrl+C)

# Delete the database
python reset_database.py

# Restart the server
python app.py
```

#### Problem: Database locked error

**Cause:** Flask server is running and has the database file open.

**Solution:**
1. Stop the Flask server (Ctrl+C)
2. Run the reset script
3. Restart the server

### Common Errors

#### JSON Parsing Error
**Error:** `Uncaught (in promise) SyntaxError: Unexpected token '<'`

**Cause:** API endpoint returned HTML error page instead of JSON.

**Solution:** Check that:
- Flask server is running
- API routes are properly registered
- Database schema matches the models

#### 500 Internal Server Error
**Cause:** Usually database schema mismatch or missing data.

**Solution:**
1. Check the Flask terminal for detailed error messages
2. Reset the database if schema issues are reported
3. Ensure all required fields are provided in API requests

### Development Tips

1. **Enable Debug Mode**: The app runs in debug mode by default (`debug=True`)
2. **Check Terminal Output**: Flask logs all requests and errors to the terminal
3. **Browser Console**: Check browser console (F12) for JavaScript errors
4. **Hard Refresh**: Use Ctrl+Shift+R to clear cached JavaScript/CSS files

## 🔐 Security Notes

⚠️ **Important Security Considerations:**

1. **Passwords**: Currently stored in plain text. For production, implement password hashing (e.g., bcrypt, werkzeug.security)
2. **Secret Key**: Change `app.secret_key` to a secure random value
3. **Admin Credentials**: Change default admin password immediately
4. **HTTPS**: Use HTTPS in production environments
5. **Input Validation**: Add server-side validation for all user inputs
6. **SQL Injection**: Currently using parameterized queries (safe), maintain this practice

## 🔄 Database Reset Utility

The `reset_database.py` script helps reset the database:

```python
# Deletes the database file
python reset_database.py

# Then restart the server to recreate tables
python app.py
```

**Warning:** This deletes all data including:
- Users
- Categories
- Questions
- Quiz results

The admin account will be recreated with default credentials.

## 📝 File Descriptions

### Core Application Files

#### `app.py`
Main Flask application file containing:
- Flask app configuration and initialization
- Database models (User, Category, Question, QuizResult, Admin)
- Route handlers for user authentication
- Route handlers for quiz functionality
- Admin authentication and dashboard routes
- API endpoints for categories and questions
- Data export functionality (JSON, CSV, XML)

**Key Functions:**
- `init_db()`: Initializes the admin table
- `admin_login()`: Handles admin authentication
- `admin_dashboard()`: Renders admin dashboard
- `categories()`: API endpoint for category management
- `questions()`: API endpoint for question management
- `export_data()`: Exports data in various formats

#### `reset_database.py`
Utility script to delete the database file and force recreation.

**Usage:**
```bash
python reset_database.py
```

### Frontend Files

#### `static/js/script.js`
Frontend JavaScript handling:
- Category loading and creation
- Question loading, creation, and deletion
- Quiz start functionality
- Error handling for API calls
- Dynamic UI updates

**Key Functions:**
- `getCategories()`: Fetches and displays categories
- `addCategory()`: Creates new category
- `loadQuestions()`: Loads questions for selected category
- `addQuestion()`: Adds new question to category
- `deleteQuestion()`: Removes question from database
- `startQuiz()`: Initiates quiz with selected categories

#### `static/css/style.css` & `static/css/style_fixed.css`
Stylesheets for the application UI.

### Template Files

#### `templates/base.html`
Base template with common HTML structure and styling.

#### `templates/index.html`
User login page with:
- Login form
- Link to registration page
- Flash message display

#### `templates/register.html`
User registration page with:
- Registration form (username, email, password)
- Link back to login page

#### `templates/quiz.html`
Quiz interface for users to take quizzes.

#### `templates/admin_login.html`
Admin login page with authentication form.

#### `templates/admin_dashboard.html`
Admin dashboard with:
- Category management interface
- Question management interface
- Add/delete functionality
- Real-time updates

## 📊 Data Flow

### User Registration Flow
```
User fills form → POST /register → Validate data → Create User record → Redirect to login
```

### User Login Flow
```
User enters credentials → POST /login → Validate credentials → Create session → Redirect to quiz
```

### Admin Login Flow
```
Admin enters credentials → POST /admin-login → Validate against admin table → Create session → Redirect to dashboard
```

### Quiz Taking Flow
```
User selects categories → GET /api/questions/<id> → Display questions → User answers → POST /submit_quiz → Store results
```

### Question Management Flow
```
Admin selects category → GET /api/questions/<id> → Display questions → Admin adds/deletes → POST/DELETE /api/questions/<id> → Update database
```

## 🚀 Deployment Considerations

### For Production Deployment:

1. **Environment Variables**
   ```python
   import os
   app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')
   ```

2. **Database**
   - Consider using PostgreSQL or MySQL instead of SQLite
   - Implement database migrations with Flask-Migrate

3. **Security**
   - Implement password hashing
   - Add CSRF protection
   - Use HTTPS
   - Implement rate limiting

4. **Server**
   - Use production WSGI server (Gunicorn, uWSGI)
   - Set `debug=False`
   - Configure proper logging

5. **Static Files**
   - Use CDN for static assets
   - Implement caching strategies

## 📈 Future Enhancements

Potential improvements for the application:

- [ ] Password hashing and security improvements
- [ ] Email verification for user registration
- [ ] Password reset functionality
- [ ] Quiz timer functionality
- [ ] Question difficulty levels
- [ ] User profile pages
- [ ] Leaderboard system
- [ ] Question categories with images
- [ ] Bulk question import (CSV/JSON)
- [ ] Quiz analytics and statistics
- [ ] Mobile-responsive design improvements
- [ ] Multi-language support
- [ ] Question randomization
- [ ] Timed quizzes
- [ ] Certificate generation
- [ ] Social sharing features

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the Flask terminal output for error messages
3. Check browser console (F12) for JavaScript errors
4. Ensure all dependencies are installed correctly
5. Verify database schema matches the models

## 📄 License

This project is open source and available for educational purposes.

---

**Happy Quizzing! 🎉**

*Built with ❤️ using Flask and SQLAlchemy*