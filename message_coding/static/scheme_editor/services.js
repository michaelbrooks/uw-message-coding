(function () {
    'use strict';

    var module = angular.module('message_coding.schemeEditor.services', [
        'message_coding.base.services'
    ]);

    module.service('message_coding.schemeEditor.services.SchemeModel', [
        'message_coding.base.services.CodeScheme',
        'message_coding.base.services.CodeGroup',
        'message_coding.base.services.Code',

        function(CodeScheme, CodeGroup, Code) {

            var SchemeModel = function(initial_scheme) {
                this.scheme = initial_scheme;
            };

            angular.extend(SchemeModel.prototype, {
                update_scheme: function() {
                    var data = angular.extend({}, this.scheme);
                    delete data['code_groups'];

                    CodeScheme.update(data);
                },
                reorder_groups: function() {
                    this.scheme.code_groups.forEach(function(grp, idx) {
                        grp.order = idx + 1;
                    });

                    CodeGroup.update(this.scheme.code_groups);
                }
            });

            return SchemeModel;
        }
    ]);

})();
