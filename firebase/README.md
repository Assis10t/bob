# Firebase Functions Deployment

Firebase functions deploy from a node.js app (_I think_). This means that your
changes won't propagate unless you deploy them to the server.

In order to deploy Firebase apps from your machine, you must first install the
packages needed.

```
$ npm install firebase firebase-functions firebase-admin
```

Once installation is complete, you can deploy to the firebase functions.

```
$ firebase deploy --only functions:<NAME_OF_FUNCTION>
```

More to come as we learn how this works...
