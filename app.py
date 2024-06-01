from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook/callback', methods=['POST'])
def webhook():
    event = request.json
    print('Received webhook:', event)
   
    return jsonify({'message': 'Webhook received'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
