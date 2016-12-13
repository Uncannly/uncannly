const present = function(data, mode) {
    return mode == 'words' ? JSON.parse(data).join('<br>') : data.slice(1, -1);
};

const checked = function(mode, option) {
    return $(`.${mode} .${option}`).is(':checked');
};

const scoringMethods = [
    'integral-product', 'integral-sum', 'mean-geometric', 'mean-arithmetic'
];

const modes = function(mode) {
    $(`.${mode} button.refresh`).click(function() {
        let url = `/${mode}`;
        const data = [];

        const returnCount = $(`.${mode} .return-count`).val();
        if (returnCount) data.push(`return-count=${returnCount}`);

        scoringMethods.forEach(function(method) {
            if (checked(mode, method)) data.push(`scoring-method=${method}`);
        });

        const scoreThresholdPower = $(`.${mode} .score-threshold-power`).val();
        const scorePower = Math.pow(10, parseInt(scoreThresholdPower));
        const scoreThreshold = $(`.${mode} .score-threshold`).val() * scorePower;
        scoreThreshold && data.push(`score-threshold=${scoreThreshold}`);

        const randomSelectionValue = $(`.${mode} .random-selection-value`).val();
        if (randomSelectionValue !== '' && checked(mode, 'random-selection')) {
            data.push(`random-selection=${randomSelection}`);
        }

        if ($(`.${mode} .unweighted`).is(':checked')) data.push('unweighted');

        if ($(`.${mode} .exclude-real`).is(':checked')) data.push('exclude-real');

        if (data.length > 0) url += '?' + data.join('&');

        $(`#${mode}`).html('Loading...');
        $.ajax({
            url: url,
            success: function(data) { $(`#${mode}`).html(present(data, mode)); }
        });
    });

    new Clipboard(`#copy-${mode}`);
};

['random-word', 'words'].forEach(function(mode) { modes(mode); });

$(".random-word .score-threshold").change(function(e) {
    $(".random-word .scoring-method input").prop("disabled", e.target.value == '');
});

$(".words .random-selection").change(function(e) {
    if (this.checked) {
        $(".random-selection-value").prop("disabled", false)
        if ($(".random-selection-value").val() == '') {
            $(".random-selection-value").val(1000000)
        }
    } else {
        $(".random-selection-value").prop("disabled", true)
    }
});