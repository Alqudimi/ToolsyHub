from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    tools = db.relationship('Tool', backref='contributor', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    
    tools = db.relationship('Tool', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Tool(db.Model):
    __tablename__ = 'tools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(500), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    contributor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tool {self.name}>'


def get_category_id(category_name):
    """
    استعلام للحصول على معرف الفئة (ID) بناءً على اسمها
    
    Args:
        category_name (str): اسم الفئة المطلوبة
    
    Returns:
        int or None: معرف الفئة إذا وجدت، أو None إذا لم توجد
    """
    category = Category.query.filter_by(name=category_name).first()
    return category.id if category else None
    
def add_tools(name, description, link, category_id, contributor_id=None):
    """
    إضافة أداة جديدة مع تحقق شامل من البيانات
    
    Args:
        name (str): اسم الأداة
        description (str): وصف الأداة
        link (str): رابط الأداة
        category_id (int): معرف الفئة
        contributor_id (int, optional): معرف المستخدم المضيف
    
    Returns:
        dict: نتيجة العملية
    """
    try:
        # التحقق من البيانات المطلوبة
        if not all([name, description, link, category_id]):
            return {
                'success': False,
                'message': '❌ جميع الحقول مطلوبة (الاسم، الوصف، الرابط، الفئة)',
                'tool_id': None
            }
        
        # التحقق من صحة الرابط
        if not link.startswith(('http://', 'https://')):
            return {
                'success': False,
                'message': '❌ الرابط يجب أن يبدأ بـ http:// أو https://',
                'tool_id': None
            }
        
        # التحقق من وجود الفئة
        category = Category.query.get(category_id)
        if not category:
            return {
                'success': False,
                'message': f'❌ الفئة ذات المعرف {category_id} غير موجودة',
                'tool_id': None
            }
        
        # التحقق من عدم تكرار الرابط
        existing_tool = Tool.query.filter_by(link=link).first()
        if existing_tool:
            return {
                'success': False,
                'message': f'⚠️ الرابط مكرر - الأداة "{existing_tool.name}" تستخدم نفس الرابط',
                'tool_id': existing_tool.id
            }
        
        # التحقق من عدم تكرار الاسم (اختياري)
        existing_name = Tool.query.filter_by(name=name).first()
        if existing_name:
            return {
                'success': False,
                'message': f'⚠️ الاسم مكرر - توجد أداة أخرى بنفس الاسم',
                'tool_id': existing_name.id
            }
        
        # إنشاء الأداة الجديدة
        new_tool = Tool(
            name=name.strip(),
            description=description.strip(),
            link=link.strip(),
            category_id=category_id,
            contributor_id=contributor_id or 1,
            is_approved=True
        )
        
        # حفظ في قاعدة البيانات
        db.session.add(new_tool)
        db.session.commit()
        
        return {
            'success': True,
            'message': f'✅ تم إضافة الأداة "{name}" بنجاح وتحتاج موافقة المدير',
            'tool_id': new_tool.id,
            'tool': new_tool
        }
        
    except Exception as e:
        db.session.rollback()
        return {
            'success': False,
            'message': f'❌ خطأ في إضافة الأداة: {str(e)}',
            'tool_id': None
        }    