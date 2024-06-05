from flask import Flask, request, jsonify
from functions.setSubscriptions import newUserSub, setNewSubscription
from functions.timeManagement import fetch_time
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the webhook API!'}), 200

@app.route('/time',methods=['GET'])
def getTime():
    timeData =  fetch_time()
    return jsonify(timeData),200

@app.route('/webhook/callback/<string:uid>/<string:newSub>/<string:period>', methods=['GET', 'POST'])
def webhook(uid, newSub,period):

    try:
        
        if request.method == 'POST':
            if request.content_type != 'application/json':
                raise ValueError("Content-Type must be application/json")

            event = request.json
            if event is None:
                raise ValueError("No JSON payload provided")
            
            print(f'Received webhook (POST) for user ID {uid} with new subscription {newSub}:', event)
            
            return jsonify({'message': 'Webhook received via POST', 'result': result}), 200

        elif request.method == 'GET':
            print(f'Received webhook (GET) for user ID {uid} with new subscription {newSub}')
            result = setNewSubscription(userId=uid, newSubscription=newSub,period=period)
            return jsonify({'message': 'Webhook received via GET','result':result}), 200

    except ValueError as ve:
        print(f'ValueError: {ve}')
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(f'Exception: {e}')
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@app.route('/newUserSub/<string:userId>/<string:subscribe>/<string:period>',methods=['POST'])
def newSub(userId,subscribe,period):
    result = newUserSub(userId= userId,newSubscription= subscribe,period=period)
    return jsonify({'result':result,'message':'Webhook received via Post new User'}),200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True, port=500)
