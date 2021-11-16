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
const playAlarm = () => {
    const mySound = document.getElementById("sound");
    mySound.play(); 
    newWords(); 
}

// T-REX SOUND
const tooLong = () => {
    console.log(`tooLong`);
    document.getElementById ("sound").setAttribute ('src', '/static/t-rex-roar.mp3');
    const mySound = document.getElementById("sound");    
    mySound.play();
    $('#too-long').text('All done!');
}

// Function that uses AJAX to access writing dictionaries
const getLoop = () => {
    $.get('/data/prompts.json', response => {
        
        // Hard-coded right now
        // let loopNumber = ((response[0]).loops);
        // let timeOfLoop = ((response[0]).time);
        let loopNumber = (response.loops);
        let timeOfLoop = (response.time);
        console.log(`loopNumber is ${loopNumber} and timeOfLoop is ${timeOfLoop}`);

        // using setTimeout on playAlarm so that it doesn't sound immediately 
        // timeOfLoop is an integer, writen as if seconds (will be something like 90 sec or 2 minutes)
        setTimeout(playAlarm, timeOfLoop*1000);

        // Sets the interval for how frequently the alarm is played
        var intervalID = setInterval(playAlarm, [timeOfLoop*1000]);
        
        // stops the interval, determined by loopNumber*timeOfLoop*1000
        // Show hidden html element and play t-rex after the interval has been cleared
        setTimeout(() => { 
            clearInterval(intervalID); 
            setTimeout(tooLong, timeOfLoop*1000); 
            setTimeout(unhideTheDiv, timeOfLoop*1000); }, 
            (loopNumber*1000*timeOfLoop));    
    });
}

getLoop();







