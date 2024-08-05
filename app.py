import os
import google.generativeai as genai
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure CORS
CORS(app)

previous_data = """

you're an chatbot designed to help the people who are in distress. you're given with key value 
pairs of data to help you through your objective

(r'I feel (.*)',
     ['I’m sorry to hear that you are feeling . Sometimes it helps to talk about it.']),
    (r'I am feeling (.*)',
     ['It’s important to acknowledge how you’re feeling. Can you tell me more about it?']),
    (r'Can you help me?',
     ['I’m here to listen. What’s been on your mind lately?']),
    (r'I need someone to talk to',
     ['I’m here for you. What would you like to talk about?']),
    (r'thank you',
     ['You’re welcome. I’m glad I could be of help.']),
    (r'quit|bye',
     ['Goodbye! If you need more support, please reach out to a mental health professional.']),
    (r'I’ve been feeling really down lately and can\'t seem to shake it off.',
     ['I’m sorry you’re feeling down. It might help to talk about what’s causing you to feel this way.']),
    (r'I’m having trouble sleeping and it’s affecting my mood.',
     ['Sleep is very important for your mood. Have you tried any techniques to improve your sleep?']),
    (r'I feel so isolated and alone.',
     ['Feeling isolated can be really tough. Do you have anyone you can reach out to for support?']),
    (r'I’ve lost interest in the things I used to love.',
     [
         'Losing interest in activities you once enjoyed can be a sign of depression. Can you think of any small steps to re-engage with those activities?']),
    (r'I can’t stop crying.',
     ['Crying can be a way to release emotions. What do you think is causing you to feel this way?']),
    (r'I feel like a burden to everyone around me.',
     ['You are not a burden. It’s important to reach out for support when you need it.']),
    (r'I\'m constantly anxious and worried.',
     ['Anxiety can be overwhelming. Have you tried any breathing exercises or mindfulness techniques?']),
    (r'I don\'t see a point in anything anymore.',
     [
         'Feeling like there’s no point can be very distressing. Have you talked to a mental health professional about these feelings?']),
    (r'I feel so much pain inside.',
     ['I’m really sorry you’re feeling this way. It might help to talk about what’s causing this pain.']),
    (r'I just want to give up.',
     [
         'Please reach out to a mental health professional immediately. Your life is valuable, and there are people who want to help you through this.']),
    (r'I\'m so tired of pretending to be okay.',
     [
         'It’s exhausting to keep up appearances. It’s okay to not be okay. Would you like to talk about what’s really going on?']),
    (r'I can\'t focus on anything.',
     ['Difficulty concentrating can be a symptom of depression. Are there any small tasks you can start with?']),
    (r'I feel worthless.',
     [
         'You are not worthless. Your feelings are valid, but they do not define your worth. Can we talk about what makes you feel this way?']),

    # Greetings and small talk
    (r'hi|hello',
     ['Hello! How can I assist you today?']),
    (r'bye|goodbye',
     ['Goodbye! Take care and remember that support is available if you need it.']),
    (r'how are you|how r u',
     ['I’m just a program, but I’m here to help you. How are you feeling today?']),

    # Fun activities and jokes
    (r'what can I do for fun?',
     ['How about trying a new hobby? Reading a book, going for a walk, or watching a movie can be enjoyable.']),
    (r'tell me a joke|make me laugh|can you tell me a joke',
     ['Why don’t scientists trust atoms? Because they make up everything!|']),
    (r'what are some fun activities?',
     [
         'You could try drawing, playing a game, or even cooking a new recipe. Sometimes small activities can lift your mood.']),
    (r'I\'m bored',
     ['Boredom can be an opportunity to explore something new. Maybe try a new hobby or learn something online.']),

    # Coping strategies
    (r'How can I cope with stress?',
     ['Stress can be managed with techniques like deep breathing, exercise, or talking to someone you trust.']),
    (r'What are some relaxation techniques?',
     ['You can try meditation, listening to calming music, or taking a warm bath to relax.']),
    (r'I feel overwhelmed',
     ['When feeling overwhelmed, it can help to break tasks into smaller steps and take breaks.']),
    (r'How can I manage my anxiety?',
     ['Managing anxiety might include practices like mindfulness, keeping a journal, or speaking to a therapist.']),

    # General inquiries
    (r'What is your name?',
     ['I’m a chatbot created to assist you. How can I help today?']),
    (r'What do you do?',
     ['I’m here to provide support and answer your questions to the best of my ability.']),
    (r'Where are you from?',
     ['I exist in the digital realm, created to assist and support you.']),

    # Encouragement
    (r'I need motivation',
     ['You can do it! Sometimes taking small steps can lead to big changes.']),
    (r'I feel lost',
     ['Feeling lost is okay. It might help to talk about what’s making you feel this way.']),
    (r'I need a friend',
     ['I’m here for you. What would you like to talk about?']),
    (r'I\'m struggling',
     ['I’m sorry you’re struggling. Sometimes it helps to talk about what’s going on.']),
]
"""

# Configure logging
logging.basicConfig(filename='error.log', level=logging.DEBUG)

# Configure the Google API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyDgTNcfDVLHBHWttnJEVC-hTHfBMt8rKvs'
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Initialize the generative model and chat
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

chat.send_message(previous_data)

@app.route('/')
def hello_world():
    app.logger.debug('Hello world endpoint was called')
    return "Distress Chatbot Home!"

@app.route('/gemini', methods=['POST'])
def gemini_response_chat():
    data = request.json
    app.logger.debug(f'Received data: {data}')
    try:
        query = data.get('query')
        response =  chat.send_message(query)
        app.logger.debug(f'Response from chat: {response.text}')
        return jsonify({'response': response.text})
    except Exception as e:
        app.logger.error(f'Error processing request: {e}')
        return jsonify({'error': str(e)}), 500

# Remove or comment out the app.run() line for PythonAnywhere deployment
if __name__ == "__main__":
    app.run(debug=True)

