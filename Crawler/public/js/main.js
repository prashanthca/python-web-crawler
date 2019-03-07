require.config({
	paths: {
		'jquery': 'lib/jquery.min',
		'underscore': 'lib/underscore-min',
		'backbone': 'lib/backbone',
		'backbone-raw': 'lib/backbone-min',
		'popper': 'lib/popper.min',
		'backbone-super': 'lib/backbone-super-min',
		'bootstrap': 'lib/bootstrap.min',
		'tree': 'tree.jquery'
	},
	shim: {
		'backbone-raw': {
			deps: ['underscore', 'jquery', 'tree'],
			exports: 'Backbone'
		},
		'backbone-super': ['backbone-raw']
	}
});

require(['components/app'], function(App) {
	var app = new App();
});