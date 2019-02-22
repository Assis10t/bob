const MongoClient = require('mongodb').MongoClient

const mongo_url = process.env.MONGO || 'mongodb://localhost:27017/db'

let client = null
let db = null

module.exports = () => {
    if (!client || !db) {
        throw new Error('Database connection has not been initialized.')
    }
    return db
}

const model = require('./model')

module.exports.init = async () => {
    client = new MongoClient(mongo_url, {
        useNewUrlParser: true
    })
    await client.connect()
    db = client.db
    try {
        await db
            .collection('bob_movement')
            .insertOne({ _id: 'movement', moving: false, markers: 1 })
            .catch(err => {})
    } catch (err) {
        console.log('Movment already in database')
        model
            .turnOff()
            .then(() => console.log('Robot Stopped'))
            .catch(err => console.error(err))
    }
    return db
}
