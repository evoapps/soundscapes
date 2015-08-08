
var EpisodeCollectionView = Backbone.View.extend({
  el: "ul",

  initialize: function () {
    var that = this;

    var maxDuration,
        maxWidth;

    maxDuration = d3.max(this.collection.models, function (episode) {
      return episode.get("duration");
    });

    this._episodeBarViews = [];
    this.collection.each(function (episode) {
      that._episodeBarViews.push(new EpisodeBarView({
        model: episode,
        maxDuration: maxDuration
        }));
    });

    this.maxWidth = window.innerWidth;
  },

  render: function () {
    var that = this;
    $(this.el).empty();

    _(this._episodeBarViews).each(function (episodeBarView) {
      $(that.el).append(episodeBarView.render().el);
    });

    this.on("soundmanager:ready", function () {
      // console.log("soundmanager:ready, so loading first episode")
      // var firstEpisodeId = this.collection.models[0].id;
      this.trigger("collection:load");
    });

    this.on("collection:load", this.loadEpisode);
  },

  loadEpisode: function () {
    this._episodeBarViews.forEach(function (episodeBarView) {
      episodeBarView.createEpisodeSound();
    });
  }

});
