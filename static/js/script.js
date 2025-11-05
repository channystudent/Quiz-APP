let currentCategory = null;
let questions = [];
let index = 0;
let score = 0;

async function getCategories() {
  try {
    const res = await fetch('/api/categories');
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    const data = await res.json();
    const select = document.getElementById('categorySelect');
    const userSelect = document.getElementById('userCategory');
    select.innerHTML = '';
    userSelect.innerHTML = '';
    data.forEach(c => {
      select.innerHTML += `<option value="${c.id}">${c.name}</option>`;
      userSelect.innerHTML += `<option value="${c.id}">${c.name}</option>`;
    });
    loadQuestions();
  } catch (error) {
    console.error('Error fetching categories:', error);
    alert('Failed to load categories. Please refresh the page.');
  }
}

async function addCategory() {
  const name = document.getElementById('categoryInput').value;
  if (!name) return alert('Enter category name');
  try {
    const res = await fetch('/api/categories', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({name})
    });
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    document.getElementById('categoryInput').value = '';
    getCategories();
  } catch (error) {
    console.error('Error adding category:', error);
    alert('Failed to add category. Please try again.');
  }
}

async function loadQuestions() {
  const catId = document.getElementById('categorySelect').value;
  if (!catId) return;
  try {
    const res = await fetch(`/api/questions/${catId}`);
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    const data = await res.json();
    const list = document.getElementById('questionList');
    list.innerHTML = data.map(q => `
      <div class="question-item">
        <b>${q.question}</b> (${q.correct})
        <button onclick="deleteQuestion(${catId}, ${q.id})">🗑</button>
      </div>
    `).join('');
  } catch (error) {
    console.error('Error loading questions:', error);
    const list = document.getElementById('questionList');
    list.innerHTML = '<p style="color: red;">Failed to load questions. Please try again.</p>';
  }
}

async function addQuestion() {
  const catId = document.getElementById('categorySelect').value;
  const q = document.getElementById('questionInput').value;
  const correct = document.getElementById('correctInput').value;
  const options = [
    document.getElementById('opt1').value,
    document.getElementById('opt2').value,
    document.getElementById('opt3').value,
    correct
  ];
  if (!q || !correct) return alert('Fill all fields');
  try {
    const res = await fetch(`/api/questions/${catId}`, {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question: q, correct, options})
    });
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    ['questionInput','correctInput','opt1','opt2','opt3'].forEach(id => document.getElementById(id).value = '');
    loadQuestions();
  } catch (error) {
    console.error('Error adding question:', error);
    alert('Failed to add question. Please try again.');
  }
}

async function deleteQuestion(catId, qId) {
  try {
    const res = await fetch(`/api/questions/${catId}?id=${qId}`, {method: 'DELETE'});
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    loadQuestions();
  } catch (error) {
    console.error('Error deleting question:', error);
    alert('Failed to delete question. Please try again.');
  }
}

function showStage(stageId) {
  document.querySelectorAll('.stage').forEach(s => s.classList.remove('active'));
  document.getElementById(stageId).classList.add('active');
  if (stageId === 'adminStage') getCategories();
}

async function startQuiz() {
  currentCategory = document.getElementById('userCategory').value;
  if (!currentCategory) {
    return alert('Please select a category first');
  }
  try {
    const res = await fetch(`/api/questions/${currentCategory}`);
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    questions = await res.json();
    if (questions.length === 0) {
      return alert('No questions available in this category');
    }
    index = 0;
    score = 0;
    showQuestion();
  } catch (error) {
    console.error('Error starting quiz:', error);
    alert('Failed to load quiz questions. Please try again.');
  }
}

function showQuestion() {
  const qBox = document.getElementById('quizContainer');
  const rBox = document.getElementById('resultContainer');
  if (index >= questions.length) return showResult();
  const q = questions[index];
  qBox.classList.remove('hidden');
  rBox.classList.add('hidden');
  qBox.innerHTML = `
    <h3>${q.question}</h3>
    ${q.options.map(o => `<button onclick="checkAnswer('${o}', '${q.correct}')">${o}</button>`).join('')}
  `;
}

function checkAnswer(ans, correct) {
  if (ans === correct) score++;
  index++;
  showQuestion();
}

function showResult() {
  const qBox = document.getElementById('quizContainer');
  const rBox = document.getElementById('resultContainer');
  qBox.classList.add('hidden');
  rBox.classList.remove('hidden');
  rBox.innerHTML = `
    <h2>🎉 Congratulations 🎉</h2>
    <p>You scored ${score} / ${questions.length}</p>
    <p>${score === questions.length ? 'Perfect!' : 'Try again!'}</p>
  `;
}

window.onload = getCategories;
