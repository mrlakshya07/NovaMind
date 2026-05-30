const cursor = document.querySelector(".cursor");
if (cursor) {
    document.addEventListener("mousemove", (e) => {
        cursor.style.left = `${e.clientX}px`;
        cursor.style.top = `${e.clientY}px`;
    });
}

const reveals = document.querySelectorAll(".reveal");

function handleReveal() {
    reveals.forEach((el) => {
        const top = el.getBoundingClientRect().top;
        if (top < window.innerHeight - 100) {
            el.classList.add("active");
        }
    });
}

window.addEventListener("scroll", handleReveal);
window.addEventListener("load", handleReveal);

function showMessage(containerId, message, success = true) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.textContent = message;
    container.classList.remove("hidden");
    container.classList.toggle("success", success);
    container.classList.toggle("warning", !success);
}

function showAchievementNotification(achievement) {

    const toast = document.createElement("div");

    toast.className = "achievement-toast";

    toast.innerHTML = `
        <div class="achievement-toast-icon">
            ${achievement.icon}
        </div>

        <div class="achievement-toast-content">
            <strong>🏆 Achievement Unlocked!</strong>
            <div>${achievement.name}</div>
            <small>+${achievement.xp || 0} XP</small>
        </div>
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("show");
    }, 100);

    setTimeout(() => {
        toast.classList.remove("show");

        setTimeout(() => {
            toast.remove();
        }, 500);

    }, 5000);
}

async function fetchJson(url, data = null, method = "GET") {
    const options = { method, headers: {} };
    if (data) {
        options.headers["Content-Type"] = "application/json";
        options.body = JSON.stringify(data);
    }
    const response = await fetch(url, options);
    return await response.json();
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60).toString().padStart(2, "0");
    const remSeconds = Math.floor(seconds % 60).toString().padStart(2, "0");
    return `${minutes}:${remSeconds}`;
}

async function setupNotesPage() {
    const noteForm = document.getElementById("note-form");
    const searchForm = document.getElementById("search-form");
    const noteList = document.getElementById("note-list");

    async function loadNotes() {
        const result = await fetchJson("/api/notes");
        if (!result.success) return;
        noteList.innerHTML = result.notes.length
            ? result.notes
                  .map((note, index) => `
                    <li>
                        <span>${index + 1}. ${note}</span>
                        <button class="secondary-btn" data-index="${index + 1}">Delete</button>
                    </li>
                `)
                  .join("")
            : `<li class="empty-state">No notes found yet. Use the form above to add one.</li>`;
        noteList.querySelectorAll("button[data-index]").forEach((button) => {
            button.addEventListener("click", async () => {
                const result = await fetchJson("/api/notes/delete", { note_num: button.dataset.index }, "POST");
                showMessage("note-message", result.message, result.success);
                loadNotes();
            });
        });
    }

    noteForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const noteText = document.getElementById("note-input").value.trim();
        const result = await fetchJson("/api/notes/add", { note: noteText }, "POST");
        if (result.achievements && result.achievements.length) {

            result.achievements.forEach(achievement => {
                showAchievementNotification(achievement);
            });

        }
        showMessage("note-message", result.message, result.success);
        if (result.success) {
            document.getElementById("note-input").value = "";
            loadNotes();
        }
    });

    searchForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const keyword = document.getElementById("search-input").value.trim();
        const result = await fetchJson("/api/notes/search", { keyword }, "POST");
        if (result.success) {
            noteList.innerHTML = result.results
                .map(([index, note]) => `
                    <li>
                        <span>${index}. ${note}</span>
                        <button class="secondary-btn" data-index="${index}">Delete</button>
                    </li>
                `)
                .join("");
            noteList.querySelectorAll("button[data-index]").forEach((button) => {
                button.addEventListener("click", async () => {
                    const result = await fetchJson("/api/notes/delete", { note_num: button.dataset.index }, "POST");
                    showMessage("note-message", result.message, result.success);
                    loadNotes();
                });
            });
        } else {
            noteList.innerHTML = `<li class="empty-state">${result.message}</li>`;
        }
    });

    loadNotes();
}

async function setupTasksPage() {
    const taskForm = document.getElementById("task-form");
    const taskList = document.getElementById("task-list");
    const taskInput = document.getElementById("task-input");

    async function loadTasks() {
        const result = await fetchJson("/api/tasks");
        if (!result.success) return;
        taskList.innerHTML = result.tasks.length
            ? result.tasks
                  .map((task) => {
                      const statusLabel = task.status === "done" ? "Todo" : "Done";
                      const actionLabel = task.status === "done" ? "Mark Todo" : "Mark Done";
                      return `
                        <li class="task-item ${task.status}">
                            <span>${task.title}</span>
                            <div class="task-actions">
                                <button class="secondary-btn" data-action="toggle" data-id="${task.id}">${actionLabel}</button>
                                <button class="secondary-btn danger" data-action="delete" data-id="${task.id}">Delete</button>
                            </div>
                        </li>
                    `;
                  })
                  .join("")
            : `<li class="empty-state">No tasks yet. Add a study task to begin.</li>`;
        taskList.querySelectorAll("button[data-action]").forEach((button) => {
            button.addEventListener("click", async () => {
                const action = button.dataset.action;
                const taskId = button.dataset.id;
                const url = action === "toggle" ? "/api/tasks/toggle" : "/api/tasks/delete";
                const result = await fetchJson(url, { task_id: taskId }, "POST");
                if (result.achievements && result.achievements.length) {

                    result.achievements.forEach(achievement => {
                        showAchievementNotification(achievement);
                    });

                }
                showMessage("task-message", result.message, result.success);
                loadTasks();
            });
        });
    }

    taskForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const result = await fetchJson("/api/tasks/add", { task: taskInput.value.trim() }, "POST");
        if (result.achievements && result.achievements.length) {

            result.achievements.forEach(achievement => {
                showAchievementNotification(achievement);
            });

        }
        showMessage("task-message", result.message, result.success);
        if (result.success) {
            taskInput.value = "";
            loadTasks();
        }
    });

    loadTasks();
}

async function setupPomodoroPage() {
    const form = document.getElementById("pomodoro-form");
    const messageId = "pomodoro-message";
    const timerValue = document.getElementById("timer-value");
    const timerLabel = document.querySelector(".timer-label");
    let interval;
    let hiddenSeconds = 0;
    let hiddenStart = null;
    let isPaused = false;
    let currentMinutes = 0;

    document.addEventListener("visibilitychange", () => {

        if (document.hidden) {

            hiddenStart = Date.now();

            isPaused = true;

            timerLabel.textContent =
                `Focus: ${result.minutes} min`;

            showMessage(
                messageId,
                "Tab hidden. Timer paused.",
                false
            );

        } else {

            if (hiddenStart) {

                hiddenSeconds += Math.floor(
                    (Date.now() - hiddenStart) / 1000
                );

                hiddenStart = null;
            }

            isPaused = false;

            timerLabel.textContent =
                `Focus: ${currentMinutes} min`;

            showMessage(
                messageId,
                "Focus session resumed.",
                true
            );
        }

    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        hiddenSeconds = 0;
        hiddenStart = null;
        const minutes = document.getElementById("minutes-input").value;
        const result = await fetchJson("/api/pomodoro/start", { minutes }, "POST");
        currentMinutes = result.minutes;
        if (!result.success) {
            showMessage(messageId, result.message, false);
            return;
        }
        showMessage(messageId, `Focus session started for ${result.minutes} minutes!`);
        let remaining = result.total_seconds;
        timerLabel.textContent = `Focus: ${currentMinutes} min`;
        timerValue.textContent = formatTime(remaining);

        if (interval) clearInterval(interval);
        interval = setInterval(async () => {
            if (isPaused) {
                return;
            }
            remaining -= 1;
            if (remaining <= 0) {

                clearInterval(interval);

                timerLabel.textContent = "Session complete!";
                timerValue.textContent = "00:00";

                const totalSeconds =
                    result.total_seconds;

                const focusScore =
                    Math.round(
                        (
                            (totalSeconds - hiddenSeconds)
                            / totalSeconds
                        ) * 100
                    );

                const saveResult = await fetchJson(
                    "/api/pomodoro/complete",
                    {
                        duration_minutes: result.minutes,
                        focus_score: focusScore
                    },
                    "POST"
                );

                if (saveResult.success) {

                    showMessage(
                        messageId,
                        "Pomodoro complete — session saved!",
                        true
                    );

                    if (
                        saveResult.achievements &&
                        saveResult.achievements.length
                    ) {

                        saveResult.achievements.forEach(achievement => {
                            showAchievementNotification(achievement);
                        });

                    }

                } else {

                    showMessage(
                        messageId,
                        saveResult.message,
                        false
                    );

                }

                return;
            }
            timerValue.textContent = formatTime(remaining);
        }, 1000);
    });
}

async function setupProgressLogPage() {
    const form = document.getElementById("progress-form");
    const dateInput = document.getElementById("progress-date");
    const hoursInput = document.getElementById("progress-hours");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const result = await fetchJson("/api/progress/log", { date: dateInput.value, hours: hoursInput.value }, "POST");
        if (result.achievements && result.achievements.length) {

            result.achievements.forEach(achievement => {
                showAchievementNotification(achievement);
            });

        }
        showMessage("progress-log-message", result.message, result.success);
        if (result.success) {
            dateInput.value = "";
            hoursInput.value = "";
        }
    });
}

async function loadProgressPage() {
    const chartArea = document.getElementById("chart-area");
    const historyOutput = document.getElementById("history-output");
    const result = await fetchJson("/api/progress");
    if (!result.success) {
        showMessage("progress-message", "Unable to load progress data.", false);
        return;
    }
    if (result.plot_url) {
        chartArea.innerHTML = `<img src="data:image/png;base64,${result.plot_url}" alt="Study Analytics Chart" />`;
    } else {
        chartArea.innerHTML = `<p class="empty-state">No study data yet. Log a session to start tracking progress.</p>`;
    }
    const sessions =
        result.sessions || [];

    if (!sessions.length) {

        historyOutput.innerHTML =
            `<p class="empty-state">
                No history available.
            </p>`;

    } else {

        historyOutput.innerHTML =
            sessions.map(session => {

                return `
                    <div class="recent-session">

                        <div>
                            ${new Date(session.date)
                                .toDateString()}
                        </div>

                        <span>
                            ${session.hours}h
                        </span>

                    </div>
                `;

            }).join("");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if (document.querySelector("#note-form")) setupNotesPage();
    if (document.querySelector("#task-form")) setupTasksPage();
    if (document.querySelector("#pomodoro-form")) setupPomodoroPage();
    if (document.querySelector("#progress-form")) setupProgressLogPage();
    if (document.querySelector("#history-output")) loadProgressPage();
});

/* =========================
   SESSION ANALYTICS
========================== */

async function loadSessionInsights() {

    const recentContainer =
        document.getElementById("recent-sessions");

    const averageElement =
        document.getElementById("focus-average");

    const targetElement =
        document.getElementById("focus-target");

    if (!recentContainer) return;

    const result =
        await fetchJson("/api/progress");

    if (!result.success) return;

    const sessions =
        result.sessions || [];

    if (!sessions.length) {

        recentContainer.innerHTML = `
            <p class="empty-state">
                No sessions logged yet.
            </p>
        `;

        return;
    }

    let totalHours = 0;

    const recentSessions =
        sessions.reverse().slice(0, 5);

    recentContainer.innerHTML =
        recentSessions.map(session => {

            const date =
                new Date(session.date)
                .toDateString();

            const hours =
                parseFloat(session.hours) || 0;

            totalHours += hours;

            return `
                <div class="recent-session">

                    <div>${date}</div>

                    <span>${hours}h</span>

                </div>
            `;

        }).join("");

    const average =
        (totalHours / recentSessions.length)
        .toFixed(1);

    averageElement.textContent =
        `${average}h`;

    const target =
        Math.max(2, Math.ceil(average + 1));

    targetElement.textContent =
        `${target}h deep work`;

}

document.addEventListener(
    "DOMContentLoaded",
    loadSessionInsights
);