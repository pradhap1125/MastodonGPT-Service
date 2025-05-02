from flask import Flask, jsonify, request, render_template

from mastodongpt.DbService import delete_link, get_links, login_dashboard
from mastodongpt.JwtAuthorizationFilter import jwt_required
from mastodongpt.LinkService import process_pdf, process_url
from mastodongpt.pdf_search_ollama import rag_query, clear_chat, load_data, clear_chat_schedule
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app,supports_credentials=True)
scheduler = BackgroundScheduler()


def refresh_data():
    with app.app_context():
        load_data()

def clear_storage():
    clear_chat_schedule()

scheduler.add_job(refresh_data, 'interval', days=1)  # Runs once every 24 hours
scheduler.add_job(clear_storage, 'interval', seconds=600)

scheduler.start()

@app.route('/app/chat', methods=['POST'])
def chat():
    data = request.get_json()
    sessionId= data.get('id')
    return rag_query(data['message'],sessionId)


@app.route('/app/clear', methods=['POST'])
def clear():
    data = request.get_json()
    sessionId= data.get('id')
    clear_chat(sessionId)
    return jsonify(message="Chat cleared!")

@app.route('/app/addFile', methods=['POST','OPTIONS'])
@cross_origin()
@jwt_required
def upload_pdf():
    user = request.jwt_payload.get("name", "unknown")
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    return process_pdf(file)

@app.route('/app/addweburl', methods=['POST','OPTIONS'])
@cross_origin()
@jwt_required
def upload_webUrl():
    user = request.jwt_payload.get("name", "unknown")
    data = request.get_json()

    return process_url(data['url'])

@app.route('/app/getLinks', methods=['GET'])
@cross_origin()
@jwt_required
def links():
    user = request.jwt_payload.get("name", "unknown")
    return jsonify(get_links())

@app.route('/app/deleteLinks', methods=['POST'])
@cross_origin()
@jwt_required
def delete():
    user = request.jwt_payload.get("name", "unknown")
    data = request.get_json()
    return delete_link(data['id'])

@app.route("/app/login", methods=["POST"])
def login():
    data = request.get_json()
    return login_dashboard(data)

if __name__ == '__main__':
     refresh_data()
     app.run(debug=True)


