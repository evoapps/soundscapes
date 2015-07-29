var context = new (window.AudioContext || window.webkitAudioContext)();

var EpisodeView = Backbone.View.extend({

  // Each episode is rendered in its own svg element
  tagName: "li",

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

    // Populate the <li> element

    d3.select(this.el)
      .append("svg")
      .attr("class", "episode-player");

    var svg = d3.select(this.el).select("svg.episode-player");

    // Copy the attributes to use with D3
    var episode = _.clone(this.model.attributes);

    var title = svg
      .append("text")
      .text(episode.title)
      .attr("x", this.timeScale(30))
      .attr("y", this.valueScale.range()[1]);

    // Width of <svg> is determined by the length of the episode
    svg
      .attr("width", this.timeScale(episode.duration))
      .attr("height", d3.max(this.valueScale.range()));

    // Create the needle
    var needle = svg.append("line")
      .attr("class", "needle");

    needle
      .style("stroke", "black")
      .attr("x1", this.timeScale(0))
      .attr("y1", d3.min(this.valueScale.range()))
      .attr("x2", this.timeScale(0))
      .attr("y2", d3.max(this.valueScale.range()));

    // Create the background
    var background = svg.append("rect")
      .attr("class", "background")

    background
      .attr("x", d3.min(this.timeScale.range()))
      .attr("y", d3.min(this.valueScale.range()))
      .attr("width", d3.max(this.timeScale.range()))
      .attr("height", d3.max(this.valueScale.range()))
      .style("opacity", 0)
      .style("stroke", "black");

    // Monitor events with D3

    function moveNeedleOnMouse() {

      // When the mouse moves, move the needle
      // to the x position of the mouse.

      var mouseX = d3.mouse(this)[0];
      needle
        .transition()
        .duration(10)
        .attr("x1", mouseX)
        .attr("x2", mouseX);
    }

    var timeScale = this.timeScale;

    function resetNeedle() {

      // Move the needle back to the beginning of the episode

      var resetX = timeScale(0);
      needle
        .transition()
        .attr("x1", resetX)
        .attr("x2", resetX);
    }

    var playEpisodeAtTime = this.playEpisodeAtTime;

    function playAtMousePos() {

      // Play the episode at the mouse position

      var mouseX = d3.mouse(this)[0],
          time = timeScale(mouseX);

      playEpisodeAtTime(time);
    }

    background
      .on("mousemove", moveNeedleOnMouse)
      .on("mouseout", resetNeedle)
      .on("click", playAtMousePos);

    /* Horizon */
    /*
    svg
      .append("path")
      .attr("class", "horizon");

    var horizon = svg.select(".horizon");

    horizon
      .attr("d", this.line(episode.moments) + "Z");
    */

    // this.loadEpisodeBuffer();

    return this;
  },

  loadEpisodeBuffer: function () {

    // This should set the buffer to an attribute on the model

    var getSound = new XMLHttpRequest(),
        that = this;

    getSound.open("GET", this.model.get("url"), true);
    getSound.responseType = "arraybuffer";
    getSound.onload = function () {
      context.decodeAudioData(getSound.response, function (buffer) {
        that.episodeBuffer = buffer;
      })
    }

    getSound.send();
  },

  playEpisodeAtTime: function (time) {

    console.log("playing episode");

    if (this.episodeBuffer) {
      var playSound = context.createBufferSource();
      playSound.buffer = this.episodeBuffer;
      playSound.connect(context.destination);
      playSound.start(time);
    }

  }
});

var EpisodeCollectionView = Backbone.View.extend({
  el: "ul",

  initialize: function () {
    var that = this;

    var maxDuration,
        maxWidth;

    maxDuration = d3.max(this.collection.models, function (episode) {
      return episode.get("duration");
    });
    maxWidth = window.innerWidth;

    this._episodeViews = [];
    this.collection.each(function (episode) {
      that._episodeViews.push(new EpisodeView({
        model: episode,
        maxDuration: maxDuration,
        maxWidth: maxWidth,
        }));
    });

    this.maxDuration =

    this.maxWidth = window.innerWidth;
  },

  render: function () {
    var that = this;
    $(this.el).empty();

    _(this._episodeViews).each(function (episodeView) {
      $(that.el).append(episodeView.render().el);
    });

  }
});
