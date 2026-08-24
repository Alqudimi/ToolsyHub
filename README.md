
# 🛠️ ToolsyHub

A curated platform for developers to discover, share, and manage development tools and resources. Built with Flask and modern web technologies.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-lightgrey.svg)

## 🌟 Features

### 🔍 Discovery & Search
- **Advanced Search**: Find tools by name, description, or category
- **Category Filtering**: Browse tools by specific categories (100+ categories available)
- **Real-time Search**: Instant search results with AJAX

### 👥 User Management
- **User Registration & Authentication**: Secure signup and login system
- **User Profiles**: Track contributions and activity
- **Admin Panel**: Special privileges for user management

### 📦 Tool Management
- **Add New Tools**: Community-driven tool submissions
- **Approval System**: Admin moderation for quality control
- **Tool Validation**: Automatic URL validation and duplicate checking
- **Personal Dashboard**: View and manage your contributions

### 🏆 Community Features
- **Contributor Leaderboard**: Recognize top contributors
- **Tool Ratings**: Community-driven tool validation
- **User Statistics**: Track approved and pending submissions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL (or SQLite for development)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone git remote add origin https://github.com/Alqudimi/ToolsyHub.git
   cd devresourcehub
```

1. Create virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Environment Setup
   ```bash
   # Set environment variables
   export DATABASE_URL="postgresql://username:password@localhost/devresourcehub"
   export SESSION_SECRET="your-secret-key-here"
   ```
4. Database Initialization
   ```bash
   python app.py
   ```
   This will create the database tables and seed initial data.
5. Run the Application
   ```bash
   python app.py
   ```
   Visit http://localhost:5000 in your browser.

📁 Project Structure

```
ToolsyHub/
├── app.py                 # Main Flask application
├── models.py             # Database models and ORM
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── static/
│   ├── css/
│   │   └── style.css    # Modern CSS with dark theme
│   └── js/
│       └── main.js      # JavaScript for interactive features
└── templates/
    ├── base.html        # Base template
    ├── index.html       # Homepage
    ├── browse.html      # Tool browsing page
    ├── add_tool.html    # Tool submission form
    ├── login.html       # Authentication pages
    ├── register.html
    ├── contributors.html # Community leaderboard
    ├── my_contributions.html # User dashboard
    └── approve_tools.html # Admin approval panel
```

🗄️ Database Models

User

· User authentication and profile management
· Admin role support
· Contribution tracking

Category

· 100+ predefined tool categories
· Comprehensive categorization system
· Category descriptions

Tool

· Tool metadata (name, description, URL)
· Category association
· Approval status tracking
· Contributor attribution

🎨 UI/UX Features

· Modern Dark Theme: Easy on eyes for developers
· Responsive Design: Mobile-friendly interface
· Interactive Elements: Smooth animations and transitions
· Accessibility: Semantic HTML and ARIA labels
· Icon System: Font Awesome integration

🔧 Configuration

Environment Variables

· DATABASE_URL: Database connection string
· SESSION_SECRET: Flask session secret key

Database Support

· PostgreSQL (production)
· SQLite (development)

👨‍💻 Admin Features

Initial administrator setup:

Set `ADMIN_PASSWORD` in the process environment before the first startup. The application creates the initial `admin` account from that value and does not ship with a default password.

```bash
export ADMIN_PASSWORD='choose-a-unique-password'
python app.py
```

Admin Capabilities:

· Approve/reject tool submissions
· Manage categories
· View user statistics
· Moderate content

🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details.

Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

📊 Categories

The platform includes 100+ carefully curated categories including:

· AI Tools & Platforms
· APIs & Web Services
· Version Control & Collaboration
· Cloud & Hosting
· DevOps & CI/CD
· And many more specialized categories

🔒 Security Features

· Password hashing with Werkzeug
· SQL injection prevention
· XSS protection
· CSRF protection
· Session management
· Input validation and sanitization

🚀 Deployment

Heroku

```bash
# Procfile
web: python app.py
```

Docker

```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

📈 Future Enhancements

· Tool ratings and reviews
· Advanced search filters
· API endpoints
· Email notifications
· Social features
· Analytics dashboard
· Bulk import/export

🐛 Troubleshooting

Common issues and solutions:

1. Database connection errors
   · Verify DATABASE_URL environment variable
   · Check database server status
2. Import errors
   · Ensure all dependencies are installed
   · Check Python version compatibility
3. Static files not loading
   · Verify Flask static folder configuration
   · Check file permissions

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

👥 Team

Developed by Alqudimi Technology

🙏 Acknowledgments

· Flask community for excellent documentation
· Contributors who help maintain and improve the platform
· The developer community for tool submissions and feedback

---

⭐ If you find this project useful, please give it a star!
