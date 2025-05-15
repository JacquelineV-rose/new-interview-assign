from flask import Flask, jsonify, render_template
import json
import os

app = Flask(__name__)



data_file = os.path.join(os.path.dirname(__file__), 'data', 'api_result.json')

with open(data_file, 'r') as f:
    materials_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/material/<material_id>')
def material_detail(material_id):
    return render_template('details.html')

@app.route('/api/materials')
def get_materials():
    return jsonify(materials_data)

if __name__ == '__main__':
    app.run(debug=True)
