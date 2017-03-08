
var counter = 1;
$('#add_img_choice').click(function(){
    $('#add_choice').prop('disabled', true)

    var choice = "<br/><div class='row' id='div "+counter+" '>\
    <div class='col-sm-4 get_files'>\
    <input type='file' name='get_image' id='imgInp"+ counter+"' onchange='readURL(this);' multiple/>\
    <img id='blah"+counter+"' style='display:none' alt='your image' /></div><div class='col-sm-2'>\
    <input placeholder='Choice "+counter+"' name='choice' id='choice"+counter+"' style='display:none' />\
    </div><div class='col-sm-1'>\
    <a class='btn clip' data-clipboard-target='#choice"+counter+"' style='display:none'>\
    <img src='https://clipboardjs.com/assets/images/clippy.svg' title='Copy to clipboard' \
    style='width:14px' alt='Copy to clipboard'></a></div></div></form>"

    $('#dynamic_choice').append(choice)
    counter++;
    return true;

});


$('#add_choice').click(function(){
    var choice = "<br/><div class='row' id='div "+counter+" '>\
    <div class='col-sm-4'><input placeholder='Choice "+counter+"' name='choice' id='choice"+counter+"'>\
    </div></div></form>"
    $('#dynamic_choice').append(choice)
    counter++;
    return true;

});

$('#add_vid_choice').click(function(){
    $('#add_choice').prop('disabled', true)

    var choice = "<br/><div class='row' id='div "+counter+" '>\
    <div class='col-sm-4 get_files'>\
    <input type='file' name='get_image' id='imgInp"+ counter+"' />\
    <video id='blah"+counter+"' style='display:none' width='420' controls preload='auto'>\
    <source type='video/mp4'></video></div><div class='col-sm-2'>\
    <input placeholder='Choice "+counter+"' name='choice' id='choice"+counter+"' style='display:none' />\
    </div><div class='col-sm-1'>\
    <a class='btn clip' data-clipboard-target='#choice"+counter+"' style='display:none'>\
    <img src='https://clipboardjs.com/assets/images/clippy.svg' title='Copy to clipboard' \
    style='width:14px' alt='Copy to clipboard'></a></div></div>"

    $('#dynamic_choice').append(choice)
    counter++;
    return true;

});


  