class BoggleGame {

    constructor(boardId, secondes=60) {
        this.boardId = $("#" + boardId);
        this.secondes = secondes;
        this.showTime();
        this.score = 0;
        this.words = new Set();

        this.timer = setInterval(this.tick.bind(this), 1000);

        $(".form", this.board).on("submit", this.handleSubmit.bind(this));
    }


    showWord(word) {
        $(".words", this.board).append($("<li>", { text: word }));
    }

    showScore(){
        $(".score", this.board).text(this.score);
    }

    showMessage(msg, cls) {
        $(".msg", this.board)
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
    }

    async handleSubmit(evt) {
        evt.preventDefault();
        const $word = $(".word", this.board);
    
        let word = $word.val();
        if (!word) return;
    
        if (this.words.has(word)) {
          this.showMessage(`Already found ${word}`, "err");
          return;
        }
    
        // check server for validity
        const resp = await axios.get("/check-word", { params: { word: word }});
        if (resp.data.result === "not-word") {
          this.showMessage(`${word} is not a valid English word`, "err");
        } else if (resp.data.result === "not-on-board") {
          this.showMessage(`${word} is not a valid word on this board`, "err");
        } else {
          this.showWord(word);
          this.score += word.length;
          this.showScore();
          this.words.add(word);
          this.showMessage(`Added: ${word}`, "ok");
        }
    
        $word.val("").focus();
      }

    showTime() {
        $(".timer", this.board).text(this.secondes);
    }

    async tick() {
        this.secondes -= 1;
        this.showTime();
        if (this.secondes === 0) {
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    async scoreGame() {
        $(".form", this.board).hide();
        const response = await axios.post("/score", { score: this.score });
        if (response.data.brokeRecord) {
            this.showMessage(`You broke the record! => ${this.score}`, "ok");
        } else {
            this.showMessage(`Score final: ${this.score}`, "ok");
        }
    }
}