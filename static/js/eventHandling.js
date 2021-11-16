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
}

// Function that makes AJAX call to get a new word for the browser
const newWords = () => {
    $.get('/random-words.json', response => {
        console.log(response);
        console.log(`${response[0]}`)
        $('.loop').text(`${response[0]}`);
    });
}

// Function that will sound an alarm and call newWords function
const playAlarm = aNum => {
    const mySound = document.getElementById("sound");
    mySound.play(); 
    newWords(); 
    console.log(`aNum-${aNum} is printing from inside the playAlarm function!`);
}

// T-REX SOUND
const tooLong = () => {
    console.log(`tooLong`);
    document.getElementById ("sound").setAttribute ('src', '/static/t-rex-roar.mp3');
    const mySound = document.getElementById("sound");    
    mySound.play();
    $('#too-long').text('All done!');
}

// Setting interval of 5 seconds on playAlarm function
var intervalID = setInterval(playAlarm(4), [4000]);

const getLoop = () => {
    $.get('/data/prompts.json', response => {
        
        
        let loopNumber = ((response[4]).loops);
        console.log(`just above playAlarm(2)`)
        playAlarm(loopNumber);
        console.log(`just below playAlarm(2)`)
        // and pass loopNumber into playAlarm
        var intervalID = setInterval(playAlarm, [4000]);
        console.log(`loopNumber is ${loopNumber}`);

        setTimeout(() => { 
            clearInterval(intervalID); 
            setTimeout(tooLong, 4000); 
            setTimeout(unhideTheDiv, 4000); }, 
            12000);    
    });
}

// Stopping the interval after 25 seconds
// Playing t-rex sound and showing 'nugget element' 5 seconds after interval has ended




getLoop();


// playAlarm could take in param, loop number
// might have to move getLoop above setTimeout




