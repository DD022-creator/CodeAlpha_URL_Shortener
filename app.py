from flask import Flask, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)

# Generate Short Code
def generate_short_code():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=6))

# Homepage
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>URL Shortener</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; text-align: center; }
        input { padding: 10px; width: 70%; }
        button { padding: 10px 20px; background: blue; color: white; border: none; cursor: pointer; }
        .short-url { margin-top: 20px; padding: 10px; background: #f0f0f0; }
    </style>
</head>
<body>
    <h1>🔗 URL Shortener</h1>
    <form method="POST">
        <input type="url" name="long_url" placeholder="Enter your long URL" required>
        <button type="submit">Shorten</button>
    </form>
    {% if short_code %}
    <div class="short-url">
        <p>Short URL: <a href="/{{ short_code }}">http://localhost:5000/{{ short_code }}</a></p>
    </div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        short_code = generate_short_code()
        new_url = URL(long_url=long_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        return render_template_string(HTML_TEMPLATE, short_code=short_code)
    return render_template_string(HTML_TEMPLATE, short_code=None)

# Redirect Route
@app.route('/<short_code>')
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        return redirect(url.long_url)
    return "URL not found", 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)