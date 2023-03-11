

$(".select-style").click(function(){
  $(".select-style").removeClass("selected_image");
  $(this).addClass('selected_image');
  var path = $(this).attr('src');
  document.form.style_file.value = path;
  document.querySelector("#hidden-style").removeAttribute('hidden');
  document.querySelector("#hidden-style img").src="../"+path;
});

var degree = document.querySelector("#degree").innerHTML;
if (degree != ""){
  document.querySelector("input[type=range]").value = degree*10;
  document.querySelector("#style-degree").innerHTML = degree;
}

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


const simple_input = document.querySelector('#simple_content_file');
var simple_uploaded_image = "";

simple_input.addEventListener("change",function() {
  const simple_reader = new FileReader();
  simple_reader.addEventListener("load",() => {
    simple_uploaded_image = simple_reader.result;
    document.querySelector("#display-simple-content").style.backgroundImage=`url(${simple_uploaded_image})`;
  });
  simple_reader.readAsDataURL(this.files[0]);
})

const simple_style_input = document.querySelector('#simple_style_file');
var simple_style_image = "";

simple_style_input.addEventListener("change",function() {
  const simple_style_reader = new FileReader();
  simple_style_reader.addEventListener("load",() => {
    simple_style_image = simple_style_reader.result;
    document.querySelector("#display-simple-style").style.backgroundImage=`url(${simple_style_image})`;
  });
  simple_style_reader.readAsDataURL(this.files[0]);
})

const painting_input = document.querySelector("#painting_content_file");
painting_input.addEventListener("change", function() {
  const painting_reader = new FileReader();
  painting_reader.addEventListener("load", () => {
    const painting_image = painting_reader.result;
    document.querySelector("#display-painting-content").style.backgroundImage = `url(${painting_image})`;
  });
  
  painting_reader.readAsDataURL(this.files[0]);
});

const is_style = document.querySelector("#if_style").innerHTML;
if (is_style == "yes"){
    document.querySelector("#display-style-result").removeAttribute("hidden");
}
                
const is_painting = document.querySelector("#if_style").innerHTML;
if (is_style == "yes"){
    document.querySelector("#display-painting-result").removeAttribute("hidden");
}
   
const is_simple = document.querySelector("#if_simple").innerHTML;
if (is_simple == "yes"){
    document.querySelector("#display-simple-result").removeAttribute("hidden");
}

var list = document.querySelector('select');
  list.addEventListener("change",event => {
  document.querySelector("input[name='number_split']").value = event.target.value;
});

