"use client";

import { useState } from "react";

export default function Home() {
  const [qpFile, setQpFile] = useState<File | null>(null);
  const [ansFile, setAnsFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>, type: "qp" | "ans") => {
    if (e.target.files && e.target.files[0]) {
      if (type === "qp") setQpFile(e.target.files[0]);
      else setAnsFile(e.target.files[0]);
    }
  };

  const uploadFile = async (file: File, docType: string) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("doc_type", docType);

    const res = await fetch("http://localhost:8000/api/process-document", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      throw new Error(`Failed to upload ${docType}`);
    }
    return res.json();
  };

  const handleEvaluate = async () => {
    if (!qpFile || !ansFile) {
      setError("Please upload both Question Paper and Answer Script.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      // For Module 1, we just test text extraction
      const qpResult = await uploadFile(qpFile, "question_paper");
      const ansResult = await uploadFile(ansFile, "answer_script");

      setResult({
        question_paper: qpResult,
        answer_script: ansResult
      });
    } catch (err: any) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans">
      <header className="bg-blue-600 text-white p-6 shadow-md">
        <h1 className="text-3xl font-bold text-center">AI Answer Evaluator</h1>
        <p className="text-center mt-2 opacity-90">Module 1: Input Processing & OCR</p>
      </header>

      <main className="max-w-4xl mx-auto p-8">
        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {/* Question Paper Upload */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h2 className="text-xl font-semibold mb-4 text-blue-800">1. Question Paper</h2>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors">
              <input
                type="file"
                onChange={(e) => handleFileChange(e, "qp")}
                accept=".pdf,.png,.jpg,.jpeg"
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              />
              <p className="mt-2 text-sm text-gray-400">Upload PDF or Image</p>
            </div>
            {qpFile && <p className="mt-2 text-green-600 font-medium">Selected: {qpFile.name}</p>}
          </div>

          {/* Answer Script Upload */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h2 className="text-xl font-semibold mb-4 text-green-800">2. Answer Script</h2>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-green-500 transition-colors">
              <input
                type="file"
                onChange={(e) => handleFileChange(e, "ans")}
                accept=".pdf,.png,.jpg,.jpeg"
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
              />
              <p className="mt-2 text-sm text-gray-400">Upload PDF or Image</p>
            </div>
            {ansFile && <p className="mt-2 text-green-600 font-medium">Selected: {ansFile.name}</p>}
          </div>
        </div>

        <div className="text-center mb-12">
          <button
            onClick={handleEvaluate}
            disabled={loading}
            className={`px-8 py-3 rounded-lg text-white font-bold text-lg shadow-lg transition-transform transform hover:scale-105 ${loading ? "bg-gray-400 cursor-not-allowed" : "bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"}`}
          >
            {loading ? "Processing..." : "Process Documents"}
          </button>
          {error && <p className="mt-4 text-red-500 font-semibold">{error}</p>}
        </div>

        {/* Results Display */}
        {result && (
          <div className="space-y-8 animate-fade-in-up">
            <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-blue-500">
              <h3 className="text-lg font-bold mb-2">Question Paper Extraction</h3>
              <pre className="bg-gray-100 p-4 rounded text-xs overflow-auto max-h-40 whitespace-pre-wrap">
                {result.question_paper.extracted_text}
              </pre>
              <div className="mt-4">
                <ExtractionSection text={result.question_paper.extracted_text} />
              </div>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-green-500">
              <h3 className="text-lg font-bold mb-2">Answer Script Extraction</h3>
              <AnswerScriptViewer text={result.answer_script.extracted_text} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

import ReactMarkdown from 'react-markdown';

function ExtractionSection({ text }: { text: string }) {
  const [questions, setQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState<any>(null);

  const extractQuestions = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/extract-questions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      setQuestions(data.questions);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button
        onClick={extractQuestions}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-blue-700 disabled:bg-gray-400"
      >
        {loading ? "Extracting..." : "Extract Questions (Module 2)"}
      </button>

      {questions.length > 0 && (
        <div className="mt-6 grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          {questions.map((q) => (
            <div
              key={q.id}
              onClick={() => setSelectedQuestion(q)}
              className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 cursor-pointer hover:shadow-md hover:border-blue-300 transition-all group"
            >
              <div className="flex justify-between items-start mb-2">
                <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-0.5 rounded">Q{q.id}</span>
                <span className="text-gray-400 text-xs group-hover:text-blue-500">View Details &rarr;</span>
              </div>
              <h5 className="font-semibold text-gray-800 text-sm line-clamp-3 mb-3">{q.question}</h5>
              <div className="flex gap-2 flex-wrap">
                <span className="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">Marks: {q.marks}</span>
                <span className="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">{q.co}</span>
                <span className="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">{q.bl}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal for Detailed View */}
      {selectedQuestion && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 backdrop-blur-sm animate-fade-in-up">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col">
            {/* Modal Header */}
            <div className="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
              <div className="flex items-center gap-3">
                <span className="bg-blue-600 text-white text-sm font-bold px-3 py-1 rounded-full">Q{selectedQuestion.id}</span>
                <div className="flex gap-2">
                  <span className="bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded font-medium">Marks: {selectedQuestion.marks}</span>
                  <span className="bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded font-medium">{selectedQuestion.co}</span>
                </div>
              </div>
              <button
                onClick={() => setSelectedQuestion(null)}
                className="text-gray-400 hover:text-gray-600 hover:bg-gray-200 p-2 rounded-full transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-8 overflow-y-auto">
              <h3 className="text-xl font-bold text-gray-800 mb-6 leading-relaxed">{selectedQuestion.question}</h3>

              <div className="bg-gray-50 p-6 rounded-xl border border-gray-200">
                <GenerateAnswerSection question={selectedQuestion.question} marks={selectedQuestion.marks} />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function GenerateAnswerSection({ question, marks }: { question: string, marks: string }) {
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/generate-answers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: question, marks }),
      });
      const data = await res.json();
      setAnswer(data.ideal_answer);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h4 className="font-bold text-gray-700">Ideal Answer</h4>
        {!answer && (
          <button
            onClick={generate}
            disabled={loading}
            className="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-indigo-700 transition-colors shadow-sm disabled:opacity-50"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating...
              </>
            ) : "Generate Answer with AI"}
          </button>
        )}
      </div>

      {answer && (
        <div className="prose prose-blue max-w-none">
          <ReactMarkdown>{answer}</ReactMarkdown>
        </div>
      )}

      {!answer && !loading && (
        <div className="text-gray-400 text-sm italic text-center py-8">
          Click the button above to generate a model answer using Gemini AI.
        </div>
      )}
    </div>
  );
}

function AnswerScriptViewer({ text }: { text: string }) {
  const [showModal, setShowModal] = useState(false);

  return (
    <div>
      <div className="relative">
        <pre className="bg-gray-100 p-4 rounded text-xs overflow-hidden max-h-40 whitespace-pre-wrap opacity-75">
          {text.slice(0, 500)}...
        </pre>
        <div className="absolute inset-x-0 bottom-0 h-20 bg-gradient-to-t from-white to-transparent"></div>
        <div className="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity bg-white/30 backdrop-blur-[1px]">
          <button
            onClick={() => setShowModal(true)}
            className="bg-green-600 text-white px-6 py-2 rounded-full font-bold shadow-lg hover:scale-105 transition-transform"
          >
            View Full Script
          </button>
        </div>
      </div>

      <div className="mt-4 text-center">
        <button
          onClick={() => setShowModal(true)}
          className="text-green-700 text-sm font-semibold hover:underline"
        >
          View Full Answer Script ({text.length} chars)
        </button>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 backdrop-blur-sm animate-fade-in-up">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
            <div className="p-6 border-b border-gray-100 flex justify-between items-center bg-green-50">
              <h3 className="text-xl font-bold text-green-800">Full Answer Script</h3>
              <button
                onClick={() => setShowModal(false)}
                className="text-gray-400 hover:text-gray-600 hover:bg-gray-200 p-2 rounded-full transition-colors"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="p-8 overflow-y-auto bg-gray-50">
              <pre className="whitespace-pre-wrap text-sm font-mono text-gray-700 bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
                {text}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
