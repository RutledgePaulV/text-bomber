$(document).ready(function () {

	$.ajaxSetup({
			crossDomain: false, beforeSend: function (xhr, settings) {
				if (!Utils.csrfSafeMethod(settings.type)) {
					xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
				}
			}
		}
	);

	_.UpdateDefinitions();

	var progressBar = $('#progress').progressbar({value: 0});

	$('#send').click(function () {

		_.registry.QUEUE_TEXTS.fire($('#form').serialize(), function (data) {

			if (data.status === 'SUCCESS') {

				var taskId = data.results[0].taskId;

				// fire off a request every second to update progress bar.
				setInterval(function () {
					_.registry.GET_PROGRESS.fire({taskId: taskId}, function (data) {
						var percentComplete = data.results[0].percentageComplete;
						progressBar.progressbar('value', percentComplete);
					});
				}, 1000);

			} else if (data.status === 'ERROR') {
				alert(data.error);
			}
		}, function (data) {

			alert("Could not complete communication with server.");

		});
	});
});