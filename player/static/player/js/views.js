
var EpisodeView = Backbone.View.extend({

  // Each episode is rendered in its own svg element
  tagName: "svg",

  initialize: function (options) {

    this.timeScale = d3.scale.linear()
      .domain([0, options.maxDuration || this.model.get('duration')])
      .range([0, options.maxWidth || window.innerWidth]);

    var svgHeight = 200;
    // Hand-tuned polylinear scale
    this.valueScale = d3.scale.linear()
      .domain([60, 93, 101, 120])
      .range([svgHeight, svgHeight/2, svgHeight/8, 0]);

    // Hand code colorbrewer ramps for Gimlet shows
    this.showColorScale = d3.scale.ordinal()
      .domain(["StartUp", "Reply All", "Mystery Show"])
      .range(["Blues", "Greens", "Purples"]);

    this.line = d3.svg.line()
      .x(function (moment) { return this.timeScale(moment.time); })
      .y(function (moment) { return this.valueScale(moment.value); })
      .interpolate("basis");
  },

  render: function () {
    var episode = _.clone(this.model.attributes);

    var svg = d3.select(this.el);

    svg
      .attr("width", this.timeScale(this.model.get("duration")))
      .attr("height", d3.max(this.valueScale.range()));

    /* Needle */
    svg
      .append("line")
      .attr("class", "needle")

    var needle = svg.select(".needle");

    needle
      .style("stroke", "black")
      .attr("x1", this.timeScale(0))
      .attr("y1", d3.min(this.valueScale.range()))
      .attr("x2", this.timeScale(0))
      .attr("y2", d3.max(this.valueScale.range()));

    /* Background */
    svg
      .append("rect")
      .attr("class", "background")

    var background = svg.select(".background");

    background
      .attr("x", d3.min(this.timeScale.range()))
      .attr("y", d3.min(this.valueScale.range()))
      .attr("width", d3.max(this.timeScale.range()))
      .attr("height", d3.max(this.valueScale.range()))
      .style("opacity", 0)
      .style("stroke", "black");

    function moveNeedle() {
      var mouseX = d3.mouse(this)[0];
      needle
        .transition()
        .duration(10)
        .attr("x1", mouseX)
        .attr("x2", mouseX);
    }

    function removeNeedle() {
      var resetX = this.timeScale(0);
      needle
        .transition()
        .attr("x1", resetX)
        .attr("x2", resetX);
    }

    function playMoment() {
      var mouseX = d3.mouse(this)[0],
          time = this.timeScale(mouseX);
      //playEpisode(time);
      console.log("playing episode at time:" + time);
    }

    background
      .on("mousemove", moveNeedle)
      .on("mouseout", removeNeedle)
      .on("click", playMoment)

    /* Horizon */
    svg
      .append("path")
      .attr("class", "horizon");

    var horizon = svg.select(".horizon");

    horizon
      .attr("d", this.line(episode.moments) + "Z");

    return this;
  },
});

var EpisodeCollectionView = Backbone.View.extend({
  el: "ul",

  initialize: function () {
    this.maxDuration = d3.max(this.collection.models, function (episode) {
      console.log(episode);
      return episode.get("duration");
    });

    this.maxWidth = window.innerWidth;
  },

  render: function () {
    var that = this;
    $(this.el).empty();

    this.collection.each(function (episode) {
      episodeView = new EpisodeView({
        model: episode,
        maxDuration: this.maxDuration,
        maxWidth: this.maxWidth
      });
      $(that.el).append("<li>" + episodeView.render().el + "</li>");
    });
  }
});
