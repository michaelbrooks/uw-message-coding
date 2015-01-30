/**
 * Top level module for dataset browsing application.
 */
(function () {
    'use strict';

    //An empty module for bootstrapping initial data
    angular.module('message_coding.coding.bootstrap', []);

    // Declare app level module which depends on other modules
    var app = angular
        .module('message_coding.coding', [
            'message_coding.coding.controllers',
            'ngCookies'
        ]);

    //Fix CSRF
    //http://django-angular.readthedocs.org/en/latest/csrf-protection.html
    app.run(['$http', '$cookies', function ($http, $cookies) {
        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    }]);
})();
