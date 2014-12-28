(function() {
    //Rudimentary scripts for coding UI

    function markCheckboxes(codeInstances) {

        var checkboxes = $('.codes input[type=checkbox]');

        codeInstances.forEach(function(inst) {
            var input_name = "messages[" + inst.message_id + "]";
            var check = checkboxes.filter('[name="' + input_name + '"][value="' + inst.code_id + '"]');
            check.prop('checked', true);
        });
    }

    $(document).ready(function() {
        if ($('body').is('.project-coding-view')) {

            var instances = window.preload.coding.instances;
            markCheckboxes(instances);
        }
    });

})();
