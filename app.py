import os

import pandas as pd
import requests
import validators
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from models import Category, Tool, User, add_tools, db, get_category_id
from security import require_admin_password

categories_dict = {
    'AI Tools & Platforms': 'Artificial intelligence development tools, machine learning platforms, and AI services for building intelligent applications.',
    'APIs & Web Services': 'Web APIs and services that allow applications to communicate and exchange data with external systems.',
    'Version Control & Collaboration': 'Tools for tracking code changes, managing different versions, and enabling team collaboration on projects.',
    'Code Hosting & CI/CD': 'Platforms for storing source code and implementing continuous integration and deployment pipelines.',
    'APIs & Mock APIs': 'Real APIs for various services and mock APIs for testing and development purposes.',
    'Developer Tools & Utilities': 'Essential software tools and utilities that assist developers in their daily work.',
    'Testing & Quality Assurance': 'Tools and frameworks for software testing, quality assurance, and bug detection.',
    'Cloud & Hosting (Free Tiers)': 'Cloud computing services and hosting platforms offering free tiers for development.',
    'Databases & Storage': 'Database management systems and data storage solutions for applications.',
    'Learning & Documentation': 'Educational resources, documentation tools, and learning platforms for developers.',
    'Design & Visual Resources': 'Design tools, graphic resources, and visual assets for UI/UX development.',
    'Monitoring & Analytics': 'Tools for tracking application performance, monitoring systems, and analyzing data.',
    'Security & Scanning': 'Security tools, vulnerability scanners, and protection services for applications.',
    'Search & Indexing': 'Search engines, indexing services, and data retrieval tools.',
    'Messaging & Email': 'Communication services for messaging, email, and notifications.',
    'Payments & Sandboxes': 'Payment processing APIs and sandbox environments for testing financial transactions.',
    'Containers & Orchestration': 'Containerization technologies and orchestration platforms for deployment management.',
    'Site Generators & Frameworks': 'Static site generators and web development frameworks.',
    'Package Managers & Repositories': 'Tools for managing software dependencies and package repositories.',
    'Editors & IDEs': 'Code editors and integrated development environments for programming.',
    'Online IDEs / Playgrounds': 'Web-based development environments and code playgrounds for quick testing.',
    'Version Control & Hosting': 'Combined version control systems with code hosting capabilities.',
    'CI / CD & Automation': 'Continuous integration, continuous deployment, and automation tools.',
    'Package Registries': 'Repositories for publishing and distributing software packages.',
    'APIs & Web Development': 'APIs specifically tailored for web development purposes.',
    'Frontend Frameworks & Tooling': 'Frameworks and tools for client-side web development.',
    'Backend Frameworks & Tools': 'Server-side frameworks and development tools for backend systems.',
    'Testing & QA': 'Software testing frameworks and quality assurance tools.',
    'Linters & Formatters': 'Code analysis tools for maintaining code quality and consistent formatting.',
    'Build Tools & Task Runners': 'Automation tools for building projects and running development tasks.',
    'Dev Tools & Terminals': 'Development utilities and terminal applications for programmers.',
    'APM, Monitoring & Logging': 'Application performance monitoring, system monitoring, and logging services.',
    'Security & Static Analysis': 'Security tools and static code analysis for vulnerability detection.',
    'Documentation & Knowledge': 'Tools for creating and managing technical documentation and knowledge bases.',
    'Design & Prototyping': 'UI/UX design tools and prototyping platforms for creating mockups.',
    'APIs & Data (Free / Public)': 'Free and publicly available APIs and data sources for development.',
    'Machine Learning & Data Science': 'Tools and platforms for machine learning and data science projects.',
    'Notebooks & Data Visualization': 'Interactive notebooks and tools for data visualization and analysis.',
    'Code Search & Snippets': 'Tools for searching code and managing code snippets.',
    'Static Analysis & Code Review': 'Automated code analysis and code review tools.',
    'APIs for Authentication & Identity': 'APIs dedicated to user authentication and identity management.',
    'CLI Utilities & Helpers': 'Command-line interface tools and helper utilities.',
    'Project Management & Collaboration': 'Tools for managing development projects and team collaboration.',
    'Learning & Tutorials': 'Educational content and tutorial resources for skill development.',
    'APIs & Tools for Developers (Misc)': 'Miscellaneous APIs and tools for various development needs.',
    'Open Source Directories & Communities': 'Directories of open source projects and developer communities.',
    'Fonts, Icons & Assets': 'Typography resources, icon sets, and design assets.',
    'Misc Useful Services': 'Various useful services that don\'t fit other specific categories.',
    'Cloud Platforms & Services': 'Comprehensive cloud computing platforms and related services.',
    'APILayer': 'API management and gateway services.',
    'Animals': 'APIs and data related to animals, pets, and wildlife.',
    'Anime': 'APIs and resources related to anime, manga, and Japanese animation.',
    'Anti-Malware': 'Security tools and APIs for malware detection and prevention.',
    'Art & Design': 'Creative resources, art APIs, and design-related services.',
    'Authentication & Authorization': 'Services for user authentication, authorization, and identity management.',
    'Blockchain': 'Blockchain technologies, cryptocurrencies, and distributed ledger services.',
    'Books': 'APIs and resources related to books, literature, and publishing.',
    'Business': 'Business-related APIs and services for commercial applications.',
    'Calendar': 'Calendar APIs and scheduling services.',
    'Cloud Storage & File Sharing': 'Online storage solutions and file sharing services.',
    'Continuous Integration': 'Tools and services for automated continuous integration processes.',
    'Cryptocurrency': 'APIs and services related to cryptocurrencies and digital assets.',
    'Currency Exchange': 'Foreign exchange rates and currency conversion APIs.',
    'Data Validation': 'Tools and services for validating and verifying data.',
    'Development': 'General development tools and programming resources.',
    'Dictionaries': 'Dictionary APIs and language reference services.',
    'Documents & Productivity': 'Document processing and productivity tools.',
    'Email': 'Email services, SMTP providers, and email-related APIs.',
    'Entertainment': 'Entertainment-related APIs for movies, TV, and media.',
    'Environment': 'Environmental data and sustainability-related APIs.',
    'Events': 'Event management and ticketing APIs.',
    'Finance': 'Financial data, stock market, and banking APIs.',
    'Food & Drink': 'APIs related to food, recipes, and beverages.',
    'Games & Comics': 'Gaming APIs and comic book resources.',
    'Geocoding': 'Geolocation and address conversion services.',
    'Government': 'Government data and public sector APIs.',
    'Health': 'Healthcare, fitness, and medical data APIs.',
    'Jobs': 'Job search and employment-related APIs.',
    'Machine Learning': 'Machine learning models and AI services.',
    'Music': 'Music APIs and audio-related services.',
    'News': 'News feeds and media content APIs.',
    'Open Data': 'Publicly available open data sets and APIs.',
    'Open Source Projects': 'Open source software projects and repositories.',
    'Patent': 'Patent search and intellectual property APIs.',
    'Personality': 'Personality assessment and psychology-related APIs.',
    'Phone': 'Telephone and communication APIs.',
    'Photography': 'Photo-related APIs and image services.',
    'Programming': 'Programming languages and coding resources.',
    'Science & Math': 'Scientific data and mathematical calculation APIs.',
    'Security': 'Cybersecurity tools and protection services.',
    'Shopping': 'E-commerce and retail APIs.',
    'Social': 'Social media APIs and networking services.',
    'Sports & Fitness': 'Sports data and fitness tracking APIs.',
    'Test Data': 'Sample data and testing datasets.',
    'Text Analysis': 'Natural language processing and text analytics tools.',
    'Tracking': 'Package tracking and shipment monitoring APIs.',
    'Transportation': 'Transportation and logistics APIs.',
    'URL Shorteners': 'URL shortening services and link management tools.',
    'Vehicle': 'Automotive and vehicle-related APIs.',
    'Video': 'Video streaming and multimedia APIs.',
    'Weather': 'Weather data and forecasting APIs.'
}
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def validate_url(url):
    if not validators.url(url):
        return False
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code < 400
    except requests.RequestException:
        try:
            response = requests.get(url, timeout=5, allow_redirects=True)
            return response.status_code < 400
        except requests.RequestException:
            return False

@app.route('/')
def index():
    tools = Tool.query.filter_by(is_approved=True).order_by(Tool.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('index.html', tools=tools, categories=categories)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))

@app.route('/add-tool', methods=['GET', 'POST'])
@login_required
def add_tool():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        link = request.form.get('link')
        category_id = request.form.get('category_id')
        
        if Tool.query.filter_by(link=link).first():
            flash('This tool already exists in the database', 'error')
            return redirect(url_for('add_tool'))
        
        if not validate_url(link):
            flash('The provided link is invalid or not accessible', 'error')
            return redirect(url_for('add_tool'))
        
        tool = Tool(
            name=name,
            description=description,
            link=link,
            category_id=category_id,
            contributor_id=current_user.id,
            is_approved=False
        )
        db.session.add(tool)
        db.session.commit()
        
        flash('Tool submitted successfully! It will be visible after approval.', 'success')
        return redirect(url_for('my_contributions'))
    
    categories = Category.query.all()
    return render_template('add_tool.html', categories=categories)

@app.route('/browse')
def browse():
    category_id = request.args.get('category')
    search_query = request.args.get('search', '')
    
    query = Tool.query.filter_by(is_approved=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if search_query:
        query = query.filter(
            db.or_(
                Tool.name.ilike(f'%{search_query}%'),
                Tool.description.ilike(f'%{search_query}%')
            )
        )
    
    tools = query.order_by(Tool.created_at.desc()).all()
    categories = Category.query.all()
    
    return render_template('browse.html', tools=tools, categories=categories, selected_category=category_id)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category_id = request.args.get('category', '')
    
    tools_query = Tool.query.filter_by(is_approved=True)
    
    if query:
        tools_query = tools_query.filter(
            db.or_(
                Tool.name.ilike(f'%{query}%'),
                Tool.description.ilike(f'%{query}%')
            )
        )
    
    if category_id:
        tools_query = tools_query.filter_by(category_id=category_id)
    
    tools = tools_query.order_by(Tool.created_at.desc()).all()
    
    return jsonify([{
        'id': tool.id,
        'name': tool.name,
        'description': tool.description,
        'link': tool.link,
        'category': tool.category.name if tool.category else 'Uncategorized',
        'contributor': tool.contributor.username
    } for tool in tools])

@app.route('/contributors')
def contributors():
    users = User.query.all()
    
    user_stats = []
    for user in users:
        approved_count = Tool.query.filter_by(contributor_id=user.id, is_approved=True).count()
        pending_count = Tool.query.filter_by(contributor_id=user.id, is_approved=False).count()
        
        user_stats.append({
            'user': user,
            'approved_count': approved_count,
            'pending_count': pending_count,
            'total_count': approved_count + pending_count
        })
    
    user_stats.sort(key=lambda x: x['approved_count'], reverse=True)
    
    return render_template('contributors.html', user_stats=user_stats)

@app.route('/my-contributions')
@login_required
def my_contributions():
    tools = Tool.query.filter_by(contributor_id=current_user.id).order_by(Tool.created_at.desc()).all()
    return render_template('my_contributions.html', tools=tools)

@app.route('/approve-tools')
@login_required
def approve_tools():
    if not current_user.is_admin:
        flash('You do not have permission to access this page', 'error')
        return redirect(url_for('index'))
    
    pending_tools = Tool.query.filter_by(is_approved=False).order_by(Tool.created_at.desc()).all()
    return render_template('approve_tools.html', tools=pending_tools)

@app.route('/approve-tool/<int:tool_id>', methods=['POST'])
@login_required
def approve_tool(tool_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    tool = Tool.query.get_or_404(tool_id)
    tool.is_approved = True
    db.session.commit()
    
    flash(f'Tool "{tool.name}" has been approved', 'success')
    return redirect(url_for('approve_tools'))

@app.route('/reject-tool/<int:tool_id>', methods=['POST'])
@login_required
def reject_tool(tool_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    tool = Tool.query.get_or_404(tool_id)
    db.session.delete(tool)
    db.session.commit()
    
    flash(f'Tool "{tool.name}" has been rejected and removed', 'success')
    return redirect(url_for('approve_tools'))

def init_db():
    with app.app_context():
        db.create_all()
        
        if Category.query.count() == 0:
            categories = [
                Category(name='Code Editors & IDEs', description='Text editors and integrated development environments'),
                Category(name='Version Control', description='Git clients and version control tools'),
                Category(name='API Development', description='Tools for building and testing APIs'),
                Category(name='Database Tools', description='Database management and design tools'),
                Category(name='Design & Prototyping', description='UI/UX design and prototyping tools'),
                Category(name='Testing & QA', description='Testing frameworks and quality assurance tools'),
                Category(name='DevOps & CI/CD', description='Deployment, automation, and continuous integration tools'),
                Category(name='Documentation', description='Documentation generators and writing tools'),
                Category(name='Learning Resources', description='Educational platforms and tutorials'),
                Category(name='Productivity', description='Task management and productivity tools'),
                Category(name='Other', description='Other useful tools for developers')
            ]
            for key ,val in categories_dict.items():
            	categories.append(Category(name=key, description=val))
            for category in categories:
                db.session.add(category)
            
            db.session.commit()
        
        if User.query.count() == 0:
            admin_password = require_admin_password()
            admin = User(
                username='admin',
                email='admin@alqudimi.tech',
                password_hash=generate_password_hash(admin_password),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
        
        if Tool.query.count() == 0:
            admin_user = User.query.filter_by(username='admin').first()
            
            sample_tools = [
                Tool(name='Visual Studio Code', description='A powerful, lightweight code editor with extensive extensions', link='https://code.visualstudio.com/', category_id=1, contributor_id=admin_user.id, is_approved=True),
                Tool(name='GitHub', description='Version control and collaboration platform for developers', link='https://github.com/', category_id=2, contributor_id=admin_user.id, is_approved=True),
                Tool(name='Postman', description='API development and testing platform', link='https://www.postman.com/', category_id=3, contributor_id=admin_user.id, is_approved=True),
                Tool(name='Figma', description='Collaborative interface design tool', link='https://www.figma.com/', category_id=5, contributor_id=admin_user.id, is_approved=True),
                Tool(name='Docker', description='Platform for developing, shipping, and running applications in containers', link='https://www.docker.com/', category_id=7, contributor_id=admin_user.id, is_approved=True),
            ]
            
               
               
            for tool in sample_tools:
                db.session.add(tool)
            
            db.session.commit()
            df = pd.read_csv('data.csv')
            for index, row in df.iterrows():
               print(f"الصف {index}:")
               add_tools(row["name"],row["description"], row["url"], get_category_id(row["main_category"]), admin_user.id)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
