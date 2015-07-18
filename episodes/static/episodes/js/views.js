
d3settings = new D3Settings();

var EpisodeView = Backbone.View.extend({
  tagName: "svg",
  initialize: function () {
    console.log(this.model);

    d3
  },
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

var collectionView = new Backbone.CollectionView( {
  el: $("ul"),
  collection: episodeCollection,
  modelView: EpisodeView
} );

collectionView.render();
