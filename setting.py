from decouple import config

# Load environment variables
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_SERVER = config("DB_SERVER")
DB_NAME = config("DB_NAME")

# Database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
