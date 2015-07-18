
var Episode = Backbone.Model.extend({});

var EpisodeCollection = Backbone.Collection.extend({
  model: Episode,
  url: '/api/episodes'
});

var episodeCollection = new EpisodeCollection();
episodeCollection.fetch();

var D3Settings = Backbone.Model.extend({
  defaults: {
    timeScale: d3.scale.linear(),
    valueScale: d3.scale.linear(),
    showColorScale: d3.scale.ordinal()
  },

  initialize: function () {
    this.attributes.timeScale
      .dom
    console.log(this.attributes.timeScale);
  }
});
