var FORM, PROGRESS_BAR;

/**
 * This handler allows us to kick off the progress bar and it will
 * make the appropriate requests and update itself until it reaches
 * one hundred percent.
 *
 * @param batchPk
 */
var updateProgressBar = function (batchPk) {
	_.registry.GET_PROGRESS.fire({batchPk: batchPk, others:[5,6,7]}, function (data) {
		var percentComplete = data.results[0].percent * 100;
		PROGRESS_BAR.progressbar('value', percentComplete);
		if(percentComplete === 100) {
			$('.sending').hide();
			$('.complete').show();
		}
		else{
			setTimeout(function(){updateProgressBar(batchPk);}, 1000);
		}
	});
};


/**
 * This handler submits the form and then begins updating the progress bar.
 */
var submitForm = function () {

	var payload ={
		number: '6512450907',
		message: 'Hi Paul!',
		provider: 1,
		count: 5
	};
	_.registry.QUEUE_TEXTS.fire(payload, function (data) {
			FORM.hide();
			$('.sending').show();
			updateProgressBar(data.results[0].batchPk);
	})
};

$(document).ready(function () {

	var csrfSafeMethod = function(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};

	/**
	 * Inject CSRF token into all ajax requests.
	 */
	$.ajaxSetup({
			crossDomain: false, beforeSend: function (xhr, settings) {
				if (!csrfSafeMethod(settings.type)) {
					xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
				}
			}
		}
	);

	/**
	 * Request the available ajax commands.
	 */
	_.UpdateDefinitions();

	// setting a couple globals for reference in callbacks
	FORM = $('.form');
	PROGRESS_BAR = $('#progress');

	// initializing the progress bar.
	PROGRESS_BAR.progressbar({value: 0});

	// hiding currently irrelevant areas
	$('.complete').hide();
	$('.sending').hide();

	/**
	 * Adding the click handler onto the submit button.
	 */
	$('#send').click(submitForm);

});