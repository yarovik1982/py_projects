class Game {
   constructor() {
      this.words = ['javascript', 'программа', 'браузер', 'функция', 'объект'];
      this.maxAttempts = 10;
      this.ui = new UI(this);
      this.start();
   }

   start() {
      this.word = this.getRandomWord();
      this.guessed = [];
      this.attempts = this.maxAttempts;
      this.ui.render();
   }

   getRandomWord() {
      return this.words[Math.floor(Math.random() * this.words.length)];
   }

   guess(letter) {
      if (this.word.includes(letter)) {
         this.guessed.push(letter);
      } else {
         this.attempts--;
      }

      this.ui.update();

      if (this.isWin()) {
         this.ui.showMessage('🎉 Победа!');
      }

      if (this.isLose()) {
         this.ui.showMessage(`💀 Проигрыш! Слово: ${this.word}`);
      }
   }

   isWin() {
      return this.word.split('').every(l => this.guessed.includes(l));
   }

   isLose() {
      return this.attempts <= 0;
   }
}

class UI {
   constructor(game) {
      this.game = game;
      this.wordEl = document.getElementById('word');
      this.keyboardEl = document.getElementById('keyboard');
      this.attemptsEl = document.getElementById('attempts');
      this.restartBtn = document.getElementById('restart');

      this.restartBtn.onclick = () => this.game.start();
   }

   render() {
      this.renderWord();
      this.renderKeyboard();
      this.renderAttempts();
   }

   update() {
      this.renderWord();
      this.renderAttempts();
   }

   renderWord() {
      this.wordEl.innerHTML = this.game.word
         .split('')
         .map(l => (this.game.guessed.includes(l) ? l : '_'))
         .join(' ');
   }

   renderKeyboard() {
      this.keyboardEl.innerHTML = '';
      const letters = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя';

      [...letters].forEach(letter => {
         const btn = document.createElement('button');
         btn.textContent = letter;
         btn.onclick = () => {
            btn.disabled = true;
            this.game.guess(letter);
         };
         this.keyboardEl.appendChild(btn);
      });
   }

   renderAttempts() {
      this.attemptsEl.textContent = `❤️ Попыток: ${this.game.attempts}`;
   }

   showMessage(text) {
      setTimeout(() => alert(text), 100);
      [...this.keyboardEl.children].forEach(btn => btn.disabled = true);
   }
}

new Game();
