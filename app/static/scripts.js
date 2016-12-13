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
    const disable = e.target.value == '' || e.target.value == '0'
    $(".random-word .scoring-method input").prop("disabled", disable);
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

const addListener = function(mode, method, significands, powers) {
    $(`.${mode} .${method}`).change(function() {
        $(`.${mode} .scoring`).attr(
            'title',
            [
                'for default settings:',
                `> 1 possibility: ${significands[0]} * 10^-${powers[0]}`,
                `> 100 possibilities:  ${significands[1]} * 10^-${powers[1]}`,
                `> 10000 possibilities: ${significands[2]} * 10^-${powers[2]}`,
                `> 1000000 possibilities: ${significands[3]} * 10^-${powers[3]}`
            ].join('\n')
        );
    });
};

const altText = function(method, significands, powers) {
    ['random-word', 'words'].forEach(function(mode) {
        addListener(mode, method, significands, powers);
    });
};

altText('integral-product', [ 1,    1,   1,   1   ], [ 3,  8,  15, 22 ]);
altText('integral-sum',     [ 2,    1,   6,   4   ], [ 1,  1,  2,  2  ]);
altText('mean-geometric',   [ 1,    1,   3,   1   ], [ 2,  3,  4,  4  ]);
altText('mean-arithmetic',  [ 4.25, 3.1, 2.9, 2.4 ], [ 1,  1,  1,  1  ]);