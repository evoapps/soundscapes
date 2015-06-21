
function drawEpisodeList(episodes) {

  // Convert release string to javascript Date
  episodes.forEach(parseEpisode);

  d3.select("#episodeList")
    .selectAll("svg")
    .data(episodes)
    .enter()
    .append("svg")
    .attr("class", "soundscape")
    .attr("id", function (episode) { return "episode" + episode.id; })
    .each(drawSegments);
}

function drawSegments(episode) {

  var svgWidth = 500,
      svgHeight = 200;

  var line = d3.svg.line(),
      timeScale = d3.scale.linear(),
      valueScale = d3.scale.linear();

  line
    .x(function (moment) { return timeScale(moment.time); })
    .y(function (moment) { return valueScale(moment.value); })
    .interpolate("basis");

  timeScale
    .domain(d3.extent(episode.moments, function (moment) { return parseFloat(moment.time); }))
    .range([0, svgWidth]);

  valueScale
    .domain(d3.extent(episode.moments, function (moment) { return moment.value; }))
    .range([svgHeight, 0]);

  episode.segments.forEach(addEndMoments);

  d3.select("#episode" + episode.id)
    .attr("width", svgWidth)
    .attr("height", svgHeight)
    .append("g")
    .attr("class", "episode")
    .attr("id", "episode" + episode.id)
    .selectAll("path.segment")
    .data(episode.segments)
    .enter()
    .append("path")
    .attr("class", "segment")
    .attr("id", function (segment) { return "segment" + segment.id; })
    .attr("d", function (segment) { return line(segment.moments) + "Z"; })

  function selectSegment(segment) {
    var episodeGroup = d3.select(this.parentNode);

    if (!episodeGroup.classed("loaded")) {
      return;
    }

    var segmentPath = d3.select(this);

    segmentPath.classed("playing", !segmentPath.classed("playing"));
    if (segmentPath.classed("playing")) {
      episode.playEpisode(segment.start_time);
    } else {
      episode.stopEpisode();
    }
  }

  // d3.selectAll("path.segment")
  //   .on("click", selectSegment);
  //
  // loadEpisodeAudioSource(episode);
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
