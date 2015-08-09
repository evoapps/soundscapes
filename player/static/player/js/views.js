
var EpisodeBarView = Backbone.View.extend({
  // Each episode is rendered in its own <li> element
  tagName: "li",

  events: {
    "click": "togglePlay"
  },

  initialize: function (options) {

    this.margin = {left: 40, top: 10, right: 10, bottom: 80};

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
      .style("fill", colorbrewer[this.showColorScale(episode.show.name)][5][3])
      .style("stroke", "black")
      .style("stroke-width", "1.5px");

    var title = episodeGroup
      .append("text")

    var waveFormHeight = d3.max(this.waveformScale.range());

    title
      .text(episode.title)
      .attr("x", this.timeScale(episode.duration)/2)
      .attr("y", waveFormHeight / 2)
      .attr("text-anchor", "middle");

    // Make sure the full title shows in the svg
    var titleWidth = title.node().getComputedTextLength();

    if (titleWidth > svg.attr("width")) {
      svg.attr("width", titleWidth);
    }

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
    // var formatTime = d3.time.format("%M"),
    //     formatSeconds = function (seconds) { return formatTime(new Date(2012, 0, 1, 0, 0, seconds)); };

    var timeAxis = d3.svg.axis()
      .scale(this.timeScale)
      .ticks(5); // d3.time.seconds, 60 * 5);

    var timeAxisHeight = waveFormHeight + 10;

        // Add the x-axis.
    episodeGroup.append("g")
        .attr("class", "axis timeline")
        .attr("transform", "translate(0," + timeAxisHeight + ")")
        .call(timeAxis);


    var moveNeedleOnMouse = function () {

      // When the mouse moves, move the needle
      // to the x position of the mouse.

      var mouseX = d3.mouse(this)[0];

      needle
        .transition()
        .duration(10)
        .attr("x1", mouseX)
        .attr("x2", mouseX);
    };

    var that = this;

    var resetNeedle = function () {

      // Move the needle back to the beginning of the episode

      var resetX = that.timeScale(0);

      needle
        .transition()
        .attr("x1", resetX)
        .attr("x2", resetX);
    };

    background
      .on("mousemove", moveNeedleOnMouse)
      .on("mouseout", resetNeedle);

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

  // Monitor events with D3



  createEpisodeSound: function () {
    soundManager.createSound({
      id: this.model.get("soundId"),
      url: this.model.get("url"),
    });
  },

  playEpisodeAtTime: function (time) {
    var episodeSound = soundManager.getSoundById(this.model.get("soundId"));

    if (episodeSound.playState == 0) {
      // stopped/uninitialized, so play
      msec = time * 1000.0
      episodeSound.play({position: msec});
    } else {
      // playing or buffering sound, so pause
      episodeSound.pause();
    }
  },

  togglePlay: function () {
    soundManager.togglePause(this.model.get("soundId"));
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

    this._episodeBarViews = [];
    this.collection.each(function (episode) {
      that._episodeBarViews.push(new EpisodeBarView({
        model: episode,
        maxDuration: maxDuration
      }));
    });

    this.maxWidth = window.innerWidth;
  },

  render: function () {
    var that = this;
    $(this.el).empty();

    _(this._episodeBarViews).each(function (episodeBarView) {
      $(that.el).append(episodeBarView.render().el);
    });

    this.on("soundmanager:ready", function () {
      // console.log("soundmanager:ready, so loading first episode")
      // var firstEpisodeId = this.collection.models[0].id;
      this.trigger("collection:load");
    });

    this.on("collection:load", this.loadEpisode);
  },

  loadEpisode: function () {
    this._episodeBarViews.forEach(function (episodeBarView) {
      episodeBarView.createEpisodeSound();
    });
  }

});
