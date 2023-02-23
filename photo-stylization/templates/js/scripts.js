const image_input_content = document.querySelector("#content_file");

image_input_content.addEventListener("change", function() {
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    const uploaded_image = reader.result;
    document.querySelector("#display-image-content").style.backgroundImage = `url(${uploaded_image})`;
  });
  reader.readAsDataURL(this.files[0]);
});

$("img").click(function(){
  $("img").removeClass("selected_image");
  $(this).addClass('selected_image');
  var path = $(this).attr('src');
  document.form.style_file.value = path;
});
$("input[type=range]").on('change',function(){
  $(this).siblings('span').html(this.value/10)
  $('input[name="style_degree"]').val(this.value/10);
});

const image_input = document.querySelector("#image-input");
image_input.addEventListener("change", function() {
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    const uploaded_image = reader.result;
    document.querySelector("#display-image").style.backgroundImage = `url(${uploaded_image})`;
  });
  reader.readAsDataURL(this.files[0]);
});