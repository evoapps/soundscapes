var Episode = Backbone.Model.extend({
  initialize: function () {
    this.set("soundId", "episode" + this.get("id"));
  }
});

var EpisodeCollection = Backbone.Collection.extend({
  model: Episode,
  url: '/api/episodes',
});
