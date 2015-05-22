(function () {
    'use strict';

    var module = angular.module('message_coding.base.services', [
        'ngResource',
        'ng.django.urls'
    ]);

    module.config(['$resourceProvider', function ($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }]);

    module.service('message_coding.base.services.Project',
        ['$resource', function ($resource) {
            return $resource('/api/projects/:id/');
        }]);

    module.service('message_coding.base.services.Dataset',
        ['$resource', 'djangoUrl', function ($resource, djangoUrl) {
            //TODO: get urls from djangoUrl conf
            //djangoUrl.reverse('api:dataset-detail')

            return $resource('/api/datasets/:id/');
        }]);

    module.service('message_coding.base.services.Message',
        ['$resource', function ($resource) {
            var Message = $resource('/api/messages/:id/');

            Message.prototype.findRelatedInstanceForCode = function (id) {
                if (this.hasOwnProperty('_codeInstances')) {
                    var ci;
                    for (var i = 0; i < this._codeInstances.length; i++) {
                        ci = this._codeInstances[i];
                        if (ci.code == id) {
                            return ci;
                        }
                    }
                }

                return false;
            };

            Message.prototype.relateCodeInstance = function (codeInstance) {
                if (!this.hasOwnProperty('_codeInstances')) {
                    this._codeInstances = [];
                }
                this._codeInstances.push(codeInstance);

                codeInstance._message = this;
            };

            Message.prototype.unrelateCodeInstance = function (codeInstance) {
                if (this.hasOwnProperty('_codeInstances')) {
                    var index = this._codeInstances.indexOf(codeInstance);
                    if (index >= 0) {
                        this._codeInstances.splice(index, 1);
                        delete codeInstance._message
                    }
                }
            };

            return Message;
        }]);

    module.service('message_coding.base.services.Selection',
        ['$resource', function ($resource) {
            return $resource('/api/selections/:id/');
        }]);

    module.service('message_coding.base.services.Task',
        ['$resource', function ($resource) {
            return $resource('/api/tasks/:id/');
        }]);

    module.service('message_coding.base.services.CodeInstance',
        ['$resource', function ($resource) {
            return $resource('/api/code_instances/:id/', {
                id: '@id'
            }, {
                'update': { method: 'PUT' }
            });
        }]);

    module.service('message_coding.base.services.Code',
        ['$resource', function($resource) {
            return $resource('/api/codes/:id/', {
                id: '@id'
            }, {
                'update': { method: 'PUT' }
            });
        }]);

    module.service('message_coding.base.services.CodeGroup',
        ['$resource', function($resource) {
            return $resource('/api/code_groups/:id/', {
                id: '@id'
            }, {
                'update': { method: 'PUT' }
            });
        }]);

    module.service('message_coding.base.services.CodeScheme',
        ['$resource', '$http', function ($resource, $http) {

            var CodeScheme = $resource('/api/schemes/:id/', {
                id: '@id'
            }, {
                'update': { method: 'PUT' }
            });

            //Iterate through all codes
            CodeScheme.prototype.forEachCode = function (callback) {
                this.code_groups.forEach(function (grp, grp_idx) {
                    grp.codes.forEach(function (code, code_idx) {
                        callback(code, code_idx, grp, grp_idx);
                    });
                });
            };
            return CodeScheme;
        }]);
})();
