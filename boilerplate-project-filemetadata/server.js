var express = require('express');
var cors = require('cors');
require('dotenv').config()

const multer = require('multer');

var storage = multer.diskStorage({   
   destination: function(req, file, cb) { 
      cb(null, './uploads');    
   }, 
   filename: function (req, file, cb) {
/*    
      fileName = file.originalname;
      fileType = file.mimetype;
      fileSize = file.size;
*/    

      cb(null , file.originalname);   
   }
});
var upload = multer({ storage: storage }).single("upfile");

var app = express();


app.use(cors());
app.use('/public', express.static(process.cwd() + '/public'));

app.get('/', function (req, res) {
    res.sendFile(process.cwd() + '/views/index.html');
});

app.post("/api/fileanalyse", (req, res) => {
  upload(req, res, (err) => {
    if(err) {
      res.status(400).send("Something went wrong!");
    }
    const fileName = req.file.originalname;
    const fileType = req.file.mimetype;
    const fileSize = req.file.size;
    console.log("******************");
    console.log(fileName);
    console.log(fileType);
    console.log(fileSize);
    console.log("******************");
    res.json({name: fileName, type: fileType, size: fileSize});
  });
});


const port = process.env.PORT || 3000;
app.listen(port, function () {
  console.log('Your app is listening on port ' + port)
});
