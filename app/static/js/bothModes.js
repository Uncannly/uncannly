const scoringMethods = [
  'integral-product', 'integral-sum', 'mean-geometric', 'mean-arithmetic'
]

const addModeListeners = function(mode) {
  addRefreshListener(mode);
  addSelectionListener(mode);
  addPoolAndSelectionBoundsListeners(mode);
  new Clipboard(`#copy-${mode}`);
};

const addRefreshListener = function(mode) {
  $(`.${mode} button.refresh`).click(function() {
    let url = `/${mode}`;
    const data = [];

    const pool = $(`.${mode} .pool`).val();
    if (pool) data.push(`pool=${pool}`);

    scoringMethods.forEach(function(method) {
      if (checked(mode, method)) data.push(`scoring-method=${method}`);
    });

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

    $(`#${mode}`).html('Loading...');
    $.ajax({
      url: url,
      success: function(data) { 
        JSON.parse(data).forEach(function(word) {
          $(`#${mode}`).append(`<div class="word-to-speak">${word}</div>`);
        });

        $('.word-to-speak').click(function(e) {
          const word = e.target.textContent;
          const request = new XMLHttpRequest();
          request.open('GET', `https://uncannly-tts.cfapps.io/pts?word=${word}`, true);
          request.responseType = 'arraybuffer';

          request.onload = function() {
            context.decodeAudioData(request.response, function(buffer) {
              var source = context.createBufferSource();
              source.buffer = buffer;
              source.connect(context.destination);
              source.start(0); 
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

modes = ['random', 'top']

modes.forEach(function(mode) {
  addModeListeners(mode);

  scoringMethods.forEach(function(method) { 
    $(`.${mode} .${method}`).change(function() {
      updateHint(mode, scoreThresholds[method])
    });
  });
})