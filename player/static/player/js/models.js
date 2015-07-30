// TODO Episodes need a method that will load the episode as
// a sound manager sound that can be played at specific times
// by the EpisodeView
var Episode = Backbone.Model.extend({});

var EpisodeCollection = Backbone.Collection.extend({
  model: Episode,
  url: '/api/episodes',
});
