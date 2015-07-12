
var svgWidth = 600,
    svgHeight = 400;

var timeScale = d3.scale.linear(),
    valueScale = d3.scale.linear(),
    showColorScale = d3.scale.ordinal();

// Set time scale range
// - domains are set based on query
timeScale
  .range([0, svgWidth])

// Set value scale globally
valueScale
  .domain([60, 93, 101, 120])
  .range([svgHeight, svgHeight/2, svgHeight/8, 0])

// Hand code colors for Gimlet shows
showColorScale
  .domain(["StartUp", "Reply All", "Mystery Show"])
  .range(["Blues", "Greens", "Purples"]);

var line = d3.svg.line();

line
  .x(function (moment) { return timeScale(moment.time); })
  .y(function (moment) { return valueScale(moment.value); })
  .interpolate("basis");

function drawEpisodeList(episodes) {

  var maxTimes = [];
  episodes.forEach(function (episode) {
    var episodeMax = d3.max(episode.moments, function (moment) { return moment.time; });
    maxTimes.push(episodeMax);
  });

  timeScale
    .domain([0, d3.max(maxTimes)]);

  var episodeList = d3.select("#episodeList")

  episodeList
    .selectAll("li")
    .data(episodes)
    .enter()
    .append("li")

  var episodeItems = episodeList.selectAll("li");

  episodeItems
    .append("div")
    .attr("class", "episode svg-container")
    .append("svg")
    .attr("preserveAspectRatio", "xMidYMid")
    .attr("viewBox", "0 0 600 400")
    .attr("class", "episode svg-content-responsive")
    .append("g")
    .attr("id", function (episode) { return "episodeGroup" + episode.id; })

  episodeItems
    .append("h3")
    .append("a")
    .text(function (episode) { return episode.title; })
    .attr("href", function (episode) { return episode.url; });

  episodeItems
    .append("audio")
    .attr("src", function (episode) { return episode.mp3; });

  episodeItems
    .each(drawSegments);
}

function drawSingleEpisode(episode) {
  timeScale
    .domain(d3.extent(episode.moments, function (moment) { return moment.time; }));

  drawSegments(episode);
}

function drawSegments(episode) {
  globalVars.episode = episode;

  // Add end moments
  episode.segments.forEach(function(segment) {
    var firstMoment = {time: segment.start_time, value: 0},
        lastMoment = {time: segment.end_time, value: 0};
    segment.moments.splice(0, 0, firstMoment);
    segment.moments.push(lastMoment);
  });

  // Determine segment color
  // - requires knowing the segment's show name
  episode.segments.forEach(function (segment) {
    var ramp = showColorScale(episode.show.name),
        size = 5,
        hue = 3;  // arbitrarily select the center hue
    segment.fill = colorbrewer[ramp][size][hue];
  });

  var episodeGroup = d3.select("#episodeGroup" + episode.id);

  // Draw player needle
  episodeGroup
    .append("line")
    .attr("id", "needle")

  var needle = episodeGroup.select("#needle");

  needle
    .style("stroke", "black")
    .attr("x1", timeScale(0))
    .attr("y1", d3.min(valueScale.range()))
    .attr("x2", timeScale(0))
    .attr("y2", d3.max(valueScale.range()));

  // Draw a rectangle behind the soundscapes
  episodeGroup
    .append("rect")
    .attr("id", "episodeBackground" + episode.id)

  var episodeBackground = episodeGroup.select("#episodeBackground" + episode.id);

  episodeBackground
    .attr("x", d3.min(timeScale.range()))
    .attr("y", d3.min(valueScale.range()))
    .attr("width", d3.max(timeScale.range()))
    .attr("height", d3.max(valueScale.range()))
    .style("opacity", 0)
    .style("stroke", "black")

  function moveNeedle() {
    var mouseX = d3.mouse(this)[0];
    needle
      .attr("x1", mouseX)
      .attr("x2", mouseX);
  }

  function removeNeedle() {
    var resetX = timeScale(0);
    needle
      .attr("x1", resetX)
      .attr("x2", resetX);
  }

  episodeBackground
    .on("mousemove", moveNeedle)
    .on("mouseout", removeNeedle)

  // Draw each segment as a path
  episodeGroup
    .selectAll("path.segment")
    .data(episode.segments)
    .enter()
    .append("path")
    .attr("class", "segment")
    .attr("id", function (segment) { return "segment" + segment.id; });

  var episodeSegments = episodeGroup.selectAll("path.segment");

  episodeSegments
    .attr("d", function (segment) { return line(segment.moments) + "Z"; })
    .style("fill", function (segment) { return segment.fill; });

  function playSegment(segment) {
    // Prevent clicking segment from triggering other click listeners
    d3.event.stopPropagation();

    var audioElement = document.querySelector("audio");

    // Toggle the audio
    if (audioElement.paused) {
      audioElement.play();
      episodeGroup.classed("playing", true);
    } else {
      audioElement.pause();
      episodeGroup.classed("playing", false);
    }
  }

  episodeSegments
    .on("click", playSegment)

  function updateProgress() {
    var audioElement = document.querySelector("audio"),
        currentTime = audioElement.currentTime;

    needle
      .attr("x1", timeScale(currentTime))
      .attr("x2", timeScale(currentTime));
  }

  var audioElement = document.querySelector("audio");
  audioElement.addEventListener("timeupdate", updateProgress, false);
}
