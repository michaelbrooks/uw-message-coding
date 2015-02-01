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
        'message_coding.base.services.Selection',
        'message_coding.base.services.Task',
        'message_coding.base.services.CodeScheme',
        'message_coding.base.services.CodeInstance',
        'message_coding.base.models.MessagePageModel',
        'message_coding.base.models.Pager',
        'message_coding.base.models.IndexedCollection',
        'message_coding.coding.bootstrap.initial_data'];
    var CodingController = function ($scope, djangoUrl,
                                     Project, Selection, Task, CodeScheme, CodeInstance,
                                     MessagePageModel, Pager, IndexedCollection,
                                     initial_data) {

        /*
         Tracking selected messages with this:
         https://github.com/jtrussell/angular-selection-model
         */

        $scope.user = initial_data.user;
        $scope.project = new Project(initial_data.project);
        $scope.task = new Task(initial_data.task);
        $scope.code_scheme = new CodeScheme(initial_data.code_scheme);

        var selection = $scope.task.selection;
        $scope.pager = new MessagePageModel({
            dataset_id: selection.dataset,
            filters: selection.selection
        });

        //The list of selected messages populated by the selection model
        $scope.selectedMessages = [];

        ////Get code instances
        //var codeInstances = IndexedCollection();
        //new Pager(CodeInstance.get({
        //    task: $scope.task.id
        //}))
        //    .forEach(function (codeInstance) {
        //        codeInstances.add(codeInstance);
        //    });

        var wireUp = function (message, codeInstance, code) {
            message._codeInstances = message._codeInstances || [];
            code._codeInstances = code._codeInstances || [];

            message._codeInstances.push(codeInstance);
            code._codeInstances.push(codeInstance);

            codeInstance._message = message;
            codeInstance._code = code;
        };


        var unWire = function (codeInstance) {
            var message = codeInstance._message;
            var code = codeInstance._code;

            message._codeInstances.splice(message._codeInstances.indexOf(codeInstance), 1);
            code._codeInstances.splice(code._codeInstances.indexOf(codeInstance), 1);

            delete codeInstance._message;
            delete codeInstance._code;
        };

        var toggleCode = function (message, code) {
            if (message.hasOwnProperty('_codeInstances')) {
                var found = message._codeInstances.some(function (codeInstance) {
                    if (codeInstance.code == code.id) {
                        //It's already coded with this, so delete it
                        codeInstance.$delete(function (deleted) {
                            unWire(codeInstance);
                        });

                        return true;
                    }
                });
                if (found) return;
            }

            //Else add the code instance
            var ci = new CodeInstance({
                task: $scope.task.id,
                message: message.id,
                code: code.id
            });

            ci.$save(function (saved) {
                wireUp(message, saved, code);
            })
        };

        $scope.codeClicked = function (code) {
            $scope.selectedMessages.forEach(function (message) {
                toggleCode(message, code);
            });
        };

        $scope.appliedToSelection = function (code) {
            if (code.hasOwnProperty('_codeInstances')) {
                return code._codeInstances.some(function (codeInstance) {
                    return codeInstance._message.selected;
                });
            }
        };

    };

    CodingController.$inject = requires;
    module.controller('message_coding.coding.controllers.CodingController', CodingController);
})();
