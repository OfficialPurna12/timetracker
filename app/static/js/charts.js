// Chart.js initialization and management

class StudyCharts {
    constructor() {
        this.charts = new Map();
        this.initializeCharts();
    }

    initializeCharts() {
        this.initializeSubjectDistributionChart();
        this.initializeWeeklyProgressChart();
        this.initializeDailyTrendChart();
    }

    initializeSubjectDistributionChart() {
        const ctx = document.getElementById('subjectDistributionChart');
        if (!ctx) return;

        const chartData = JSON.parse(ctx.getAttribute('data-chart'));
        
        this.charts.set('distribution', new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: chartData.subject_names,
                datasets: [{
                    data: chartData.subject_times,
                    backgroundColor: chartData.subject_colors,
                    borderWidth: 2,
                    borderColor: '#FFFFFF'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Study Time Distribution'
                    }
                }
            }
        }));
    }

    initializeWeeklyProgressChart() {
        const ctx = document.getElementById('weeklyProgressChart');
        if (!ctx) return;

        // This would typically come from server-side data
        const weeklyData = this.getWeeklyData();
        
        this.charts.set('weekly', new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Study Hours',
                    data: weeklyData,
                    backgroundColor: '#6366F1',
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Weekly Study Progress'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Hours'
                        }
                    }
                }
            }
        }));
    }

    initializeDailyTrendChart() {
        const ctx = document.getElementById('dailyTrendChart');
        if (!ctx) return;

        const trendData = this.getDailyTrendData();
        
        this.charts.set('trend', new Chart(ctx, {
            type: 'line',
            data: {
                labels: trendData.labels,
                datasets: [{
                    label: 'Daily Study Time',
                    data: trendData.data,
                    borderColor: '#8B5CF6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Daily Study Trend'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Hours'
                        }
                    }
                }
            }
        }));
    }

    getWeeklyData() {
        // Mock data - in real app, this would come from the server
        return [2, 3, 1.5, 2.5, 4, 1, 2];
    }

    getDailyTrendData() {
        // Mock data for the last 7 days
        const labels = [];
        const data = [];
        
        for (let i = 6; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            labels.push(date.toLocaleDateString('en', { weekday: 'short' }));
            data.push(Math.random() * 4 + 1); // Random data between 1-5 hours
        }
        
        return { labels, data };
    }

    updateCharts() {
        // Method to refresh all charts with new data
        this.charts.forEach(chart => {
            chart.destroy();
        });
        this.charts.clear();
        this.initializeCharts();
    }
}

// Initialize charts when page loads
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.chart-container')) {
        window.studyCharts = new StudyCharts();
    }
});