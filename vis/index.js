const app = require('express')();
const execSync  = require('child_process').execSync;
const bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({extended: false}));
app.use(bodyParser.json());

app.set('views', './views');
app.set('view engine', 'hbs');
app.set('view options', { layout: 'layout'});

app.post('/parse', (req, res) => {
    if (!req.body) {
        return res.sendStatus(400);
    }

    let input = req.body.input + "\n" + req.body.output;
    let output = JSON.parse(execSync('./parse.py', { input: input }));
    if (output) {
        return res.render('view', {data: JSON.stringify(output) });
    }
});

app.get('/', (req, res) => {
    res.render('index');
})

app.listen(process.argv.PORT || 3000, () => {
    console.log("Listening on " + (process.argv.PORT || 3000));
});
