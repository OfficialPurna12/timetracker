// Dashboard real-time functionality

class DashboardUpdater {
    constructor() {
        this.updateInterval = 30000; // Update every 30 seconds
        this.init();
    }

    init() {
        // Update stats immediately
        this.updateStats();
        
        // Set up periodic updates
        setInterval(() => {
            this.updateStats();
        }, this.updateInterval);

        // Add event listeners for manual refresh
        this.addEventListeners();
    }

    async updateStats() {
        try {
            const response = await fetch('/api/dashboard_stats');
            const data = await response.json();
            
            if (data.success) {
                this.updateDisplay(data.stats);
            }
        } catch (error) {
            console.error('Error updating dashboard stats:', error);
        }
    }

    updateDisplay(stats) {
        // Update today's study time
        const todayElement = document.querySelector('.stat-number');
        if (todayElement) {
            todayElement.textContent = `${stats.today_hours}h`;
        }

        // Update subject progress bars
        stats.subject_progress.forEach(subject => {
            const progressBar = document.querySelector(`[data-subject-id="${subject.subject_id}"] .progress-fill`);
            if (progressBar) {
                progressBar.style.width = `${subject.percentage}%`;
                
                // Update time display
                const timeDisplay = progressBar.closest('.subject-card').querySelector('.subject-time');
                if (timeDisplay) {
                    timeDisplay.textContent = `${subject.today_minutes}m today`;
                }
            }
        });

        // Update weekly total
        const weeklyElement = document.querySelectorAll('.stat-number')[2];
        if (weeklyElement) {
            weeklyElement.textContent = `${stats.weekly_hours}h`;
        }

        // Update goal progress
        const goalElement = document.querySelectorAll('.stat-number')[3];
        if (goalElement) {
            goalElement.textContent = `${stats.daily_goal_percentage}%`;
        }
    }

    addEventListeners() {
        // Refresh button if exists
        const refreshBtn = document.getElementById('refreshStats');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.updateStats();
                this.showNotification('Stats updated!', 'success');
            });
        }
    }

    showNotification(message, type) {
        const flashContainer = document.querySelector('.flash-messages');
        if (flashContainer) {
            const flash = document.createElement('div');
            flash.className = `flash ${type}`;
            flash.textContent = message;
            flashContainer.appendChild(flash);
            
            setTimeout(() => flash.remove(), 3000);
        }
    }
}

// Global function to update dashboard stats
function updateDashboardStats() {
    if (window.dashboardUpdater) {
        window.dashboardUpdater.updateStats();
    }
}

// Initialize dashboard updater
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.dashboard-header')) {
        window.dashboardUpdater = new DashboardUpdater();
    }
});