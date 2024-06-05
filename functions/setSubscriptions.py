from functions.firebaseInit import initFirebase
from firebase_admin import firestore

from functions.timeManagement import fetch_time


initFirebase()
db = firestore.client()
userRef = db.collection('users')
subscriptionRef = db.collection('admin').document("subscription")

def setNewSubscription(userId, newSubscription,period):
    try:
        userDoc = userRef.document(userId).get()
        if not userDoc.exists:
            raise ValueError(f"User ID {userId} does not exist")

        subscribed = userDoc.to_dict().get("subscription")
        timeData = fetch_time()
       
        userRef.document(userId).update({"subscription": {
            "subscribed":newSubscription,
            "startingDate":timeData["current_time"],
            "endingDate":timeData[period],
            "period":period
        }})
        subscriptionRemove(userId, subscribed)

        return {"status": "success", "userId": userId, "newSub": newSubscription}
    except Exception as e:
        print(f'Error in setNewSubscription: {e}')
        return {"status": "error", "message": str(e)}

def subscriptionRemove(userId, subscribed):
    try:
        subDoc = subscriptionRef.get()
        if not subDoc.exists:
            raise ValueError("Subscription document does not exist")

        subscriptions = subDoc.to_dict().get("items", [])
        for subs in subscriptions:
            if subs["id"] == subscribed:
                subs["subscribers"].remove(userId)
                subscriptionRef.update({"items": subscriptions})

        return {"status": "success"}
    except Exception as e:
        print(f'Error in subscriptionRemove: {e}')
        return {"status": "error", "message": str(e)}


def newUserSub(userId,newSubscription,period):
    try:
        timeData = fetch_time()
        userRef.document(userId).update({"subscription": {
               "subscribed":newSubscription,
               "startingDate":timeData["current_time"],
               "endingDate":timeData[period],
               "period":period
           }})
        return {"status":'success'}
    except Exception as e:
        return {"status": "error", "message": str(e)}