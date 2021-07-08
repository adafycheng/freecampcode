const express = require('express')
const app = express()
const cors = require('cors')
const fs = require("fs");
const uuid = require('uuid')
require('dotenv').config()

app.use(express.urlencoded({ extended: true }));
app.use(cors())
app.use(express.static('public'))
app.use(express.static('data')); 

// Data files
const userLogFileName = "/data/users.txt";
const exerciseLogFileName = "/data/exercises.txt";

let users = [];
let exercises = [];

function readUsers() {
    fs.readFile(__dirname + userLogFileName, "utf-8", (err, data) => {
      if (err) {
        console.log(err);
      } else {
        // Converting to JSON
        users = JSON.parse(data);
      }

  })
}

// Exercises
function readExercies() {
    fs.readFile(__dirname + exerciseLogFileName, "utf-8", (err, data) => {
      if (err) {
        console.log(err);
      } else {
        // Converting to JSON
        exercises = JSON.parse(data);          
      }

  })
}

readUsers();
readExercies();

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/views/index.html')
});

app.get('/api/users', (req, res) => {
  readUsers();
  res.json(users);
});

app.post('/api/users', (req, res) => {
  const username = req.body.username;

  var result = users.filter(item => item.username.toLowerCase() == username.toLowerCase());

  if (result.length > 0) {
    // Return an existing user
    res.send("Username already taken");
  } else {
    // Create a new user
    let uid = uuid.v1();
    uid = uid.replace(/-/g, "");
    let user = {"_id": uid, "username": username};
    users.push(user);

    // Write created user into file.
    fs.writeFile(__dirname + userLogFileName, JSON.stringify(users), err => {
        // Checking for errors
        if (err) {
          console.log(err); 
        }
    });

    res.json(user);
  }
  
});

// Get logs by User ID
app.get('/api/users/:_id/logs', (req, res) => {
  const userId = req.params._id;

  const result = users.filter(item => item._id == userId);


  if (result.length > 0) {
    // User found
    // 1. Filter by User ID
    var result2 = exercises.filter(item => item._id == userId);

    // 2. Filter by Date From
    if (req.query.from != undefined) {
      result2 = result2.filter(item => item.date >= req.query.from);
    }

    // 3. Filter by Date To
    if (req.query.to != undefined) {
      result2 = result2.filter(item => item.date <= req.query.to);
    }

    // 4. Filter by Limit
    if (req.query.limit != undefined) {
      result2 = result2.slice(0, req.query.limit);
    }

    let finalResult = [];
    // Convert output date
    for (let i=0; i<result2.length; i++) {
      let exercise = result2[i];
      exercise.date = convertToOutputDate(exercise.date);
      finalResult.push(exercise);
    }

    let logs = {"_id": userId, "username": result[0].username, "count": finalResult.length, "log": finalResult};

    res.json(logs);
  } else {
    // User ID not found
    res.send("User ID " + userId + " is not found.");
  }

});

// Submit exercise by User ID
app.post('/api/users/:_id/exercises', (req, res) => {
  const userId = req.params._id;
  var result = users.filter(item => item._id == userId);

  if (result.length > 0) {
    // User found
    const description = req.body.description;
    const duration = req.body.duration;
    let exdate = req.body.date;

    if ((description == "") || (typeof description === 'undefined')) {
      return res.send('Path `description` is required.');
    }

    if ((duration == "") || (typeof duration === 'undefined')) {
      return res.send('Path `duration` is required.');
    }

    if (isNaN(duration)) {
      return res.send('Cast to Number failed for value "gfdgfsd" at path "duration"');
    }


    if ((exdate == "") || (typeof exdate === 'undefined')) {
      // Date not found. Use current date.
      exdate = getCurrentDate();
    } else {
      try {
        let exerciseDate = new Date(exdate);
      } catch (e) {
        // Invalid date
        exdate = getCurrentDate();
      }
    }

    const finalDate = exdate;
    let exercise = result[0];
    exercise.date = finalDate;
    exercise.duration = eval(duration);
    exercise.description = description;
    exercises.push(exercise);

    // Write exercise into file.
    fs.writeFile(__dirname + exerciseLogFileName, JSON.stringify(exercises), err => {
        // Checking for errors
        if (err) {
          console.log(err); 
        }
    });

    // Format output
    let outputDate = convertToOutputDate(finalDate);
    let outputExercise = {...exercise};
    outputExercise.date = outputDate;

    res.json(outputExercise);
  } else {
    // Uesr ID not found.
    res.send("User ID " + userId + " is not found.");
  }
});

function convertToOutputDate(inputDate) {
  let returnDate = new Date(inputDate).toString();
  let dateArr = returnDate.split(" 00:00:00");
  return dateArr[0];
}

function getCurrentDate() {
    let current_datetime = new Date();
    let month = current_datetime.getMonth() + 1;
    if (month < 10) {
      month = "0" + month;
    }
    let day = current_datetime.getDate();
    if (day < 10) {
      day = "0" + day;
    }
    let today = current_datetime.getFullYear() + "-" + month + "-" + day;

    return today;
}

const listener = app.listen(process.env.PORT || 3000, () => {
  console.log('Your app is listening on port ' + listener.address().port)
})