show_soundscapes = function(episodes) {
  var episodes = JSON.parse(episodes); // don't know why this isn't automatic

  episodes.forEach(function(el) {
    el.fields.released = Date.parse(el.fields.released);
  });

  var numEpisodes = episodes.length,
      perEpisodeHeight = 30;

  var svgWidth = 700,
      svgHeight = perEpisodeHeight * (numEpisodes + 1);

  d3.select("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight)
    .selectAll("g")
    .data(episodes)
    .enter()
      .append("g")
      .attr("class", "episode");

  var episodeNodes = d3.selectAll("g.episode")

  var episodeDetailLeftBuffer = 100;

  episodeNodes.append("g")
    .append("text")
    .text(function(ep) { return ep.fields.title; })
    .attr("x", episodeDetailLeftBuffer)
    .attr("y", function(ep, i) { return perEpisodeHeight * (i + 1); })
    .on("mouseover", function(ep) {
      d3.select(this).classed("hover", true);
    })
    .on("mouseout", function(ep) {
      d3.select(this).classed("hover", false);
    });

  var rightNow = Date.now(),
      firstEpisode = d3.min(episodes,
        function(el) { return el.fields.released; });

  var timeNodeLeftBuffer = 10,
      timeNodeRadius = 5;

  var timeScale = d3.time.scale()
    .domain([firstEpisode, rightNow])
    .range([svgHeight + timeNodeRadius, timeNodeRadius]);

  episodeNodes.append("g")
    .append("circle")
    .attr("r", timeNodeRadius)
    .attr("cx", timeNodeLeftBuffer + timeNodeRadius)
    .attr("cy", function(el) { return timeScale(el.fields.released); });
}
