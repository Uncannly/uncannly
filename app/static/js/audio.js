window.AudioContext = window.AudioContext || window.webkitAudioContext;
const context = new AudioContext();

SPOKEN_WORDS = []
ALREADY_SAVED = []