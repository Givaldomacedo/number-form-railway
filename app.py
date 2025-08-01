from flask import Flask, render_template, request
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables from file if present

app = Flask(__name__)

# MySQL config from environment (Railway variables or local .env)
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': int(os.getenv('MYSQL_PORT', '3306'))
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        number = request.form.get('number')
        if not number:
            return "Please provide a number.", 400

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS numbers (id INT AUTO_INCREMENT PRIMARY KEY, value INT NOT NULL)")
            cursor.execute("INSERT INTO numbers (value) VALUES (%s)", (number,))
            conn.commit()
            cursor.close()
            conn.close()
            return "Number saved successfully!"
        except Exception as e:
            return f"Error saving number: {e}", 500

    return render_template('form.html')

# Optional: quick check route for debugging
@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    # For local development; in Railway use the Procfile (gunicorn)
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8080')), debug=True)
