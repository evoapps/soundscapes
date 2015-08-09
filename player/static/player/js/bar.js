
var BarView = Backbone.View.extend({
  el: "svg",
  initialize: function () {
    var svg = d3.select(this.el);

    var width = window.innerWidth,
        height = window.innerHeight;

    svg
      .attr("width", width)
      .attr("height", height);

    // BarView is a stack layout
    var stackedBars = d3.layout.stack()
      .values(function (episode) { return episode.get("duration"); });
    this.stackedBars = stackedBars;

    // Define scales
    var timeScale = d3.scale.linear(),
        orderScale = d3.scale.ordinal(),
        colorScale = d3.scale.ordinal();

    // Set timeScale
    var maxDuration = d3.max(this.collection.models, function (episode) {
      return episode.get("duration");
    });

    timeScale
      .domain([0, maxDuration])
      .range([0, window.innerWidth]);
    this.timeScale = timeScale;

    // Set orderScale
    orderScale
      .domain(this.collection.pluck("id"))
      .rangeBands([0, height]);
    this.orderScale = orderScale;

    // Set colorScale
    // Hand code colorbrewer ramps for Gimlet shows
    colorScale = d3.scale.ordinal()
      .domain(["StartUp", "Reply All", "Mystery Show"])
      .range(["Blues", "Greens", "Purples"]);
    this.colorScale = colorScale;
  },
  render: function () {
    // Render collection using D3
    var episodes = _.clone(this.collection.models),
        that = this;

    var svg = d3.select(this.el);

    // Create a <g> for each episode model
    var episodes = svg.selectAll("g.episode")
      .data(episodes)
      .enter()
      .append("g")
      .attr("class", "episode")
      .attr("transform", function (episode) {
        return "translate(0," + that.orderScale(episode.get("id")) + ")";
      });

    // Create titles for each episode
    var titleDY = 20;
    var episodeTitle = episodes.append("text")
      .text(function (episode) { return episode.get("title"); })
      .attr("dy", titleDY);

    // Create <rects> for each episode
    var barHeight = 40;
    var episodeRects = episodes.append("rect")
      .attr("x", 0)
      .attr("y", 0)
      .attr("height", barHeight)
      .attr("width", function (episode) {
        return that.timeScale(episode.get("duration"));
      });
  },
});
