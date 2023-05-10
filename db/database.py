import os
from supabase import create_client
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv('.env')

supabase_url = os.environ.get("SUPABASE_URL")
assert supabase_url, "SUPABASE_URL not set"
supabase_key = os.environ.get("SUPABASE_KEY")
assert supabase_key, "SUPABASE_KEY not set"
supabase = create_client(supabase_url, supabase_key)

db = SQLAlchemy()