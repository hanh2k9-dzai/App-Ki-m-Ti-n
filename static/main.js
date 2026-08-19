let selectedOption = null;

document.addEventListener("DOMContentLoaded", () => {
    // Logic đếm ngược trang Quiz
    const timerElem = document.getElementById("timer");
    if (timerElem) {
        let timeLeft = 15; // 15 giây đếm ngược
        const countdown = setInterval(() => {
            timeLeft--;
            timerElem.innerText = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(countdown);
                document.getElementById("timer-box").style.display = "none";
                
                // Mở khoá các nút đáp án
                document.querySelectorAll(".opt-btn").forEach(btn => btn.disabled = false);
            }
        }, 1000);
    }
});

function selectOption(opt) {
    selectedOption = opt;
    // Bỏ chọn nút cũ, highlight nút mới
    document.querySelectorAll(".opt-btn").forEach(btn => btn.classList.remove("selected"));
    event.target.classList.add("selected");
    
    // Mở nút Gửi
    document.getElementById("submit-btn").disabled = false;
}

function submitAnswer() {
    const quizBox = document.getElementById("quiz-box");
    const qId = quizBox.getAttribute("data-id");

    if (!selectedOption) {
        alert("Vui lòng chọn một đáp án!");
        return;
    }

    fetch("/api/submit-quiz", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question_id: qId, choice: selectedOption })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        if (data.status === "success") {
            window.location.reload(); // Tải lại câu mới
        }
    })
    .catch(err => console.error(err));
}
