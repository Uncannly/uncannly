define("audio", function() { 

const AudioContext = window.AudioContext || window.webkitAudioContext;
const context = new AudioContext();

const spokenWords = []
const alreadySaved = []

return { context: context, spokenWords: spokenWords, alreadySaved: alreadySaved }

});