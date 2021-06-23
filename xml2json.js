fs = require("fs");
var parser = require("xml2json");

fs.readFile(
  "C:/ahmed/official-cpe-dictionary_v2.3/official-cpe-dictionary_v2.3.xml",
  function (err, data) {
    var json = parser.toJson(data);
    console.log(json);
  } 
);
  