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
        $('.loop2').text(`${response[1]}`);
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
    
        let loopNumber = (response.loops);
        let timeOfLoop = (response.time);
        console.log(`loopNumber is ${loopNumber} and timeOfLoop is ${timeOfLoop}`);
        let promptName = (response.name);
        if (promptName !== 'Single Words with Multiple Meanings') {

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
                (loopNumber*1000*timeOfLoop));    }
        else {
            console.log(`this is the loop zero.`);
            const zeroAlarm = () => {
                const mySound = document.getElementById("sound");
                mySound.play();  
            } // end of zeroAlarm function

            setTimeout(zeroAlarm, timeOfLoop*1000);
            var intervalID = setInterval(zeroAlarm, [timeOfLoop*1000]);
            setTimeout(() => {
                clearInterval(intervalID);
                setTimeout(tooLong, timeOfLoop*1000);
                setTimeout(unhideTheDiv, timeOfLoop*1000);
            }, (loopNumber*1000*timeOfLoop));



        } // end of else statement
            
        
        })  // line 75 paren next to get and bracket after response
        }  // line 74
        


getLoop();

// // Accessing dropdown menu on the homepage
// const select = document.querySelector("select");

// // Getting the selected value and returning it as a number
// const selectedChoice = Number(select.value);

// // Listening for the choice to be changed
// select.addEventListener('change', (event) => {
//     console.log(`something is happening`);
//     const {
//         value,
//         text
//     } = event.target.options[event.target.selectedIndex]
//     console.log(`value: ${value}, text: ${text}`);
// }) 

// Alarm specific to the homepage
const thisAlarm = () => {
    const mySound = document.getElementById("sound-homepage");
    mySound.play();  
}

// Two functions to display text in element with id timer-started
const timerStarted = () => {
    $('#timer-started').html('Timer started');
}
const timerStopped = () => {
    $('#timer-started').html('All Done!');  
}

// When button is clicked, adds text, sets timer, and then alters text again
$('#start-timer').on('click', () => {
    console.log('the timer button was pressed'); 
    const select = document.querySelector("select");
    // gets the number from the drop down menu
    const selectedChoice = Number(select.value);
    console.log(`${selectedChoice} - selectedChoice`);
    timerStarted();
    setTimeout(thisAlarm, selectedChoice*1000);
    setTimeout(timerStopped, selectedChoice*1000); 
});










