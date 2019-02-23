const db = require('./db')
const robotPathfinding = require('./robot-pathfinding')
const assert = require('assert')
const ObjectID = require('mongodb').ObjectID
const factory = db => ({
    getAllOrders: () =>
        new Promise((res, rej) => {
            db()
                .collection('orders')
                .find({})
                .toArray((err, docs) => {
                    err ? rej(err) : res(docs)
                })
        }),
    getOrderById: orderId =>
        new Promise((res, rej) => {
            db()
                .collection('orders')
                .find({ _id: orderId })
                .toArray((err, docs) => {
                    err ? rej(err) : res(docs[0])
                })
        }),
    addOrder: orderData =>
        new Promise((res, rej) => {
            db()
                .collection('orders')
                .insertOne(orderData, (err, order) => {
                    if (err) {
                        rej(err)
                        return
                    }
                    Promise.all(orderData.items.map(i => factory(db).removeItem(i)))
                        .then(() => factory(db).turnOn(1))
                        .then(() => res(orderData))
                        .catch(err => rej(err))
                })
        }),
    addJob: jobData =>
        new Promise((res, rej) => {
            db()
                .collection('jobs')
                .insertOne(jobData, (err, job) => {
                    err ? rej(err) : res(jobData)
                })
        }),
    getAllJobs: () =>
        new Promise((res, rej) => {
            db()
                .collection('jobs')
                .find({})
                .toArray((err, docs) => {
                    err ? rej(err) : res(docs)
                })
        }),
    turnOn: markers =>
        new Promise((res, rej) => {
            db()
                .collection('bob_movement')
                .updateOne(
                    { _id: 'movement' },
                    { $set: { moving: true, markers: parseInt(markers) } },
                    (err, count_modified) => {
                        err ? rej(err) : res('on')
                    }
                )
        }),
    turnOff: () =>
        new Promise((res, rej) => {
            db()
                .collection('bob_movement')
                .updateOne({ _id: 'movement' }, { $set: { moving: false } }, (err, count_modified) => {
                    err ? rej(err) : res('off')
                })
        }),
    getMovement: () =>
        new Promise((res, rej) => {
            db()
                .collection('bob_movement')
                .find({})
                .toArray((err, docs) => {
                    err ? rej(err) : res(docs[0])
                })
        }),

    addItem: item =>
        new Promise((res, rej) => {
            db()
                .collection('inventory')
                .insertOne({ _id: new ObjectID(), ...item }, (err, item) => {
                    err ? rej(err) : res(item)
                })
        }),
    removeItem: item =>
        new Promise((res, rej) => {
            db()
                .collection('inventory')
                .deleteOne({ _id: item._id}, (err, item) => {
                    err ? rej(err) : res(item)
                })
        }),
    getItems: () =>
        new Promise((res, rej) => {
            db()
                .collection('inventory')
                .find({})
                .toArray((err, items) => {
                    err ? rej(err) : res(items)
                })
        }),
    createUser: (uname, pass) =>
        new Promise((res, rej) => {
            db()
                .collection('users')
                .insertOne({ _id: new ObjectID(), username: uname, password: pass }, (err, user) => {
                    err ? rej(err) : res(user)
                })
        }),
    authUser: (uname, pass) =>
        new Promise((res, rej) => {
            db()
                .collection('users')
                .find({ username: uname, password: pass })
                .toArray((err, users) => {
                    console.log(users)
                    err ? rej(err) : res(users.length > 0)
                })
        }),
    setHome: (robot_id,home_x,home_y) => 
        new Promise((res, rej) => {
            db()
                .collection('robot')
                .updateOne({_id : robot_id}, {$set: {"home_x": home_x, "home_y":home_y}}, (err, warehouse) => {
                    err ? rej(err) : res(warehouse);
                });
        }),
    addRobot: (robot_id, home_x, home_y) =>
        new Promise((res,rej) => {
            db()
                .collection('robot')
                .insertOne(
                            {   
                                _id: robot_id, 
                                home_x:home_x,
                                home_y:home_y,
                                location: {
                                    x:0,
                                    y:0,
                                    z:0
                                }
                            }, (err,robot) => {
                    err ? rej(err) : res(robot)
                });
        }),
    getNextJob: (robot_id) =>
        new Promise((res,rej) => {
            db().collection('robot')
            .find({"_id":robot_id})
            .toArray((err,robot) => {
                if (err) {
                    rej(err)
                } else {
                    db()
                        .collection('warehouse')
                        .find({})
                        .toArray((err,warehouse) => {
                            db()
                                .collection('orders')
                                .updateOne({"status":"PENDING"}, {$set:{"status":"IN_TRANSIT"}}, (err, order) => {
                                    console.log(err)
                                    if (err) {
                                        rej(err)
                                    } else {
                                        res(robotPathfinding.get_robot_path(order,robot[0],warehouse[0]))   
                                    }
                                })          
                        })
                }
            })
        })
})

module.exports = factory(db)

module.exports.factory = factory
