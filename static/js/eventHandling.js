

// const button = document.getElementById("nuggets");
// function Function() {
//     button.innerHTML = "A hard-coded nugget";
//     console.log('hi');
// }
// button.addEventListener('click', Function);





// $('#get-nuggets').on('click', () => { 
//     console.log('the button was pressed');
//     $('#nugget-1').text('nugget-1');
//   });



// $('#get-nuggets').on('click', () => { 
//     console.log('the button was pressed');
//     $.get('/homepage.json', response => {
//         console.log(response);
//         $('#nugget-1').text(response);
//     });
    
//   });

$('#get-nuggets').on('click', () => {
    console.log('the button was pressed');
    $.get('/homepage.json', response => {
        console.log(response);
        console.log(`response length = ${response.length}`)
        for (let i = 0; i < response.length; i += 1) {
            console.log(`This is nugget #${i}:`)
            console.log(response[i]);
            $('#nuggets').append(`<li>${response[i]}</li>`);
        }
    });
});