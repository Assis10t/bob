const RobotConnection = require('./RobotConnection')

RobotConnection.getInstance().onData(data => {
    console.log(data)
})
