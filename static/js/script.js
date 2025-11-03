let currentCategory = null;
let questions = [];
let index = 0;
let score = 0;

async function getCategories() {
  const res = await fetch('/api/categories');
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
}

async function addCategory() {
  const name = document.getElementById('categoryInput').value;
  if (!name) return alert('Enter category name');
  await fetch('/api/categories', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name})
  });
  document.getElementById('categoryInput').value = '';
  getCategories();
}

async function loadQuestions() {
  const catId = document.getElementById('categorySelect').value;
  if (!catId) return;
  const res = await fetch(`/api/questions/${catId}`);
  const data = await res.json();
  const list = document.getElementById('questionList');
  list.innerHTML = data.map(q => `
    <div class="question-item">
      <b>${q.question}</b> (${q.correct})
      <button onclick="deleteQuestion(${catId}, ${q.id})">🗑</button>
    </div>
  `).join('');
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
  await fetch(`/api/questions/${catId}`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({question: q, correct, options})
  });
  ['questionInput','correctInput','opt1','opt2','opt3'].forEach(id => document.getElementById(id).value = '');
  loadQuestions();
}

async function deleteQuestion(catId, qId) {
  await fetch(`/api/questions/${catId}?id=${qId}`, {method: 'DELETE'});
  loadQuestions();
}

function showStage(stageId) {
  document.querySelectorAll('.stage').forEach(s => s.classList.remove('active'));
  document.getElementById(stageId).classList.add('active');
  if (stageId === 'adminStage') getCategories();
}

async function startQuiz() {
  currentCategory = document.getElementById('userCategory').value;
  const res = await fetch(`/api/questions/${currentCategory}`);
  questions = await res.json();
  index = 0;
  score = 0;
  showQuestion();
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
