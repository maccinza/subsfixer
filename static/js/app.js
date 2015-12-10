/**
 * Created by infante on 07/12/15.
 */


function checkSelected() {
    var selected_file = $('#subtitle_file').get(0).value;
    return selected_file != "";
}

function validateSelected() {
    var selected_file = $('#subtitle_file').get(0).value;
    return (checkSelected() && selected_file.indexOf('.srt') != -1);
}

function validateAdjustment() {
    var adjustment = $('#adjustment').get(0).value;
    return (adjustment != "" && adjustment != undefined && !isNaN(parseInt(adjustment)));
}

function cleanErrors() {
    $('#file_error').text("");
    $('#adjustment_error').text("");
}


function handleSubmission(event) {
    cleanErrors();
    var flag_file = false, flag_adjustment = false;
    if(validateSelected()){
        flag_file = true;
    }
    else {
        $("#file_error").text("Please, select a valid .srt file before submitting.");
    }

    if(validateAdjustment()){
        flag_adjustment = true;
    }
    else {
        $("#adjustment_error").text("Please, inform a valid value in seconds.");
    }

    if(flag_file && flag_adjustment) {
        return true;
    }
    else {
        event.preventDefault();
        return false;
    }
}

function insertAdderListener() {
    $('#plus').on('click', function(){
        var adjustment = $('#adjustment').get(0);
        if(isNaN(parseInt(adjustment.value))) {
            adjustment.value = 1;
        }
        else {
            adjustment.value ++;
        }
    });
}

function insertSubtractorListener() {
    $('#minus').on('click', function(){
        var adjustment = $('#adjustment').get(0);
        if(isNaN(parseInt(adjustment.value))) {
            adjustment.value = -1;

        }
        else {
            adjustment.value --;
        }
    });
}

function insertFileListener() {
    $('#subtitle_file').on('change', function(){
        cleanErrors();
        if(!checkSelected()) {
            $("#file_placeholder").attr('data-content', "Choose your .srt file...");
        }
        else {
            $("#file_placeholder").attr('data-content', this.value);
        }
    });
}

function insertFormHandleListener(){
     $('#subtitle_form').on('submit', function(event){
         return handleSubmission(event);
     });
}

function insertRefreshListener() {
    $('#refresh_button').on('click', function() {
        window.location = "/";
    });
}