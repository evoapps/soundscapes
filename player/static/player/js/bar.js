
var BarView = Backbone.View.extend({
  el: "svg",
  initialize: function () {
    _.bindAll(this, "center", "left");

    this.on("center", this.center);
    this.on("left", this.left);

    var svg = d3.select(this.el);

    var width = window.innerWidth,
        height = window.innerHeight;

    svg
      .attr("width", width)
      .attr("height", height);

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

    var that = this;

    // hack!
    // Clone each models attributes
    // so we can use D3 layouts
    var episodesData = [];
    this.collection.forEach(function (episode) {
      var datum = _.clone(episode.attributes);
      episodesData.push(datum);
    });

    var svg = d3.select(this.el);

    // Create a <g> for each episode

    var episodes = svg.selectAll("g.episode")
      .data(episodesData)
      .enter()
      .append("g")
      .attr("class", "episode");

    // Create titles for each episode
    var titleDY = 20;

    var titles = episodes.append("g")
      .attr("class", "title");

    titles.append("text")
      .text(function (episode) { return episode.title; });

    // Create <rects> for each episode
    this.barHeight = 40;

    var bars = episodes.append("g")
      .attr("class", "bar");

    bars
      .append("rect")
      .attr("x", 0)
      .attr("y", 0)
      .attr("height", this.barHeight)
      .attr("width", function (episode) {
        return that.timeScale(episode.duration);
      })
      .style("fill", function (episode) {
        var num_colors = episode.show.color_scheme.length;
        return episode.show.color_scheme[episode.id % num_colors];
      });

    var logoSize = this.barHeight;
    var logos = episodes.append("g")
      .attr("class", "logos")
      .attr("transform", "translate(0,-" + logoSize/2 + ")");

    logos
      .append("image")
      .attr("xlink:href", function (episode) { return episode.show.image_url; })
      .attr("width", logoSize)
      .attr("height", logoSize);

    var needle = bars.append("line")
      .attr("class", "needle");

    needle
      .attr("x1", this.timeScale(0))
      .attr("y1", this.barHeight)
      .attr("x2", this.timeScale(0))
      .attr("y2", 0);

    this.needle = needle;

    function moveNeedleOnMouse() {
      var mouseX = d3.mouse(this)[0];
      that.needle
        .transition()
        .duration(10)
        .attr("x1", mouseX)
        .attr("x2", mouseX);
    };

    var resetNeedle = function () {
      var resetX = that.timeScale(0);

      needle
        .transition()
        .attr("x1", resetX)
        .attr("x2", resetX);
    };

    bars.selectAll("rect")
      .on("mousemove", moveNeedleOnMouse)
      .on("mouseout", resetNeedle);

    this.trigger("left");
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

    // Translate the bars
    episodes.selectAll("g.bar")
      .attr("transform", function (episode) {
        var barWidth = that.timeScale(episode.duration),
            barHeight = that.barHeight; // Smelly
        return "translate(-" + barWidth/2 + ",-" + barHeight/2 + ")";
      });

    // Translate the titles
    episodes.selectAll("g.title").selectAll("text")
      .attr("dominant-baseline", "central")
      .attr("text-anchor", "middle");
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

    // Translate the bars
    var logoWidth = 40;
    episodes.selectAll("g.bar")
      .attr("transform", "translate(" + logoWidth + ",-" + that.barHeight/2 + ")");

    episodes.selectAll("g.title")
      .attr("transform", "translate(" + logoWidth + ",0)");

    // Translate the titles
    episodes.selectAll("g.title").selectAll("text")
      .attr("dominant-baseline", "central")
      .attr("text-anchor", "left");

  }
});
