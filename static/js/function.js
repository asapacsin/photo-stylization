/*function validateForm() {
    let y = document.forms["form"]["style_file"].value;
    if (y == "") {
      alert("please select style image");
      return false;
    }
  }*/
function readURL(input) {
  if(input.files && input.files[0]){
    var reader = new FileReader();
    reader.onload = function(e){
      $("#image_content").attr('src', e.target.result);
    }
    reader.readAsDataURL(input.files[0]);
  }
}