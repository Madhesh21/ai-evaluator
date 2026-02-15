# AI Answer Evaluator

An intelligent system designed to automate the evaluation of handwritten answer scripts. This project leverages OCR technology to digitize handwritten text and uses advanced Large Language Models (LLMs) to grade and provide feedback on student answers.

## 🚀 Features

-   **Handwriting Recognition**: Extracts text from images and PDF answer scripts using **EasyOCR**.
-   **AI-Powered Grading**: Evaluates answers against a provided question/key using **Google's Generative AI**.
-   **Multi-Format Support**: Handles both image files (JPG, PNG) and PDF documents.
-   **Modern UI**: A clean, responsive interface built with **Next.js** and **Tailwind CSS**.
-   **Detailed Feedback**: Provides comprehensive feedback and scores for each answer.

##  Tech Stack

### Frontend
-   **Framework**: [Next.js 15](https://nextjs.org/) (App Directory)
-   **Language**: [TypeScript](https://www.typescriptlang.org/)
-   **Styling**: [Tailwind CSS v4](https://tailwindcss.com/)
-   **Markdown Rendering**: `react-markdown`

### Backend
-   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
-   **OCR Engine**: [EasyOCR](https://github.com/JaidedAI/EasyOCR)
-   **AI Model**: [Google Generative AI](https://ai.google.dev/) (Gemini)
-   **PDF Processing**: `pdfplumber`
-   **Image Processing**: `Pillow`

## 🛠️ Installation & Setup

### Prerequisites
-   Node.js & npm
-   Python 3.8+
-   Git

### 1. Clone the Repository
```bash
git clone https://github.com/Madhesh21/ai-evaluator.git
cd ai-evaluator
```
### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```
### 3. Create a .env file in the backend directory with your API keys and run the server
```bash
GOOGLE_API_KEY=your_google_api_key_here
uvicorn main:app --reload
```
The API will differ at http://localhost:8000.

### 4. Frontend Setup
```bash
cd ../frontend
npm install
# Run the server
npm run dev
```
The application will be available at http://localhost:3000.

### Usage
- Open the web application.
- Upload an image or PDF of a handwritten answer script.
- The system will extract the text and display it for verification.
- Submit the extracted text for evaluation to receive a grade and feedback.

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
