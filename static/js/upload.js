
function testMe(form_data){
  var formData = new FormData(form_data);
  $.ajax({
     url: '/file',
     type: 'POST',
     data: formData,
     async: true,
     cache: false,
     contentType: false,
     enctype: 'multipart/form-data',
     processData: false,
     success: function (data) {
      if (data.choices) {
        for (var i = data.choices.length - 1; i >= 0; i--) {
          new Clipboard('.clip');
          console.log(i, data.choices[i], "#choice"+(i+1));
          console.log(choices_var[i].slice(-1));

          $(".get_files").find("br").remove(); //removing an extra break tag after image is uploaded.
          $("#"+choices_var[i]).remove(); //removing input tag to choose file after image is uploaded.
          $("#upload_file").prop('disabled', true); //removing upload button after image is uploaded.
          $("#upload_file").prop('title', 'You can upload as many options just once.'); //removing upload button after image is uploaded.


          var image_link = data.choices[i]

          $("#choice"+choices_var[i].slice(-1)).val(image_link);
          // $("#choice"+choices_var[i].slice(-1)).html("Choice");
          


          $("#choice"+choices_var[i].slice(-1)).css({'display': 'inline'});
          $(".clip").css({'display': 'inline'});

          $('#blah'+choices_var[i].slice(-1)).attr('src', data.choices[i]);

          $('#blah'+choices_var[i].slice(-1)).css({'height': '200px', 'width': '200px','display': 'inline'});

           // $("#imgInp"+(i+1)).prop('disabled', true);

           $("#preview").css({'display': 'inline'})
      }
      }
      else{
        for (var i = data.text_choices.length - 1; i >= 0; i--) {
          console.log(i, data.text_choices[i], "#choice"+(i+1));
        }
      }
      window.location.href = "/solution"
      // window.open("/preview", "preview", "width=400, resizable=yes, height=400");

  }
  });
}