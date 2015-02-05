(function () {
    'use strict';

    var module = angular.module('message_coding.coding.models', [
        'message_coding.base.models'
    ]);

    /**
     * The CodingRelationModel joins together
     * messages, code instances, and codes.
     *
     * It maintains internal collections of these three entities,
     * and they may be added and removed from outside using the public methods.
     * 
     * The items added to this model will have connections created between
     * them. For example:
     *  - a message would have a _codeInstances array added.
     *  - a codeInstance would have _message and _code properties added.
     *  - a code is not augmented currently
     *  
     *  Additionally, reverse relations are created for these. Objects
     *  are unlinked when they are removed from the model.
     */
    module.factory('message_coding.coding.models.CodingRelationModel', [
        'message_coding.base.models.IndexedCollection',
        function (IndexedCollection) {

            var default_init = {};

            // Model constructor
            var CodingRelationModel = function (options) {
                options = angular.extend({}, default_init, options);

                this.messageIndex = new IndexedCollection();
                this.codeIndex = new IndexedCollection();
                this.codeInstanceIndex = new IndexedCollection();
            };


            //Public methods
            angular.extend(CodingRelationModel.prototype, {
                
                updateCodeScheme: function(codeScheme) {
                    console && console.log && console.log("Updating code scheme", codeScheme);
                    
                    var self = this;
                    
                    //Replace the codes index with the new codes
                    self.codeIndex.clear();
                    codeScheme.forEachCode(function(code) {
                        self.codeIndex.add(code);
                    });

                    //Replace all references to codes in the code instances
                    this.codeInstanceIndex.forEach(function(codeInstance) {
                        codeInstance._code = self.codeIndex.get(codeInstance.code);
                        
                        //We don't need to connect codes to code instances, I think
                    });
                },
                
                addMessages: function(messages) {
                    console && console.log && console.log("Adding " + messages.length + " messages", messages);
                    
                    var self = this;
                    
                    //Add the new messages to the index
                    this.messageIndex.addAll(messages);
                    
                    //Hook up existing code instances to messages
                    this.codeInstanceIndex.forEach(function(codeInstance) {
                        var message = self.messageIndex.get(codeInstance.message);
                        if (message) {
                            message.relateCodeInstance(codeInstance);
                        }
                    });
                },
                
                addCodeInstance: function(codeInstance) {
                    console && console.log && console.log("Adding code instance", codeInstance);
                    
                    //Add the code instance to our index
                    if (this.codeInstanceIndex.add(codeInstance)) {
                        //Point the code instance at its message
                        var message = this.messageIndex.get(codeInstance.message);
                        if (message) {
                            //Add the code instance to the message
                            message.relateCodeInstance(codeInstance);
                        }

                        //Point the code instance at its code
                        codeInstance._code = this.codeIndex.get(codeInstance.code);
                        //We don't add code instances to codes
                    }
                },
                
                removeCodeInstance: function(codeInstance) {
                    console && console.log && console.log("Removing code instance", codeInstance);
                    
                    //Remove the code instance from our index
                    if (this.codeInstanceIndex.remove(codeInstance)) {
                        codeInstance._message.unrelateCodeInstance(codeInstance);
                        
                        //We don't currently have any reference from code to code instance
                    }
                }
            });

            return CodingRelationModel;
        }]);
})();
