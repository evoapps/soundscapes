var audioContext = new (window.AudioContext || window.webkitAudioContext)();

function loadEpisodeAudioSource(episode) {
  var episodeBuffer = null,
      source = null;

  var request = new XMLHttpRequest();
  request.open('GET', episode.mp3, true);
  request.responseType = 'arraybuffer';

  // Decode asynchronously
  request.onload = function () {
    audioContext.decodeAudioData(request.response,
      function (buffer) {
        episodeBuffer = buffer;
        var episodeGroup = document.getElementById("episode" + episode.id);
        episodeGroup.classList.add("loaded");
      },
      function (error) { console.log(error); });
  }
  request.send();

  function playEpisode(offset) {
    source = audioContext.createBufferSource();
    source.buffer = episodeBuffer;
    source.connect(audioContext.destination);
    source.start(0, offset);
  }

  episode.playEpisode = playEpisode;
  episode.stopEpisode = function () { source.stop(); };
}
