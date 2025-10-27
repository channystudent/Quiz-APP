// Quiz questions across different categories
const quizQuestions = [
    // Geography
    {
        question: "What is the capital of France?",
        options: ["London", "Berlin", "Paris", "Madrid"],
        correct: 2,
        category: "Geography"
    },
    {
        question: "Which is the largest continent by area?",
        options: ["North America", "Africa", "Asia", "Europe"],
        correct: 2,
        category: "Geography"
    },
    {
        question: "Which country is known as the Land of the Rising Sun?",
        options: ["China", "Korea", "Japan", "Vietnam"],
        correct: 2,
        category: "Geography"
    },
    
    // Science
    {
        question: "Which planet is known as the Red Planet?",
        options: ["Venus", "Mars", "Jupiter", "Saturn"],
        correct: 1,
        category: "Science"
    },
    {
        question: "What is the chemical symbol for gold?",
        options: ["Ag", "Fe", "Au", "Cu"],
        correct: 2,
        category: "Science"
    },
    {
        question: "What is the hardest natural substance on Earth?",
        options: ["Gold", "Iron", "Diamond", "Platinum"],
        correct: 2,
        category: "Science"
    },
    
    // Mathematics
    {
        question: "What is 2 + 2?",
        options: ["3", "4", "5", "6"],
        correct: 1,
        category: "Mathematics"
    },
    {
        question: "What is the square root of 64?",
        options: ["6", "7", "8", "9"],
        correct: 2,
        category: "Mathematics"
    },
    {
        question: "What is 15% of 200?",
        options: ["20", "25", "30", "35"],
        correct: 2,
        category: "Mathematics"
    },
    
    // History
    {
        question: "Who was the first President of the United States?",
        options: ["Thomas Jefferson", "John Adams", "George Washington", "Benjamin Franklin"],
        correct: 2,
        category: "History"
    },
    {
        question: "In which year did World War II end?",
        options: ["1943", "1944", "1945", "1946"],
        correct: 2,
        category: "History"
    },
    {
        question: "Who painted the Mona Lisa?",
        options: ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Michelangelo"],
        correct: 1,
        category: "History"
    },
    
    // Technology
    {
        question: "What does CPU stand for?",
        options: ["Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Central Program Unit"],
        correct: 1,
        category: "Technology"
    },
    {
        question: "Which company created the iPhone?",
        options: ["Samsung", "Apple", "Nokia", "Microsoft"],
        correct: 1,
        category: "Technology"
    },
    {
        question: "What does HTML stand for?",
        options: ["Hyper Text Markup Language", "High Tech Modern Language", "Hyper Transfer Markup Language", "High Text Machine Language"],
        correct: 0,
        category: "Technology"
    }
    ,
    // Extra questions
    {
        question: "Which river runs through the city of London?",
        options: ["Seine", "Danube", "Thames", "Rhine"],
        correct: 2,
        category: "Geography"
    },
    {
        question: "What gas do plants primarily absorb from the atmosphere?",
        options: ["Oxygen", "Carbon dioxide", "Nitrogen", "Helium"],
        correct: 1,
        category: "Science"
    },
    {
        question: "What is 12 × 12?",
        options: ["124", "144", "132", "156"],
        correct: 1,
        category: "Mathematics"
    },
    {
        question: "Which year did the Berlin Wall fall?",
        options: ["1987", "1989", "1991", "1993"],
        correct: 1,
        category: "History"
    },
    {
        question: "Which company developed the Android operating system?",
        options: ["Microsoft", "Google", "Apple", "IBM"],
        correct: 1,
        category: "Technology"
    },
    {
        question: "Which language is primarily used for styling web pages?",
        options: ["HTML", "Python", "CSS", "Java"],
        correct: 2,
        category: "General"
    }
];

let currentUser = null;

// Handle registration
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', function(e) {
        // Let the form submit normally to the server
        return true;
    });
}

// Handle login
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
        // Let the form submit normally to the server
        return true;
    });
}

// Initialize quiz
function initializeQuiz() {
    const quizSection = document.getElementById('quiz-section');
    const quizQuestionsDiv = document.getElementById('quiz-questions');
    
    quizSection.classList.remove('hidden');
    
    // Add progress indicator
    const progressDiv = document.createElement('div');
    progressDiv.className = 'quiz-progress';
    progressDiv.innerHTML = `
        <span class="count">Questions: ${quizQuestions.length}</span>
        <span class="categories">Categories: ${[...new Set(quizQuestions.map(q => q.category))].length}</span>
    `;
    quizQuestionsDiv.appendChild(progressDiv);
    
    // Add questions grouped by category
    const categories = {};
    quizQuestions.forEach(q => {
        if (!categories[q.category]) {
            categories[q.category] = [];
        }
        categories[q.category].push(q);
    });
    
    let questionIndex = 0;
    for (const [category, questions] of Object.entries(categories)) {
        // Add category header
        const categoryHeader = document.createElement('h3');
        categoryHeader.className = 'category-header';
        categoryHeader.textContent = category;
        quizQuestionsDiv.appendChild(categoryHeader);
        
        // Add questions for this category
        questions.forEach(q => {
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question';
            questionDiv.innerHTML = `
                <div class="category-label">${category}</div>
                <p><strong>Question ${questionIndex + 1}:</strong> ${q.question}</p>
                <div class="options">
                    ${q.options.map((opt, i) => `
                        <div>
                            <input type="radio" name="q${questionIndex}" value="${i}" id="q${questionIndex}o${i}">
                            <label for="q${questionIndex}o${i}">${opt}</label>
                        </div>
                    `).join('')}
                </div>
            `;
            quizQuestionsDiv.appendChild(questionDiv);
            questionIndex++;
        });
    }
    
    document.getElementById('submit-quiz').classList.remove('hidden');
}

// Handle quiz submission
const submitQuizBtn = document.getElementById('submit-quiz');
if (submitQuizBtn) {
    submitQuizBtn.addEventListener('click', async () => {
        const answers = [];
        let score = 0;
        
        quizQuestions.forEach((q, index) => {
            const selected = document.querySelector(`input[name="q${index}"]:checked`);
            const answer = selected ? parseInt(selected.value) : -1;
            answers.push(answer);
            if (answer === q.correct) score++;
        });
        
        const quizData = {
            user_id: currentUser.id,
            score: score,
            answers: answers
        };
        
        try {
            const response = await fetch('/submit_quiz', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(quizData)
            });
            
            if (response.ok) {
                showResults(score, answers);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
}

// Show quiz results
function showResults(score, answers) {
    document.getElementById('quiz-section').classList.add('hidden');
    const resultSection = document.getElementById('result-section');
    const scoreDiv = document.getElementById('score');
    const reviewDiv = document.getElementById('answers-review');
    
    resultSection.classList.remove('hidden');
    
    // Calculate category-wise scores
    const categoryScores = {};
    answers.forEach((answer, index) => {
        const question = quizQuestions[index];
        const category = question.category;
        if (!categoryScores[category]) {
            categoryScores[category] = { correct: 0, total: 0 };
        }
        categoryScores[category].total++;
        if (answer === question.correct) {
            categoryScores[category].correct++;
        }
    });
    
    // Display overall score
    let scoreHtml = `<h3>Your Overall Score: ${score}/${quizQuestions.length}</h3>`;
    
    // Display category-wise scores
    scoreHtml += '<div class="category-scores">';
    for (const [category, scores] of Object.entries(categoryScores)) {
        const percentage = Math.round((scores.correct / scores.total) * 100);
        scoreHtml += `
            <div class="category-score">
                <h4>${category}</h4>
                <p>${scores.correct}/${scores.total} (${percentage}%)</p>
            </div>
        `;
    }
    scoreHtml += '</div>';
    scoreDiv.innerHTML = scoreHtml;
    
    // Display detailed review
    let reviewHtml = '<h3>Detailed Review:</h3>';
    
    // Group questions by category
    const categorizedReview = {};
    answers.forEach((answer, index) => {
        const question = quizQuestions[index];
        const category = question.category;
        if (!categorizedReview[category]) {
            categorizedReview[category] = [];
        }
        categorizedReview[category].push({ question, answer, index });
    });
    
    // Generate review HTML by category
    for (const [category, questions] of Object.entries(categorizedReview)) {
        reviewHtml += `<div class="category-review"><h4>${category}</h4>`;
        questions.forEach(({ question, answer, index }) => {
            const isCorrect = answer === question.correct;
            reviewHtml += `
                <div class="review-item ${isCorrect ? 'correct' : 'incorrect'}">
                    <p><strong>Question ${index + 1}:</strong> ${question.question}</p>
                    <p>Your answer: ${answer === -1 ? 'No answer' : question.options[answer]}</p>
                    <p>Correct answer: ${question.options[question.correct]}</p>
                </div>
            `;
        });
        reviewHtml += '</div>';
    }
    
    reviewDiv.innerHTML = reviewHtml;
}