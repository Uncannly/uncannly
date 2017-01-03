require(["jquery", "helpers", "requestWords"], function($, helpers, requestWords) { 

const scoringMethods = [
    'integral-product', 'integral-sum', 'mean-geometric', 'mean-arithmetic'
];

const otherOptions = [
    'unweighted', 'unstressed', 'exclude-real', 'ignore-position', 'ignore-length'
];

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
        if (helpers.checked(mode, 'selection')) {
            data.push(`selection=${selectionValue == '' ? pool : selectionValue}`);
        }

        otherOptions.forEach(function(option) {
            if (helpers.checked(mode, option)) { data.push(option); };
        })

        const minLength = $(`.${mode} .min-length`).val();
        const maxLength = $(`.${mode} .max-length`).val();
        if (minLength) data.push(`min-length=${minLength}`);
        if (maxLength) data.push(`max-length=${maxLength}`);

        if (data.length > 0) url += '?' + data.join('&');
        
        requestWords.requestWords(url, mode);
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

const addBoundsListeners = function(mode, lesser, greater) {
    $(`.${mode} .${lesser}`).change(function(e) {
        $(`.${mode} .${greater}`).attr("min", e.target.value || 0);
    });

    $(`.${mode} .${greater}`).change(function(e) {
        $(`.${mode} .${lesser}`).attr("max", e.target.value);
    });
}

const addScoringMethodListener = function(mode) {
    $(`select[name=${mode}-scoring-method]`).change(function(e) {
        helpers.updateHint(mode, helpers.scoreThresholds[e.target.value])
    });
}

modes = ['random', 'top']

modes.forEach(function(mode) {
    addRefreshListener(mode);
    addSelectionListener(mode);
    addBoundsListeners(mode, 'selection-value', 'pool');
    addBoundsListeners(mode, 'min-length', 'max-length');
    addScoringMethodListener(mode);
});

});