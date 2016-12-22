const present = function(data) {
	return JSON.parse(data).join('<br>');
};

const checked = function(mode, option) {
	return $(`.${mode} .${option}`).is(':checked');
};

const scoringMethods = [
	'integral-product', 'integral-sum', 'mean-geometric', 'mean-arithmetic'
];

const selectionModes = ['random', 'top']

$("input[name='mode']").change(function(e){
	if($(this).val() == 'random') {
		$('.random').css({display: 'block'});
		$('.top').css({display: 'none'});
	} else {
		$('.top').css({display: 'block'});
		$('.random').css({display: 'none'});
	}
});

const modes = function(mode) {
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
		if (selectionValue !== '' && checked(mode, 'selection')) {
			data.push(`selection=${selectionValue}`);
		}

		if ($(`.${mode} .unweighted`).is(':checked')) data.push('unweighted');
		if ($(`.${mode} .unstressed`).is(':checked')) data.push('unstressed');
		if ($(`.${mode} .exclude-real`).is(':checked')) data.push('exclude-real');

		if (data.length > 0) url += '?' + data.join('&');

		$(`#${mode}`).html('Loading...');
		$.ajax({
			url: url,
			success: function(data) { $(`#${mode}`).html(present(data)); }
		});
	});

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

	$(`.${mode} .selection-value`).change(function(e) {
		$(`.${mode} .pool`).attr("min", e.target.value);
	});

	$(`.${mode} .pool`).change(function(e) {
		$(`.${mode} .selection-value`).attr("max", e.target.value);
	});

	new Clipboard(`#copy-${mode}`);
};

selectionModes.forEach(function(mode) { modes(mode); });

$(".random .selection").change(function(e) {
	updateScoringMethodInputs({
		scoreThreshold: $(".random .score-threshold").val(),
		selection: this.checked
	})
});

$(".random .score-threshold").change(function(e) {
	updateScoringMethodInputs({
		scoreThreshold: e.target.value, 
		selection: $(".random .selection").is(':checked')
	})
});

const updateScoringMethodInputs = function(options) {
	const scoreThresholdIsOff = options.scoreThreshold == '' || options.scoreThreshold == '0'
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

const updateHint = function(mode, scoreThreshold) {
	$(`.${mode} .scoring`).attr('title', 
		`to return just over 45 words with default settings, set threshold to ${scoreThreshold}.`
	)
}

const scoreThresholds = {
	'integral-product': '2.0 * 10^-7',
	'integral-sum': 		'1.2 * 10^-1',
	'mean-geometric': 	'2.0 * 10^-3',
	'mean-arithmetic': 	'3.4 * 10^-1'
}
	
selectionModes.forEach(function(mode) {
	scoringMethods.forEach(function(method) { 
		$(`.${mode} .${method}`).change(function() {
			updateHint(mode, scoreThresholds[method])
		});
	});
})

updateHint('top', scoreThresholds['integral-product']);

$("body").keyup(function(e){
	if (e.keyCode == 13) {
		const mode = $("input[name='mode']:checked").val()
		console.log(mode)
		$(`.${mode} button.refresh`).click();
	}
});