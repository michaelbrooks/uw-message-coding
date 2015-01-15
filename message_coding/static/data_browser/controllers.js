(function () {
    'use strict';

    var module = angular.module('message_coding.dataBrowser.controllers', [
        'message_coding.dataBrowser.services',
        'ng.django.urls'
    ]);

    var BrowserController = function ($scope, Project, Dataset, Message, Selection, djangoUrl) {
        var dataset_id = 1;
        var project_id = 1;
        var user_id = 1;

        $scope.project = Project.get({pk: project_id});
        $scope.dataset = Dataset.get({pk: dataset_id});

        $scope.page = 1;
        $scope.messages = Message.get({
            dataset_id: dataset_id,
            page: $scope.page
        });

        var loadMessages = function (page) {
            Message
                .get({
                    dataset_id: dataset_id,
                    page: page
                })
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
            var selection = new Selection({
                dataset: dataset_id,
                type: 'json',
                selection: {'text__like': 'cat'}
            });

            selection
                .$save()
                .then(function () {
                    document.location.href = djangoUrl.reverse('task_create', {
                        project_slug: $scope.project.slug,
                        selection_pk: selection.id
                    });
                });
        };
    };

    BrowserController.$inject = ['$scope', 'Project', 'Dataset', 'Message', 'Selection', 'djangoUrl'];

    module.controller('BrowserController', BrowserController);
})();
