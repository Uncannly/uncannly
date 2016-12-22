const updateScoringMethodInputs = function(options) {
	const scoreThresholdIsOff = !parseFloat(options.scoreThreshold)
	const selectionIsOff = !options.selection
	const disableScoringMethodInputs = scoreThresholdIsOff && selectionIsOff

	const inputs = $(".random .scoring-method input");
	inputs.prop("disabled", disableScoringMethodInputs);

	if (disableScoringMethodInputs) {
		inputs.prop("checked", "");
		$(`.random .scoring`).attr('title', 
			'Choose a threshold and method to see suggested threshold settings.'
		)
	} else if (!inputs.is(':checked')) {
		$(".random .integral-product").prop("checked", "checked");
		updateHint('random', scoreThresholds['integral-product']);
	}
}

$(".random .selection").change(function() {
	updateScoringMethodInputs({
		scoreThreshold: $(".random .score-threshold").val(),
		selection: checked('random', 'selection')
	})
});

$(".random .score-threshold").change(function(e) {
	updateScoringMethodInputs({
		scoreThreshold: e.target.value, 
		selection: checked('random', 'selection')
	})
});