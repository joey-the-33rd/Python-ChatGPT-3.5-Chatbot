# Python + ChatGPT-3.5 Chatbot Project

## Project Overview

This project is a chatbot application that integrates OpenAI's GPT-3.5 model. It consists of three main components:

- **Flask Backend:** A web server providing REST API endpoints for user registration, login, and chat functionality. It uses OpenAI's API to generate chatbot responses.
- **CLI Chatbot:** A command-line interface chatbot that allows users to interact with the GPT-3.5 model directly from the terminal.
- **React Frontend:** A React-based user interface (located in the `frontend/` directory) that interacts with the Flask backend to provide a web-based chat experience.

## Features

- User registration and login with in-memory user storage (for demonstration purposes).
- Chat endpoint that maintains conversation context and generates responses using OpenAI GPT-3.5.
- CLI chatbot for direct terminal interaction with the GPT-3.5 model.
- React frontend for a modern web chat interface.
- Environment variable support for OpenAI API key.
- CORS enabled for frontend-backend communication.

## Project Structure

```
.
├── app.py                  # Flask backend application
├── chatbot.py              # CLI chatbot script
├── frontend/               # React frontend application
│   ├── README.md           # Frontend-specific README (Create React App default)
│   ├── package.json
│   └── src/                # React source code
├── requirements.txt        # Python dependencies for backend
├── requirements-dev.txt    # Development dependencies
├── LICENSE                 # License file
├── README.md               # This file
└── ...                     # Other configuration and support files
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Node.js and npm (for frontend)
- OpenAI API key (set in environment variable `OPENAI_API_KEY`)

### Backend Setup

1. Create and activate a Python virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Run the Flask backend server:

   ```bash
   python app.py
   ```

   The backend server will start on `http://127.0.0.1:5000`.

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install frontend dependencies:

   ```bash
   npm install
   ```

3. Start the React development server:

   ```bash
   npm start
   ```

   The frontend will be available at `http://localhost:3000`.

### CLI Chatbot Setup

1. Ensure your Python environment has the dependencies installed (same as backend).

2. Run the CLI chatbot:

   ```bash
   python chatbot.py
   ```

3. Type your messages and interact with the chatbot in the terminal. Type `exit` or `quit` to end the session.

## Usage

- Use the React frontend to register, login, and chat with the GPT-3.5 powered assistant.
- Alternatively, use the CLI chatbot for quick terminal-based interaction.
- The backend API can be extended or integrated with other clients as needed.

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

---

For frontend-specific details and commands, please refer to the `frontend/README.md` file.
