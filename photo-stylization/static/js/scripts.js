$(".select-style").click(function(){
  $(".select-style").removeClass("selected_image");
  $(this).addClass('selected_image');
  var path = $(this).attr('src');
  document.form.style_file.value = path;
  document.querySelector("#hidden-style").removeAttribute('hidden');
  document.querySelector("#hidden-style img").src="../"+path;
});
$("input[type=range]").on('change',function(){
  $(this).siblings('span').html(this.value/10)
  $('input[name="style_degree"]').val(this.value/10);
});


const image_input = document.querySelector("#content_file");
image_input.addEventListener("change", function() {
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    const uploaded_image = reader.result;
    document.querySelector("#display-image-content").style.backgroundImage = `url(${uploaded_image})`;
  });
  reader.readAsDataURL(this.files[0]);
});
