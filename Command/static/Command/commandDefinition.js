var _ = (function (_) {

	/**
	 * Constructs a command object to be passed to the command service.
	 *
	 * @param {string} name The command key that the server will respond to.
	 * @param {object.<string,*>} [params] The required parameters for the command.
	 * @param {object.<string,*>} [defaults] Any defaults that should be applied.
	 * @constructor
	 */
	_.Command = function (name, params, defaults) {
		this.name = name.toUpperCase();
		this.params = params || {};
		this.defaults = defaults || {};
	};

	/**
	 * A factory method to take a backend result from the list of available commands
	 * and generate a command object out of it.
	 *
	 * @param {object} def
	 * @returns {Command}
	 */
	_.Command.fromServer = function (def) {
		var params = {}, defaults = {};
		for (var index in def.params) {
			if (def.params.hasOwnProperty(index)) {
				var param = def.params[index];
				params[param.name] = {type: param.type, required: param.required};
				if (param.default !== undefined) {
					defaults[param.name] = param.default;
				}
			}
		}
		return new _.Command(def.name, params, defaults);
	};

	/**
	 * @lends _.Command
	 */
	_.Command.prototype = {

		constructor: _.Command,

		/**
		 * Executes a command and appropriately calls the success and failure callbacks.
		 *
		 * @param {object} [data]
		 * @param {function} [success]
		 * @param {function} [failure]
		 */
		fire: function (data, success, failure) {
			_.ExecuteCommand(this, data, success, failure);
		},

		/**
		 * Builds the data request given some input data for the specific command and any defaults that were defined.
		 * Any data that is passed in takes preference over the defaults if they share a key.
		 *
		 * @param data
		 * @returns {object}
		 */
		buildData: function (data) {
			var commandData = $.extend(true, {}, this.defaults, data);
			commandData.command = this.name;
			return commandData;
		},

		/**
		 * Returns a more readable representation of a command definition. Does not include defaults.
		 *
		 * @returns {string}
		 */
		toString: function () {
			var params = [];
			for (var key in this.params) {
				if (this.params.hasOwnProperty(key)) {
					var param = this.params[key];
					params.push(key + ":<" + param.type + ">");
				}
			}
			return this.name + "=[" + params.join(", ") + "]";
		}
	};

	return _;
})(_ || {});


