var remainingTime;
var choice_divs = document.getElementsByClassName('choice');
var wrong_div = document.getElementsByClassName('wrong-div');
var submit_button = document.querySelector('#submit-button');
var correct_div = document.getElementsByClassName('correct-div');
var radio_buttons = document.getElementsByClassName('radio-choices');
var option_labels = document.getElementsByClassName('option-labels');


if (wrong_div.length > 0 || correct_div.length > 0) {
    for (radio of radio_buttons) {
        radio.disabled = true;
    }

    for (choice_div of choice_divs) {
        choice_div.style.cursor = 'not-allowed';
    }

    for (option_label of option_labels) {
        option_label.style.cursor = 'not-allowed'
    }
}

function showErrorMessage() {
    scrolled = false;
    questionsDivs = document.getElementsByClassName('Questions');

    for (radio_counter = 1; radio_counter <= 100; radio_counter++) {
        questionDiv = questionsDivs[radio_counter - 1];
        error_message = questionDiv.getElementsByClassName('error-message')[0];

        if (isAllRadioButtonsSelected(radio_counter)) {
            if (scrolled == false) {
                scrolled = true;
                questionDiv.scrollIntoView()
            }

            error_message.classList.add('show-error-message');
        }

        else {
            error_message.classList.remove('show-error-message');
        }
    }
}

function isAllRadioButtonsSelected(radio_counter) {
    not_selected = 0;

    for (radios of document.getElementsByName(`choices ${radio_counter}`)) {
        if (radios.checked == false) {
            not_selected += 1;
        }
    }

    return not_selected == 4;
}

function checkForSubmission() {
    isFinished = true;

    if (remainingTime <= 0) {
        isFinished = true;
    }

    else {
        for (radio_counter = 1; radio_counter <= 100; radio_counter++) {
            if (isAllRadioButtonsSelected(radio_counter) == true) {
                isFinished = false;
                break
            }
        }

        if (isFinished == false) {
            showErrorMessage();
            return false;
        }
    }

    return isFinished;
}


window.addEventListener("load", () => {
    priorDuration = 5 * 1000;
    priorEndTime = Date.now() + priorDuration;

    examEndTime = 0;
    examCountDownDuration = 0;
    examCountDownInterval = 0;

    timer_text = document.querySelector('#timer-text');

    if (timer_text) {
        priorCountDownInterval = setInterval(priorTime, 50);
    }

    function priorTime() {
        remainingTime = priorEndTime - Date.now();
        seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

        if (remainingTime <= 1300) {
            clearInterval(priorCountDownInterval);

            examCountDownDuration = 2 * 60 * 60 * 1000;
            examEndTime = Date.now() + examCountDownDuration + 1000;
            examCountDownInterval = setInterval(startExamTime, 50);
        }

        else {
            timer_text.innerText = `Starts at: ${seconds}`;
        }
    }

    function startExamTime() {
        remainingTime = examEndTime - Date.now();

        if (remainingTime <= 0) {
            clearInterval(examCountDownInterval);
            submit_button.click();
            return true;
        }

        hours = Math.floor(remainingTime / (1000 * 60 * 60));
        minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
        seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

        hours = hours.toString().padStart(2, "0");
        minutes = minutes.toString().padStart(2, "0");
        seconds = seconds.toString().padStart(2, "0");

        timer_text.innerText = `${hours} : ${minutes} : ${seconds}`;
    }
});


function createQuestionHTML(question, qIndex, total) {
    const wrapper = document.createElement("div");
    wrapper.className = "question-card";
    wrapper.dataset.index = qIndex;

    // Question details
    const details = document.createElement("div");
    details.className = "question-details";
    wrapper.appendChild(details);

    // Question title + flag
    const qBox = document.createElement("div");
    qBox.className = "Question";
    details.appendChild(qBox);

    const qNum = document.createElement("p");
    qNum.className = "question-number";
    qNum.textContent = `${qIndex}.`;
    qBox.appendChild(qNum);

    const qTitle = document.createElement("p");
    qTitle.className = "question-title";
    qTitle.textContent = question.title;
    qBox.appendChild(qTitle);

    const flag = document.createElement("a");
    flag.href = `/report-question/${question.id}/`;
    flag.target = "_blank";
    flag.innerHTML = `<i class="bx bxs-flag-alt alt-flag" title="Report"></i>`;
    qBox.appendChild(flag);

    // Choices
    const optionsDiv = document.createElement("div");
    optionsDiv.className = "options";
    details.appendChild(optionsDiv);

    (question.choices || []).forEach((choice, i) => {
        const choiceDiv = document.createElement("div");
        choiceDiv.className = "choice";

        const input = document.createElement("input");
        input.type = "radio";
        input.className = "radio-choices";
        input.name = `choices ${qIndex}`;
        input.value = i + 1;
        input.id = `q${qIndex}_opt${i + 1}`;
        choiceDiv.appendChild(input);

        const label = document.createElement("label");
        label.className = "option-labels";
        label.setAttribute("for", `q${qIndex}_opt${i + 1}`);
        label.textContent = choice;
        choiceDiv.appendChild(label);

        optionsDiv.appendChild(choiceDiv);
    });

    // Nav buttons
    const navDiv = document.createElement("div");
    navDiv.className = "question-nav-buttons";

    if (qIndex > 1) {
        const backBtn = document.createElement("button");
        backBtn.type = "button";
        backBtn.className = "back-btn";
        backBtn.textContent = "← Back";
        backBtn.onclick = () => showQuestion(qIndex - 1);
        navDiv.appendChild(backBtn);
    }

    if (qIndex < total) {
        const nextBtn = document.createElement("button");
        nextBtn.type = "button";
        nextBtn.className = "next-btn";
        nextBtn.textContent = "Next →";
        nextBtn.onclick = () => showQuestion(qIndex + 1);
        navDiv.appendChild(nextBtn);
    } else {
        // Last question → show Submit button
        const submitBtn = document.createElement("button");
        submitBtn.type = "submit";                    // submit the form
        submitBtn.className = "submit-btn";
        submitBtn.textContent = "Submit Quiz";
        navDiv.appendChild(submitBtn);
    }

    details.appendChild(navDiv);
    return wrapper;
}


document.addEventListener('DOMContentLoaded', () => {
    setTimeout(renderQuestions, 4000);
});


function renderQuestions() {
    const container = document.querySelector("#questions-root");
    if (!container) return;

    const dataEl = document.getElementById("question_details");
    if (!dataEl) {
        console.error("Missing #question_details JSON script tag.");
        return;
    }

    let questions = [];
    try {
        questions = JSON.parse(dataEl.textContent || "[]");
    } catch (e) {
        console.error("Invalid questions JSON", e);
        return;
    }

    // Build all
    questions.forEach((q, i) =>
        container.appendChild(createQuestionHTML(q, i + 1, questions.length))
    );

    // Hide all by default; then show first
    container.querySelectorAll(".question-card").forEach(q => (q.style.display = "none"));
    showQuestion(1);

    if (window.MathJax && window.MathJax.typesetPromise) {
        MathJax.typesetPromise();
    }
}


function showQuestion(idx) {
    const cards = document.querySelectorAll("#questions-root .question-card");
    cards.forEach((q, i) => {
        q.style.display = (i + 1 === idx) ? "block" : "none";
    });

    if (window.MathJax && window.MathJax.typesetPromise) {
        MathJax.typesetPromise();
    }
}
