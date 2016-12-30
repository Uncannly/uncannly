const requestWords = function(url, mode) {
  $(`#${mode}`).empty().append('<div class="loading">Loading...</div>');

  $.ajax({
    url: url,
    success: function(data) { 
      addWordRows(data, mode);
      $('.speak-word').click(speak);
    }
  });
}

const addWordRows = function(data, mode) {
  $(`#${mode}`).empty();
  JSON.parse(data).forEach(addWordRow.bind(mode));
}

const addWordRow = function(word, i) {
  if (word == window.noWordsMessage || word == window.tooFewMessage) {
    $(`#${this}`).append(`<div class="message">${word}</div>`);
  } else {
    $(`#${this}`).append(wordRow(word, i));
    new Clipboard(`#copy-word-${i}`);
  }
}

const wordRow = function(word, i) {
  return (`
    <div class="word" id="word-${i}">
      <i 
        class="fa fa-clipboard" 
        aria-hidden="true" 
        id="copy-word-${i}" 
        data-clipboard-target="#text-${i}"
      >
      </i>
      <i class="fa fa-volume-up speak-word" aria-hidden="true"></i>
      <div class="no-block word-text" id="text-${i}">${word}</div>
    </div>
  `)
}

const speak = function(e) {
  const target = e.target;
  const word = $(target).parent().text();
  const blob = SPOKEN_WORDS[word]
  if (blob) {
    ALREADY_SAVED[word] ? say(blob) : downloadSpeech(blob, target, word);
  } else {
    getSpeech(target, word)
  }
}

const getSpeech = function(target, word) {
  $(target).removeClass("fa fa-volume-up speak-word").addClass("fa fa-spinner fa-spin");

  const request = new XMLHttpRequest();
  request.open('GET', `https://uncannly-tts.cfapps.io/pts?word=${word}`, true);
  request.responseType = 'arraybuffer';
  request.onload = onLoadSpeech.bind(request, word, target);
  request.send();
}

const say = function(blob) {
  const fileReader = new FileReader();
  fileReader.onload = onReloadSpeech;
  fileReader.readAsArrayBuffer(blob);
}

const onLoadSpeech = function(word, target) {
  SPOKEN_WORDS[word] = new Blob([this.response], {type: "octet/stream"});
  window.context.decodeAudioData(this.response, function(buffer) {
    playSound(buffer);
    $(target).removeClass("fa fa-spinner fa-spin").addClass("fa fa-download");
  });
}

const onReloadSpeech = function() {
  window.context.decodeAudioData(this.result, function(buffer) {
    playSound(buffer);
  });
}

const playSound = function(buffer) {
  const source = window.context.createBufferSource();
  source.buffer = buffer;
  source.connect(window.context.destination);
  source.start(0); 
}

const downloadSpeech = function(blob, target, word) {
  saveAs(blob, 'uncannly.mp3');
  ALREADY_SAVED[word] = true;
  $(target).removeClass("fa fa-download").addClass("fa fa-volume-up speak-word");
}