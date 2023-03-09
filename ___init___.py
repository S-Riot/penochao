from flask import Flask, render_template, request, flash, Markup, redirect, url_for
from app import app, db
from app.models import User

app = Flask(__name__)
app.secret_key = 'dev'

if __name__ == '__main__':
    app.run(debug=True)
    
if __name__ == "__main__":
    app.debug = True
    app.run()