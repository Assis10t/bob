const express = require('express')

const PORT = process.argv[2] || 9000

const app = express()

app.get('/', (req, res) => {
    res.send('Hello World!')
})

app.listen(PORT, () => console.log(`Listening on port ${PORT}.`))
