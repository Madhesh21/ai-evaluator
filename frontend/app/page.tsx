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
                <ExtractionSection
                  qpText={result.question_paper.extracted_text}
                  ansText={result.answer_script.extracted_text}
                />
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

function ExtractionSection({ qpText, ansText }: { qpText: string, ansText: string }) {
  const [questions, setQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState<any>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [evaluationResults, setEvaluationResults] = useState<any[]>([]);
  const [evaluating, setEvaluating] = useState(false);

  const extractQuestions = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/extract-questions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: qpText }),
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        alert(`Failed to extract questions: ${errData.detail || res.statusText}`);
        return;
      }
      const data = await res.json();
      setQuestions(data.questions || []);
    } catch (e) {
      console.error(e);
      alert("Error extracting questions.");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateAnswer = (id: string, text: string) => {
    setAnswers(prev => ({ ...prev, [id]: text }));
  };

  const runEvaluation = async () => {
    setEvaluating(true);
    try {
      const res = await fetch("http://localhost:8000/api/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          questions: questions,
          ideal_answers: answers,
          answer_script: ansText
        }),
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        alert(`Evaluation failed: ${errData.detail || res.statusText}`);
        return;
      }
      const data = await res.json();
      setEvaluationResults(data.evaluation || []);

      // Scroll to results
      setTimeout(() => {
        document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (e) {
      console.error(e);
      alert("Error running evaluation.");
    } finally {
      setEvaluating(false);
    }
  };

  const downloadReport = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/generate-report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          evaluation_results: evaluationResults,
          student_name: "Madhesh" // Default name, could be made dynamic
        }),
      });

      if (!res.ok) {
        throw new Error(`Failed to generate report: ${res.statusText}`);
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      window.open(url, '_blank');
    } catch (e) {
      console.error("Report generation/view failed", e);
      alert("Failed to generate and open report.");
    }
  };

  const getEvaluationForQuestion = (id: string) => {
    return evaluationResults.find(r => r.id === id);
  };

  return (
    <div>
      <div className="flex gap-4">
        <button
          onClick={extractQuestions}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? "Extracting..." : "Extract Questions (Module 2)"}
        </button>

        {questions.length > 0 && (
          <button
            onClick={runEvaluation}
            disabled={evaluating}
            className="bg-indigo-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-indigo-700 disabled:bg-gray-400 flex items-center gap-2"
          >
            {evaluating ? "Evaluating..." : "🚀 Run Full Evaluation (Module 3)"}
          </button>
        )}
      </div>

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
                <span className="bg-purple-100 text-purple-800 text-[10px] font-bold px-2 py-0.5 rounded ml-2">Part {q.part}</span>
                <span className="text-gray-400 text-xs group-hover:text-blue-500 ml-auto">View Details &rarr;</span>
              </div>
              <h5 className="font-semibold text-gray-800 text-sm line-clamp-3 mb-3">{q.question}</h5>
              <div className="flex gap-2 flex-wrap mb-2">
                <span className="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">Max: {q.marks}</span>
                <span className="bg-gray-100 text-gray-600 text-xs px-2 py-0.5 rounded">{q.co}</span>
              </div>

              <div className="space-y-1">
                {answers[q.id] && (
                  <div className="text-[10px] text-blue-600 font-medium flex items-center gap-1">
                    <span className="w-1.5 h-1.5 bg-blue-500 rounded-full"></span>
                    Ideal Answer Set
                  </div>
                )}
                {getEvaluationForQuestion(q.id) && (
                  <div className="text-[10px] text-indigo-600 font-bold flex items-center gap-1">
                    <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></span>
                    Score: {getEvaluationForQuestion(q.id).marks_awarded} / {q.marks}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Results Section */}
      {evaluationResults.length > 0 && (
        <div id="results-section" className="mt-12 pt-8 border-t-2 border-dashed border-gray-200 animate-fade-in-up">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl font-bold text-indigo-900 flex items-center gap-3">
              <span className="bg-indigo-100 p-2 rounded-lg">📊</span>
              Evaluation Results
            </h2>
            <div className="flex flex-col items-end gap-3">
              <div className="bg-indigo-600 text-white px-6 py-3 rounded-2xl shadow-lg text-center min-w-[150px]">
                <div className="text-xs uppercase opacity-80 font-bold tracking-wider">Total Score</div>
                <div className="text-3xl font-black">
                  {Math.min(100, evaluationResults.reduce((acc, curr) => acc + (parseFloat(curr.marks_awarded) || 0), 0))}
                  <span className="text-sm font-normal opacity-70 ml-1">
                    / 100
                  </span>
                </div>
              </div>
              <button
                onClick={downloadReport}
                className="bg-white text-indigo-600 border-2 border-indigo-600 px-4 py-2 rounded-xl text-xs font-bold hover:bg-indigo-50 transition-colors flex items-center gap-2 shadow-sm"
              >
                <span>📥</span> Download PDF Report
              </button>
            </div>
          </div>

          <div className="space-y-8">
            {["A", "B", "C"].map((part) => {
              const partResults = evaluationResults.filter(res => {
                const q = questions.find(question => question.id === res.id);
                return q?.part === part;
              });

              if (partResults.length === 0) return null;

              return (
                <div key={part} className="bg-white rounded-2xl shadow-xl border border-indigo-50 overflow-hidden">
                  <div className="bg-indigo-50 px-6 py-3 border-b border-indigo-100 flex justify-between items-center">
                    <h3 className="font-bold text-indigo-900 uppercase tracking-widest text-sm">Part {part} Results</h3>
                    <span className="text-xs font-semibold text-indigo-600 bg-white px-2 py-1 rounded shadow-sm">
                      {part === 'B' ? 'Choice-based' : 'Compulsory'}
                    </span>
                  </div>
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="text-gray-400 border-b border-gray-50">
                        <th className="p-4 font-bold text-[10px] uppercase tracking-wider w-16">ID</th>
                        <th className="p-4 font-bold text-[10px] uppercase tracking-wider">Assessment & Feedback</th>
                        <th className="p-4 font-bold text-[10px] uppercase tracking-wider text-right w-24">Marks</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-50">
                      {partResults.map((res) => {
                        const q = questions.find(q => q.id === res.id);
                        const marks = parseFloat(res.marks_awarded) || 0;
                        const maxMarks = q ? parseFloat(q.marks) : 0;
                        const percentage = maxMarks > 0 ? (marks / maxMarks) * 100 : 0;
                        const status = res.status || (marks > 0 ? "Attempted" : "Not Attempted");

                        return (
                          <tr key={res.id} className="hover:bg-gray-50 transition-colors group">
                            <td className="p-4 align-top">
                              <span className="inline-block bg-gray-100 text-gray-700 font-bold px-2 py-1 rounded text-[10px]">
                                {res.id}
                              </span>
                            </td>
                            <td className="p-4">
                              <div className="flex items-center gap-2 mb-1">
                                <div className="font-medium text-gray-900 text-sm">
                                  {q?.question.slice(0, 80)}...
                                </div>
                                <span className={`text-[9px] px-1.5 py-0.5 rounded-full font-bold uppercase ${status === "Attempted" ? "bg-green-100 text-green-700" :
                                  status === "Alternative Choice Chosen" ? "bg-blue-100 text-blue-700" :
                                    "bg-red-100 text-red-700"
                                  }`}>
                                  {status}
                                </span>
                              </div>
                              <p className="text-xs text-gray-500 leading-relaxed italic border-l-2 border-indigo-100 pl-3 py-1">
                                "{res.feedback}"
                              </p>
                            </td>
                            <td className="p-4 text-right align-top">
                              <div className={`font-bold text-base ${percentage >= 80 ? 'text-green-600' : percentage >= 40 ? 'text-yellow-600' : 'text-red-500'}`}>
                                {res.marks_awarded}
                              </div>
                              <div className="text-[10px] text-gray-400">/ {q?.marks || '-'}</div>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              );
            })}
          </div>
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
                  <span className="bg-gray-200 text-gray-700 text-xs px-2 py-1 rounded font-medium">Part: {selectedQuestion.part}</span>
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
                <GenerateAnswerSection
                  question={selectedQuestion.question}
                  marks={selectedQuestion.marks}
                  answer={answers[selectedQuestion.id] || ""}
                  onUpdate={(text) => handleUpdateAnswer(selectedQuestion.id, text)}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function GenerateAnswerSection({
  question,
  marks,
  answer,
  onUpdate
}: {
  question: string,
  marks: string,
  answer: string,
  onUpdate: (val: string) => void
}) {
  const [loading, setLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(!answer); // Default to edit mode if empty

  const generate = async () => {
    setLoading(true);
    setIsEditing(true); // Switch to edit mode to see the result being typed
    try {
      const res = await fetch("http://localhost:8000/api/generate-answers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: question, marks }),
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        alert(`Generation failed: ${errData.detail || res.statusText}`);
        return;
      }
      const data = await res.json();
      onUpdate(data.ideal_answer || "");
    } catch (e) {
      console.error(e);
      alert("Error generating answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h4 className="font-bold text-gray-700">Answer Key (Ideal Answer)</h4>
        <div className="flex gap-2">
          <button
            onClick={() => setIsEditing(!isEditing)}
            className={`text-xs px-3 py-1.5 rounded border transition-colors ${isEditing
              ? "bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
              : "bg-blue-50 border-blue-200 text-blue-700 hover:bg-blue-100"
              }`}
          >
            {isEditing ? "👁 Preview Markdown" : "✎ Edit Answer"}
          </button>

          <button
            onClick={generate}
            disabled={loading}
            className="flex items-center gap-2 bg-indigo-600 text-white px-3 py-1.5 rounded-lg text-xs font-semibold hover:bg-indigo-700 transition-colors shadow-sm disabled:opacity-50"
          >
            {loading ? "Generating..." : "✨ AI Generate"}
          </button>
        </div>
      </div>

      {isEditing ? (
        <textarea
          value={answer}
          onChange={(e) => onUpdate(e.target.value)}
          className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm bg-white"
          placeholder="Enter the ideal answer here, or click 'AI Generate'..."
        />
      ) : (
        <div className="bg-white p-6 rounded-lg border border-gray-200 min-h-[16rem]">
          {answer ? (
            <div className="prose prose-blue max-w-none">
              <ReactMarkdown>{answer}</ReactMarkdown>
            </div>
          ) : (
            <div className="text-gray-400 text-sm italic text-center py-20">
              No answer defined yet. Switch to Edit mode to write one or generate with AI.
            </div>
          )}
        </div>
      )}

      <p className="mt-2 text-xs text-gray-400 text-right">
        {isEditing ? "Supports Markdown formatting." : "Reviewing formatted answer."}
      </p>
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
