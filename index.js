// AUTHOR :: Siddharth Shah 2/26/22

// Establish Framework
const express = require('express')
const app = express();
const port = 3000;

// Handlebars
const hbs = require('hbs');
app.set('view engine', 'hbs');

// Python Process
const spawn = require('child_process').spawn;
var SUBJECT_ID = '1'
const ls = spawn('python', ['generateQs.py', SUBJECT_ID]);

[genTar, perTar, relTar] = [3,2,5] // Question breakdown


// parse through buffer data sent from python file
var [ques, ans] = [[], []]
var quesAns = []
var [numGen, numPer, numRel] = [0, 0, 0]
ls.stdout.on('data', (data) => {
    strStream = data.toString().split("\r\n");
    for (let i=0; i < strStream.length; i+=2) {
        if(strStream[i] == "PLACEHOLDER"){
            break;
        }
        ques.push(strStream[i])
        ans.push(strStream[i+1])
        quesAns.push([strStream[i], strStream[i+1]]);
    }
    numGen = Number(strStream[ strStream.length-4 ])
    numPer = Number(strStream[ strStream.length-3 ])
    numRel = Number(strStream[ strStream.length-2 ])
    // quesAns.splice(quesAns.length-1, 1); // delete empty idx at end of array
    console.log(quesAns) // FOR TESTING
});

ls.stderr.on('data', (data) => {
  console.log(`stderr: ${data}`);
});

ls.on('close', (code) => {
  console.log(`child process exited with code ${code}`);
});

// GET Requests
app.get('/', (req, res) => {
  res.send("Sample frontend GUI for Memory Rention " +
    "Questionaire -- by Siddharth Shah (VU '25')")
});

app.get('/home', (req, res) => {
    res.render('home')
});

app.get('/json', (req,res) => {
    res.json( {"data": quesAns, "numGen": numGen, 
        "numPer": numPer, "numRel": numRel} )
});

app.get('/all', (req,res) => {
    var obj = {}
    obj.quesLst = ques
    obj.ansLst = ans
    res.render('all', obj); /* hbs */
})

app.get('/quiz',(req,res) => {
    // Arrays holding displayed Q-and-A
    rQues = []
    rAns = []
    // Random General Questions
    rGenIdx = [];
    while(rGenIdx.length < genTar) {
        idx = Math.floor(Math.random() * numGen);
        if(!rGenIdx.includes(idx)) {
            rGenIdx.push(idx)
            rQues.push( ques[idx] )
            rAns.push( ans[idx] )
        }
    }
    // Random Personal Questions
    rPerIdx = [];
    while(rPerIdx.length < perTar) {
                // translate up by numGen
        idx = Math.floor(Math.random() * numPer) + numGen;
        if(!rPerIdx.includes(idx)) {
            rPerIdx.push(idx)
            rQues.push( ques[idx] )
            rAns.push( ans[idx] )
        }
    }
    // Random Relations Questions
    rRelIdx = [];
    while(rRelIdx.length < relTar) {
                // translate up by (numGen + numPer)
        idx = Math.floor(Math.random() * numRel) + (numGen + numPer);
        if(!rRelIdx.includes(idx)) {
            rRelIdx.push(idx)
            rQues.push( ques[idx] )
            rAns.push( ans[idx] )
        }
    }
    // Assign and render
    var obj = {}
    obj.rQuesLst = rQues
    obj.rAnsLst = rAns
    res.render('quiz', obj)
});

// Initialize Listener
app.listen(port, () => {
  console.log(`Express server started on port: ${port}!`)
});