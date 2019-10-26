import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import exceptions

# Use a service account
cred = credentials.Certificate('./fireapp-58e6e-firebase-adminsdk-9zyak-1c7a34bb01.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# doc_ref = db.collection(u'users').document(u'aturing2')
# doc_ref.set({
#     u'first': u'Alan',
#     u'middle': u'Mathison',
#     u'last': u'Turing',
#     u'born': 1912
# })

reviewCounRef = db.collection(u'ReviewCount').document(u'qlhNCPyY28nmo7lUHJEa')
try:
    doc = reviewCounRef.get()
    data = doc.to_dict()
    firebaseReviewCount = data['amount']
    print(u'Document data: {}'.format(doc.to_dict()))
except exceptions.NotFound:
    print(u'No such document!')

print(5)