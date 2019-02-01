const domain_gen = require('./domain-generator/DomainGenerator.js');
const functions = require('firebase-functions');


exports.onCreate = functions.firestore
    .document('orders/{orderID}')
    .onCreate((snap, context) => {
      return snap.ref.set({
        name: "BOB"
      }, {merge: true});
    });
