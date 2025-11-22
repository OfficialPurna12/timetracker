class StudyTimer {
    constructor() {
        this.isRunning = false;
        this.timeLeft = 25 * 60; // 25 minutes in seconds
        this.originalTime = 25 * 60;
        this.interval = null;
        this.selectedSubject = null;
        this.startTime = null;
        
        this.initializeEventListeners();
        this.updateDisplay();
    }

    initializeEventListeners() {
        // Preset buttons
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const minutes = parseInt(e.target.dataset.minutes);
                this.setTime(minutes);
                this.updatePresetButtons(e.target);
            });
        });

        // Control buttons
        document.getElementById('startBtn').addEventListener('click', () => this.start());
        document.getElementById('pauseBtn').addEventListener('click', () => this.pause());
        document.getElementById('stopBtn').addEventListener('click', () => this.stop());

        // Subject selection
        const subjectSelect = document.getElementById('subjectSelect');
        if (subjectSelect) {
            subjectSelect.addEventListener('change', (e) => {
                this.selectedSubject = e.target.value;
            });
        }

        // Custom time input
        const customTimeInput = document.getElementById('customTime');
        if (customTimeInput) {
            customTimeInput.addEventListener('change', (e) => {
                const minutes = parseInt(e.target.value);
                if (minutes > 0 && minutes <= 180) {
                    this.setTime(minutes);
                } else {
                    alert('Please enter a time between 1 and 180 minutes');
                    e.target.value = '';
                }
            });
        }
    }

    setTime(minutes) {
        this.timeLeft = minutes * 60;
        this.originalTime = minutes * 60;
        this.updateDisplay();
        
        // Update preset buttons
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.classList.remove('active');
            if (parseInt(btn.dataset.minutes) === minutes) {
                btn.classList.add('active');
            }
        });
    }

    updatePresetButtons(activeBtn) {
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        activeBtn.classList.add('active');
    }

    start() {
        if (!this.selectedSubject) {
            alert('Please select a subject first!');
            return;
        }

        if (!this.isRunning) {
            this.isRunning = true;
            this.startTime = new Date();
            
            this.interval = setInterval(() => {
                this.timeLeft--;
                this.updateDisplay();

                if (this.timeLeft <= 0) {
                    this.completeSession();
                }
            }, 1000);

            document.getElementById('startBtn').style.display = 'none';
            document.getElementById('pauseBtn').style.display = 'inline-flex';
            
            // Visual feedback
            document.body.style.backgroundColor = '#f0f9ff';
        }
    }

    pause() {
        this.isRunning = false;
        clearInterval(this.interval);
        
        document.getElementById('startBtn').style.display = 'inline-flex';
        document.getElementById('pauseBtn').style.display = 'none';
        
        // Reset background
        document.body.style.backgroundColor = '';
    }

    stop() {
        this.isRunning = false;
        clearInterval(this.interval);
        
        const minutesStudied = Math.round((this.originalTime - this.timeLeft) / 60);
        
        if (minutesStudied > 1) { // At least 1 minute studied
            if (confirm(`Save ${minutesStudied} minutes of study time for this session?`)) {
                this.saveSession(minutesStudied);
            }
        } else if (minutesStudied > 0) {
            if (confirm(`Save ${minutesStudied} minute of study time?`)) {
                this.saveSession(minutesStudied);
            }
        }
        
        this.reset();
    }

    completeSession() {
        this.isRunning = false;
        clearInterval(this.interval);
        
        const minutesStudied = this.originalTime / 60;
        this.saveSession(minutesStudied);
        this.reset();
        
        // Show completion alert with confetti effect
        this.showCompletionAlert();
    }

    async saveSession(durationMinutes) {
        try {
            console.log('Saving session:', {
                subject_id: this.selectedSubject,
                duration: durationMinutes
            });

            const response = await fetch('/api/stop_timer', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    subject_id: this.selectedSubject,
                    duration: Math.round(durationMinutes)
                })
            });

            const data = await response.json();
            
            if (data.success) {
                console.log('Study session saved successfully');
                this.showNotification('Study session saved! 🎉', 'success');
                
                // Update dashboard stats if on dashboard page
                if (typeof updateDashboardStats === 'function') {
                    updateDashboardStats();
                }
            } else {
                console.error('Error saving session:', data.error);
                this.showNotification('Error saving session. Please try again.', 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showNotification('Network error. Please check your connection.', 'error');
        }
    }

    showCompletionAlert() {
        // Create a beautiful completion modal
        const modal = document.createElement('div');
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 10000;
        `;
        
        modal.innerHTML = `
            <div style="background: white; padding: 2rem; border-radius: 12px; text-align: center; max-width: 400px;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
                <h2 style="color: #10B981; margin-bottom: 1rem;">Session Complete!</h2>
                <p style="margin-bottom: 2rem; color: #6B7280;">Great job! You've completed your study session.</p>
                <button onclick="this.closest('div').parentElement.remove()" 
                        style="background: #6366F1; color: white; border: none; padding: 0.75rem 1.5rem; 
                               border-radius: 8px; cursor: pointer; font-weight: 600;">
                    Continue Studying
                </button>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Add confetti effect
        this.createConfetti();
    }

    createConfetti() {
        const confettiCount = 100;
        const colors = ['#6366F1', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444'];
        
        for (let i = 0; i < confettiCount; i++) {
            const confetti = document.createElement('div');
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                top: -10px;
                left: ${Math.random() * 100}vw;
                border-radius: 2px;
                z-index: 9999;
                pointer-events: none;
            `;
            
            document.body.appendChild(confetti);
            
            // Animate confetti
            const animation = confetti.animate([
                { transform: 'translateY(0) rotate(0deg)', opacity: 1 },
                { transform: `translateY(${window.innerHeight}px) rotate(${360 + Math.random() * 360}deg)`, opacity: 0 }
            ], {
                duration: 1000 + Math.random() * 2000,
                easing: 'cubic-bezier(0.1, 0.8, 0.2, 1)'
            });
            
            animation.onfinish = () => confetti.remove();
        }
    }

    showNotification(message, type) {
        // Use existing flash message system or create a new one
        const flashContainer = document.querySelector('.flash-messages') || this.createFlashContainer();
        
        const flash = document.createElement('div');
        flash.className = `flash ${type}`;
        flash.textContent = message;
        flash.style.animation = 'slideIn 0.3s ease-out';
        
        flashContainer.appendChild(flash);
        
        setTimeout(() => {
            flash.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => flash.remove(), 300);
        }, 3000);
    }

    createFlashContainer() {
        const container = document.createElement('div');
        container.className = 'flash-messages';
        container.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 1000;
        `;
        document.body.appendChild(container);
        return container;
    }

    reset() {
        this.timeLeft = this.originalTime;
        this.isRunning = false;
        this.startTime = null;
        clearInterval(this.interval);
        this.updateDisplay();
        
        document.getElementById('startBtn').style.display = 'inline-flex';
        document.getElementById('pauseBtn').style.display = 'none';
        
        // Reset background
        document.body.style.backgroundColor = '';
    }

    updateDisplay() {
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;
        
        const timerDisplay = document.getElementById('timerDisplay');
        if (timerDisplay) {
            timerDisplay.textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }

        // Update progress circle if exists
        const progressCircle = document.querySelector('.progress-circle');
        if (progressCircle) {
            const circumference = 2 * Math.PI * 45;
            const offset = circumference - (this.timeLeft / this.originalTime) * circumference;
            progressCircle.style.strokeDashoffset = offset;
        }
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .timer-active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: background 0.5s ease;
    }
`;
document.head.appendChild(style);

// Initialize timer when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('timerDisplay')) {
        window.studyTimer = new StudyTimer();
    }
});