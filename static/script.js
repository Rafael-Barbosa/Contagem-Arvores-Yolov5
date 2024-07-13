document
  .getElementById("importImageButton")
  .addEventListener("click", function () {
    document.getElementById("imageInput").click();
  });

document
  .getElementById("imageInput")
  .addEventListener("change", function (event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
      const img = document.getElementById("importedImage");
      img.src = e.target.result;
      img.style.display = "block";
    };

    reader.readAsDataURL(file);
  });

document
  .getElementById("countImagesButton")
  .addEventListener("click", function () {
    const importedImageSrc = document.getElementById("importedImage").src;
    const img = document.getElementById("countedImage");
    img.src = importedImageSrc;
    img.style.display = "block";
  });

document.getElementById("saveButton").addEventListener("click", function () {
  document.getElementById("uploadForm").submit();
});

window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const imageUrl = urlParams.get("filename");
  if (imageUrl) {
    const img = document.getElementById("importedImage");
    img.src = "/uploads/" + imageUrl;
    img.style.display = "block";
  }
};
