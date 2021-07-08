var express = require('express');
var bodyParser = require('body-parser');
var app = express();
console.log("Hello World");

app.use(bodyParser.urlencoded({extended: false}));

// Middleware function
app.get("*", function(req, res, next) {
  console.log(req.method + " " + req.path + " - " + req.ip);
  next();
});

// Chained Middleware function
app.get('/now', function(req, res, next) {
  let now = new Date();
  // the time is 3 minutes lagging behind freeCodeCamp
  now.setHours(now.getHours()+8);
  req.time = now.toString();
  
  console.log("now1: " + req.time);
  next();
}, function(req, res) {
  console.log("now2: " + req.time);
  res.json({"time": req.time});
});

// Accepts path params
app.get("/:word/echo", function(req, res) {
  console.log(req.params.word);
  res.json({"echo": req.params.word});
});

// Query params
app.get("/name", function(req, res) {
  console.log(req.query);
  let query = req.query;
  res.json({"name": query.first + " " + query.last});
});

// Post params
app.post("/name", function(req, res) {
  const body = req.body;

  res.json({"name": body.first + " " + body.last});
});

// Serve a static file
app.get("/", function(req, res) {
  res.sendFile(__dirname + "/views/index.html");
});

// Make a folder public
app.use("/public", express.static(__dirname + "/public"));

// Serve JSON data
app.get("/json", function(req, res) {
  let message = "Hello json";
  if (process.env.MESSAGE_STYLE == "uppercase") {
    message = message.toUpperCase();
  }
  res.json({"message": message});
});




































 module.exports = app;
