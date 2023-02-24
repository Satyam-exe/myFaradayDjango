import pyrebase

config = {
    'apiKey': "AIzaSyD-V1cl7LkMt-4Pq_N7dkfMnrNhw1vXS28",
    'authDomain': "myfaraday.firebaseapp.com",
    'databaseURL': "https://myfaraday-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "myfaraday",
    'storageBucket': "myfaraday.appspot.com",
    'messagingSenderId': "408458516517",
    'appId': "1:408458516517:web:06441d737e4238001ac7cc",
    'measurementId': "G-1XPH6VNLF9",
}
# Initialising database,auth and firebase for further use
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()
