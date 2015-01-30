(function () {
    'use strict';

    var module = angular.module('message_coding.dataBrowser.controllers', [
        'message_coding.dataBrowser.services',
        'message_coding.dataBrowser.bootstrap',
        'message_coding.dataBrowser.models',
        'ng.django.urls',
        'ui.bootstrap.datetimepicker'
    ]);

    var requires = ['$scope', 'djangoUrl',
        'message_coding.base.services.Project',
        'message_coding.base.services.Dataset',
        'message_coding.base.services.Task',
        'message_coding.base.models.MessagePageModel',
        'message_coding.dataBrowser.bootstrap.initial_data'];
    var BrowserController = function ($scope, djangoUrl,
                                      Project, Dataset, Task,
                                      MessagePageModel,
                                      initial_data) {

        $scope.$watch(function(){
            console.log("digest called");
        });                                    
                                      
        $scope.user = initial_data.user;
        $scope.project = new Project(initial_data.project);
        $scope.dataset = new Dataset(initial_data.dataset);

        $scope.model = new MessagePageModel({
            dataset_id: $scope.dataset.id,
            filters: {
                time__gte: $scope.dataset.min_time,
                time__lte: $scope.dataset.max_time,
            }
        });
        

        $scope.createTask = function () {

            //Create a new task
            var task = new Task({
                project: $scope.project.id,
                selection: {
                    dataset: $scope.dataset.id,
                    type: 'json',
                    selection: $scope.model.filters
                }
            });

            task.$save()
                .then(function () {

                    //Then go edit it
                    document.location.href = djangoUrl.reverse('task_edit', {
                        project_slug: $scope.project.slug,
                        task_pk: task.id
                    });
                });
        };
    };

    
    BrowserController.$inject = requires;
    module.controller('message_coding.dataBrowser.controllers.BrowserController', BrowserController);
    module.directive('datetimeFormat', function() {
      return {
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelController) {
          ngModelController.$parsers.push(function(data) {
            //convert data from view format to model format
            debugger
            return data; //converted
          });

          ngModelController.$formatters.push(function(data) {
            //convert data from model format to view format
            return data; //converted
          });
        }
      }
    });
    
})();
