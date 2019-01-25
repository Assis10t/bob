const realNet = require('net')

const robotConnectionFactory = net =>
    class RobotConnection {
        constructor() {
            this.onConnectedListeners = []
            this.onDataListeners = []
            this.server = net.createServer(socket => {
                this.isConnected = true
                this.onConnectedListeners.forEach(listener => listener())

                socket.on('data', data => {
                    this.onDataListeners.forEach(listener =>
                        listener(data.toString())
                    )
                    //TODO: Parse the data before notifying listener.
                })

                socket.on('end', () => {
                    this.isConnected = false
                    console.log('Client disconnected.')
                })
            })

            this.server.listen(8000, () => {
                console.log('Server is listening.')
            })
        }

        onConnected(listener) {
            this.onConnectedListeners.push(listener)
            if (this.isConnected) {
                listener()
            }
        }

        onData(listener) {
            this.onDataListeners.push(listener)
        }
    }

module.exports = robotConnectionFactory(realNet)

module.exports.factory = robotConnectionFactory
