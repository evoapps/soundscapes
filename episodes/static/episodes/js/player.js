
function updateProgress() {
  var audioElement = document.querySelector("audio");

  currentTime = audioElement.currentTime;
  console.log(timeScale(currentTime));

  d3.select("#needle")
    .attr("x1", timeScale(currentTime))
    .attr("x2", timeScale(currentTime));
}

function toggleAudio() {
  var audioElement = document.querySelector("audio");

  if (audioElement.paused) {
    audioElement.play();
  } else {
    audioElement.pause();
  }

}
