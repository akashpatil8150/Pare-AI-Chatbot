from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import json
import random
import datetime
from typing import Dict, List, Any, Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import logging
import sys

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Disable Flask debug mode in production
app.config['DEBUG'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# Configure Gemini API
# Configure Gemini API
api_key = os.getenv('GEMINI_API_KEY', '').strip()
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables!")
    # Don't crash on startup - handle gracefully in routes
    client = None
else:
    logger.info(f"API Key loaded successfully (length: {len(api_key)} characters)")
    try:
        client = genai.Client(api_key=api_key)
        logger.info("Gemini API configured successfully")
    except Exception as e:
        logger.error(f"Failed to configure Gemini API: {str(e)}")
        client = None

# Global Data Storage
APPOINTMENTS: List[Dict] = []

# Ultra-optimized System Prompt
SYSTEM_PROMPT = '''Pare AI for interior/exterior.

Products: INNOV+ (waterproof), INNOV2+ (3D walls), DURA+ (exterior), EASY+ (easy install), LUXE (premium), Acoustic (sound).

Rules: Products only. English/Hindi. Hours: 9-18. JSON: {"type":"message","content":"text","language":"en"}

Tools: book_appointment(name,address,date,time), cancel_appointment(id)

Brief answers only.'''

MODEL_NAME = "gemini-2.0-flash"

GENERATION_CONFIG = types.GenerateContentConfig(
    temperature=0.2,
    top_p=0.8,
    top_k=5,
    max_output_tokens=100,
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
    """Main chat function using new google-genai SDK"""
    if not client:
        return {"type": "error", "content": "API key not configured. Please set GEMINI_API_KEY.", "language": "en"}
    try:
        logger.info(f"Processing chat request: {user_input[:50]}...")
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}\n\nAssistant:"

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt,
            config=GENERATION_CONFIG,
        )

        if not response.text:
            logger.warning("Empty response from Gemini")
            return {
                "type": "error",
                "content": "No response generated. Please try again.",
                "language": "en"
            }

        response_text = response.text.strip()
        processed_response = process_tool_call(response_text)
        logger.info("Chat request processed successfully")
        return processed_response

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Chat error: {error_msg}")
        if "429" in error_msg or "quota" in error_msg.lower():
            return {"type": "error", "content": "API quota exceeded. Please wait and try again.", "language": "en"}
        elif "timeout" in error_msg.lower() or "deadline" in error_msg.lower():
            return {"type": "error", "content": "Response too slow. Try a shorter question.", "language": "en"}
        else:
            return {"type": "error", "content": f"Error: {error_msg}", "language": "en"}

def chat_stream(user_input: str):
    """Streaming chat function using new google-genai SDK"""
    if not client:
        yield f"data: {json.dumps({'done': True, 'result': {'type': 'error', 'content': 'API key not configured. Please set GEMINI_API_KEY.', 'language': 'en'}})}\n\n"
        return
    try:
        logger.info(f"Processing streaming chat request: {user_input[:50]}...")
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_input}\n\nAssistant:"

        accumulated_text = ""
        for chunk in client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=full_prompt,
            config=GENERATION_CONFIG,
        ):
            if chunk.text:
                accumulated_text += chunk.text
                yield f"data: {json.dumps({'chunk': chunk.text})}\n\n"

        if accumulated_text:
            processed = process_tool_call(accumulated_text)
            yield f"data: {json.dumps({'done': True, 'result': processed})}\n\n"
            logger.info("Streaming chat request completed successfully")
        else:
            yield f"data: {json.dumps({'done': True, 'result': {'type': 'error', 'content': 'No response generated.', 'language': 'en'}})}\n\n"
            logger.warning("Streaming chat generated no response")

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Streaming chat error: {error_msg}")
        if "429" in error_msg or "quota" in error_msg.lower():
            content = "API quota exceeded. Please wait and try again."
        elif "timeout" in error_msg.lower() or "deadline" in error_msg.lower():
            content = "Response too slow. Try a shorter question."
        else:
            content = f"Error: {error_msg}"
        yield f"data: {json.dumps({'done': True, 'result': {'type': 'error', 'content': content, 'language': 'en'}})}\n\n"

# Routes
@app.route('/')
def index():
    logger.info("Index page accessed")
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Pare AI Chatbot",
        "api_configured": client is not None,
        "timestamp": datetime.datetime.now().isoformat()
    }), 200

@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        use_streaming = data.get('stream', False)
        
        if not user_message:
            return jsonify({"type": "error", "content": "Message is required"}), 400
        
        if use_streaming:
            return Response(
                stream_with_context(chat_stream(user_message)),
                mimetype='text/event-stream'
            )
        else:
            response = chat(user_message)
            return jsonify(response)
    except Exception as e:
        logger.error(f"API chat error: {str(e)}")
        return jsonify({
            "type": "error",
            "content": "An error occurred processing your request"
        }), 500

@app.route('/api/appointments', methods=['GET'])
def api_appointments():
    try:
        return jsonify({"appointments": view_appointments()})
    except Exception as e:
        logger.error(f"API appointments error: {str(e)}")
        return jsonify({"error": "Failed to fetch appointments"}), 500

@app.route('/api/appointments/book', methods=['POST'])
def api_book_appointment():
    try:
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
        
        logger.info(f"Appointment booked: {result.get('appointment_id')}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"API book appointment error: {str(e)}")
        return jsonify({"status": "error", "message": "Failed to book appointment"}), 500

@app.route('/api/appointments/cancel', methods=['POST'])
def api_cancel_appointment():
    try:
        data = request.json
        result = cancel_appointment(appointment_id=data.get('appointment_id'))
        logger.info(f"Appointment cancelled: {data.get('appointment_id')}")
        return jsonify(result)
    except Exception as e:
        logger.error(f"API cancel appointment error: {str(e)}")
        return jsonify({"status": "error", "message": "Failed to cancel appointment"}), 500

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Hugging Face Spaces requires port 7860
    # Render uses $PORT env variable
    # Local dev defaults to 5000
    port = int(os.getenv('PORT', 7860))

    logger.info(f"Starting Pare AI Chatbot on port {port}")
    logger.info(f"Environment: {'Production' if not app.config['DEBUG'] else 'Development'}")

    app.run(host='0.0.0.0', port=port, debug=False)
