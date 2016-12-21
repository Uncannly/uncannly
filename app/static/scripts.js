const present = function(data) {
	return JSON.parse(data).join('<br>');
};

const checked = function(mode, option) {
	return $(`.${mode} .${option}`).is(':checked');
};

const scoringMethods = [
	'integral-product', 'integral-sum', 'mean-geometric', 'mean-arithmetic'
];

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

['random', 'top'].forEach(function(mode) { modes(mode); });

$(".random .score-threshold").change(function(e) {
	const disable = e.target.value == '' || e.target.value == '0';
	const inputs = $(".random .scoring-method input");
	inputs.prop("disabled", disable);
	if (disable) {
		inputs.prop("checked", "");
		$(`.random .scoring`).attr('title', 
			'Choose a threshold and method to see suggested threshold settings.'
		)
	} else if (!inputs.is(':checked')) {
		$(".random .integral-product").prop("checked", "checked");
		updateHint('random', [ 1, 1, 1 ], [ 3, 8, 15 ]);
	}
});

const updateHint = function(mode, significands, powers) {
	$(`.${mode} .scoring`).attr(
		'title',
		[
			'for default settings:',
			`> 1 possibility: ${significands[0]} * 10^-${powers[0]}`,
			`> 100 possibilities:	${significands[1]} * 10^-${powers[1]}`,
			`> 10000 possibilities: ${significands[2]} * 10^-${powers[2]}`
		].join('\n')
	);
}

const addHintListener = function(mode, method, significands, powers) {
	$(`.${mode} .${method}`).change(function() {
		updateHint(mode, significands, powers)
	});
};

const altText = function(method, significands, powers) {
	['random', 'top'].forEach(function(mode) {
		addHintListener(mode, method, significands, powers);
	});
};

const significands = {
	'integral-product': [ 1,		1,	 1	 ],
	'integral-sum': 		[ 2,		1,	 6	 ],
	'mean-geometric': 	[ 1,		1,	 3	 ],
	'mean-arithmetic': 	[ 4.25, 3.1, 2.9 ]
}

const powers = {
	'integral-product': [ 3,	8,	15	],
	'integral-sum': 		[ 1,	1,	2		],
	'mean-geometric': 	[ 2,	3,	4		],
	'mean-arithmetic': 	[ 1,	1,	1		]
}

scoringMethods.forEach(function(method) { 
	altText(method, significands[method], powers[method])
})

updateHint('top', [ 1, 1, 1 ], [ 3, 8, 15 ]);