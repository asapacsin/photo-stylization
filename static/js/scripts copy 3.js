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

document.querySelector("#test").innerHTML ="getit";
const image_input = document.querySelector("#content_file");
image_input.addEventListener("change", function() {
  
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    const uploaded_image = reader.result;
    document.querySelector("#display-image-content").style.backgroundImage=`url('/static/image/hill.jpg')` ;
  });
  reader.readAsDataURL(this.files[0]);
});

const selects = document.querySelectorAll('select');
selects.forEach(el=>el.addEventListener('click'),event=>{
    document.querySelector('input[name="number_split"]').val(event.target.value);
  }
)

const painting_input = document.querySelector('#painting_content_file');
var painting_uploaded_image = "";

painting_input.addEventListener("change",function() {
  
  const painting_reader = new FileReader();
  painting_reader.addEventListener("load",() => {
    painting_uploaded_image = painting_reader.result;
    document.querySelector("#display-painting-content").style.backgroundImage=`url(${painting_uploaded_image})`;
  });
  painting_reader.readAsDataURL(this.files[0]);
})

const is_style = document.querySelector("#if_style").innerHTML;
if (is_style == "yes"){
    document.querySelector("#display-style-result").removeAttribute("hidden");
}
                
const is_painting = document.querySelector("#if_style").innerHTML;
if (is_style == "yes"){
    document.querySelector("#display-painting-result").removeAttribute("hidden");
}
                