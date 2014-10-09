var _ = (function (_) {

	/**
	 * Returns the subtype based on a definition.
	 *
	 * @param {string} key
	 * @returns {string}
	 */
	function getArrayType(key) {
		return key.substr(0, key.length - 2);
	}

	_.Validation = _.Validation || {

		/**
		 * Serializable type definitions shared between
		 * front and back end to communicate param types.
		 *
		 * @enum
		 */
		TYPES: {
			'string': [String],
			'string[]': [Array, String],
			'number': [Number],
			'number[]': [Array, Number],
			'object': [Object],
			'object[]': [Array, Object]
		},

		/**
		 * Checks that a given object matches a type of the available options.
		 * Used for validation parameter types before sending a request to the server.
		 *
		 * @param {*} obj
		 * @param {string} type
		 */
		typeIs: function (obj, type) {

			// if type isn't a definition key, return false
			if (!(type in this.TYPES)) {
				return false;
			}

			var def = this.TYPES[type];

			// if first type doesn't match, return false
			if (obj.constructor !== def[0]) {
				return false;
			}

			// if the first one matched and that's all there is, return true
			if (def.length === 1) {
				return true;
			}

			// outer layer must have been an array
			// (maybe we can support arbitrary nesting objects in the future)
			for (var index in obj) {
				if (obj.hasOwnProperty(index)) {
					if(!this.typeIs(obj[index], getArrayType(type))){
						return false;
					}
				}
			}

			return true;
		}
	};

	return _;
})(_ || {});