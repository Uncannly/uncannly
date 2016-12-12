$(".random-word button.refresh").click(function(e) {
    let url = '/random-word'
    const data = []
    if ($(".random-word .unweighted").is(':checked')) data.push('unweighted')
    if ($(".random-word .exclude-real").is(':checked')) data.push('exclude-real')
    if (data.length > 0) url += '?' + data.join('&')

    $.ajax({
        url: url,
        success: function(result) {
            $("#random-word").html(result);
        }
    });
});

$(".words button.refresh").click(function(e) {
    let url = '/words'
    const data = []
    const returnCount = $(".words .return-count").val()
    if (returnCount) data.push(`return-count=${returnCount}`)
    if ($(".words .mean-arithmetic").is(':checked')) data.push("mean-arithmetic")
    if ($(".words .random-selection").is(':checked')) data.push("random-selection")
    if ($(".words .unweighted").is(':checked')) data.push('unweighted')
    if ($(".words .exclude-real").is(':checked')) data.push('exclude-real')
    if (data.length > 0) url += '?' + data.join('&')

    $("#words").html('Loading...')
    $.ajax({
        url: url,
        success: function(result) {
            $("#words").html(JSON.parse(result).join('<br>'));
        }
    });
});

new Clipboard('#copy-random-word');
new Clipboard('#copy-words');