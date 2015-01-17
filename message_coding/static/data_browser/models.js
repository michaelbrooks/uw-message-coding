(function() {
    'use strict';

    var module = angular.module('message_coding.dataBrowser.models', [
        'message_coding.dataBrowser.services'
    ]);

    module.factory('message_coding.dataBrowser.models.MessagePageModel',
        ['message_coding.dataBrowser.services.Message', function(Message) {

        // Default page model state
        var default_init = {
            initial_page: 1,
            filters: {}
        };

        // Model constructor
        var MessagePageModel = function(options) {
            if (typeof(options.dataset_id) == 'undefined') {
                throw("You must provide a dataset_id");
            }

            options = angular.extend({}, default_init, options);

            //This stays the same
            this.dataset_id = options.dataset_id;

            //These are controlled by the user
            this.page = options.initial_page;
            this.filters = options.filters;

            //These are returned by the server
            this.messages = [];
            this.hasNext = false;
            this.hasPrevious = false;
            this.totalCount = 0;
            this.pageCount = 0;

            loadMessages.call(this);
        };

        //Public methods
        angular.extend(MessagePageModel.prototype, {
            nextPage: function () {
                if (this.hasNext) {
                    loadMessages.call(this, this.page + 1);
                }
            },

            previousPage: function () {
                if (this.hasPrevious) {
                    loadMessages.call(this, this.page - 1);
                }
            },

            setFilters: function (filters) {
                this.filters = filters;
                loadMessages.call(this, this.page);
            }
        });

        //Privde data loading method
        var loadMessages = function (page, filters) {
            if (page instanceof Object) {
                filters = page;
                page = undefined;
            }

            filters = filters || this.filters;
            page = page || this.page;

            var query = angular.extend({
                dataset_id: this.dataset_id,
                page: page
            }, filters);

            var self = this;
            return Message.get(query).$promise.then(function (result) {
                //Save the server data
                self.messages = result.results;
                self.hasNext = Boolean(result.next);
                self.hasPrevious = Boolean(result.previous);
                self.totalCount = result.count;
                self.pageCount = result.page_count;

                //Update the state
                self.page = page;
                self.filters = filters;
            });
        };

        return MessagePageModel;
    }]);
})();
