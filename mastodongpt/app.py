from flask import Flask, jsonify, request, render_template
from mastodongpt.pdf_search_ollama import rag_query, clear_chat


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/app/chat', methods=['POST'])
def chat():
    data = request.get_json()
    return rag_query(data['message'])


@app.route('/app/clear')
def clear():
    clear_chat()
    return jsonify(message="Chat cleared!")

if __name__ == '__main__':
     app.run(debug=True)
