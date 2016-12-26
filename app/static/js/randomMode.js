const updateScoringMethod = function(options) {
  const scoreThresholdIsOff = !parseFloat(options.scoreThreshold)
  const selectionIsOff = !options.selection
  const disableScoringMethod = scoreThresholdIsOff && selectionIsOff

  const scoringMethod = $("select[name=random-scoring-method]");
  scoringMethod.prop("disabled", disableScoringMethod);

  if (disableScoringMethod) {
    $(`.random .scoring`).attr('title', 
      'Choose a threshold and method to see suggested threshold settings.'
    )
  } else {
    updateHint('random', scoreThresholds[scoringMethod.val()]);
  }
}

$(".random .selection").change(function() {
  updateScoringMethod({
    scoreThreshold: $(".random .score-threshold").val(),
    selection: checked('random', 'selection')
  })
});

$(".random .score-threshold").change(function(e) {
  updateScoringMethod({
    scoreThreshold: e.target.value, 
    selection: checked('random', 'selection')
  })
});