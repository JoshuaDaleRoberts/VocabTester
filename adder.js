//This file is temporarily stored here and will be moved to adder.html when finished.


//code that switches between additional shown fields by part of speech. 
var nounDivs = document.getElementsByClassName("nounHandler");
var posSelector = document.getElementById("pos");
var englishHandler = document.getElementById("englishHandler");
var addToListCheckbox = document.getElementById("addToList");
var transitiveHandler = document.getElementById("transitive");

    
function updateMenu() {
    //removes all noun fields if pos is not noun
    let selectedPos = posSelector.value;
    if (selectedPos === "noun") {
        for (let i = 0; i < nounDivs.length; i++) {
            nounDivs[i].style.display = "table-row";
        }
    } else {
        for (let i = 0; i < nounDivs.length; i++) {
            nounDivs[i].style.display = "none";
        }
    }
    if (selectedPos === "verb") {
        transitiveHandler.style.display = "table-row";
    } else {
        transitiveHandler.style.display = "none";
    }
    //shows or hides english meaning field based on addToList checkbox
    let addToList = addToListCheckbox.checked
    if (addToList){
        englishHandler.style.display = "table-row";
    } else {
        englishHandler.style.display = "none";
    }
}

posSelector.addEventListener("change",  () => updateMenu());
addToListCheckbox.addEventListener("change",  () => updateMenu());

//code that smart completes noun class and plural form
const wordInput = document.getElementById("word_input");

function guessWord() {
    rootAttempt = wordInput.value;

    firstLetter = rootAttempt.charAt(0);
    firstTwoLetters = rootAttempt.slice(0,2);
    firstThreeLetters = rootAttempt.slice(0,3);
    firstFourLetters = rootAttempt.slice(0,4);

    let guessPOS = "noun"
    let guessRoot = rootAttempt
    let alreadyGuessed = false;

    //guesses infinitive
    if (firstTwoLetters === "ku") {
        guessPOS = "verb"
        guessRoot = rootAttempt.slice(2)
        alreadyGuessed = true; 
    }

    //guess positive indicative
    
    let positiveTenseInfixes = ["na","li","ta","me","ki"]
    let positiveSubjectPrefixes = ["ni","u","a","tu","m","wa"]

    //looping through positive indicative prefixes
    if (!alreadyGuessed) {
        for (let i = 0; i < positiveSubjectPrefixes.length; i++) {
            for (let j = 0; j< positiveTenseInfixes.length; j++) {
                let prefix = positiveSubjectPrefixes[i] + positiveTenseInfixes[j]
                //if a verb begins with this prefix, guess verb and remove accordingly.
                if((rootAttempt.slice(0, prefix.length) === prefix) && (rootAttempt.length > prefix.length)) {
                    guessPOS = "verb"
                    guessRoot = rootAttempt.slice(prefix.length)
                    alreadyGuessed = true;
                }
            }
        }
    }

    //looping through negative indicative prefixes, excluding the present missing tense. 
    let negativeTenseInfixes = ["ku","ta","ja","ki"]
    let negativeSubjectPrefixes = ["si","hu","ha","hatu","ham","hawa"]
    if (!alreadyGuessed) {
        for (let i = 0; i < negativeSubjectPrefixes.length; i++) {
            for (let j = 0; j< negativeTenseInfixes.length; j++) {
                let prefix = negativeSubjectPrefixes[i] + negativeTenseInfixes[j]
                //if a verb begins with this prefix, guess verb and remove accordingly.
                if((rootAttempt.slice(0, prefix.length) === prefix) && (rootAttempt.length > prefix.length)) {
                    guessPOS = "verb"
                    guessRoot = rootAttempt.slice(prefix.length)
                    alreadyGuessed = true;
                }
            }
        }
    }

    //loops through the negative prefixes, present tense only
    if (rootAttempt.slice(-1) === "i" && !alreadyGuessed) {
        for (let i = 0; i < negativeSubjectPrefixes.length; i++) {
            let prefix = negativeSubjectPrefixes[i]
            //if a verb begins with this prefix, guess verb and remove accordingly.
            if((rootAttempt.slice(0, prefix.length) === prefix) && (rootAttempt.length > prefix.length)) {
                guessPOS = "verb"
                guessRoot = rootAttempt.slice(prefix.length, -1) + "a"
            }
        }
    }

    //loops through subjunctive verbs
    if (rootAttempt.slice(-1) === "e" && !alreadyGuessed) {
        for (let i = 0; i < positiveSubjectPrefixes.length; i++) {
            let prefix = positiveSubjectPrefixes[i]
            //if a verb begins with this prefix, guess verb and remove accordingly.
            if((rootAttempt.slice(0, prefix.length) === prefix) && (rootAttempt.length > prefix.length)) {
                guessPOS = "verb"
                guessRoot = rootAttempt.slice(prefix.length, -1) + "a"
                alreadyGuessed = true;
            }
        } 
    }

    //if all verb checks fail, default to nouns
    //check for common two letter noun class prefixes
    //default to n/n
    let guessPlural = rootAttempt
    if (!alreadyGuessed && rootAttempt.length > 2) {
        switch (firstTwoLetters) {
            case "wa":
                guessRoot = "m" + rootAttempt.slice(2)
                guessPlural = rootAttempt
                alreadyGuessed = true;

                break;
            case "mi":
                guessRoot = "m" + rootAttempt.slice(2)
                guessPlural = rootAttempt
                alreadyGuessed = true;
                break;
            case "ki":
                guessRoot = rootAttempt
                guessPlural = "vi" + rootAttempt.slice(2)
                alreadyGuessed = true;
                break;
            case "vi":
                guessRoot = "ki" + rootAttempt.slice(2)
                guessPlural = rootAttempt
                alreadyGuessed = true;
                break;
            case "ch":
                guessRoot = rootAttempt
                guessPlural = "vy" + rootAttempt.slice(2)
                alreadyGuessed = true;
                break;
            case "vy":
                guessRoot = "ch" + rootAttempt.slice(2)
                guessPlural = rootAttempt
                alreadyGuessed = true;
                break;
            case "ma":
                guessRoot = rootAttempt.slice(2)
                alreadyGuessed = true;
                break;
        }
    }

    

    //set the guessed values
    document.getElementById("root").value = guessRoot;
    document.getElementById("pos").value = guessPOS;
    document.getElementById("plural").value = guessPlural;
    //updates the menu to show noun fields if necessary
    updateMenu();
    
}

document.getElementById("word_input").addEventListener("input", () => guessWord());
document.body.onload = () => {
    guessWord();
    updateMenu();
}

const addWordForm = document.getElementById("addWordForm");
addWordForm.addEventListener("submit", (event) => {

    // Ensure that if the part of speech is noun, a plural form is provided
    const isNoun = document.getElementById("pos").value === "noun";
    const pluralValue = document.getElementById("plural").value;
    if (isNoun && pluralValue.trim() === "") {
        event.preventDefault();
        alert("Please provide a plural form for the noun.");
    }
    const addToList = document.getElementById("addToList").checked;
    const englishTranslation = document.getElementById("englishMeaning").value;
    if (addToList && englishTranslation.trim() === "") {
        event.preventDefault();
        alert("Please provide an English translation if you want to add the word to the vocab list.");
    }
}); 

// Code for not swahili button
const notSwahiliButton = document.getElementById("not_swahili");
notSwahiliButton.addEventListener("click", () => {
    // Set the part of speech to other
    document.getElementById("pos").value = "other";
    // Uncheck the add to vocabulary list checkbox
    document.getElementById("addToList").checked = false;
    updateMenu();
});
