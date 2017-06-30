"""
__name__		= config.py
__author__		= Cheetrios
__description__ = Flask global config parameters
"""

WTF_CSRF_ENABLED = True
SECRET_KEY       = "you'-ll-never-know"
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '1312089722235483',
        'secret': 'bccb52b81daa2c64dec3c59207871f1e'
    }
}
ALLOWED_EXTENSIONS = set(['mp3'])