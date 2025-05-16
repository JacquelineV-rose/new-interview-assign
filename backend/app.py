from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)

# Load data once when the app starts
with open(os.path.join("data", "api_result.json")) as f:
    materials = json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/material/<material_id>')
def show_material(material_id):
    return render_template('details.html')

@app.route('/api/materials')
def api():
    return jsonify(materials)

if __name__ == '__main__':
    app.run(debug=True)
