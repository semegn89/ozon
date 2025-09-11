"""
WSGI entry point for Vercel deployment
"""
from api import app

# This is the entry point for Vercel
application = app

if __name__ == "__main__":
    app.run()
