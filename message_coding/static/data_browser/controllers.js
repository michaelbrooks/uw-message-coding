(function () {
    'use strict';

    var module = angular.module('message_coding.dataBrowser.controllers', [
        'message_coding.dataBrowser.services',
        'ng.django.urls'
    ]);

    var requires = ['$scope', 'Project', 'Dataset', 'Message', 'Task', 'djangoUrl'];
    var BrowserController = function ($scope, Project, Dataset, Message, Task, djangoUrl) {
        var dataset_id = 1;
        var project_id = 1;
        var user_id = 1;

        $scope.selection = {};

        $scope.project = Project.get({pk: project_id});
        $scope.dataset = Dataset.get({pk: dataset_id});

        $scope.page = 1;
        $scope.messages = Message.get({
            dataset_id: dataset_id,
            page: $scope.page
        });

        var loadMessages = function (page) {
            var selection = angular.extend({
                dataset_id: dataset_id,
                page: page
            }, $scope.selection);

            Message
                .get(selection)
                .$promise.then(function (result) {
                    $scope.messages = result;
                    $scope.page = page;
                });
        };

        $scope.nextMessages = function () {
            if ($scope.messages.next) {
                loadMessages($scope.page + 1);
            }
        };

        $scope.previousMessages = function () {
            if ($scope.messages.previous) {
                loadMessages($scope.page - 1);
            }
        };

        $scope.createTask = function () {
            var task = new Task({
                project: project_id,
                selection: {
                    dataset: dataset_id,
                    type: 'json',
                    selection: $scope.selection
                }
            });

            task.$save()
                .then(function () {
                    document.location.href = djangoUrl.reverse('task_edit', {
                        project_slug: $scope.project.slug,
                        task_pk: task.id
                    });
                });
        };
    };

    BrowserController.$inject = requires;

    module.controller('BrowserController', BrowserController);
})();
