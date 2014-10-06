/**
 * The actual values defined here are overridden on each DefinitionUpdate call, but they're
 * also typed explicitly (and unfortunately, a synchronization point) in order to provide
 * intellisense support and give a feeling of robustness, even though they are defined dynamically.
 *
 * !!!
 * Note: it is intended that this file never even be loaded, it's here merely as a reference
 * and to provide intellisense support while maintaining a clean commandService.js
 * !!!
 *
 * @lends _.registry
 * @enum {Command}
 */
var COMMAND_LIST = {
	QUEUE_TEXTS: undefined,
	GET_PROGRESS: undefined
};