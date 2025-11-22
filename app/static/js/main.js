// Main JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Flash messages auto-hide
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });

    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });
    }

    // Delete subject confirmation
    const deleteButtons = document.querySelectorAll('.delete-subject');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const subjectName = this.getAttribute('data-subject-name');
            
            if (confirm(`Are you sure you want to delete "${subjectName}"? This will also delete all associated study sessions.`)) {
                const subjectId = this.getAttribute('data-subject-id');
                deleteSubject(subjectId);
            }
        });
    });
});

async function deleteSubject(subjectId) {
    try {
        const response = await fetch(`/api/delete_subject/${subjectId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const data = await response.json();
        
        if (data.success) {
            // Remove subject card from DOM
            const subjectCard = document.querySelector(`[data-subject-id="${subjectId}"]`).closest('.subject-card');
            subjectCard.remove();
            
            showFlash('Subject deleted successfully', 'success');
        } else {
            showFlash('Error deleting subject', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showFlash('Error deleting subject', 'error');
    }
}

function showFlash(message, type) {
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    
    const flash = document.createElement('div');
    flash.className = `flash ${type}`;
    flash.textContent = message;
    
    flashContainer.appendChild(flash);
    
    setTimeout(() => {
        flash.style.opacity = '0';
        setTimeout(() => flash.remove(), 300);
    }, 5000);
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

// Format time functions
function formatTime(minutes) {
    const hrs = Math.floor(minutes / 60);
    const mins = minutes % 60;
    
    if (hrs > 0) {
        return `${hrs}h ${mins}m`;
    }
    return `${mins}m`;
}

function formatMinutes(minutes) {
    const hrs = Math.floor(minutes / 60);
    const mins = minutes % 60;
    
    if (hrs > 0) {
        return `${hrs}:${mins.toString().padStart(2, '0')}`;
    }
    return `0:${mins.toString().padStart(2, '0')}`;
}