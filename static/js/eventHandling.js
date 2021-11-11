
const nuggetRetrieve = () => {
    $.get('/homepage.json', response => {
        console.log(response);
        console.log(`response length = ${response.length}`);
        for (let i = 0; i < response.length; i += 1) {
            console.log(response[i]);
            $('#nuggets').append(`<li>${response[i]}</li>`);
        }
        if (response.length == 0) {
            $('#no-nuggets').html("You haven't added any nuggets yet!");
        }
    });
}

$('#get-nuggets').on('click', () => {
    console.log('the button was pressed');
    nuggetRetrieve();
    $('#get-nuggets').off();    
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

// Hides the nugget element on writing_prompt.html from the get-go
$('#hidden-element').hide()

// Function that will show the hidden element and call the sound file
const unhideTheDiv = () => {
    $('#hidden-element').show(); 
    const mySound = document.getElementById("sound");
    mySound.play();   
}

// Determining the time after which unhideTheDiv will be called
setTimeout(unhideTheDiv, 2000)

// Another alarm is trigger (sound and text) using the setTimeout function
const tooLong = () => {
    console.log(`tooLong`);
    document.getElementById ("sound").setAttribute ('src', '/static/t-rex-roar.mp3');
    const mySound = document.getElementById("sound");    
    mySound.play();
    $('#too-long').text('Seriously, stop writing.');
}

setTimeout(tooLong, 5000)












      






