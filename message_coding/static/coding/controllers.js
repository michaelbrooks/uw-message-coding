(function () {
    'use strict';

    var module = angular.module('message_coding.coding.controllers', [
        'message_coding.coding.services',
        'message_coding.coding.bootstrap',
        'message_coding.coding.models',
        'ng.django.urls'
    ]);

    var requires = ['$scope', 'djangoUrl',
        'message_coding.base.services.Project',
        'message_coding.base.services.Dataset',
        'message_coding.base.services.Task',
        'message_coding.coding.bootstrap.initial_data'];
    var CodingController = function ($scope, djangoUrl,
                                      Project, Dataset, Task,
                                      MessagePageModel,
                                      initial_data) {

        $scope.user = initial_data.user;
        $scope.project = new Project(initial_data.project);
        $scope.dataset = new Dataset(initial_data.dataset);
        $scope.task = new Task(initial_data.task);

    };

    CodingController.$inject = requires;
    module.controller('message_coding.coding.controllers.CodingController', CodingController);
})();
