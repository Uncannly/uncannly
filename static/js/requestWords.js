define('requestWords', ["jquery", "Clipboard"],
    function($, Clipboard) {

const requestWords = function(url, mode) {
    $(`#${mode}`).empty().append('<span class="message">Loading...</span>');

    $.ajax({
        url: url,
        success: function(data) {
            addWordRows(data, mode);
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
            <span class="word-text" id="text-${i}">${word[0]}</span>
            <span class="word-score">${word[1] ? word[1] : ''}</span>
        </div>
    `)
}

return { requestWords: requestWords }

});