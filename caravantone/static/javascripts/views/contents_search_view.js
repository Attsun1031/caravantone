"use strict";

$(function() {
    var submit_search_form_event = "submit_search_form";

    var SearchFormView = Backbone.View.extend({
        el: "#contents_search .search_form_area",

        events: {
            "submit #contents_search_form": "handle_submit"
        },

        initialize: function(options) {
            this.$keyword_input = $("#keyword");
        },

        handle_submit: function(e) {
            e.preventDefault();

            var keyword = this.$keyword_input.val();
            if (!_.isEmpty(keyword)) {
                this.trigger(submit_search_form_event, keyword);
            } else {
                alert("検索キーワードを入力してください。")
            }
        }
    });

    var ContentView = Backbone.View.extend({
        template: _.template($("#content_template").html()),

        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    var ContentsListView = Backbone.View.extend({
        el: "#contents_search .search_results",

        initialize: function(options) {
            this.listenTo(this.collection, 'reset', this.render);
            this.listenTo(this.collection, 'add', this.render_each_model);
        },

        render_each_model: function(content) {
            // 各アイテムのレンダリング
            var content_view = new ContentView({model: content});
            this.$el.append(content_view.render().el);
        },

        render: function(contents) {
            // アイテムを空にした上でレンダリング
            this.$el.empty();
            contents.each(_.bind(this.render_each_model, this));
        }
    });

    var MainView = Backbone.View.extend({
        el: "#contents_search",

        events: {"add_item": "add_item2list"},

        initialize: function(options) {
            this.form = new SearchFormView();
            this.listenTo(this.form, submit_search_form_event, this.reload);
            this.contents = [];
            this.list_view = undefined;
            this.mugen_loader = undefined;
        },

        reload: function(keyword) {
            // TODO: nextPageTokenの受け渡しをどうするか？
            this.mugen_loader = new MugenLoader({
                on_next: _.bind(this.next, this),
                $view: this.$el
            });
            this.contents = new Contents.YoutubeVideos(keyword);
            this.list_view = new ContentsListView({collection: this.contents});
            this.contents.fetch({
                reset: true,
                success: _.bind(this.mugen_loader.start, this.mugen_loader)
            });
        },

        next: function() {
            this.contents.next({success: _.bind(this.on_after_loading, this)});
        },

        add_item2list: function(e, item) {
            this.add_item_dialog.handle_add_item(item);
        },

        on_after_loading: function() {
            if (!this.contents.is_last_page()) {
                // まだアイテムがあればロードを再開する。
                this.mugen_loader.resume();
            }
        }
    });

    new MainView();
});
