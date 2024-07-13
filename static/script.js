document.getElementById("importImageButton").addEventListener("click", function () {
  document.getElementById("imageInput").click();
});

document.getElementById("imageInput").addEventListener("change", function (event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function (e) {
      const img = document.getElementById("importedImage");
      img.src = e.target.result;
      img.style.display = "block";
  };

  reader.readAsDataURL(file);
});

document.getElementById("countImagesButton").addEventListener("click", function () {
  const countedImage = document.getElementById("countedImage");
  if (countedImage.src !== "#") {
      countedImage.style.display = "block";
  }
  const importedImage = document.getElementById("importedImage");
  importedImage.style.display = "block";
});

document.getElementById("saveButton").addEventListener("click", function () {
  document.getElementById("uploadForm").submit();
});

window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const imageUrl = urlParams.get("filename");
  const processedImageUrl = urlParams.get("processed_image");
  const processedFolder = urlParams.get("processed_folder");
  const originalImage = urlParams.get("original_image");

  if (originalImage) {
      const img = document.getElementById("importedImage");
      if (!img.src.includes(originalImage)) {
          img.src = "/uploads/" + originalImage;
      }
      img.style.display = "block";
  }
  
  if (processedImageUrl && processedFolder) {
      const processedImg = document.getElementById("countedImage");
      processedImg.src = `/runs/detect/${processedFolder}/${processedImageUrl}`;
      processedImg.style.display = "block";
  }
};
