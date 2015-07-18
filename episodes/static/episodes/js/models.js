
var Episode = Backbone.Model.extend({});

var EpisodeCollection = Backbone.Collection.extend({
  model: Episode,
  url: '/api/episodes'
});

var episodeCollection = new EpisodeCollection();
episodeCollection.fetch();
