const fs = require("fs");

class CPEAnalyzer {
  constructor(props) {

    const xmlData = fs.readFileSync(props.database).toString("utf-8")

    const x2j = require('rapidx2j');
    const options = {
      attr_group: false,
      attr_prefix: '@',
      ignore_attr: false,
      empty_tag_value: null,
      parse_boolean_values: true,
      parse_int_numbers: true,
      parse_float_numbers: true,
      preserve_case: false,
      explicit_array: false,
      skip_parse_when_begins_with: '',
      value_key: 'keyValue'
    };
    const json = x2j.parse(xmlData, options);
    console.log(JSON.stringify(json))
  }
}/*
new CPEAnalyzer({
  database: "./official-cpe-dictionary_v2.3/official-cpe-dictionary_v2.3.xml",
});


*/



const {chain}  = require('stream-chain');
 
const {parser} = require('stream-json');
const {streamValues} = require('stream-json/streamers/StreamValues');
 

const pipeline = chain([
  fs.createReadStream("C:\\ahmed\\official-cpe-dictionary_v2.3\\official-cpe-dictionary_v2.3.json") ,
  ,(...Ars) =>{
   return (Ars[0].toString("utf-8"));
  },
  parser(),
  streamValues(),
  data => {
    const value = data.value;
    // keep data only for the accounting department
    return value && value.department === 'accounting' ? data : null;
  }
]);
 
let counter = 0;
pipeline.on('data', () => ++counter);
pipeline.on('end', () =>
  console.log(`The accounting department has ${counter} employees.`));