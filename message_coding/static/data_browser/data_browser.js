/**
 * Top level module for dataset browsing application.
 */
(function () {
    'use strict';


    // Declare app level module which depends on other modules
    var app = angular
        .module('message_coding.dataBrowser', [
            'message_coding.dataBrowser.controllers',
            'message_coding.dataBrowser.services',
            'ngRoute',
            'ngCookies'
        ]);

    // Define the app routes
    app.config(['$routeProvider', 'django_config', function ($routeProvider, django_config) {

        // Similar to Django's static template tag
        function djstatic(url) {
            return django_config.STATIC_URL + url;
        }

        $routeProvider
            .when('/', {
                templateUrl: djstatic('data_browser/templates/browser.html'),
                controller: 'BrowserController'
            })
            .otherwise({redirectTo: '/'});
    }]);

    //Fix CSRF
    //http://django-angular.readthedocs.org/en/latest/csrf-protection.html
    app.run(['$http', '$cookies', function ($http, $cookies) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    }]);
})();
