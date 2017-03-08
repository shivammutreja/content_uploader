
var choices_var = new Array();
function readURL(input) {
    choices_var.push(input.id);
    // console.log(this.choices_var);
    console.log(input.id.slice(-1));
    choice_id = input.id.slice(-1);
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        console.log(reader);
    
        reader.onload = function (e) {
            $('#blah'+choice_id).attr('src', e.target.result);
            console.log('#'+input.id);
            $('#'+input.id).after('<br>');
            // $('.get_data').data(e.target.result);
            $('#blah'+choice_id).css({'height': '100px', 'width': '100px','display': 'inline'});
        }

    
        reader.readAsDataURL(input.files[0]);
    }
}

function readVideo(input) {
    choices_var.push(input.id);
    // console.log(this.choices_var);
    console.log(input.id.slice(-1));
    choice_id = input.id.slice(-1);
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
    
        reader.onload = function (e) {
            console.log('#'+input.id);
            $('#'+input.id).after('<br>');
            // $('.get_data').data(e.target.result);
            $('#blah'+choice_id).css({'display': 'inline'});
        }

    
        reader.readAsDataURL(input.files[0]);
    }
}