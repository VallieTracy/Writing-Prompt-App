
const nuggetRetrieve = () => {
    $.get('/homepage.json', response => {
        console.log(response);
        console.log(`response length = ${response.length}`);
        for (let i = 0; i < response.length; i += 1) {
            console.log(response[i]);
            $('#nuggets').append(`<li>${response[i]}</li>`);
        }
        if (response.length == 0) {
            // alert("You haven't stored any nuggets yet!");
            $('#no-nuggets').html("You haven't added any nuggets yet!");
        }
    });
}

$('#get-nuggets').on('click', () => {
    console.log('the button was pressed');
    nuggetRetrieve();
    // $('#get-nuggets').off();    
});

const wordRetrieve = () => {
    $.get('/homepage-words.json', response => {
        console.log(response);
        console.log(response.length);
        for (let i = 0; i < response.length; i += 1) {
            $('#words').append(`<li>${response[i]}</li>`);
        }
        if (response.length == 0) {
            $('#no-words').html("You haven't added any words yet!");
        }
    });
}

$('#get-words').on('click', () => {
    console.log('word button clicked');
    wordRetrieve();
    $('#get-words').off();
})




