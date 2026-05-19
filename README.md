---
title: Pare AI Chatbot
emoji: 🏢
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# Pare AI Chatbot 🏢

An intelligent AI-powered chatbot for Pare Interior & Exterior Solutions. Built with Flask and Google Gemini AI, this chatbot helps customers learn about products and book appointments with real-time slot management.

## Features ✨

- **AI-Powered Chat**: Intelligent responses about Pare products using Google Gemini AI
- **Product Information**: Detailed info about 6 product series (INNOV+, INNOV2+, DURA+, EASY+, LUXE, Acoustic)
- **Smart Appointment Booking**: 
  - Book via chat or direct UI
  - Time slots: 9 AM - 6 PM in 1-hour intervals
  - Real-time slot availability checking
  - Prevents double bookings
  - Auto-refresh every 5 seconds when booking modal is open
- **Bilingual Support**: English and Hindi language support
- **Real-time Validation**: 
  - Business hours enforcement (9 AM - 6 PM only)
  - Full hour slots only (no 9:30, 10:15, etc.)
  - Date format normalization
- **Usage Tracking**: Monitor API quota usage in real-time
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations

## Product Series 📦

1. **INNOV+**: Waterproof, termite-proof wood-look interiors
2. **INNOV2+**: 3D textured walls (Wave, Dome, Stripes, Prism)
3. **DURA+**: UV-resistant exterior cladding (Norma, Stretta)
4. **EASY+**: Direct installation without plywood
5. **LUXE**: Premium dead-matt finish (Panelo, Flut, Verto)
6. **Acoustic**: Sound absorption with louver design

## Tech Stack 🛠️

- **Backend**: Flask (Python 3.8+)
- **AI**: Google Gemini API (gemini-flash-lite-latest)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Custom CSS with modern design patterns
- **Icons**: Font Awesome 6.4.0
- **Environment**: python-dotenv for secure config

## Key Features in Detail 🔍

### Smart Appointment System
- **Dual Booking Methods**: Book via AI chat or direct UI form
- **Time Slot Management**:
  - Business hours: 9:00 AM to 6:00 PM
  - 1-hour intervals only (9:00, 10:00, 11:00, etc.)
  - No partial hours (9:30, 10:15 rejected)
- **Real-time Sync**: 
  - Chat bookings instantly reflect in UI
  - Auto-refresh every 5 seconds when modal is open
  - Visual indicators for booked slots
- **Validation**:
  - Backend validates all time slots
  - Prevents bookings outside business hours
  - Checks for duplicate bookings
  - Date format normalization (YYYY-MM-DD internally)

### Usage Tracking
- **Request Counter**: Shows current API usage (X/60 requests per minute)
- **Color Coding**: Green (safe), Red (near limit)
- **Auto-reset**: Counter resets every 60 seconds
- **Detailed Stats**: Click info icon for full usage breakdown
- **Quota Monitoring**: Direct link to Google's quota dashboard

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get it here](https://aistudio.google.com/app/apikey))

### Setup Steps

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Pare_chatbot
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**
```bash
# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install flask flask-cors google-generativeai python-dotenv
```

5. **Configure API key**

Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_api_key_here
```

6. **Run the application**
```bash
python app.py
```

7. **Open in browser**
```
http://localhost:5000
```

## Project Structure 📁

```
Pare_chatbot/
├── app.py                  # Main Flask application
├── .env                    # Environment variables (API key)
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css      # Styling
│   └── js/
│       └── script.js      # Frontend logic
└── venv/                  # Virtual environment (not in git)
```

## Usage 💬

### Chat with AI
- Type your questions about Pare products
- Click product buttons in sidebar for quick info
- Get instant AI-powered responses in English or Hindi
- Ask in Hindi: "INNOV+ के बारे में बताओ"

### Book Appointments

#### Method 1: Via Chat
```
User: "I want to book an appointment"
Bot: "Sure! Please provide your name, address, date, and time."
User: "Name: John Doe, Address: 123 Main St, Date: tomorrow, Time: 2 PM"
Bot: *Creates appointment with validation*
```

**Chat Booking Rules:**
- AI validates time slots (9 AM - 6 PM only)
- Rejects invalid times (8 AM, 9:30 AM, 7 PM, etc.)
- Checks for duplicate bookings
- Provides helpful error messages

#### Method 2: Direct UI
1. Click "Book Appointment" button
2. Fill in your details (Name, Address)
3. Select date from calendar
4. Choose from available time slots
   - Booked slots show as "(Booked)" and are disabled
   - Only valid hours (9 AM - 6 PM) are shown
5. Confirm booking
6. Receive appointment confirmation with unique ID

**UI Features:**
- Auto-selects tomorrow if past business hours
- Real-time slot availability
- Auto-refresh every 5 seconds
- Visual "Updating..." indicator

### View & Manage Appointments
- Click "View Appointments" to see all bookings
- Each appointment shows:
  - Unique ID (APT-XXXX)
  - Name, Address, Date, Time
  - Cancel button
- Cancel appointments with confirmation
- Canceled slots become available immediately

## Features in Detail 🔍

### Smart Time Slot Management
- **1-hour intervals**: 9:00 AM, 10:00 AM, 11:00 AM, etc.
- **Business hours**: 9 AM - 6 PM
- **Real-time availability**: Shows only available slots
- **Auto-date selection**: Defaults to tomorrow if past business hours
- **Double-booking prevention**: Validates before confirming

### AI Capabilities
- Product recommendations
- Detailed product information
- Bilingual responses (English/Hindi)
- Appointment booking via chat
- JSON-formatted responses

## API Endpoints 🔌

### Chat
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Tell me about INNOV+ series"
}

Response:
{
  "type": "message",
  "content": "INNOV+ is a waterproof, termite-proof...",
  "language": "en",
  "usage": {
    "request_count": 1,
    "timestamp": "2026-02-10T20:30:00"
  }
}
```

### Book Appointment
```http
POST /api/appointments/book
Content-Type: application/json

{
  "name": "John Doe",
  "address": "123 Main St",
  "date": "2026-02-11",
  "time": "14:00"
}

Success Response (200):
{
  "status": "confirmed",
  "appointment_id": "APT-1234",
  "name": "John Doe",
  "address": "123 Main St",
  "date": "2026-02-11",
  "time": "14:00",
  "created_at": "2026-02-10T20:30:00"
}

Error Response (400):
{
  "status": "error",
  "message": "Time slot 14:00 on 2026-02-11 is already booked."
}
```

### View Appointments
```http
GET /api/appointments

Response:
{
  "appointments": [
    {
      "appointment_id": "APT-1234",
      "name": "John Doe",
      "address": "123 Main St",
      "date": "2026-02-11",
      "time": "14:00",
      "status": "confirmed",
      "created_at": "2026-02-10T20:30:00"
    }
  ]
}
```

### Cancel Appointment
```http
POST /api/appointments/cancel
Content-Type: application/json

{
  "appointment_id": "APT-1234"
}

Response:
{
  "status": "cancelled",
  "appointment_id": "APT-1234",
  "message": "Appointment successfully cancelled"
}
```

### Usage Statistics
```http
GET /api/usage

Response:
{
  "total_appointments": 5,
  "free_tier_limit": "60 requests/minute",
  "recommendation": "Monitor at https://ai.dev/rate-limit",
  "current_model": "gemini-flash-lite-latest"
}
```

## Configuration ⚙️

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Model Configuration
Current model: `gemini-flash-lite-latest`
- Temperature: 0.7
- Max output tokens: 512
- Timeout: 30 seconds
- Retry logic: 2 attempts on timeout

To change model, edit `app.py`:
```python
model = genai.GenerativeModel(
    "models/gemini-flash-lite-latest",  # Change model here
    generation_config={...}
)
```

### Business Hours
Default: 9 AM - 6 PM (1-hour slots)

To change, edit `static/js/script.js`:
```javascript
const startHour = 9;  // Change start hour (24-hour format)
const endHour = 18;   // Change end hour (24-hour format)
```

Also update `app.py` validation:
```python
def validate_time_slot(time: str) -> tuple[bool, str]:
    # Check business hours (9 AM to 6 PM)
    if hour < 9 or hour > 18:  # Change these values
        return False, "Appointments are available only from 9:00 AM to 6:00 PM."
```

### Auto-refresh Interval
Default: 5 seconds

To change, edit `static/js/script.js`:
```javascript
window.timeSlotsRefreshInterval = setInterval(() => {
    // ...
}, 5000); // Change milliseconds (5000 = 5 seconds)
```

## Troubleshooting 🔧

### API Key Issues
- Ensure `.env` file exists with valid API key
- Check API key at: https://aistudio.google.com/app/apikey
- Verify no quotes around the key in `.env`
- Format: `GEMINI_API_KEY=AIzaSyC...` (no quotes)

### Quota Exceeded (429 Error)
**Error**: "You exceeded your current quota"
- **Cause**: Hit free tier limit (60 requests/minute)
- **Solution**: 
  - Wait 1 minute for quota reset
  - Check usage: https://ai.dev/rate-limit
  - Monitor with built-in usage tracker (top-right corner)
  - Consider upgrading API plan

### Timeout Errors (504)
**Error**: "Deadline expired before operation could complete"
- **Cause**: API is slow or overloaded
- **Solution**:
  - Retry after a few seconds
  - Check internet connection
  - Try different model (gemini-2.0-flash)
  - Increase timeout in `app.py`

### Invalid Time Slot
**Error**: "Appointments are available only from 9:00 AM to 6:00 PM"
- **Cause**: Requested time outside business hours or not full hour
- **Valid times**: 09:00, 10:00, 11:00, 12:00, 13:00, 14:00, 15:00, 16:00, 17:00, 18:00
- **Invalid times**: 08:00, 09:30, 10:15, 19:00, etc.

### Slot Already Booked
**Error**: "Time slot X on Y is already booked"
- **Cause**: Someone else booked that slot
- **Solution**: 
  - Choose different time
  - Refresh booking modal to see updated slots
  - Check "View Appointments" to see all bookings

### Date Format Issues
- Backend stores: `YYYY-MM-DD` (2026-02-11)
- Display shows: `DD-MM-YYYY` (11-02-2026)
- AI accepts both formats, automatically normalized

### Port Already in Use
```bash
# Change port in app.py
app.run(debug=True, port=5001)  # Use different port
```

### Slots Not Refreshing
- Check browser console for errors (F12)
- Ensure `/api/appointments` endpoint is working
- Hard refresh: `Ctrl + Shift + R`
- Clear browser cache

## Security 🔒

- API key stored in `.env` (not in code)
- `.gitignore` prevents committing secrets
- Input validation on appointments
- CORS enabled for API access

## Future Enhancements 🚀

- [ ] Database integration (SQLite/PostgreSQL) for persistent storage
- [ ] User authentication and login system
- [ ] Email/SMS notifications for appointments
- [ ] Admin dashboard for managing bookings
- [ ] Payment integration for booking fees
- [ ] Multi-language support expansion (Spanish, French, etc.)
- [ ] Voice input/output capabilities
- [ ] Image upload for product queries
- [ ] Calendar integration (Google Calendar, Outlook)
- [ ] Appointment reminders (24 hours before)
- [ ] Customer feedback and ratings
- [ ] Analytics dashboard (booking trends, popular times)
- [ ] Waiting list for fully booked slots
- [ ] Recurring appointments
- [ ] Export appointments to CSV/PDF

## Recent Updates 📝

### v1.2.0 (Latest)
- ✅ Added usage tracking with real-time counter
- ✅ Implemented auto-refresh for time slots (5-second interval)
- ✅ Added date format normalization (YYYY-MM-DD)
- ✅ Enhanced validation for business hours
- ✅ Improved error messages for quota/timeout issues
- ✅ Added visual indicators for slot updates

### v1.1.0
- ✅ Dual booking methods (Chat + Direct UI)
- ✅ Real-time slot synchronization
- ✅ Duplicate booking prevention
- ✅ Time slot validation (9 AM - 6 PM, full hours only)

### v1.0.0
- ✅ Initial release
- ✅ AI-powered chat with Gemini
- ✅ Basic appointment booking
- ✅ Bilingual support (English/Hindi)

## Contributing 🤝

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License.


## Acknowledgments 🙏

- Google Gemini AI for powering the chatbot
- Flask framework for backend
- Font Awesome for icons
- Pare for product information

---
**project purpose only**
