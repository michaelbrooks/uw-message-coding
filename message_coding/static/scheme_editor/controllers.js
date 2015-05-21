(function () {
    'use strict';

    var module = angular.module('message_coding.schemeEditor.controllers', [
        'message_coding.schemeEditor.services',
        'message_coding.schemeEditor.bootstrap',
        'message_coding.schemeEditor.models',
        'ng.django.urls'
    ]);

    var requires = ['$scope', 'djangoUrl',
        'message_coding.base.services.Project',
        'message_coding.base.services.CodeScheme',
        'message_coding.schemeEditor.bootstrap.initial_data'];
    var EditorController = function ($scope, djangoUrl,
                                      Project, CodeScheme,
                                      initial_data) {

        $scope.user = initial_data.user;
        $scope.project = new Project(initial_data.project);
        $scope.scheme = new CodeScheme(initial_data.scheme);

        $scope.saveScheme = function() {
            console.log($scope.scheme);
            debugger;
        };
    };

    EditorController.$inject = requires;
    module.controller('message_coding.schemeEditor.controllers.EditorController', EditorController)
})();
