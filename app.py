from flask import Flask, render_template_string, request, redirect, url_for, session
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

PASSWORD = 'plaque!'

STARTER_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Access</title>
    <style>
        html, body {
            height: 100%;
        }
        body {
            min-height: 100vh;
            margin: 0;
            background: #09090c;
            color: #c0c0c0;
            font-family: monospace, monospace;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        input[type="text"] {
            background: #18181b;
            color: #c0c0c0;
            border: 1px solid #222226;
            border-radius: 3px;
            padding: 0.5rem 0.8rem;
            font-size: 1rem;
            margin-bottom: 1rem;
            outline: none;
        }
        input[type="text"]:focus {
            background: #1a1a1e;
            border: 1px solid #333336;
        }
        button {
            background: #18181b;
            color: #c0c0c0;
            border: 1px solid #222226;
            border-radius: 3px;
            padding: 0.5rem 1.5rem;
            font-size: 1rem;
            cursor: pointer;
        }
        button:hover {
            background: #23232a;
            color: #fff;
        }
        .error {
            color: #a33;
            margin-bottom: 0.8rem;
            font-size: 0.95rem;
        }
    </style>
</head>
<body>
    {% if error %}<div class="error">{{ error }}</div>{% endif %}
    <form method="post">
        <input type="text" name="password" autofocus required autocomplete="off">
        <button type="submit">check</button>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def starter():
    error = None
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('protected'))
        else:
            error = 'wrong key.'
    return render_template_string(STARTER_HTML, error=error)

@app.route('/protected')
def protected():
    if not session.get('authenticated'):
        return redirect(url_for('starter'))
    return '<h2 style="color:#c0c0c0;background:#09090c;height:100vh;display:flex;align-items:center;justify-content:center;font-family:monospace,monospace;">access granted</h2>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
