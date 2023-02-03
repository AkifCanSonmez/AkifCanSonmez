async function takePicture() {
  const stream = await navigator.mediaDevices.getUserMedia({
    video: { facingMode: "environment" },
  });
  const video = document.getElementById("video");
  video.srcObject = stream;
  video.onloadedmetadata = () => {
    video.play();
  };
}

function captureImage() {
  const canvas = document.getElementById("canvas");
  const video = document.getElementById("video");
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  
  document.getElementById("submitButton").style.display = "inline-block";
}

async function submitForm() {
  const canvas = document.getElementById("canvas");
  const imageData = canvas.toDataURL("image/jpeg");
  const imageBlob = await fetch(imageData).then((res) => res.blob());
  const formData = new FormData();
  formData.append("image", imageBlob, "image.jpeg");

  const response = await fetch("/objects", {
    method: "POST",
    body: formData,
  });
  if (response.status === 200) {
    window.location.href = "/objects/display";
  } else {
    console.error("Error response", response);
  }
}