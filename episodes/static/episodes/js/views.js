

var EpisodeView = Backbone.View.extend({
  tagName: "svg",
  initialize: function () {},
  render: function () {
    var episode = this.model.attributes;

    // Set svg attributes for this episode
    var svg = d3.select(this.el);

    var width = 600, //d3.max(d3settings.timeScale.range()),
        height = 400; // d3.max(valueScale.range());

    svg
      .attr("width", width)
      .attr("height", height);

    svg
      .append("text")
      .text(episode.title);
  }
})

var EpisodeCollectionView = Backbone.View.extend({
  el: "ul",

  initialize: function () {
    this._episodeViews = [];
  },

  render: function () {
    var that = this;
    $(this.el).empty();

    this.collection.each(function (episode) {
      episodeView = new EpisodeView({ model: episode });
      that._episodeViews.push(episodeView);
    });

    _(this._episodeViews).each(function (episodeView) {
      $(that.el).append("<li>" + episodeView.render().el + "</li>");
    });
  }
});

var collectionView = new EpisodeCollectionView({collection: episodeCollection});
collectionView.render();

// var collectionView = new Backbone.CollectionView( {
//   el: $("ul"),
//   collection: episodeCollection,
//   modelView: EpisodeView
// } );
//
// collectionView.render();
