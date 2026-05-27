const cursor = document.querySelector(".cursor");
if (cursor) {
    document.addEventListener("mousemove", (e) => {
        cursor.style.left = `${e.clientX}px`;
        cursor.style.top = `${e.clientY}px`;
    });
}

const reveals = document.querySelectorAll(".reveal");
window.addEventListener("scroll", () => {
    reveals.forEach((el) => {
        const top = el.getBoundingClientRect().top;
        if (top < window.innerHeight - 100) {
            el.classList.add("active");
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("pomodoro-form");
    const display = document.getElementById("timer-display");
    const minutesInput = document.getElementById("minutes-input");

    if (form && display && minutesInput) {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            const minutes = minutesInput.value;
            const formData = new FormData();
            formData.append("minutes", minutes);

            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
            });
            const result = await response.json();

            if (!result.success) {
                display.querySelector(".timer-label").textContent = result.message;
                return;
            }

            let remaining = result.total_seconds;
            const timerLabel = display.querySelector(".timer-label");
            const timerValue = display.querySelector(".timer-value");

            timerLabel.textContent = `Focus session set for ${result.minutes} minutes.`;
            timerValue.textContent = formatTime(remaining);

            const interval = setInterval(() => {
                remaining -= 1;
                if (remaining <= 0) {
                    clearInterval(interval);
                    timerLabel.textContent = "Session complete! Take a short break.";
                    timerValue.textContent = "00:00";
                    return;
                }
                timerValue.textContent = formatTime(remaining);
            }, 1000);
        });
    }
});

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
    const remainingSeconds = Math.floor(seconds % 60).toString().padStart(2, "0");
    return `${minutes}:${remainingSeconds}`;
}
