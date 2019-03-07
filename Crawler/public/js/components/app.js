define(['backbone', 'jquery'], function (Backbone, $) {
	return Backbone.View.extend({
		el: 'body',
		events: {
			'click #get-links': '_startCrawl',
			'click .list-group-item': '_getImagesOrLinks',
			'click #back-btn': '_backButtonClicked'
		},
		initialize: function(){
			this._views = {};
			this._container = $("#links-views-container");
			this.render();
		},

		render: function(){
			this._container.show();
		},
		_startCrawl: function(){
			var url = $("#url").val();
			var self = this;
			var level = $("#level").val();
			if(url != "" || level != "") {
				window._levels = {};
				window._numberOfLevels = level;
				this._views = {};
				this._container.find(".links-view").remove();
				this._container.find("#links-views-container-header #view-title").text("Loading...");
				this._container.find("#links-views-container-header").removeClass("bb");
				this._views["level1"] = $("<div id='lvl1' class='links-view'></div>");
				this._container.append(this._views['level1']);
				$.ajax({
					'url': '/getlinks',
					'type': 'POST',
					'contentType': 'application/json',
					'data': JSON.stringify({
						'url': url,
						'level': level 
					}),
					success: function(data) {
						var _links = data.treeView; //JSON.parse(data.links);
						window._levels["1"] = _links;
						self._views["level1"].tree({
							data: _links,
							autoOpen: false
						});
						self._container.find("#links-views-container-header").addClass("bb");
						self._container.find("#links-views-container-header #view-title").text("Links Tree");
					}
				});
			}
		},
		_getImagesOrLinks: function(e){
			var element = $(e.target);
			var url = element.text();
			var self = this;
			var level = element.attr('level');
			var _nextLevel = parseInt(level)+1;
			if(_nextLevel <= _numberOfLevels)
			{
				this._container.find("#links-views-container-header #view-title").text("Loading...");
				this._container.find("#links-views-container-header").removeClass("bb");
				this._views["level"+_nextLevel] = $("<div id='lvl"+_nextLevel+"' class='links-view'><ul class='list-group'></ul></div>");
				this._container.append(this._views["level"+_nextLevel]);
				var aURL = _nextLevel == _numberOfLevels ? '/getimages': '/getlinks';
				var _type = _nextLevel == _numberOfLevels ? 'images': 'links';
				var decoration = _nextLevel == _numberOfLevels ? '(Images)': '';
				$.ajax({
					'url': aURL,
					'type': 'POST',
					'contentType': 'application/json',
					'data': JSON.stringify({
						'url': url
					}),
					success: function(data) {
						var _links = JSON.parse(data[_type]);
						window._levels[_nextLevel] = _links;
						if(_links.length > 0)
						{
							_links.forEach(function(link){
								self._views["level"+_nextLevel].find(".list-group").append("<li class='list-group-item' level='"+_nextLevel+"'>"+link+"</li>");
							});
							self._container.find("#links-views-container-header").addClass("bb");
						}
						self._container.find("#links-views-container-header #view-title").text("Level "+_nextLevel+" "+decoration);
						self._container.find(".links-view").hide();
						self._views["level"+_nextLevel].show();
						self._container.find("#back-btn").attr("current", _nextLevel).show();
						$('html, body').animate({
							scrollTop: self._container.offset().top
						}, 1000);
					}
				});
			}
		},
		_backButtonClicked: function(){
			var current = $("#back-btn").attr("current");
			var _prev = parseInt(current)-1;
			if(this._views["level"+_prev] != undefined)
			{
				delete this._views[current];
				this._container.find("#lvl"+current).remove();
				this._container.find(".links-view").hide();
				this._views["level"+_prev].show();
				this._container.find("#links-views-container-header #view-title").text("Level "+_prev);
				$("#back-btn").attr("current", _prev);
			}
			if(_prev == "1")
			{
				this._container.find("#back-btn").hide();
			}
		}
	});
});