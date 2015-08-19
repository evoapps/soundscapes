var waveformLayout,
    episodesData,
    episodesLayout,
    waveformArea;

var WaveformView = Backbone.View.extend({
  el: "svg",
  initialize: function () {

    // Set up <svg> and D3 scales

    var that = this,
        svg = d3.select(this.el);

    this.heightPerEpisode = 100;

    var height = this.heightPerEpisode * this.collection.models.length,
        width = window.innerWidth * 0.75;

    svg
      .attr("width", width)
      .attr("height", height);

    // Scales
    // x is timeScale, y is episodeScale
    // waveformScale is a subscale of y for plotting episode waveforms
    this.timeScale = d3.scale.linear()
      .domain([0, d3.max(this.collection.pluck("duration"))])
      .range([0, width]);
    this.episodeScale = d3.scale.ordinal()
      .domain(this.collection.pluck("id"))  // I have no idea what this does
      .rangeBands([0, height]);

    var waveforms = this.collection.pluck("waveform");
    this.waveformScale = d3.scale.linear()
      .domain([d3.min(_.pluck(waveforms, "min")), d3.max(_.pluck(waveforms, "max"))]);
      // .range() is set for each episode

    // Waveform area generator
    // Each d is an array with lower and upper bound values
    var interval = this.collection.models[0].get("waveform").interval;
    this.waveformArea = d3.svg.area()
      .x(function (d, i) { return that.timeScale(i * interval); })
      .y0(function (d) { return that.waveformScale(d[0]); })
      .y1(function (d) { return that.waveformScale(d[1]); })
      .interpolate("cardinal")
      .tension(0);

    // Axes
    this.episodeAxis = d3.svg.axis()
      .scale(this.episodeScale)
      .orient("left");

    // hack!
    // Clone each models attributes
    // so we can use D3 layouts
    this.episodesData = [];
    this.collection.forEach(function (episode) {
      var datum = _.clone(episode.attributes);
      that.episodesData.push(datum);
    });
  },
  render: function () {

    // Render episodes using D3

    var that = this,
        svg = d3.select(this.el);

    this.episodesData.forEach(function (datum) {
      datum.x = that.timeScale(0);
      datum.y = that.episodeScale(datum.id);
      datum.width = that.timeScale(datum.duration);
      datum.height = that.heightPerEpisode;
    });

    var episodes = svg.selectAll("g.episode")
      .data(this.episodesData)
      .enter()
      .append("g")
      .attr("class", "episode");

    // Create a background rect for each episode
    episodes
      .append("rect")
      .attr("class", "background")
      .attr("x", function (episode) { return episode.x; })
      .attr("y", function (episode) { return episode.y; })
      .attr("width", function (episode) { return episode.width; })
      .attr("height", function (episode) { return episode.height; });

    // Create a waveform for each episode
    episodes
      .each(function (episode) {
        var fillColor = episode.show.color_scheme[episode.id % episode.show.color_scheme.length];

        that.waveformScale.range([episode.y, episode.y + episode.height]);

        d3.select(this)
          .append("path")
          .datum(episode.waveform.values)
          .attr("class", "area")
          .attr("d", that.waveformArea)
          .attr("fill", fillColor);
      });

    // Label each episode
    episode
      .append("g")
      .class("x axis")
      .call(this.episodeAxis);

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
