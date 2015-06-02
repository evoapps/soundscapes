
show_soundscapes = function(episodes) {
  var episodes = JSON.parse(episodes); // don't know why d3.json doesn't handle this

  // Convert release string to javascript Date
  episodes.forEach(function(el) {
    el.fields.released = Date.parse(el.fields.released);
  });

  var numEpisodes = episodes.length,
      episodeDetailHeight = 30,
      episodeTimelineRadius = 5;

  var svgWidth = 700,
      svgHeight = episodeDetailHeight * numEpisodes;

  var episodeDetailX = 100,
      episodeTimelineX = 20;

  var episodeDetailScale = d3.scale.linear()
    .domain([episodes.length, 1])
    .range([svgHeight - episodeDetailHeight, episodeDetailHeight]);

  var episodeTimelineScale = d3.time.scale()
    .domain([
      d3.min(episodes, function(el) { return el.fields.released; }),
      Date.now()
    ])
    .range([svgHeight - episodeTimelineRadius, episodeTimelineRadius]);

  var hover = function(el, bool) { d3.select(this).classed("hover", bool); },
      hoverOn = function(el) { return hover(el, true); },
      hoverOff = function(el) { return hover(el, false); };

  d3.select("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight)

  highlight = function(el) {
    var gEpisode = d3.select(this);
    gEpisode.select("text").classed("hover", true);
    gEpisode.select("circle").classed("hover", true);
    gEpisode.select("path").classed("hover", true);
  }

  unlight = function(el) {
    var gEpisode = d3.select(this);
    gEpisode.select("text").classed("hover", false);
    gEpisode.select("circle").classed("hover", false);
    gEpisode.select("path").classed("hover", false);
  }

  d3.select("svg")
    .selectAll("g")
    .data(episodes)
    .enter()
    .append("g")
    .attr("class", "episode")
    .on("mouseover", highlight)
    .on("mouseout", unlight);

  d3.select("svg")
    .selectAll("g")
    .append("text")
    .text(function(ep) { return ep.fields.title; })
    .attr("x", episodeDetailX)
    .attr("y", function(el, i) { return episodeDetailScale(i); });

  d3.select("svg")
    .selectAll("g")
    .append("circle")
    .attr("r", episodeTimelineRadius)
    .attr("cx", episodeTimelineX)
    .attr("cy", function(el) { return episodeTimelineScale(el.fields.released); });

  var connector = d3.svg.diagonal.radial()
    .source(function(el) { return {x: episodeTimelineX, y: episodeTimelineScale(el.fields.released)}; })
    .target(function(el, i) { return {x: episodeDetailX, y: episodeDetailScale(i)}; });

  d3.select("svg")
    .selectAll("g")
    .append("path")
    .attr("d", connector)
    .attr("class", "link");
}
