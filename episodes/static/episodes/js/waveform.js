var waveformLayout,
    episodesData,
    episodesLayout,
    waveformArea;

var WaveformView = Backbone.View.extend({
  el: "svg",
  initialize: function () {
    var that = this;

    var svg = d3.select(this.el);

    var width = window.innerWidth * 0.75,
        height = 200 * this.collection.models.length;

    svg
      .attr("width", width)
      .attr("height", height);

    // Define scales
    var timeScale = d3.scale.linear(),
        waveformScale = d3.scale.linear(),
        orderScale = d3.scale.ordinal();

    // Waveform area generator
    var interval = 5; // hardcoded!
    waveformArea = d3.svg.area()
      .x(function (d, i) { return timeScale(i * interval); })
      .y0(function (d) { return waveformScale(d[0]); })
      .y1(function (d) { return waveformScale(d[1]); });
    this.waveformArea = waveformArea;

    // Set timeScale
    var maxDuration = d3.max(this.collection.pluck("duration"));

    timeScale
      .domain([0, maxDuration])
      .range([0, window.innerWidth]);
    this.timeScale = timeScale;

    // Set waveformScale
    waveformScale
      .domain([-10000, 10000])
      .range([40, -40]);
    this.waveformScale = waveformScale;

    // Set orderScale
    orderScale
      .domain(this.collection.pluck("id"))
      .rangeBands([80, height]);
    this.orderScale = orderScale;

  },
  render: function () {

    // Render collection using D3

    var that = this;

    // hack!
    // Clone each models attributes
    // so we can use D3 layouts
    episodesData = [];
    this.collection.forEach(function (episode) {
      var datum = _.clone(episode.attributes);

      // custom layout
      datum.yEpisode = that.orderScale(datum.id);
      datum.xEpisode = 0; // left-aligned

      episodesData.push(datum);
    });

    var svg = d3.select(this.el);

    var episodes = svg.selectAll("g.episode")
      .data(episodesData)
      .enter()
      .append("g")
      .attr("class", "episode")

    // Create a waveform for each episode
    episodes
      .each(function (episode) {
        var fillColor = episode.show.color_scheme[episode.id % episode.show.color_scheme.length];

        d3.select(this)
          .append("path")
          .datum(episode.waveform.values)
          .attr("class", "area")
          .attr("d", that.waveformArea)
          .attr("fill", fillColor);
      });
    //
    // // Create titles for each episode
    // var titleDY = 20;
    //
    // var titles = episodes.append("g")
    //   .attr("class", "title");
    //
    // titles.append("text")
    //   .text(function (episode) { return episode.title; });
    //
    // var logoSize = 80;
    // var logos = episodes.append("g")
    //   .attr("class", "logos")
    //   .attr("transform", "translate(0,-" + logoSize/2 + ")");
    //
    // logos
    //   .append("image")
    //   .attr("xlink:href", function (episode) { return episode.show.image_url; })
    //   .attr("width", logoSize)
    //   .attr("height", logoSize);
    //
    // this.logoSize = logoSize;
    //
    // var needle = waveforms.append("line")
    //   .attr("class", "needle");
    //
    // needle
    //   .attr("x1", this.timeScale(0))
    //   .attr("y1", this.barHeight)
    //   .attr("x2", this.timeScale(0))
    //   .attr("y2", 0);
    //
    // this.needle = needle;
    //
    // function moveNeedleOnMouse() {
    //   var mouseX = d3.mouse(this)[0];
    //   that.needle
    //     .transition()
    //     .duration(10)
    //     .attr("x1", mouseX)
    //     .attr("x2", mouseX);
    // };
    //
    // var resetNeedle = function () {
    //   var resetX = that.timeScale(0);
    //
    //   needle
    //     .transition()
    //     .attr("x1", resetX)
    //     .attr("x2", resetX);
    // };
    //
    // this.trigger("left");
  },

  center: function () {
    var episodes = d3.select(this.el).selectAll("g.episode");
    var xMax = d3.max(this.timeScale.range());

    var that = this;

    episodes
      .attr("transform", function (episode) {
        var x = xMax/2;
            y = that.orderScale(episode.id);
        return "translate(" + x + "," + y + ")";
      });

    // Translate the areas
    var drop = d3.max(this.waveformScale.range()) + 10;
    episodes.selectAll("g.waveform")
      .attr("transform", function (episode) {
        var waveformWidth = that.timeScale(episode.duration);
        return "translate(-" + waveformWidth/2 + "," + drop + ")";
      });

    // Translate the titles
    var groupWidth = this.logoSize + textWidth
    var textDX = 0.5 * groupWidth;
    episodes.selectAll("g.title")
      .attr("translate", "transform(" + textDX + ",0)")
      .selectAll("text")
      .attr("dominant-baseline", "central")
      .attr("text-anchor", "left");

  },

  left: function () {
    var episodes = d3.select(this.el).selectAll("g.episode");
    var xMax = d3.max(this.timeScale.range());

    var that = this;

    episodes
      .attr("transform", function (episode) {
        var y = that.orderScale(episode.id);
        return "translate(0," + y + ")";
      });

    // Move waveforms down from logo and text
    var timeScaleExtent = 80;
    episodes.selectAll("g.waveform")
      .attr("transform", "translate(0," + timeScaleExtent + ")");

    episodes.selectAll("g.title")
      .attr("transform", "translate(" + that.logoSize + ",0)");

    // Translate the titles
    episodes.selectAll("g.title").selectAll("text")
      .attr("dominant-baseline", "central")
      .attr("text-anchor", "left");

  }
});
