console.log('hello world');


$(document.body).on('click', '@action-delete', function(e) {
	console.log("Got a click to delete")
	var id = $(e.target).attr('vid');
	console.log("Video: " + id);
});
