import os

# 数据库路径与当前目录同级
base_dir = os.path.dirname(os.path.abspath(__file__))
dev_db = 'sqlite:///' + base_dir + "/data.db"
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = os.getenv('SECRET_KEY', 'admin123')
# 应用配置
POST_COUNT = 5
CATALOG_COUNT = 5
RECENT_POST_COUNT = 3
RECENT_COMMENT_COUNT = 3
