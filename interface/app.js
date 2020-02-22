const express = require('express')
const app = express()
const router = express.Router();
const port = 8888

router.get('/', (req, res) => {
    res.sendFile(__dirname + 'html/index.html')
})

router.get('/dev', (req, res) => {
    res.sendFile(__dirname + 'html/index.html');
})

app.use('/', router);
app.listen(port, () => console.log(`App listening on port ${port}`))