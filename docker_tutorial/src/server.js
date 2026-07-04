const express = require('express'); 
const app = express();

app.get('/', (re,res)=>{
    res.send("Welcome to my homescreen!");
})

app.listen(3000, function() {
    console.log("app listenting on port 3000")
}); 