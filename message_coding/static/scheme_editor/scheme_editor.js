/**
 * Top level module for scheme editor application.
 */
(function () {
    'use strict';

    //An empty module for bootstrapping initial data
    angular.module('message_coding.schemeEditor.bootstrap', []);

    // Declare app level module which depends on other modules
    var app = angular
        .module('message_coding.schemeEditor', [
            'message_coding.schemeEditor.controllers',
            'ngCookies',
            'xeditable'
        ]);

    //Fix CSRF
    //http://django-angular.readthedocs.org/en/latest/csrf-protection.html
    app.run(['$http', '$cookies', 'editableOptions',
        function ($http, $cookies, editableOptions) {
            $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
            editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
        }
    ]);
})();
