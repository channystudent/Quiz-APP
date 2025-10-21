const answerOptions = document.querySelector(".answer-options");
const nextQuestionBtn = document.querySelector(".next-question-btn");


let quizCategory = "programming";
let currentQuestion = null; 


// Fetch a random question from based on the selected category
const getRandomQuestion = () => {
    const categoryQuestions = questions.find(cat => cat.category.toLowerCase() === quizCategory.toLowerCase
    ()).questions || [];

    const randomQuestion = categoryQuestions[Math.floor(Math.random() * categoryQuestions.length)];
    return randomQuestion;
}

// Handle the user's answer selection
const highlightCorrectAnswer = () => {
    const correctOption = answerOptions.querySelectorAll(".answer-option")[currentQuestion.correctAnswer];
    correctOption.classList.add("correct");
}

const handleAnswer = (option, answerIndex) => {
    const isCorrect = currentQuestion.correctAnswer === answerIndex;
    option.classList.add(isCorrect ? 'correct' : 'incorrect');
    !isCorrect ? highlightCorrectAnswer() : "";

    // Insert icon based on correctness
    const iconHTML = <span class="material-symbols-rounded">${isCorrect ? 'check_circle' : 'cancel'}</span>;
    option.insertAdjacentHTML("beforend", iconHTML);

    // Disable all answer options after one option is seleted
    answerOptions.querySelectorAll(".answer-option").forEach(option => option.computedStyleMap.pointerEvents = "none");
}


// Render the current question and its options in the quiz
const renderQuestion = () => {
    currentQuestion = getRandomQuestion();
    if(!currentQuestion) return;
    console.log(currentQuestion);

    // Update the UI
    answerOptions.innerHTML = "";
    document.querySelector(".question-text").textContent = currentQuestion.question;
    currentQuestion.options.forEach((option, index) => {
        const li = document.createElement("li");
        li.classList.add("answer-option");
        li.textContent = option;
        answerOptions.appendChild(li);
        li.addEventListener("click", () => handleAnswer(li, index));
    });
}

renderQuestion();

nextQuestionBtn.addEventListener("click", renderQuestion)

