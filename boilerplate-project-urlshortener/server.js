require('dotenv').config();
const express = require('express');
const cors = require('cors');
const app = express();
let urlMap = [];

// Basic Configuration
const port = process.env.PORT || 3000;

app.use(express.urlencoded({ extended: true }));

app.use(cors());

app.use('/public', express.static(`${process.cwd()}/public`));

app.get('/', function(req, res) {
  res.sendFile(process.cwd() + '/views/index.html');
});

// Your first API endpoint
app.get('/api/hello', function(req, res) {
  res.json({ greeting: 'hello API' });
});

app.post('/api/shorturl', function(req, res) {
  const url_input = req.body.url;

  let valid = /^(ftp|http|https):\/\/[^ "]+$/.test(url_input);

  if (!valid) {
    res.json({  error: 'invalid url' });
  } else {
    let found = false;
    let idx = 0;
    for (let i=0; i<urlMap.length; i++) {
      if (urlMap[i] == url_input) {
        found = true;
        idx = i;
      }
    }
    if (!found) {
      idx = urlMap.length;
      urlMap.push(url_input);
    }
    res.json({ original_url : url_input, short_url : idx});
  }
});

app.get('/api/shorturl/:surl', function(req, res) {
  console.log("req.surl: " + req.params.surl);
  let url = urlMap[req.params.surl];
  if (url != undefined) {
    res.redirect(url);
  } else {
    res.json({ error: 'Short url not found.' });
  }
});


app.listen(port, function() {
  console.log(`Listening on port ${port}`);
});
