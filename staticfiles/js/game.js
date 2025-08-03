document.addEventListener('DOMContentLoaded', () => {
    const words = [
        'function', 'variable', 'constant', 'array', 'object', 'class', 'interface', 
        'module', 'import', 'export', 'async', 'await', 'promise', 'callback', 
        'component', 'state', 'props', 'react', 'angular', 'vue', 'python', 'django',
        'javascript', 'html', 'css', 'grid', 'flexbox', 'algorithm', 'database'
    ];

    const timeLeftDisplay = document.getElementById('time-left');
    const scoreDisplay = document.getElementById('score');
    const wordDisplay = document.getElementById('word-display');
    const wordInput = document.getElementById('word-input');
    const startBtn = document.getElementById('start-game-btn');
    const gameOverScreen = document.getElementById('game-over-screen');
    const finalScoreDisplay = document.getElementById('final-score');
    const restartBtn = document.getElementById('restart-game-btn');

    let score = 0;
    let time = 60;
    let isPlaying;
    let countdownInterval;

    function init() {
        showWord();
        wordInput.addEventListener('input', checkInput);
        startBtn.addEventListener('click', startGame);
        restartBtn.addEventListener('click', restartGame);
    }

    function startGame() {
        isPlaying = true;
        time = 60;
        score = 0;
        
        startBtn.classList.add('hidden');
        gameOverScreen.classList.add('hidden');
        wordInput.disabled = false;
        wordInput.focus();

        scoreDisplay.textContent = score;
        timeLeftDisplay.textContent = time;

        showWord();
        countdownInterval = setInterval(countdown, 1000);
    }

    function countdown() {
        if (time > 0) {
            time--;
        } else if (time === 0) {
            endGame();
        }
        timeLeftDisplay.textContent = time;
    }

    function showWord() {
        const randomIndex = Math.floor(Math.random() * words.length);
        wordDisplay.textContent = words[randomIndex];
    }

    function checkInput() {
        if (!isPlaying) return;

        if (wordInput.value.toLowerCase() === wordDisplay.textContent.toLowerCase()) {
            score++;
            showWord();
            wordInput.value = '';
        }
        scoreDisplay.textContent = score;
    }

    function endGame() {
        isPlaying = false;
        clearInterval(countdownInterval);
        wordInput.disabled = true;
        gameOverScreen.classList.remove('hidden');
        finalScoreDisplay.textContent = score;
    }

    function restartGame() {
        wordInput.value = '';
        startGame();
    }
    
    // Elementlar mavjudligini tekshirish
    if (wordDisplay) {
        init();
    }
});