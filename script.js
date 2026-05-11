const playBtn = document.getElementById("playBtn");
const audio = document.getElementById("audio");

playBtn.addEventListener("click", () => {
    audio.src = "your-song.mp3"; // temporary test
    audio.play();
});