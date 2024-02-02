import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore_async
from firebase_admin import auth
from firebase_admin import firestore
from datetime import date
 
today = str(date.today())

# Initialize an firbase account
cred = credentials.Certificate('/Users/erkangxia/Downloads/whatsappchatbot-fabc9-firebase-adminsdk-mryvt-2bce3645a3.json')
app = firebase_admin.initialize_app(cred)

db = firestore.client()

def firebase_sign_up(email, password):
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return user.uid
    except Exception as e:
        return str(e)

def firebase_sign_in(email, password):
    # Firebase Admin SDK doesn't support sign-in operations.
    # You would normally use Firebase Authentication SDK in a client app.
    # For CLI, consider an alternative method like custom token generation.
    pass

def get_user_by_uid(uid):
    try:  
        return auth.get_user(uid)
    except firebase_admin.auth.UserNotFoundError:
        return "No user found for the provided UID."
    except Exception as e:
        return f"An error occurred: {e}"
    
def add_task(uid,task,time, repeat):
    event_ref = db.collection("user").document(uid).collection("date").document(today).collection("task").document(task)
    try:
        event_ref.set({"repeat": repeat,"time":time})
        return("task has been set")
    except:
        return("an error occured, try again later")
        
    