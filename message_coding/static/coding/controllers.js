(function () {
    'use strict';

    var module = angular.module('message_coding.coding.controllers', [
        'message_coding.coding.services',
        'message_coding.coding.bootstrap',
        'message_coding.coding.models',
        'ng.django.urls'
    ]);

    var requires = ['$scope',
        'message_coding.base.services.Project',
        'message_coding.base.services.Task',
        'message_coding.base.services.CodeScheme',
        'message_coding.base.services.CodeInstance',
        'message_coding.base.services.Message',
        'message_coding.base.models.Pager',
        'message_coding.coding.models.CodingRelationModel',
        'message_coding.coding.bootstrap.initial_data'];
    var CodingController = function ($scope,
                                     Project, Task, CodeScheme, CodeInstance, Message,
                                     Pager, CodingRelationModel,
                                     initial_data) {


        $scope.user = initial_data.user;
        $scope.project = new Project(initial_data.project);
        $scope.task = new Task(initial_data.task);
        $scope.code_scheme = new CodeScheme(initial_data.code_scheme);
        $scope.messages = [];

        $scope.pager = new Pager({
            resource: Message,
            query: {
                task: $scope.task.id
            },
            callback: function (messages, pager) {
                $scope.model.addMessages(messages);
                $scope.messages = $scope.messages.concat(messages);
            }
        });

        $scope.model = new CodingRelationModel();
        $scope.model.updateCodeScheme($scope.code_scheme);

        $scope.refreshCodeScheme = function () {
            $scope.code_scheme.get(function (result) {
                $scope.model.updateCodeScheme(result);
            })
        };

        //The list of selected messages populated by the selection model
        $scope.selectedMessages = [];

        var toggleCode = function (message, code) {
            var codeInstance = message.findRelatedInstanceForCode(code.id);
            if (codeInstance) {
                codeInstance.$delete(function (deleted) {
                    $scope.model.removeCodeInstance(codeInstance);
                });
            } else {
                codeInstance = new CodeInstance({
                    task: $scope.task.id,
                    message: message.id,
                    code: code.id
                });

                codeInstance.$save(function (saved) {
                    $scope.model.addCodeInstance(codeInstance);
                });
            }
        };

        $scope.codeClicked = function (code) {
            $scope.selectedMessages.forEach(function (message) {
                toggleCode(message, code);
            });
        };

        $scope.appliedToSelection = function (code) {
            return $scope.selectedMessages.some(function (message) {
                return message.findRelatedInstanceForCode(code.id);
            });
        };

        $scope.infiniteScroll = function () {
            $scope.pager.loadNextPage();
        };

        var codeInstancePager = new Pager({
            resource: CodeInstance,
            query: {
                task: $scope.task.id,
                owner: $scope.user.id
            }
        });
        codeInstancePager.forEach(function (codeInstance) {
            $scope.model.addCodeInstance(codeInstance);
        });
    };

    CodingController.$inject = requires;
    module.controller('message_coding.coding.controllers.CodingController', CodingController);
})();
