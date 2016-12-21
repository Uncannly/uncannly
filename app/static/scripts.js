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
	} else if (!inputs.is(':checked')) {
		$(".integral-product").prop("checked", "checked");
	}
});

const addListener = function(mode, method, significands, powers) {
	$(`.${mode} .${method}`).change(function() {
		$(`.${mode} .scoring`).attr(
			'title',
			[
				'for default settings:',
				`> 1 possibility: ${significands[0]} * 10^-${powers[0]}`,
				`> 100 possibilities:	${significands[1]} * 10^-${powers[1]}`,
				`> 10000 possibilities: ${significands[2]} * 10^-${powers[2]}`
			].join('\n')
		);
	});
};

const altText = function(method, significands, powers) {
	['random', 'top'].forEach(function(mode) {
		addListener(mode, method, significands, powers);
	});
};

altText('integral-product', [ 1,		1,	 1	 ], [ 3,	8,	15	]);
altText('integral-sum',			[ 2,		1,	 6	 ], [ 1,	1,	2		]);
altText('mean-geometric',		[ 1,		1,	 3	 ], [ 2,	3,	4		]);
altText('mean-arithmetic',	[ 4.25, 3.1, 2.9 ], [ 1,	1,	1		]);