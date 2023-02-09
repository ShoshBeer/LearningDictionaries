// const engDictionary = require('./kaikki.org-dictionary-English-most-senses-10.json');
const bfj = require('bfj');
const fs = require('fs');

// const dataStream = bfj.match(fs.createReadStream('./sampleDict.jsonl'), "word", { ndjson: true });
//returns words but there are more keys with word in deeper elements and they are also returned

// dataStream.on('data', item => {console.log(item)});


const dataStream = bfj.read('./kaikki.org-dictionary-English-most-senses-10.json', { ndjson: true })
  .then(data => {
    if (data["pos"] == "adj") {
      console.log(data);
    }
  })
  .catch(error => {
    console.log(error);
  })



// const writePackage = require('graceful-fs');

// function filterWords(dictionary) {
//   let count = 0;
//   for (let lines = 0; lines < dictionary.length(); lines++) {
//     count++;
//   }
//   // const singleWords = dictionary.filter(entry => !entry.word.includes(' '));
//   return count;
// }

// console.log(filterWords(engDictionary));

