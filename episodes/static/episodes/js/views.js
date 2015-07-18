var EpisodeView = Backbone.View.extend({
  tagName: "svg",
  render: function () {
    var episode = this.model;

    d3.select(this.el)
      .append("text")
      .text(episode.attributes.title);


  }
})

var collectionView = new Backbone.CollectionView( {
  el: $("ul"),
  collection: episodeCollection,
  modelView: EpisodeView
} );

collectionView.render();
