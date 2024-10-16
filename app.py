
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create an SQLite database to store orders
def init_db():
    with sqlite3.connect('orders.db') as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, phone TEXT, address TEXT, items TEXT, total INTEGER
            )
        """)
init_db()

# Home route to display the form
@app.route('/', methods=['GET', 'POST'])
def order():
    items = {
        'Shenguli Che Laadoo': 800,
        'Dinka Che Laadoo (Dry fruits)': 1000,
        'Sweet Shankarpali': 500,
        'Salty Shankarpali': 500,
        'Khawyachi (Mawa) Karanji': 1000,
        'Gulab Jamun': 600
    }
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        selected_items = request.form.getlist('items')
        total = sum(int(items[item]) * int(request.form[item + '_qty']) for item in selected_items)

        # Save the order to the database
        with sqlite3.connect('orders.db') as conn:
            conn.execute("""
                INSERT INTO orders (name, phone, address, items, total) VALUES (?, ?, ?, ?, ?)
            """, (name, phone, address, ', '.join(selected_items), total))

        # Redirect to UPI payment link
        return redirect(f'upi://pay?pa=9284549845@upi&pn=Diwali%20Sweets&am={total}&cu=INR')

    return render_template('order.html', items=items)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
