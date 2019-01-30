# Firebase Functions Deployment

Firebase functions deploy from a node.js app (_I think_). This means that your
changes won't propagate unless you deploy them to the server.


## Usage

### Set Up

In order to deploy Firebase apps from your machine, you must first install the
packages needed.

```
$ npm install firebase firebase-functions firebase-admin
```

### Writing Functions

To write a function, add it to the index.js file.

**This is a bad solution! We need a better way to do this to prevent Git hell!!!**

### Enabling Deployment

In order to deploy your amazing functions you must first log in to Firebase.
```
$ firebase login
```
This will prompt you to enter your details. If you have not been given access to the project please contact Oktay. Once you have logged in, you will be able to deploy functions to Firebase.

**It is very important when deploying that you only deploy your function incase you have broken another!**
```
$ firebase deploy --only functions:<YOUR_FUNCTION>
```
