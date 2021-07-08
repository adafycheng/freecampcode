// server.js
// where your node app starts

// init project
var express = require('express');
var app = express();

// enable CORS (https://en.wikipedia.org/wiki/Cross-origin_resource_sharing)
// so that your API is remotely testable by FCC 
var cors = require('cors');
app.use(cors({optionsSuccessStatus: 200}));  // some legacy browsers choke on 204

// http://expressjs.com/en/starter/static-files.html
app.use(express.static('public'));

// http://expressjs.com/en/starter/basic-routing.html
app.get("/", function (req, res) {
  res.sendFile(__dirname + '/views/index.html');
});


// your first API endpoint... 
app.get("/api/hello", function (req, res) {
  res.json({greeting: 'hello API'});
});

// Accepts path params
app.get("/api/:date?", function(req, res) {
  const reqDate = req.params.date;
  const regEx = /\D/g;
  let respDate = new Date();
  try {
    console.log(reqDate);
    if (reqDate != undefined) {
      if (!regEx.test(reqDate)) {
        console.log("parsing 1");
        respDate.setTime(reqDate);
      } else {
        console.log("parsing 2");
        respDate = new Date(reqDate);
      }
    }
    console.log(respDate);
    if (respDate == "Invalid Date") {
      res.json({ error : "Invalid Date" });
    } else {
      res.json({unix: respDate.getTime(), utc: respDate.toUTCString()});
    }
  } catch (e) {
    res.json({ error : "Invalid Date" });
  }
});



// listen for requests :)
var listener = app.listen(process.env.PORT, function () {
  console.log('Your app is listening on port ' + listener.address().port);
});
