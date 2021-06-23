const { default: parse } = require('mvn-artifact-name-parser')
const fs = require("fs")


const readline = require("readline")
const jsonStream = require('JSONStream')

var rd = readline.createInterface({ input: fs.createReadStream("./reduced/echantillion-artifact-names.txt") });

var out = jsonStream.stringifyObject();
const jsonFileStream = fs.createWriteStream("./reduced/echantillion-artifact-names.json")
out.pipe(jsonFileStream);

rd.on('line', function (line) {
    try {
        out.write([line, parse(line)]);
    } catch (e) {
        console.log({ e });
    }
});

rd.on("close", function () { out.end(); })

