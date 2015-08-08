var context = new (window.AudioContext || window.webkitAudioContext)();

var EpisodeView = Backbone.View.extend({

  // Each episode is rendered in its own <li> element
  tagName: "li",

  initialize: function (options) {

    this.margin = {left: 40, top: 40, right: 80, bottom: 80};

    this.timeScale = d3.scale.linear()
      .domain([0, options.maxDuration || this.model.get('duration')])
      .range([0, window.innerWidth - 2 * (this.margin.left + this.margin.right)]);

    this.waveformScale = d3.scale.linear()
      .range([0, 200])

    // Hand code colorbrewer ramps for Gimlet shows
    this.showColorScale = d3.scale.ordinal()
      .domain(["StartUp", "Reply All", "Mystery Show"])
      .range(["Blues", "Greens", "Purples"]);

    // Attach this view to functions
    _.bindAll(this, "createEpisodeSound", "playEpisodeAtTime");
  },

  render: function () {

    // Render the episode using D3

    var episode = _.clone(this.model.attributes);

    d3.select(this.el)
      .append("svg")
      .attr("class", "episode-player");

    var svg = d3.select(this.el).select("svg.episode-player");

    // Width of <svg> is determined by the length of the episode
    var svgWidth = this.timeScale(episode.duration),
        svgHeight = d3.max(this.waveformScale.range());

    svg
      .attr("width", svgWidth + this.margin.left + this.margin.right)
      .attr("height", svgHeight + this.margin.top + this.margin.bottom);

    episodeGroup = svg.append("g")
      .attr("transform", "translate(" + this.margin.top + "," + this.margin.right + ")");

    // Create the background
    var background = episodeGroup.append("rect")
      .attr("class", "background")

    background
      .attr("x", d3.min(this.timeScale.range()))
      .attr("y", d3.min(this.waveformScale.range()))
      // rect width needs to be determined by this episode
      .attr("width", this.timeScale(episode.duration))
      .attr("height", d3.max(this.waveformScale.range()))
      .style("fill", "white")
      .style("stroke", "black")
      .style("stroke-width", "1.5px");

    var title = episodeGroup
      .append("text")
      .text(episode.title)
      .attr("x", this.timeScale(30))
      .attr("y", this.waveformScale.range()[1]);

    // Create the needle
    var needle = episodeGroup.append("line")
      .attr("class", "needle");

    needle
      .style("stroke", "black")
      .attr("x1", this.timeScale(0))
      .attr("y1", d3.min(this.waveformScale.range()))
      .attr("x2", this.timeScale(0))
      .attr("y2", d3.max(this.waveformScale.range()));


    // Axes
    var timeLine = d3.svg.axis()
      .scale(this.timeScale)

        // Add the x-axis.
    episodeGroup.append("g")
        .attr("class", "axis timeline")
        .attr("transform", "translate(0," + svgHeight + ")")
        .call(timeLine);

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

  createEpisodeSound: function () {
    // Load soundManager object
    var episodeSound = soundManager.createSound({
      id: "episode" + this.model.get("id"),
      url: this.model.get("url"),
    });

    this.episodeSound = episodeSound;
  },

  playEpisodeAtTime: function (time) {
    console.log("playing at time:" + time);

    if (this.episodeSound.playState == 1) {
      this.episodeSound.stop();
    } else {
      console.log("position: " + this.episodeSound.position);
      this.episodeSound.setPosition(time * 1000.0);
      console.log("position: " + this.episodeSound.position);
      this.episodeSound.play();
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

    this._episodeViews = [];
    this.collection.each(function (episode) {
      that._episodeViews.push(new EpisodeView({
        model: episode,
        maxDuration: maxDuration
        }));
    });

    this.maxWidth = window.innerWidth;
  },

  render: function () {
    var that = this;
    $(this.el).empty();

    _(this._episodeViews).each(function (episodeView) {
      $(that.el).append(episodeView.render().el);
    });

    this.on("soundmanager:ready", function () {
      // console.log("soundmanager:ready, so loading first episode")
      // var firstEpisodeId = this.collection.models[0].id;
      this.trigger("collection:load");
    });

    this.on("collection:load", this.loadEpisode);
  },

  loadEpisode: function () {
    this._episodeViews.forEach(function (episodeView) {
      episodeView.createEpisodeSound();
    });
  }

});
