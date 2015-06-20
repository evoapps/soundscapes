
function drawEpisodeList(episodes) {
  globalVars.episodes = episodes;

  // Convert release string to javascript Date
  episodes.forEach(parseEpisode);

  d3.select("#episodeList")
    .selectAll("div.episode")
    .data(episodes)
    .enter()
    .append("div")
    .attr("class", "episode");

  var episodeDivs = d3.selectAll("div.episode");

  episodeDivs.append("h2")
    .append("a")
    .attr("href", function (ep) { return ep.url; })
    .text(function (ep) { return ep.title; });
}

function drawSegments(episode) {
  // don't know if this is going to be a single object or an array
  globalVars.episode = episode;

  parseEpisode(episode);
  episode.segments.forEach(addEndMoments);

  var svgWidth = 500,
      svgHeight = 200;

  var line = d3.svg.line(),
      timeScale = d3.scale.linear(),
      valueScale = d3.scale.linear();

  line
    .x(function (moment) { return timeScale(moment.time); })
    .y(function (moment) { return valueScale(moment.value); });

  timeScale
    .domain(d3.extent(episode.moments, function (moment) { return parseFloat(moment.time); }))
    .range([0, svgWidth]);

  valueScale
    .domain(d3.extent(episode.moments, function (moment) { return moment.value; }))
    .range([svgHeight, 0]);

  d3.select("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight)
    .selectAll("path.segment")
    .data(episode.segments)
    .enter()
    .append("path")
    .attr("class", "segment")
    .attr("d", function (segment) { return line(segment.moments) + "Z"; })
}

function parseEpisode(episode) {
  episode.released = Date.parse(episode.released);
}

function addEndMoments(segment) {
  var firstMoment = {time: segment.start_time, value: 0.0},
      lastMoment = {time: segment.end_time, value: 0.0};
  segment.moments.splice(0, 0, firstMoment);
  segment.moments.push(lastMoment);
}
