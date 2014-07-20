"use strict";

var Contents = {};

/*
A Youtube Video Content
 */
Contents.YoutubeVideo = Backbone.Model.extend({
    urlRoot: '/contents',

    defaults: function() {
        return {"url": "", "title": "", "publishedAt": ""};
    }
});


/*
Collection of Youtube Video Contents
 */
Contents.YoutubeVideos = Backbone.Collection.extend({
    model: Contents.YoutubeVideo,

    url: "/contents",

    initialize: function(keyword) {
        this.next_page_token = null;
        this.keyword = keyword;
    },

    parse: function(resp) {
        this.next_page_token = resp.next_page_token;
        return resp.items;
    },

    is_last_page: function() {
        return !this.next_page_token;
    },

    fetch: function(options) {
        options = options !== undefined ? options : {};
        options = _.extend(options, {
            data: {keyword: this.keyword, next_page_token: this.next_page_token}
        });
        return Backbone.Collection.prototype.fetch.call(this, options);
    },

    next: function(options) {
        options = options !== undefined ? options : {};
        options = _.extend(options, {
            reset: false,
            remove: false
        });
        this.fetch(options);
    }
});
