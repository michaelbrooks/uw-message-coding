(function () {
    'use strict';

    var module = angular.module('message_coding.dataBrowser.services', [
        'ngResource',
        'ng.django.urls'
    ]);

    module.config(['$resourceProvider', function ($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }]);

    module.service('message_coding.dataBrowser.services.Project',
        ['$resource', function ($resource) {
            return $resource('/api/projects/:pk/');
        }]);

    module.service('message_coding.dataBrowser.services.Dataset',
        ['$resource', 'djangoUrl', function ($resource, djangoUrl) {
            //TODO: get urls from djangoUrl conf
            //djangoUrl.reverse('api:dataset-detail')

            return $resource('/api/datasets/:pk/');
        }]);

    module.service('message_coding.dataBrowser.services.Message',
        ['$resource', function ($resource) {
            return $resource('/api/messages/:pk/');
        }]);

    module.service('message_coding.dataBrowser.services.Selection',
        ['$resource', function ($resource) {
            return $resource('/api/selections/:pk/');
        }]);

    module.service('message_coding.dataBrowser.services.Task',
        ['$resource', function ($resource) {
            return $resource('/api/tasks/:pk/');
        }]);

})();
