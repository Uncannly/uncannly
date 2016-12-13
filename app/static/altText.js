// random-word

$(".random-word .integral-product").change(function() {
    $('.random-word .scoring').attr(
        'title',
        [
            'for default settings:',
            '> 1 possibility: 1 * 10^-3',
            '> 100 possibilities:  1 * 10^-8',
            '> 10000 possibilities: 1 * 10^-15',
            '> 1000000 possibilities: 1 * 10^-22'
        ].join('\n')
    )
});

$(".random-word .integral-sum").change(function() {
    $('.random-word .scoring').attr(
        'title',
        [
            'for default settings:',
            '> 1 possibility: 2 * 10^-1',
            '> 100 possibilities: 1 * 10^-1',
            '> 10000 possibilities: 6 * 10^-2',
            '> 1000000 possibilities: 4 * 10^-2'
        ].join('\n')
    )
});

$(".random-word .mean-geometric").change(function() {
    $('.random-word .scoring').attr(
        'title',
        [
            'for default settings:',
            '> 1 possibility: 1 * 10^-2',
            '> 100 possibilities: 1 * 10^-3',
            '> 10000 possibilities: 3 * 10^-4',
            '> 1000000 possibilities: 1 * 10^-4'
        ].join('\n')
    )
});

$(".random-word .mean-arithmetic").change(function() {
    $('.random-word .scoring').attr(
        'title',
        [
            'for default settings:',
            '> 1 possibility: 4.25 * 10^-1',
            '> 100 possibilities: 3.1 * 10^-1',
            '> 10000 possibilities: 2.95 * 10^-1',
            '> 1000000 possibilities: 2.415 * 10^-1'
        ].join('\n')
    )
});

// words

$(".words .integral-product").change(function() {
    $('.words .scoring').attr(
        'title',
        [
            'for default settings:',
            '> 1 possibility: 1 * 10^-3',
            '> 100 possibilities:  1 * 10^-8',
            '> 10000 possibilities: 1 * 10^-15',
            '> 1000000 possibilities: 1 * 10^-22'
        ].join('\n')
    )
});

$(".words .integral-sum").change(function() {
    $('.words .scoring').attr(
        'title',
        [
            'for default settings:',
            '> 1 possibility: 2 * 10^-1',
            '> 100 possibilities: 1 * 10^-1',
            '> 10000 possibilities: 6 * 10^-2',
            '> 1000000 possibilities: 4 * 10^-2'
        ].join('\n')
    )
});

$(".words .mean-geometric").change(function() {
    $('.words .scoring').attr(
        'title',
        [
            'for default settings:',
            '> 1 possibility: 1 * 10^-2',
            '> 100 possibilities: 1 * 10^-3',
            '> 10000 possibilities: 3 * 10^-4',
            '> 1000000 possibilities: 1 * 10^-4'
        ].join('\n')
    )
});

$(".words .mean-arithmetic").change(function() {
    $('.words .scoring').attr(
        'title',
        [
            'for default settings:',
            '> 1 possibility: 4.25 * 10^-1',
            '> 100 possibilities: 3.1 * 10^-1',
            '> 10000 possibilities: 2.95 * 10^-1',
            '> 1000000 possibilities: 2.415 * 10^-1'
        ].join('\n')
    )
});