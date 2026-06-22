import os

# Support Render.com disk mount
if os.environ.get("RENDER"):
    DB_PATH = "/app/data/foodloop.db"
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "foodloop.db")

SECRET_KEY = os.environ.get("SECRET_KEY", "foodloop-secret-key-change-in-production")
JWT_EXPIRATION_HOURS = int(os.environ.get("JWT_EXPIRATION_HOURS", 24))
PLATFORM_FEE_PCT = int(os.environ.get("PLATFORM_FEE_PCT", 15))
