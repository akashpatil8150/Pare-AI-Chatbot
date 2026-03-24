// Chat functionality with streaming support
function sendMessage() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    addUserMessage(message);
    input.value = '';
    
    showTypingIndicator();
    
    // Use streaming for faster perceived response
    sendMessageWithStreaming(message);
}

function sendMessageWithStreaming(message) {
    let streamingMessageDiv = null;
    let accumulatedText = '';
    
    // Create message div for streaming
    const chatMessages = document.getElementById('chatMessages');
    streamingMessageDiv = document.createElement('div');
    streamingMessageDiv.className = 'message bot-message';
    streamingMessageDiv.innerHTML = `
        <div class="message-content">
            <p class="streaming-text"></p>
        </div>
        <span class="message-time">${getCurrentTime()}</span>
    `;
    
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message, stream: true })
    })
    .then(async response => {
        hideTypingIndicator();
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        chatMessages.appendChild(streamingMessageDiv);
        const textElement = streamingMessageDiv.querySelector('.streaming-text');
        
        while (true) {
            const { done, value } = await reader.read();
            
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    
                    if (data.chunk) {
                        accumulatedText += data.chunk;
                        textElement.textContent = accumulatedText;
                        scrollToBottom();
                    }
                    
                    if (data.done && data.result) {
                        // Remove streaming message and handle final result
                        streamingMessageDiv.remove();
                        handleBotResponse(data.result);
                    }
                }
            }
        }
    })
    .catch(error => {
        hideTypingIndicator();
        if (streamingMessageDiv && streamingMessageDiv.parentNode) {
            streamingMessageDiv.remove();
        }
        
        // Fallback to non-streaming
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message, stream: false })
        })
        .then(response => response.json())
        .then(data => handleBotResponse(data))
        .catch(err => {
            addBotMessage('Sorry, something went wrong. Please try again.');
            console.error('Error:', err);
        });
    });
}

function handleBotResponse(data) {
    if (data.type === 'message') {
        addBotMessage(data.content);
    } else if (data.type === 'appointment_result') {
        if (data.status === 'confirmed') {
            addAppointmentCard(data.details);
        } else if (data.status === 'cancelled') {
            addBotMessage(data.details.message);
            // Refresh appointments list if modal is open
            const appointmentsModal = document.getElementById('appointmentsModal');
            if (appointmentsModal && appointmentsModal.style.display === 'block') {
                showAppointments();
            }
        } else if (data.status === 'not_found') {
            addBotMessage(data.details.message || 'Appointment not found.');
        } else {
            addBotMessage(data.details.message || 'Unable to process appointment.');
        }
    } else if (data.type === 'error') {
        addBotMessage(data.content || 'An error occurred. Please try again.');
    } else {
        addBotMessage(data.content || 'I received your message.');
    }
}

function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
        </div>
        <span class="message-time">${getCurrentTime()}</span>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addBotMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
        </div>
        <span class="message-time">${getCurrentTime()}</span>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

function addAppointmentCard(details) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    // Format date for display (YYYY-MM-DD to DD-MM-YYYY)
    const displayDate = formatDateForDisplay(details.date);
    const displayTime = formatTimeForDisplay(details.time);
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="appointment-card">
                <h4><i class="fas fa-check-circle"></i> Appointment Confirmed!</h4>
                <p><strong>Name:</strong> ${escapeHtml(details.name)}</p>
                <p><strong>Address:</strong> ${escapeHtml(details.address)}</p>
                <p><strong>Date:</strong> ${displayDate}</p>
                <p><strong>Time:</strong> ${displayTime}</p>
                <div class="appointment-id">ID: ${escapeHtml(details.appointment_id)}</div>
            </div>
        </div>
        <span class="message-time">${getCurrentTime()}</span>
    `;
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    
    // Refresh time slots only if booking modal is open and date matches
    const appointmentModal = document.getElementById('appointmentModal');
    const dateInput = document.getElementById('date');
    if (appointmentModal && appointmentModal.style.display === 'block' && 
        dateInput && dateInput.value === details.date) {
        updateTimeSlots();
    }
}

// Format date from YYYY-MM-DD to DD-MM-YYYY for display
function formatDateForDisplay(dateStr) {
    try {
        const parts = dateStr.split('-');
        if (parts.length === 3 && parts[0].length === 4) {
            // YYYY-MM-DD format
            return `${parts[2]}-${parts[1]}-${parts[0]}`;
        }
        return dateStr; // Return as-is if already in different format
    } catch {
        return dateStr;
    }
}

// Format time from 24-hour to 12-hour with AM/PM
function formatTimeForDisplay(timeStr) {
    try {
        const [hours] = timeStr.split(':').map(Number);
        return formatTime12Hour(hours);
    } catch {
        return timeStr;
    }
}

function showTypingIndicator() {
    document.getElementById('typingIndicator').style.display = 'flex';
}

function hideTypingIndicator() {
    document.getElementById('typingIndicator').style.display = 'none';
}

function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Product quick links
function askAboutProduct(productName) {
    const input = document.getElementById('messageInput');
    input.value = `Tell me about ${productName} series`;
    sendMessage();
}

// Appointment Modal Functions
function showAppointmentForm() {
    document.getElementById('appointmentModal').style.display = 'block';
    
    // Initialize date and time slots
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date();
        const currentHour = today.getHours();
        
        // If it's past business hours (after 6 PM), default to tomorrow
        if (currentHour >= 18) {
            const tomorrow = new Date(today);
            tomorrow.setDate(tomorrow.getDate() + 1);
            dateInput.value = tomorrow.toISOString().split('T')[0];
        } else {
            dateInput.value = today.toISOString().split('T')[0];
        }
        
        updateTimeSlots();
    }
}

function closeModal() {
    document.getElementById('appointmentModal').style.display = 'none';
    document.getElementById('appointmentForm').reset();
}

function submitAppointment(event) {
    event.preventDefault();
    
    const name = document.getElementById('name').value;
    const address = document.getElementById('address').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    
    // Check if time slot is already booked
    fetch('/api/appointments')
        .then(response => response.json())
        .then(data => {
            const isSlotTaken = data.appointments.some(apt => 
                apt.date === date && apt.time === time
            );
            
            if (isSlotTaken) {
                alert('⚠️ This time slot is already booked! Please select another time.');
                return;
            }
            
            // Proceed with booking
            return fetch('/api/appointments/book', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, address, date, time })
            });
        })
        .then(response => {
            if (!response) return; // Slot was taken
            
            // Check if response is error (400)
            if (!response.ok) {
                return response.json().then(err => {
                    throw new Error(err.message || 'Booking failed');
                });
            }
            
            return response.json();
        })
        .then(data => {
            if (!data) return; // Slot was taken
            closeModal();
            addAppointmentCard(data);
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message || 'Failed to book appointment. Please try again.');
        });
}

// Appointments List Functions
function showAppointments() {
    fetch('/api/appointments')
        .then(response => response.json())
        .then(data => {
            displayAppointments(data.appointments);
            document.getElementById('appointmentsModal').style.display = 'block';
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load appointments.');
        });
}

function displayAppointments(appointments) {
    const appointmentsList = document.getElementById('appointmentsList');
    
    if (appointments.length === 0) {
        appointmentsList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-calendar-times"></i>
                <p>No appointments found</p>
            </div>
        `;
        return;
    }
    
    appointmentsList.innerHTML = appointments.map(apt => {
        const displayDate = formatDateForDisplay(apt.date);
        const displayTime = formatTimeForDisplay(apt.time);
        
        return `
            <div class="appointment-item">
                <h4><i class="fas fa-calendar-check"></i> ${escapeHtml(apt.appointment_id)}</h4>
                <p><strong>Name:</strong> ${escapeHtml(apt.name)}</p>
                <p><strong>Address:</strong> ${escapeHtml(apt.address)}</p>
                <p><strong>Date:</strong> ${displayDate}</p>
                <p><strong>Time:</strong> ${displayTime}</p>
                <button class="cancel-btn" onclick="cancelAppointment('${escapeHtml(apt.appointment_id)}')">
                    <i class="fas fa-times"></i> Cancel Appointment
                </button>
            </div>
        `;
    }).join('');
}

function cancelAppointment(appointmentId) {
    if (!confirm('Are you sure you want to cancel this appointment?')) {
        return;
    }
    
    fetch('/api/appointments/cancel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ appointment_id: appointmentId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'cancelled') {
            showAppointments(); // Refresh the list
            addBotMessage(`Appointment ${appointmentId} has been cancelled successfully.`);
        } else {
            alert('Failed to cancel appointment.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to cancel appointment.');
    });
}

function closeAppointmentsModal() {
    document.getElementById('appointmentsModal').style.display = 'none';
}

// Close modals when clicking outside
window.onclick = function(event) {
    const appointmentModal = document.getElementById('appointmentModal');
    const appointmentsModal = document.getElementById('appointmentsModal');
    
    if (event.target === appointmentModal) {
        closeModal();
    }
    if (event.target === appointmentsModal) {
        closeAppointmentsModal();
    }
}

// Set minimum date to today for appointment booking
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date();
        const todayStr = today.toISOString().split('T')[0];
        dateInput.setAttribute('min', todayStr);
        
        // If it's past business hours (after 6 PM), default to tomorrow
        const currentHour = today.getHours();
        if (currentHour >= 18) {
            const tomorrow = new Date(today);
            tomorrow.setDate(tomorrow.getDate() + 1);
            dateInput.value = tomorrow.toISOString().split('T')[0];
        } else {
            dateInput.value = todayStr;
        }
        
        updateTimeSlots();
    }
});

// Generate available time slots based on selected date
function updateTimeSlots() {
    const dateInput = document.getElementById('date');
    const timeSelect = document.getElementById('time');
    const refreshIndicator = document.getElementById('slotsRefreshIndicator');
    
    if (!dateInput || !timeSelect) return;
    
    // Show refresh indicator
    if (refreshIndicator) {
        refreshIndicator.style.display = 'inline';
    }
    
    const selectedDate = new Date(dateInput.value + 'T00:00:00');
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const isToday = selectedDate.getTime() === today.getTime();
    
    // Clear existing options
    timeSelect.innerHTML = '<option value="">Select time slot</option>';
    
    // Generate time slots from 9 AM to 6 PM (business hours)
    const startHour = 9;  // 9 AM
    const endHour = 18;   // 6 PM
    
    let currentHour = new Date().getHours();
    let minHour = isToday ? currentHour + 1 : startHour; // Next hour if today
    
    // Ensure minHour is within business hours
    if (minHour < startHour) minHour = startHour;
    
    // Fetch existing appointments to check booked slots
    fetch('/api/appointments')
        .then(response => response.json())
        .then(data => {
            const bookedSlots = data.appointments
                .filter(apt => apt.date === dateInput.value)
                .map(apt => apt.time);
            
            for (let hour = minHour; hour <= endHour; hour++) {
                const time24 = `${hour.toString().padStart(2, '0')}:00`;
                const time12 = formatTime12Hour(hour);
                
                const option = document.createElement('option');
                option.value = time24;
                
                // Check if slot is booked
                if (bookedSlots.includes(time24)) {
                    option.textContent = `${time12} (Booked)`;
                    option.disabled = true;
                    option.style.color = '#ef4444';
                } else {
                    option.textContent = time12;
                }
                
                timeSelect.appendChild(option);
            }
            
            // If no slots available
            if (timeSelect.options.length === 1) {
                const option = document.createElement('option');
                option.value = '';
                option.textContent = isToday ? 'No more slots today - Select tomorrow' : 'No slots available';
                option.disabled = true;
                timeSelect.appendChild(option);
            }
            
            // Hide refresh indicator
            if (refreshIndicator) {
                refreshIndicator.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error loading appointments:', error);
            // Fallback: show all slots without booking info
            for (let hour = minHour; hour <= endHour; hour++) {
                const time24 = `${hour.toString().padStart(2, '0')}:00`;
                const time12 = formatTime12Hour(hour);
                
                const option = document.createElement('option');
                option.value = time24;
                option.textContent = time12;
                timeSelect.appendChild(option);
            }
        });
}

// Convert 24-hour format to 12-hour format with AM/PM
function formatTime12Hour(hour) {
    if (hour === 0) return '12:00 AM';
    if (hour === 12) return '12:00 PM';
    if (hour < 12) return `${hour}:00 AM`;
    return `${hour - 12}:00 PM`;
}
