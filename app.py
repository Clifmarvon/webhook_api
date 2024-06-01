from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the webhook API!'}), 200

@app.route('/webhook/callback', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        event = request.json
        print('Received webhook (POST):', event)
        return jsonify({'message': 'Webhook received via POST'}), 200
    elif request.method == 'GET':
        print('Received webhook (GET)')
        return jsonify({'message': 'Webhook received via GET'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
