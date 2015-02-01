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
            return $resource('/api/messages/:id/');
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
            });
        }]);

    module.service('message_coding.base.services.CodeScheme',
        ['$resource', function ($resource) {
            return $resource('/api/schemes/:id/');
        }]);
})();
