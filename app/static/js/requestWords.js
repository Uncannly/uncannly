define('requestWords', ["jquery", "Clipboard", "filesaver", "audio"], 
    function($, Clipboard, saveAs, audio) { 

const requestWords = function(url, mode) {
    $(`#${mode}`).empty().append('<span class="message">Loading...</span>');

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
        $(`#${this}`).append(`<span class="message">${word}</span>`);
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
            <span class="word-text" id="text-${i}">${word[0]}</span>
            <span class="word-score">${word[1] ? word[1] : ''}</span>
        </div>
    `)
}

const speak = function(e) {
    const target = e.target;
    const word = $($(target).parent()).find('.word-text').text();
    const blob = audio.spokenWords[word]
    if (blob) {
        audio.alreadySaved[word] ? say(blob) : downloadSpeech(blob, target, word);
    } else {
        getSpeech(target, word)
    }
}

const getSpeech = function(target, word) {
    $(target).removeClass("fa fa-volume-up speak-word").addClass("fa fa-spinner fa-spin");

    const request = new XMLHttpRequest();
    request.open('GET', `https://uncannly-tts.douglasblumeyer.com/pts?word=${word}`, true);
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
    audio.spokenWords[word] = new Blob([this.response], {type: "octet/stream"});
    audio.context.decodeAudioData(this.response, function(buffer) {
        playSound(buffer);
        $(target).removeClass("fa fa-spinner fa-spin").addClass("fa fa-download");
    });
}

const onReloadSpeech = function() {
    audio.context.decodeAudioData(this.result, function(buffer) {
        playSound(buffer);
    });
}

const playSound = function(buffer) {
    const source = audio.context.createBufferSource();
    source.buffer = buffer;
    source.connect(audio.context.destination);
    source.start(0); 
}

const downloadSpeech = function(blob, target, word) {
    saveAs(blob, 'uncannly.mp3');
    audio.alreadySaved[word] = true;
    $(target).removeClass("fa fa-download").addClass("fa fa-volume-up speak-word");
}

return { requestWords: requestWords }

});