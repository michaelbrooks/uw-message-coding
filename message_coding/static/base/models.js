(function () {
    'use strict';

    var module = angular.module('message_coding.base.models', [
        'message_coding.base.services'
    ]);

    /**
     * A Pager is constructed from an Angular Resource type
     * that implements a paginated delivery system following a specific
     * format.
     *  
     * When constructed, options must include the resource class.
     * You may also specify 'query' data to be included with the
     * request, and a callback to be used every time a new
     * page is loaded.
     */
    module.factory('message_coding.base.models.Pager',
        [function () {

            var default_init = {
                callback: null,
                query: {}
            };
            
            var Pager = function (options) {
                options = angular.extend({}, default_init, options);

                if (!options.hasOwnProperty('resource')) {
                    throw('Must provide resource');
                }

                this.resource = options.resource;
                this.callback = options.callback;
                this.query = options.query;

                this.page = 0;
                this.hasNext = true;
                this.hasPrevious = false;
                this.totalCount = 0;
                this.pageCount = 0;
                this.currentSet = null;
                
                this.isLoading = false;
            };

            //Transparent iteration -- return false to cancel
            Pager.prototype.forEach = function (callback) {
                loadAndContinueWith.call(this, callback);
            };

            function loadAndContinueWith(callback) {
                this.loadNextPage(function (currentSet, self) {

                    //Return false to cancel
                    if (callback) {
                        for (var i = 0; i < currentSet.length; i++) {
                            if (false === callback(currentSet[i], self)) return;
                        }
                    }

                    if (self.hasNext) {
                        loadAndContinueWith(callback);
                    }

                });
            }

            Pager.prototype.loadNextPage = function (callback) {
                if (!this.hasNext) {
                    return;
                }

                if (this.isLoading) return;
                this.isLoading = true;

                var page = this.page + 1;
                var query = angular.extend({
                    page: page
                }, this.query);

                var self = this;
                
                var success = function (result) {
                    self.isLoading = false;
                    
                    self.currentSet = result.results.map(function(item) {
                        return new self.resource(item);
                    });

                    self.hasNext = Boolean(result.next);
                    self.hasPrevious = Boolean(result.previous);
                    self.totalCount = result.count;
                    self.pageCount = result.page_count;

                    //Update the state
                    self.page = page;
                    
                    callback && callback(self.currentSet, self);
                    self.callback && self.callback(self.currentSet, self);
                };
                
                var failure = function(result) {
                    self.isLoading = false;
                };
                
                return this.resource.get(query, success, failure);
            };

            return Pager;
        }]);

    module.factory('message_coding.base.models.IndexedCollection',
        [function () {
            // Default page model state
            var default_init = {
                id: 'id',
                items: []
            };
            
            var toId = function(idOrObj, idProp) {
                if (typeof(idOrObj) === 'object') {
                    return idOrObj[idProp];
                } else {
                    return idOrObj;
                }
            };

            var IndexedCollection = function (options) {
                options = angular.extend({}, default_init, options);

                this._id_property = options.id;

                this.clear();

                for (var i = 0; i < options.items.length; i++) {
                    this.add(options.items[i]);
                }
            };

            angular.extend(IndexedCollection.prototype, {
                get: function (id) {
                    id = toId(id, this._id_property);
                    
                    if (this.contains(id)) {
                        return this._index[id];
                    }
                },
                add: function (obj) {
                    var id = obj[this._id_property];
                    if (!this.contains(id)) {
                        this._index[id] = obj;
                        this._items.push(obj);
                        this._size += 1;
                        return true;
                    }
                    return false;
                },
                addAll: function (arr) {
                    for (var i = 0; i < arr.length; i++) {
                        this.add(arr[i]);
                    }
                },
                contains: function (id) {
                    id = toId(id, this._id_property);
                    return this._index.hasOwnProperty(id);
                },
                remove: function (id) {
                    id = toId(id, this._id_property);
                    if (this.contains(id)) {
                        delete this._index[id];
                        return true;
                    }
                    return false;
                },
                clear: function () {
                    this._index = {};
                    this._size = 0;
                    this._items = [];
                },
                size: function () {
                    return this._size;
                },
                forEach: function (callback) {
                    this._items.forEach(callback);
                }
            });

            return IndexedCollection;
        }]);

    module.factory('message_coding.base.models.MessagePageModel',
        ['message_coding.base.services.Message', function (Message) {

            // Default page model state
            var default_init = {
                initial_page: 1,
                filters: {}
            };

            // Model constructor
            var MessagePageModel = function (options) {
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
                },

                applyFilter: function () {
                    loadMessages.call(this);
                }
            });

            //Private data loading method
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
