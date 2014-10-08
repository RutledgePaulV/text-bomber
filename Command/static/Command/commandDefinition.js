/**
 * Constructs a command object to be passed to the command service.
 *
 * @param {string} name The command key that the server will respond to.
 * @param {{name:string, type:string}[]} required The required parameters for the command.
 * @param {object.<string,*>} [defaults] Any defaults that should be applied.
 * @constructor
 */
var Command = function (name, required, defaults) {

	/**
	 *
	 * @type {string}
	 */
	this.name = name.toUpperCase() || '';

	/**
	 *
	 * @type {Object.<string, *>}
	 */
	this.defaults = defaults || {};

	/**
	 *
	 * @type {{name: string, type: string}[]}
	 */
	this.required = required || [];

};

/**
 * A factory method to take a backend result from the list of available commands
 * and generate a command object out of it.
 *
 * @param {{name:string,required:{name:string, type:string, default?:*}[]}} serverDef
 * @returns {Command}
 */
Command.fromServer = function(serverDef){
	var defaults = {};
	var required = [];
	for(var index in serverDef.params){
		if(serverDef.params.hasOwnProperty(index)){
			var param = serverDef.params[index];
			if(param.default !== undefined){
				defaults[param.name] = param.default;
				delete param.default;
			}
			required.push({name:param.name, type:param.type});
		}
	}
	return new Command(serverDef.name, required, defaults);
};

/**
 *
 * @lends Command
 */
Command.prototype = {

	/**
	 * The constructor for the command definition object.
	 */
	constructor: Command,

	/**
	 * Executes a command and appropriately calls the success and failure callbacks.
	 *
	 * @param {object} [data]
	 * @param {function} [success]
	 * @param {function} [failure]
	 */
	fire: function(data, success, failure){
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
		for (var index in this.required) {
			if (this.required.hasOwnProperty(index)) {
				var param = this.required[index];
				params.push(param.name + ":<" + param.type + ">");
			}
		}
		return this.name + "=[" + params.join(", ") + "]";
	}
};
