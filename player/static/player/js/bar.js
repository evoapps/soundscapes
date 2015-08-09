
var EpisodeBarView = Backbone.View.extend({
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
      .style("fill", colorbrewer[this.showColorScale(episode.show.name)][5][3])
      .style("stroke", "black")
      .style("stroke-width", "1.5px");

    var title = episodeGroup
      .append("text")

    title
      .text(episode.title)
      .attr("x", this.timeScale(30))
      .attr("y", this.waveformScale.range()[1]);

    // Make sure the full title shows in the svg
    var titleWidth = title.node().getComputedTextLength();

    console.log(episode.title + ": " + titleWidth);
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
    var formatTime = d3.time.format("%M"),
        formatSeconds = function (seconds) { return formatTime(new Date(2012, 0, 1, 0, 0, seconds)); };

    var timeAxes = d3.svg.axis()
      .scale(this.timeScale)
      .ticks(d3.time.seconds, 60 * 5)
      .tickFormat(formatSeconds);


        // Add the x-axis.
    episodeGroup.append("g")
        .attr("class", "axis timeline")
        .attr("transform", "translate(0," + svgHeight + ")")
        .call(timeAxes);

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
    soundManager.createSound({
      id: this.model.get("soundId"),
      url: this.model.get("url"),
    });
  },

  playEpisodeAtTime: function (time) {
    console.log("playing at time:" + time);

    episodeSound = soundManager.getSoundById(this.model.get("soundId"));

    if (episodeSound.playState == 1) {
      episodeSound.stop();
    } else {
      console.log("position: " + this.episodeSound.position);
      episodeSound.setPosition(time * 1000.0);
      console.log("position: " + this.episodeSound.position);
      episodeSound.play();
    }
  }
});
