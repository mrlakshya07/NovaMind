// Achievement definitions for UI
const ACHIEVEMENT_DEFS = {
    // Study Achievements
    "first_session": {
        "name": "First Session",
        "description": "Log your first study session",
        "icon": "🌱",
        "category": "Study Achievements",
        "rarity": "common"
    },
    "ten_study_hours": {
        "name": "Study Apprentice",
        "description": "Reach 10 study hours",
        "icon": "📚",
        "category": "Study Achievements",
        "rarity": "uncommon"
    },
    "fifty_study_hours": {
        "name": "Knowledge Builder",
        "description": "Reach 50 study hours",
        "icon": "🎓",
        "category": "Study Achievements",
        "rarity": "rare"
    },
    "hundred_study_hours": {
        "name": "Study Master",
        "description": "Reach 100 study hours",
        "icon": "🏆",
        "category": "Study Achievements",
        "rarity": "epic"
    },

    // Note Achievements
    "first_note": {
        "name": "First Note",
        "description": "Create your first note",
        "icon": "📝",
        "category": "Note Achievements",
        "rarity": "common"
    },
    "ten_notes": {
        "name": "Note Taker",
        "description": "Create 10 notes",
        "icon": "📒",
        "category": "Note Achievements",
        "rarity": "uncommon"
    },
    "hundred_notes": {
        "name": "Knowledge Scribe",
        "description": "Create 100 notes",
        "icon": "📖",
        "category": "Note Achievements",
        "rarity": "rare"
    },
    
    // Task Achievements
    "first_task": {
        "name": "First Task",
        "description": "Create your first task",
        "icon": "✅",
        "category": "Task Achievements",
        "rarity": "common"
    },
    "first_task_completed": {
        "name": "Task Starter",
        "description": "Complete your first task",
        "icon": "🎯",
        "category": "Task Achievements",
        "rarity": "common"
    },
    "ten_tasks_completed": {
        "name": "Productivity Starter",
        "description": "Complete 10 tasks",
        "icon": "⚡",
        "category": "Task Achievements",
        "rarity": "uncommon"
    },
    "fifty_tasks_completed": {
        "name": "Task Champion",
        "description": "Complete 50 tasks",
        "icon": "🚀",
        "category": "Task Achievements",
        "rarity": "epic"
    },
    
    // Focus Achievements
    "first_pomodoro": {
        "name": "First Focus Session",
        "description": "Complete your first Pomodoro",
        "icon": "⏳",
        "category": "Focus Achievements",
        "rarity": "common"
    },
    "twenty_five_pomodoros": {
        "name": "Focus Builder",
        "description": "Complete 25 Pomodoro sessions",
        "icon": "🎯",
        "category": "Focus Achievements",
        "rarity": "uncommon"
    },
    "hundred_pomodoros": {
        "name": "Deep Work Master",
        "description": "Complete 100 Pomodoro sessions",
        "icon": "🔥",
        "category": "Focus Achievements",
        "rarity": "epic"
    },
    "focus_perfectionist": {
        "name": "Focus Perfectionist",
        "description": "Complete a session with 95%+ focus score",
        "icon": "💎",
        "category": "Focus Achievements",
        "rarity": "rare"
    },
    
    // Consistency Achievements
    "three_day_streak": {
        "name": "3 Day Streak",
        "description": "Maintain a 3-day study streak",
        "icon": "📅",
        "category": "Consistency Achievements",
        "rarity": "uncommon"
    },
    "seven_day_streak": {
        "name": "7 Day Streak",
        "description": "Maintain a 7-day study streak",
        "icon": "🔥",
        "category": "Consistency Achievements",
        "rarity": "rare"
    },
    "thirty_day_streak": {
        "name": "30 Day Streak",
        "description": "Maintain a 30-day study streak",
        "icon": "🚀",
        "category": "Consistency Achievements",
        "rarity": "epic"
    },
    "consistency_legend": {
        "name": "Consistency Legend",
        "description": "Maintain a 100-day study streak",
        "icon": "👑",
        "category": "Consistency Achievements",
        "rarity": "legendary"
    }
};

// Load and display achievements
async function loadAchievements() {
    try {
        const [achievementsRes, progressRes, statsRes] = await Promise.all([
            fetch('/api/achievements'),
            fetch('/api/achievements/progress'),
            fetch('/api/achievements/stats')
        ]);

        if (!achievementsRes.ok || !progressRes.ok || !statsRes.ok) {
            console.error('Failed to load achievement data');
            return;
        }

        const achievementsData = await achievementsRes.json();
        const progressData = await progressRes.json();
        const statsData = await statsRes.json();

        if (achievementsData.success) {
            displayStats(statsData.stats);
            displayAchievements(achievementsData.achievements, progressData.progress);
        }
    } catch (error) {
        console.error('Error loading achievements:', error);
    }
}

// Display statistics cards
function displayStats(stats) {
    const statsContainer = document.getElementById('stats-container');
    
    if (!stats) {
        return;
    }

    const totalCard = createStatCard(
        'Total Achievements',
        stats.total,
        '🏅'
    );

    const unlockedCard = createStatCard(
        'Unlocked',
        stats.unlocked,
        '⭐'
    );

    const completionCard = createStatCard(
        'Completion',
        `${stats.completion_percentage}%`,
        '📊'
    );

    const streakCard = createStatCard(
        'Total XP',
        stats.total_xp || 0,
        '⭐'
    );

    statsContainer.innerHTML = totalCard + unlockedCard + completionCard + streakCard;
    statsContainer.querySelectorAll('.stat-card').forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('active');
        }, index * 100);
    });
}

// Create a single stat card
function createStatCard(label, value, icon) {
    return `
        <div class="stat-card reveal active">
            <div style="font-size: 2rem; margin-bottom: 12px;">${icon}</div>
            <div class="stat-value">${value}</div>
            <div class="stat-label">${label}</div>
        </div>
    `;
}

// Display achievements organized by category
function displayAchievements(earnedAchievements, progress) {
    const container = document.getElementById('achievements-container');
    const earnedTypes = new Set(earnedAchievements.map(a => a.type));

    // Group achievements by category
    const grouped = {};
    for (const [type, def] of Object.entries(ACHIEVEMENT_DEFS)) {
        const category = def.category;
        if (!grouped[category]) {
            grouped[category] = [];
        }
        grouped[category].push({ type, ...def });
    }

    // Sort categories
    const categoryOrder = [
        'Study Achievements',
        'Note Achievements',
        'Task Achievements',
        'Focus Achievements',
        'Consistency Achievements'
    ];

    let html = '';

    for (const category of categoryOrder) {
        if (!grouped[category]) continue;

        html += `<div class="categories-section">
            <div class="category-title">${category}</div>
            <div class="achievements-grid">`;

        for (const achievement of grouped[category]) {
            const isUnlocked = earnedTypes.has(achievement.type);
            const progressData = getProgressForAchievement(achievement.type, progress);
            
            html += createAchievementCard(achievement, isUnlocked, progressData);
        }

        html += `</div>
        </div>`;
    }

    container.innerHTML = html;

    // Trigger reveal animation
    document.querySelectorAll('.achievement-card').forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('active');
        }, index * 30);
    });
}

// Create achievement card HTML
function createAchievementCard(achievement, isUnlocked, progressData) {
    const statusClass = isUnlocked ? 'unlocked' : 'locked';
    const statusText = isUnlocked ? '✓ Unlocked' : '🔒 Locked';
    const progressHtml = progressData ? createProgressBar(progressData) : '';

    return `
        <div class="achievement-card ${statusClass} reveal">
            <div class="achievement-icon">${achievement.icon}</div>
            <div class="achievement-name">${achievement.name}</div>
            <div class="achievement-description">${achievement.description}</div>
            ${progressHtml}
            <div class="achievement-status ${statusClass}">${statusText}</div>
        </div>
    `;
}

// Create progress bar for in-progress achievements
function createProgressBar(progressData) {
    if (!progressData || progressData.percentage === undefined) {
        return '';
    }

    const percentage = Math.min(100, progressData.percentage);
    
    return `
        <div class="achievement-progress">
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: ${percentage}%"></div>
            </div>
            <div class="progress-text">${progressData.current}/${progressData.target}</div>
        </div>
    `;
}

// Get progress data for specific achievement
function getProgressForAchievement(type, progress) {
    if (!progress) return null;

    // Study hour milestones
    if (type === 'ten_study_hours' && progress.study_hours) {
        return {
            current: progress.study_hours.current,
            target: 10,
            percentage: (progress.study_hours.current / 10) * 100
        };
    }
    if (type === 'fifty_study_hours' && progress.study_hours) {
        return {
            current: progress.study_hours.current,
            target: 50,
            percentage: (progress.study_hours.current / 50) * 100
        };
    }
    if (type === 'hundred_study_hours' && progress.study_hours) {
        return {
            current: progress.study_hours.current,
            target: 100,
            percentage: (progress.study_hours.current / 100) * 100
        };
    }

    // Task milestones
    if (type === 'ten_tasks_completed' && progress.tasks) {
        return {
            current: progress.tasks.current,
            target: 10,
            percentage: (progress.tasks.current / 10) * 100
        };
    }
    if (type === 'fifty_tasks_completed' && progress.tasks) {
        return {
            current: progress.tasks.current,
            target: 50,
            percentage: (progress.tasks.current / 50) * 100
        };
    }

    // Pomodoro milestones
    if (type === 'twenty_five_pomodoros' && progress.pomodoros) {
        return {
            current: progress.pomodoros.current,
            target: 25,
            percentage: (progress.pomodoros.current / 25) * 100
        };
    }
    if (type === 'hundred_pomodoros' && progress.pomodoros) {
        return {
            current: progress.pomodoros.current,
            target: 100,
            percentage: (progress.pomodoros.current / 100) * 100
        };
    }

    return null;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', loadAchievements);

// Refresh achievements periodically
setInterval(loadAchievements, 30000); // Refresh every 30 seconds