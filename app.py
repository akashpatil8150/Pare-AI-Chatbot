from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import json
import random
import datetime
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found! Please set it in .env file")

# Debug: Print first/last few characters (for verification without exposing full key)
print(f"API Key loaded: {api_key[:10]}...{api_key[-4:]}")
print(f"API Key length: {len(api_key)}")

genai.configure(api_key=api_key)

# Global Data Storage
APPOINTMENTS: List[Dict] = []

# Ultra-optimized System Prompt
SYSTEM_PROMPT = '''Pare AI for interior/exterior.

Products: INNOV+ (waterproof), INNOV2+ (3D walls), DURA+ (exterior), EASY+ (easy install), LUXE (premium), Acoustic (sound).

Rules: Products only. English/Hindi. Hours: 9-18. JSON: {"type":"message","content":"text","language":"en"}

Tools: book_appointment(name,address,date,time), cancel_appointment(id)

Brief answers only.'''

model = genai.GenerativeModel(
    "models/gemini-flash-lite-latest",
    generation_config={
        "temperature": 0.2,  # Very low for fastest responses
        "top_p": 0.8,
        "top_k": 5,  # Minimal choices for speed
        "max_output_tokens": 100,  # Very short responses
    }
)

# Tool Functions
def validate_time_slot(time: str) -> tuple[bool, str]:
    """Validate if time slot is within business hours and in correct format"""
    try:
        # Parse time
        hour, minute = map(int, time.split(':'))
        
        # Check if minutes are 00 (only full hours allowed)
        if minute != 0:
            return False, "Appointments are only available on the hour (e.g., 9:00, 10:00, 11:00). Please choose a valid slot."
        
        # Check business hours (9 AM to 6 PM)
        if hour < 9 or hour > 18:
            return False, "Appointments are available only from 9:00 AM to 6:00 PM. Please choose a valid slot."
        
        return True, "Valid time slot"
    except:
        return False, "Invalid time format. Please use HH:MM format (e.g., 10:00, 14:00)."

def book_appointment(name: str, address: str, date: str, time: str) -> Dict[str, Any]:
    """Book a new appointment with validation"""
    
    # Normalize date format to YYYY-MM-DD
    try:
        # Try parsing different date formats
        if '-' in date:
            parts = date.split('-')
            if len(parts[0]) == 4:  # Already YYYY-MM-DD
                normalized_date = date
            else:  # DD-MM-YYYY format
                normalized_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
        else:
            normalized_date = date
    except:
        return {
            "status": "error",
            "message": "Invalid date format. Please use YYYY-MM-DD format."
        }
    
    # Validate time slot
    is_valid, message = validate_time_slot(time)
    if not is_valid:
        return {
            "status": "error",
            "message": message
        }
    
    # Check if slot is already booked
    for apt in APPOINTMENTS:
        if apt["date"] == normalized_date and apt["time"] == time:
            return {
                "status": "error",
                "message": f"Time slot {time} on {normalized_date} is already booked. Please choose another time."
            }
    
    # Create appointment
    apt_id = f"APT-{random.randint(1000, 9999)}"
    appointment_data = {
        "status": "confirmed",
        "appointment_id": apt_id,
        "name": name,
        "address": address,
        "date": normalized_date,  # Store in YYYY-MM-DD format
        "time": time,
        "created_at": datetime.datetime.now().isoformat()
    }
    APPOINTMENTS.append(appointment_data)
    return appointment_data

def cancel_appointment(appointment_id: str) -> Dict[str, Any]:
    """Cancel an existing appointment"""
    global APPOINTMENTS
    original_count = len(APPOINTMENTS)
    APPOINTMENTS = [a for a in APPOINTMENTS if a["appointment_id"] != appointment_id]
    
    if len(APPOINTMENTS) < original_count:
        return {
            "status": "cancelled",
            "appointment_id": appointment_id,
            "message": "Appointment successfully cancelled"
        }
    else:
        return {
            "status": "not_found",
            "appointment_id": appointment_id,
            "message": "Appointment not found"
        }

def view_appointments() -> List[Dict[str, Any]]:
    """View all appointments"""
    return APPOINTMENTS

def process_tool_call(response_text: str) -> Optional[Dict[str, Any]]:
    """Process tool calls from the AI response"""
    try:
        if response_text.startswith('```json') and response_text.endswith('```'):
            response_text = response_text.lstrip('```json').rstrip('```').strip()
        
        response_json = json.loads(response_text)
        
        if response_json.get("type") == "tool_call":
            function_name = response_json.get("name")
            args = response_json.get("args", {})
            
            if function_name == "book_appointment":
                result = book_appointment(
                    name=args.get("name"),
                    address=args.get("address"),
                    date=args.get("date"),
                    time=args.get("time")
                )
                
                # Check if booking failed due to validation
                if result.get("status") == "error":
                    return {
                        "type": "message",
                        "content": result.get("message"),
                        "language": "en"
                    }
                
                return {
                    "type": "appointment_result",
                    "status": "confirmed",
                    "details": result
                }
            
            elif function_name == "cancel_appointment":
                result = cancel_appointment(
                    appointment_id=args.get("appointment_id")
                )
                return {
                    "type": "appointment_result",
                    "status": result["status"],
                    "details": result
                }
        
        return response_json
    
    except json.JSONDecodeError:
        return {
            "type": "error",
            "content": "Invalid response format",
            "raw_response": response_text
        }

def chat(user_input: str) -> Dict[str, Any]:
    """Main chat function with optimized timeout"""
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}\n\nAssistant:"
        
        # Single attempt with very short timeout for speed
        response = model.generate_content(
            full_prompt,
            request_options={"timeout": 10}
        )
        
        # Better response handling
        if not response.candidates:
            return {
                "type": "error",
                "content": "No response generated. Please try again.",
                "language": "en"
            }
        
        candidate = response.candidates[0]
        
        # Check if response was blocked or empty
        if not candidate.content or not candidate.content.parts:
            return {
                "type": "error",
                "content": "Response blocked or empty. Please rephrase your question.",
                "language": "en"
            }
        
        response_text = candidate.content.parts[0].text.strip()
        processed_response = process_tool_call(response_text)
        return processed_response
                
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            return {
                "type": "error",
                "content": "API quota exceeded. Please wait and try again.",
                "language": "en"
            }
        elif "504" in error_msg or "deadline" in error_msg.lower() or "timeout" in error_msg.lower():
            return {
                "type": "error",
                "content": "Response too slow. Try a shorter question or wait a moment.",
                "language": "en"
            }
        else:
            return {
                "type": "error",
                "content": f"Error: {error_msg}",
                "language": "en"
            }

def chat_stream(user_input: str):
    """Streaming chat function for real-time responses"""
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}\n\nAssistant:"
        
        response = model.generate_content(
            full_prompt,
            stream=True,
            request_options={"timeout": 10}
        )
        
        accumulated_text = ""
        for chunk in response:
            if chunk.candidates and chunk.candidates[0].content.parts:
                text = chunk.candidates[0].content.parts[0].text
                if text:
                    accumulated_text += text
                    yield f"data: {json.dumps({'chunk': text})}\n\n"
        
        # Process complete response for tool calls
        if accumulated_text:
            processed = process_tool_call(accumulated_text)
            yield f"data: {json.dumps({'done': True, 'result': processed})}\n\n"
        else:
            error_response = {
                "type": "error",
                "content": "No response generated. Please try again.",
                "language": "en"
            }
            yield f"data: {json.dumps({'done': True, 'result': error_response})}\n\n"
                
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            error_response = {
                "type": "error",
                "content": "API quota exceeded. Please wait and try again.",
                "language": "en"
            }
        elif "504" in error_msg or "deadline" in error_msg.lower() or "timeout" in error_msg.lower():
            error_response = {
                "type": "error",
                "content": "Response too slow. Try a shorter question or wait a moment.",
                "language": "en"
            }
        else:
            error_response = {
                "type": "error",
                "content": f"Error: {error_msg}",
                "language": "en"
            }
        yield f"data: {json.dumps({'done': True, 'result': error_response})}\n\n"

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    user_message = data.get('message', '')
    use_streaming = data.get('stream', False)
    
    if use_streaming:
        return Response(
            stream_with_context(chat_stream(user_message)),
            mimetype='text/event-stream'
        )
    else:
        response = chat(user_message)
        return jsonify(response)

@app.route('/api/appointments', methods=['GET'])
def api_appointments():
    return jsonify({"appointments": view_appointments()})

@app.route('/api/appointments/book', methods=['POST'])
def api_book_appointment():
    data = request.json
    result = book_appointment(
        name=data.get('name'),
        address=data.get('address'),
        date=data.get('date'),
        time=data.get('time')
    )
    
    # Return appropriate status code
    if result.get('status') == 'error':
        return jsonify(result), 400
    
    return jsonify(result)

@app.route('/api/appointments/cancel', methods=['POST'])
def api_cancel_appointment():
    data = request.json
    result = cancel_appointment(appointment_id=data.get('appointment_id'))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
