from flask import Flask, request, Response, render_template
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    value = db.Column(db.String(120))

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    all_data = Data.query.all()
    return render_template('index.html', data=all_data)


@app.route('/api/records', methods=['GET'])
def get_records():
    all_data = Data.query.all()
    records = [{'id': item.id, 'name': item.name, 'value': item.value} for item in all_data]
    response_json = json.dumps(records)
    return Response(response_json, status=200, mimetype='application/json')


@app.route('/api/records', methods=['POST'])
def create_record():
    if request.is_json:
        data = request.get_json()
        new_data = Data(name=data['name'], value=data['value'])
        db.session.add(new_data)
        db.session.commit()
        
        response_data = {"message": "Record created"}
        response_json = json.dumps(response_data)
        return Response(response_json, status=201, mimetype='application/json')
    else:
        error_data = {"error": "Request must be JSON"}
        error_json = json.dumps(error_data)
        return Response(error_json, status=400, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)

