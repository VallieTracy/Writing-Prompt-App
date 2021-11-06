const button = document.getElementById("nuggets");
function Function() {
    button.innerHTML = "A hard-coded nugget";
    console.log('hi');
}
button.addEventListener('click', Function);