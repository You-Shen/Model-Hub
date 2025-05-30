# reset_db.py
from app import app
from models import db, User, Feedback, Conversations
from werkzeug.security import generate_password_hash
def reset_database():
    with app.app_context():
        # 删除所有表
        db.drop_all()
        print("所有表已删除")
        # 重新创建所有表
        db.create_all()
        print("所有表已重新创建")
        # 创建管理员用户
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', is_admin=True)
            admin.password = 'admin'  # 使用加密密码
            db.session.add(admin)
            db.session.commit()
            print("✅ 管理员用户已创建（用户名：admin，密码：admin）")
        else:
            print("⚠️ 管理员用户已存在，无需重复创建")

if __name__ == '__main__':
    reset_database()
