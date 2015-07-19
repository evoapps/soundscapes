

var EpisodeView = Backbone.View.extend({
  tagName: "svg",
  initialize: function () {
    
  },
  render: function () {
    var episode = _.clone(model.attributes);

    var svg = d3.select(this.el);

    // Set svg attributes for this episode
    var width = 600, //d3.max(d3settings.timeScale.range()),
        height = 400; // d3.max(valueScale.range());

    svg
      .attr("width", width)
      .attr("height", height);

    svg
      .append("line")
      .attr("class", "needle")

    var needle = svg.select(".needle");

    needle
      .style("stroke", "black")
      .attr("x1", timeScale(0))
      .attr("y1", d3.min(valueScale.range()))
      .attr("x2", timeScale(0))
      .attr("y2", d3.max(valueScale.range()));

    svg
      .append("rect")
      .attr("class", "background")

    var background = svg.select(".background");

    background
      .attr("x", d3.min(timeScale.range()))
      .attr("y", d3.min(valueScale.range()))
      .attr("width", d3.max(timeScale.range()))
      .attr("height", d3.max(valueScale.range()))
      .style("opacity", 0)
      .style("stroke", "black");

    svg
      .append("path")
      .attr("class", "horizon");

    var horizon = svg.select(".horizon");

    horizon
      .attr("d", line(episode.moments) + "Z");
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
