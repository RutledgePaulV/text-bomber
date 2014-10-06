/**
 * This jQuery plugin provides a basic implementation of the publish / subscribe event model. This
 * allows us to take advantage of the event system within jQuery without being directly tied to DOM
 * elements, and so we can use it for driving any custom events for plain JS.
 *
 *
 */
(function ($) {

	/**
	 * A dummy jquery object through which events will be routed.
	 *
	 * @type {$}
	 */
	var queue = $({});

	/**
	 * Publishes a topic
	 *
	 * @param {string} topic The topic to publish.
	 * @param {...*} args The arguments to pass along with the publication.
	 */
	$.pub = function(topic, args){
		queue.trigger.apply(queue, arguments);
	};

	/**
	 * Subscribes to a topics publication.
	 *
	 * @param {string} topic The topic to subscribe to.
	 * @param {function} callback The callback to execute when the event fires.
	 */
	$.sub = function(topic, callback){
		queue.on(topic, callback);
	};

	/**
	 * Unsubscribes to a topics publication.
	 *
	 * @param {string} topic The topic to unsubscribe from.
	 */
	$.unsub = function(topic){
		queue.off(topic);
	}


}(jQuery));