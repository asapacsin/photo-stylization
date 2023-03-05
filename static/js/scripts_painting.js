const image_input = document.querySelector("#content_file");
image_input.addEventListener("change", function() {
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    const uploaded_image = reader.result;
    document.querySelector("#display-image-content").style.backgroundImage = `url(${uploaded_image})`;
  });
  reader.readAsDataURL(this.files[0]);
});

const selects = document.querySelectorAll('select');
selects.forEach(el=>el.addEventListener('click'),event=>{
    document.querySelector('input[name="number_split"]').val(event.target.value);
  }
)