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