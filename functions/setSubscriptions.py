from functions.firebaseInit import initFirebase
from firebase_admin import firestore
from flask import jsonify

# Initialize Firebase and Firestore
initFirebase()
db = firestore.client()
userRef = db.collection('users')
subscriptionRef = db.collection('admin').document("subscription")

def setNewSubscription(userId, newSubscription):
    try:
        userDoc = userRef.document(userId).get()
        if not userDoc.exists:
            raise ValueError(f"User ID {userId} does not exist")

        subscribed = userDoc.to_dict().get("subscription")
        userRef.document(userId).update({"subscription": newSubscription})
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
