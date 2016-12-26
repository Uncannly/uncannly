const scoringMethods = [
  'integral-product', 'integral-sum', 'mean-geometric', 'mean-arithmetic'
]

const addRefreshListener = function(mode) {
  $(`.${mode} button.refresh`).click(function() {
    let url = `/${mode}`;
    const data = [];

    const pool = $(`.${mode} .pool`).val();
    if (pool) data.push(`pool=${pool}`);

    if (!$(`select[name=${mode}-scoring-method]`).prop('disabled')) {
      const val = $(`select[name=${mode}-scoring-method]`).val();
      data.push(`scoring-method=${val}`);
    };

    const scoreThresholdPower = $(`.${mode} .score-threshold-power`).val();
    const scorePower = Math.pow(10, parseInt(scoreThresholdPower));
    const scoreThreshold = $(`.${mode} .score-threshold`).val() * scorePower;
    scoreThreshold && data.push(`score-threshold=${scoreThreshold}`);

    const selectionValue = $(`.${mode} .selection-value`).val();
    if (checked(mode, 'selection')) {
      data.push(`selection=${selectionValue == '' ? pool : selectionValue}`);
    }

    ['unweighted', 'unstressed', 'exclude-real'].forEach(function(option) {
      if (checked(mode, option)) { data.push(option); };
    })

    if (data.length > 0) url += '?' + data.join('&');

    $(`#${mode}`).empty().append('<div class="loading">Loading...</div>');
    $.ajax({
      url: url,
      success: function(data) { 
        $(`#${mode}`).empty();
        JSON.parse(data).forEach(function(word, i) {
          if (word == window.noWordsMessage || word == window.tooFewMessage) {
            $(`#${mode}`).append(`<div class="message">${word}</div>`);
          } else {
            $(`#${mode}`).append(
              `<div class="word" id="word-${i}">
                <i 
                  class="fa fa-clipboard" 
                  aria-hidden="true" 
                  id="copy-word-${i}" 
                  data-clipboard-target="#text-${i}"
                >
                </i>
                <i class="fa fa-volume-up speak-word" aria-hidden="true"></i>
                <div class="no-block word-text" id="text-${i}">${word}</div>
              </div>`
            );
            new Clipboard(`#copy-word-${i}`);
          }
        });

        $('.speak-word').click(function(e) {
          const word = $(e.target).parent().text();
          $(e.target).removeClass("fa fa-volume-up speak-word");
          $(e.target).addClass("fa fa-spinner fa-spin");
          const request = new XMLHttpRequest();
          request.open('GET', `https://uncannly-tts.cfapps.io/pts?word=${word}`, true);
          request.responseType = 'arraybuffer';

          request.onload = function() {
            context.decodeAudioData(request.response, function(buffer) {
              var source = context.createBufferSource();
              source.buffer = buffer;
              source.connect(context.destination);
              source.start(0); 
              $(e.target).removeClass("fa fa-spinner fa-spin");
              $(e.target).addClass("fa fa-volume-up speak-word");
            });
          }
          request.send();
        });
      }
    });
  });
}

const addSelectionListener = function(mode) {
  $(`.${mode} .selection`).change(function(e) {
    if (this.checked) {
      $(`.${mode} .selection-value`).prop("disabled", false);

      const selectionValue = parseInt($(`.${mode} .selection-value`).val());
      const pool = parseInt($(`.${mode} .pool`).val());
      let value;
      if (selectionValue > pool) {
        value = pool;
      } else if (selectionValue == '') {
        value = pool < 10 ? pool : 10;
      }

      value && $(`.${mode} .selection-value`).val(value);
    } else {
      $(`.${mode} .pool`).attr("min", 1)
      $(`.${mode} .selection-value`).prop("disabled", true);
    }
  });
}

const addPoolAndSelectionBoundsListeners = function(mode) {
  $(`.${mode} .selection-value`).change(function(e) {
    $(`.${mode} .pool`).attr("min", e.target.value);
  });

  $(`.${mode} .pool`).change(function(e) {
    $(`.${mode} .selection-value`).attr("max", e.target.value);
  });
}

const addScoringMethodListener = function(mode) {
  $(`select[name=${mode}-scoring-method]`).change(function(e) {
    updateHint(mode, scoreThresholds[e.target.value])
  });
}

modes = ['random', 'top']

modes.forEach(function(mode) {
  addRefreshListener(mode);
  addSelectionListener(mode);
  addPoolAndSelectionBoundsListeners(mode);
  addScoringMethodListener(mode);
})