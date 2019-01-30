const functions = require('firebase-functions');


// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions
//
exports.createUser = functions.firestore
    .document('orders/{orderID}')
    .onCreate((snap, context) => {
      return snap.ref.set({
        name: "BOB"
      }, {merge: true});
    });
