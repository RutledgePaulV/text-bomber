var Utils = (function (Utils) {

	Utils.getFileName = function (filePath) {
		var fullName = Utils.getFullFileName(filePath);
		var extension = Utils.getFileExtension(fullName);
		return fullName.replace(extension, '');
	};

	Utils.getFullFileName = function (filePath) {
		return filePath.substr(filePath.lastIndexOf('/') + 1);
	};

	Utils.getFileExtension = function (fileName) {
		return fileName.substr(fileName.lastIndexOf('.'));
	};

	Utils.format = function (text) {
		var args = [].slice.call(arguments, 1);
		for (var index = 0; index < args.length; index++) {
			text = text.replace("{" + index + "}", args[index]);
		}
		return text;
	};

	Utils.csrfSafeMethod = function(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	};

	Utils.hitch = function(context, func){
		return function(){
			func.apply(context, arguments);
		};
	};

	return Utils;
})(Utils || {});