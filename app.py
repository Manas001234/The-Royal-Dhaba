from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'royal-dhaba-secret-key-change-this-later')

# ---------- GOOGLE OAUTH SETUP ----------
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/item1')
def item1():
    return render_template('item1.html')

@app.route('/item2')
def item2():
    return render_template('item2.html')

@app.route('/item3')
def item3():
    return render_template('item3.html')

@app.route('/item4')
def item4():
    return render_template('item4.html')

@app.route('/item5')
def item5():
    return render_template('item5.html')

@app.route('/item6')
def item6():
    return render_template('item6.html')

@app.route('/item7')
def item7():
    return render_template('item7.html')

@app.route('/item8')
def item8():
    return render_template('item8.html')

@app.route('/payment')
def payment():
    return render_template('payment.html')


# ---------- GOOGLE LOGIN ROUTES (naye) ----------

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('auth_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/auth/callback')
def auth_callback():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    if user_info:
        session['user'] = {
            'name': user_info.get('name'),
            'email': user_info.get('email'),
            'picture': user_info.get('picture')
        }
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ---------- CART ROUTES (purane) ----------

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')

    cart = session.get('cart', [])

    # agar item already cart me hai to quantity +1 karo
    found = False
    for item in cart:
        if item['name'] == name:
            item['quantity'] += 1
            found = True
            break
    if not found:
        cart.append({'name': name, 'price': price, 'quantity': 1})

    session['cart'] = cart
    return jsonify({'status': 'ok'})


@app.route('/get_cart')
def get_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return jsonify({'cart': cart, 'total': total})


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = []
    return jsonify({'status': 'cleared'})


if __name__ == '__main__':
    app.run(debug=True)