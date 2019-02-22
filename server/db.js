const MongoClient = require('mongodb').MongoClient
const MongoMemoryServer = require('mongodb-memory-server').MongoMemoryServer
const FAKE_DB = process.env.DB === 'fake'
const MONGO_URL = process.env.MONGO || 'mongodb://localhost:27017/db'

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
    let mongo_url = MONGO_URL
    if (FAKE_DB) {
        console.log('Using fake mongo in memory.')
        const mongod = new MongoMemoryServer()
        mongo_url = await mongod.getConnectionString()
    } else {
        console.log('Using real mongo at ' + mongo_url)
    }
    client = new MongoClient(mongo_url, {
        useNewUrlParser: true
    })
    await client.connect()
    db = client.db('bob')
    try {
        await db.collection('bob_movement').insertOne({ _id: 'movement', moving: false, markers: 1 })
    } catch (err) {
        console.log('Movment already in database')
        await model
            .turnOff()
            .then(() => console.log('Robot Stopped'))
            .catch(err => console.error(err))
    }
    return db
}
