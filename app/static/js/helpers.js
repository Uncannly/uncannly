const poolDefault = $('.pool').attr("max")

const scoreThresholds = {
	'integral-product': '2.0 * 10^-7',
	'integral-sum': 		'1.2 * 10^-1',
	'mean-geometric': 	'2.0 * 10^-3',
	'mean-arithmetic': 	'3.4 * 10^-1'
}

const checked = function(mode, option) {
	return $(`.${mode} .${option}`).is(':checked');
};

const updateHint = function(mode, scoreThreshold) {
	$(`.${mode} .scoring`).attr('title', 
		`to return just over ${poolDefault} words with default settings, set threshold to ${scoreThreshold}.`
	)
}