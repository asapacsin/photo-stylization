function validateForm() {
    let y = document.forms["form"]["style_file"].value;
    if (y == "") {
      alert("please select style image");
      return false;
    }
  }