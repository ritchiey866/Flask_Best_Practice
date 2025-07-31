# Flask Blog Application

A comprehensive Flask web application featuring blueprint architecture, template rendering, data persistence, and static file management. Built with Content Engineering methodology.

## Features

- **Blueprint Architecture**: Modular and scalable code organization
- **User Authentication**: Login, registration, and profile management
- **Blog Post Management**: Create, edit, and manage blog posts
- **Category Organization**: Organize posts by categories
- **RESTful API**: Comprehensive API endpoints for all functionality
- **Admin Dashboard**: Administrative interface for content management
- **Search Functionality**: Full-text search across posts
- **Responsive Design**: Modern UI with Bootstrap 5
- **Content Engineering**: Systematic approach to content management

## Technology Stack

- **Backend**: Flask 2.3.3
- **Database**: SQLAlchemy with SQLite (development)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Frontend**: Bootstrap 5, Font Awesome
- **API**: RESTful endpoints with JSON responses
- **Testing**: pytest with coverage

## Project Structure

```
flask_app/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── category.py
│   ├── views/                   # Main routes
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── auth/                    # Authentication routes
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── api/                     # API endpoints
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── admin/                   # Admin routes
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── forms/                   # Form definitions
│   │   ├── __init__.py
│   │   ├── auth_forms.py
│   │   ├── post_forms.py
│   │   └── category_forms.py
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   └── template_filters.py
│   ├── templates/               # Jinja2 templates
│   │   ├── base.html
│   │   ├── components/
│   │   ├── main/
│   │   ├── auth/
│   │   └── admin/
│   ├── static/                  # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/
│   └── errors.py               # Error handlers
├── config.py                   # Configuration settings
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
└── Flask_practice.md          # Comprehensive documentation
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flask_app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows
   venv\Scripts\activate
   # Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   # Windows
   set FLASK_APP=run.py
   set FLASK_ENV=development
   set SECRET_KEY=your-secret-key
   
   # Unix/MacOS
   export FLASK_APP=run.py
   export FLASK_ENV=development
   export SECRET_KEY=your-secret-key
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Register a new account or use the default admin account

## API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### Available Endpoints

#### Users
- `GET /users` - Get all users
- `GET /users/{id}` - Get specific user
- `POST /users` - Create new user

#### Posts
- `GET /posts` - Get all posts
- `GET /posts/{id}` - Get specific post
- `POST /posts` - Create new post (authenticated)

#### Categories
- `GET /categories` - Get all categories
- `GET /categories/{id}` - Get specific category

#### Search
- `GET /search?q={query}` - Search posts

### Example API Usage

```bash
# Get all posts
curl http://localhost:5000/api/v1/posts

# Create a new user
curl -X POST http://localhost:5000/api/v1/users \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

## Content Engineering Methodology

This project follows Content Engineering principles:

### 1. Content Modeling
- Structured data models using SQLAlchemy
- Clear separation of content types (Users, Posts, Categories)
- Consistent naming conventions

### 2. Content Architecture
- Blueprint-based modular structure
- Separation of concerns (models, views, templates)
- Reusable components and templates

### 3. Content Workflow
- Development → Testing → Deployment pipeline
- Version control for all content
- Documentation-driven development

### 4. Content Governance
- Coding standards and conventions
- Review processes
- Quality assurance guidelines

## Development

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_models.py
```

### Code Formatting
```bash
# Format code with Black
black .

# Check code style with flake8
flake8 .
```

### Database Migrations
```bash
# Create a new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

## Configuration

The application uses different configurations for different environments:

- **Development**: `config.DevelopmentConfig`
- **Testing**: `config.TestingConfig`
- **Production**: `config.ProductionConfig`

Environment variables can be set in a `.env` file:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db
```

## Deployment

### Production Setup

1. **Set production environment**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URL=postgresql://user:pass@localhost/dbname
   ```

2. **Install production dependencies**
   ```bash
   pip install gunicorn
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 run:app
   ```

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Email: support@flaskblog.com
- Documentation: See `Flask_practice.md` for comprehensive documentation

## Acknowledgments

- Flask community for the excellent framework
- Bootstrap team for the responsive CSS framework
- Font Awesome for the beautiful icons
- SQLAlchemy team for the powerful ORM

---

**Built with ❤️ and Flask** 