/**
 * This module acts as the main entry point for dealing with FE -> BE commands.
 * In particular, it provides validation per the definitions provided by the backend
 * to prevent sending requests that would be rejected anyway. This may not be necessary
 * as the amount of ajax content shouldn't be excessive yet, but nonetheless it forces
 * clean and maintainable structure.
 *
 *
 * @module _
 */
var _ = (function (_) {

	/**
	 * The url endpoint at which commands can be executed.
	 *
	 * @type {string}
	 */
	var execution_endpoint = '/command/';

	/**
	 * The url endpoint at which all of the command definitions can be retrieved.
	 *
	 * @type {string}
	 */
	var all_endpoint = '/command/all/';

	/**
	 * The url endpoint at which the available command definitions can be retrieved.
	 *
	 * @type {string}
	 */
	var available_endpoint = '/command/available/';

	/**
	 * The command definitions by command name as defined per the latest definition update.
	 * In general, there's no reason to not access a command out of the registry for execution
	 * since is the most closely related to the server definitions since it will be populated by
	 * them.
	 *
	 * @enum Command
	 */
	_.registry = {};

	/**
	 * A publicly accessible method that reloads the available commands
	 * cache that is used to validate commands before they are sent to the server.
	 *
	 * @param {function} ready A callback that gets fired after the command definitions have been loaded.
	 * @param {string} [uriEndpoint] An optional alternative endpoint from which to populate the commands.
	 */
	_.UpdateDefinitions = function (ready, uriEndpoint) {
		this.registry = {};
		var done = $.proxy(this._doneUpdatingCallback, this);

		var callback = function(data){
			done(data);
			if(ready){ready(data);}
		};

		$.get(uriEndpoint || available_endpoint).done(callback).fail(this._errorUpdatingCallback);
	};

	/**
	 * A publicly accessible method that executes a given command
	 * after first performing validation.
	 *
	 * @param {Command} command
	 * @param {object} [data]
	 * @param {function} [success]
	 * @param {function} [failure]
	 */
	_.ExecuteCommand = function (command, data, success, failure) {

		if (!command instanceof Command) {
			throw new Error("Invalid command object provided. Aborting execution of command.");
		}

		data = command.buildData(data || {});

		if (this._validateCommand(command, data)) {

			// If no success function was given, let's just print it to the console.
			if(!success){
				success = function(data){console.log(data);};
			}

			// This is the actual execution of the validated command.
			$.post(execution_endpoint, data).done(success).fail(failure);

		} else {

			var message = this._buildCommandMessage(command);

			// either passing the error to their failure callback or just throwing it.
			if (failure) {
				failure(new Error(message));
			} else {
				throw new Error(message);
			}
		}
	};

	/**
	 * This builds a meaningful message intended to provide the necessary information
	 * to diagnose why a given command failed validation.
	 */
	_._buildCommandMessage = $.proxy(function (command) {

		var message;

		if (this.registry.hasOwnProperty(command.name)) {
			message = "The server definition was: " + this.registry[command.name].toString();
		} else {
			message = 'No server definition of this command was found.';
		}

		message += "\nThe provided command definition was: " + command.toString();
		message += "\nThe provided data was: " + JSON.stringify(data);

		return message;
	}, _);

	/**
	 * This represents the success function from a command definition retrieval.
	 *
	 * @param {{name:string,required:{name:string, type:string}[]}[]} results
	 * @private
	 */
	_._doneUpdatingCallback = $.proxy(function (results) {
		for (var index in results) {
			if (results.hasOwnProperty(index)) {
				var command = results[index];
				this.registry[command.name] = Command.fromServer(command);
			}
		}
	}, _);

	/**
	 * This represents the error function on an unsuccessful command definition retrieval.
	 *
	 * @param {error} error
	 * @private
	 */
	_._errorUpdatingCallback = $.proxy(function (error) {
		alert('An error was encountered while retrieving available commands. Logging error to console.');
		console.log(error);
	}, _);

	/**
	 * Validates a command prior to execution according to the definitions
	 * received from the server, and any defaults that have been set on the
	 * front end.
	 *
	 * @param {Command} command The command key to be validated.
	 * @param {object} data The data intended to be sent along with the command.
	 * @private
	 */
	_._validateCommand = function (command, data) {
		var valid = true;
		if (this.registry.hasOwnProperty(command.name)) {
			var required = this.registry[command.name].required;
			for (var index in required) {
				if (required.hasOwnProperty(index)) {
					var required_param = required[index];
					if (!data.hasOwnProperty(required_param.name)) {
						valid = false;
						break;
					}
					// FIXME: if we're going to be supplying type, we should do validation against that here too.
				}
			}
		}
		return valid;
	};

	return _;
})(_ || {});