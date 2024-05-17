from config.default import *

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(
    os.path.join(BASE_DIR, 'pybo.db')
)

SQLALCHEMY_TRACK_MODIFICATIONS=False

SECRET_KEY=b'\xfb-\xb1\t\xe9[\xaaX\x98x)@\xc4\x85\xec\x98'