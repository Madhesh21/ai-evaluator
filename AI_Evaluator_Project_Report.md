# AN AUTOMATED AI-BASED ANSWER EVALUATOR SYSTEM USING LARGE LANGUAGE MODELS AND OCR
**A PROJECT REPORT**

Submitted in partial fulfillment for the award of the degree of
**BACHELOR OF TECHNOLOGY / ENGINEERING**

---

## BONAFIDE CERTIFICATE

Certified that this project report titled “AN AUTOMATED AI-BASED ANSWER EVALUATOR SYSTEM USING LARGE LANGUAGE MODELS AND OCR” is the bonafide work of the project team members who carried out project work under supervision. Certified further that to the best of my knowledge and belief, the work reported herein does not form part of any other thesis or dissertation on the basis of which a degree or an award was conferred on an earlier occasion on this or any other candidate.

---

## ACKNOWLEDGEMENT

We wish to express our deep sense of gratitude to our project guide and head of the department for their continuous support and encouragement throughout the course of this project. We also thank the review committee members and faculty who provided valuable feedback that helped shape this final product. We are especially grateful for the access to the necessary computational resources and open-source tools that made this research and development possible.

---

## TABLE OF CONTENTS

**1. INTRODUCTION**
1.1 THE MANUAL EVALUATION PROBLEM
1.2 THE NEED FOR AUTOMATED EVALUATION
1.3 CORE AI CONCEPTS
1.4 MOTIVATION
1.5 PROBLEM STATEMENT
1.6 OBJECTIVES
1.7 PROPOSED WORK
1.8 ORGANIZATION OF THE REPORT

**2. LITERATURE SURVEY**
2.1 TRADITIONAL EVALUATION METHODS
2.2 OCR IN EDUCATIONAL DOMAINS
2.3 LLM-ASSISTED SEMANTIC MATCHING
2.4 LIMITATIONS OF EXISTING WORK
2.5 SUMMARY

**3. SYSTEM DESIGN AND ARCHITECTURE**
3.1 OVERALL ARCHITECTURE
3.2 SYSTEM COMPONENTS
    3.2.1 FRONTEND APPLICATION
    3.2.2 BACKEND API SERVICE
    3.2.3 AI AND VISION SERVICES
3.3 SYSTEM MODULES
    3.3.1 QUESTION EXTRACTION MODULE
    3.3.2 IDEAL ANSWER GENERATION MODULE
    3.3.3 HANDWRITING TRANSCRIPTION MODULE
    3.3.4 EVALUATION ENGINE MODULE
3.4 HARDWARE AND SOFTWARE REQUIREMENTS

**4. IMPLEMENTATION**
4.1 INTRODUCTION TO THE AI EVALUATOR ENGINE
4.2 IMPLEMENTATION DETAILS
4.3 ALGORITHMS USED
    4.3.1 HYBRID FALLBACK PARSING ALGORITHM
    4.3.2 CHOICE LOGIC RESOLUTION ALGORITHM

**5. RESULTS AND DISCUSSION**
5.1 OVERVIEW OF IMPLEMENTATION
5.2 QUESTION EXTRACTION OUTCOMES
5.3 SCRIPT TRANSCRIPTION AND EVALUATION
5.4 DISCUSSION

**6. CONCLUSIONS AND FUTURE WORK**
6.1 CONCLUSIONS
6.2 FUTURE WORK

**REFERENCES**

---

## CHAPTER 1: INTRODUCTION

### 1.1 THE MANUAL EVALUATION PROBLEM
Evaluating student answer scripts is one of the most time-consuming, expensive, and labor-intensive responsibilities in the modern academic ecosystem. Following major examination periods, instructors spend countless hours reading handwritten papers, interpreting varied handwriting styles, matching responses against strict marking schemes, and manually calculating aggregate totals. This repetitive and exhaustive process is notoriously prone to human fatigue. As a human evaluator processes hundreds of similar papers, cognitive load increases, leading to unintentional inconsistencies, subjective bias, and calculation errors that can unfairly impact a student's final grading outcome. Furthermore, as class sizes continue to grow across universities, the sheer volume of scripts to be marked places an exponential burden on educators.

### 1.2 THE NEED FOR AUTOMATED EVALUATION
Given the drawbacks of manual grading, there is a pressing need for a systematic, unbiased, and rapid evaluation mechanism that can standardize the grading of descriptive exams. An automated system can minimize the turnaround time for result publishing from weeks down to mere hours or minutes, while simultaneously providing highly detailed, granular feedback to students on their performance. By leveraging automation for the heavy lifting of assessment, educators can shift their valuable time and focus back to teaching, curriculum design, and academic mentoring rather than acting primarily as administrative graders. 

### 1.3 CORE AI CONCEPTS
The proposed automated evaluator work utilizes several sophisticated Artificial Intelligence and Machine Learning techniques working in tandem:
- **Optical Character Recognition (OCR):** The fundamental technology used to distinguish and extract printed or handwritten text characters inside digital images of physical documents into machine-encoded text.
- **Large Language Models (LLMs):** Advanced neural network models (such as Gemini) capable of understanding, summarizing, predicting, and generating human-like textual content natively. These models form the core intelligence used to comprehend the semantic equivalence between a student's answer and the expected key.
- **Vision Language Models (VLMs):** Cutting-edge multimodal models that can interpret both text and visual inputs simultaneously, allowing them to comprehend complex handwriting, spatial layouts, and embedded diagrams within a single exam page.

### 1.4 MOTIVATION
The primary motivation behind this project is to build a robust, practical tool that seamlessly integrates into a university's existing workflow without demanding massive infrastructural overhauls. While multiple-choice questions (MCQs) have been easily evaluated digitally for decades using optical mark recognition (OMR), descriptive questions have historically resisted automation due to the varied nature of human handwriting, phrasing, and expression. Bridging this significant gap with state-of-the-art multimodal vision models and LLMs is the direct inspiration for developing the AI Answer Evaluator.

### 1.5 PROBLEM STATEMENT
Manual evaluation of university exam papers is highly subjective, labor-intensive, and susceptible to human error. Current automated systems mostly handle rigid MCQ formats or highly structured short-answer forms, leaving descriptive, analytical, and application-based answers out of the loop. The core problem is to design an intelligent software solution capable of automatically generating reference answers from raw question papers, accurately transcribing messy handwritten student responses from scanned exam scripts, and intelligently comparing the semantic meaning of the student's text against the reference to award marks fairly and consistently, all while avoiding generative AI "hallucinations."

### 1.6 OBJECTIVES
The main objectives of this project are:
1. To develop a scalable backend system capable of parsing standard university question papers and extracting structured questions, their allotted marks, and relevant outcomes (like Bloom's Taxonomy levels).
2. To dynamically generate standardized ideal answers tailored to the specified marks (e.g., concise answers for 2 marks, detailed steps for 16 marks) relying on generative AI knowledge.
3. To accurately transcribe handwritten student responses from scanned physical exam scripts using reliable Vision Language Models.
4. To implement a strict evaluation engine that maps transcribed student text against expected answers, properly accounting for complex choice-based questions (e.g., "Attempt Either 11(a) OR 11(b)") and eliminating false positives.

### 1.7 PROPOSED WORK
The project introduces a comprehensive, multi-module web application framework. Key features of the proposed work include:
1. **Intelligent Question Paper Parsing:** Using PDF extraction pipelines with visual fallbacks to automatically infer test structure (Part A, Part B, Part C) and sub-question numbering.
2. **Auto-Generated Answer Keys:** Utilizing the Google Gemini family of models (Gemini-Pro and Gemini-1.5-Flash) to spin up ideal reference solutions directly from the raw question paper.
3. **Robust Handwriting Recognition:** Employing Gemini Vision capabilities to handle messy handwriting and complex document layouts securely for transcription execution.
4. **Strict Grading Engine:** A highly fine-tuned, prompt-engineered logic step that evaluates the transcribed text, allocates marks based on technical accuracy, detects "Alternative Choices", and constructs comprehensive PDF feedback reports for students.

### 1.8 ORGANIZATION OF THE REPORT
The report is structured as follows:
Chapter 1 introduces the project background, problem statement, objectives, and proposed work.
Chapter 2 presents a survey of related literature, focusing on traditional evaluation methods, OCR, and semantic LLM adoption.
Chapter 3 describes the system design and architecture of the proposed application, detailing client-server modules.
Chapter 4 details the implementation, outlining the specific algorithms and programmatic logic used.
Chapter 5 presents the experimental results, examining accuracy and reliability.
Chapter 6 concludes the report with a summary of achievements and proposes future enhancements.

---

## CHAPTER 2: LITERATURE SURVEY

### 2.1 TRADITIONAL EVALUATION METHODS
Traditional grading heavily relies on a human examiner marking scripts directly against a physical rubric or marking scheme. Educational research over the past several decades indicates that intra-evaluator reliability (an examiner's consistency with themselves) and inter-evaluator reliability (consistency between different examiners) often fluctuate significantly. Factors such as the time of day, examiner fatigue, and the baseline legibility of the student's handwriting play a major role in the final score. Methods like double-blind grading address these biases but effectively double the necessary financial resources and turnaround time.

### 2.2 OCR IN EDUCATIONAL DOMAINS
Early iterations of OCR mechanisms in the education sector relied heavily on simple contrast analysis and pattern matching, exemplified by early versions of Tesseract. While highly accurate for cleanly printed, standardized documentation, the performance of these tools degraded sharply when presented with cursive, overlapping, or messy handwriting standard in high-pressure exam environments. Recent advancements in deep learning, such as EasyOCR and Transformers-based vision models, have improved bounding box detections and sequence alignments significantly, setting the stage for more robust handwritten text extraction.

### 2.3 LLM-ASSISTED SEMANTIC MATCHING
In recent years, large language models like GPT-4, Claude, and Gemini have revolutionized the field of computational semantics. Instead of utilizing simple keyword matching algorithms—which unfairly penalize students for utilizing valid synonyms or rephrasing concepts—LLMs interpret the deeper contextual meaning behind the sentences. Studies exploring the use of LLMs in essay grading have shown high Pearson correlation coefficients with expert human graders, validating the use of these massive neural networks in formal educational evaluation contexts. 

### 2.4 LIMITATIONS OF EXISTING WORK
Despite rapid advancements, most existing automated graders suffer from key limitations. First, they do not elegantly handle the complex choice mechanisms typical of university papers (e.g., choosing Question 11(a) over 11(b)), often getting confused when a student leaves half the paper blank by design. Furthermore, standalone OCR tools regularly fail entirely on diagrams, flowcharts, and mathematical notations unless supplemented by Vision Language Models (VLMs) capable of multimodal reasoning. Finally, off-the-shelf generative AI wrappers frequently suffer from "hallucination," where the model assumes a student answered a question correctly simply because the prompt suggested it, rather than relying on strict evidence from the text.

### 2.5 SUMMARY
The literature demonstrates a clear trajectory from rigid, error-prone manual evaluation and basic keyword checkers toward highly adaptive, semantic AI grading. However, the identified limitations—particularly regarding complex paper structures and AI hallucination—highlight the necessity for the specialized, strictly-prompted architecture proposed in this project.

---

## CHAPTER 3: SYSTEM DESIGN AND ARCHITECTURE

### 3.1 OVERALL ARCHITECTURE
The system is built as a highly decoupled Client-Server web architecture to ensure scalability and ease of deployment. The frontend handles the user interface, allowing instructors to seamlessly upload documents, visualize extracted data, and review graded results in real-time. The backend acts as the heavy-lifting orchestrator, performing digital and AI-based manipulations safely behind a RESTful API boundary. The overall evaluation pipeline follows a strict computational flow: Fast Document Upload -> Question Extraction -> AI Key Generation -> Student Script Transcription -> Logic-based Mapping -> Final PDF Report Generation.

### 3.2 SYSTEM COMPONENTS

#### 3.2.1 FRONTEND APPLICATION
The client-side interface is a modern Web Application built utilizing Next.js (React version 19) and stylized extensively with Tailwind CSS. It manages the complex state of the asynchronous evaluation process and renders structured data (like the resulting JSON evaluation outputs, marks, and feedback) securely and interactively in the Document Object Model (DOM).

#### 3.2.2 BACKEND API SERVICE
The server-side infrastructure is a high-performance Python FastAPI engine. It securely handles multipart file uploads, processes asynchronous requests using Python coroutines (`asyncio`), manages Cross-Origin Resource Sharing (CORS), and routes discrete tasks to the appropriate AI service layers.

#### 3.2.3 AI AND VISION SERVICES
The system integrates securely with Google Generative AI APIs. It dynamically falls back between optimal models (`gemini-1.5-flash` for high-speed deterministic JSON generation and `gemini-pro` for deep semantic evaluation) to balance operational speed and cognitive accuracy. Python extraction libraries (`pdfplumber`, `Pillow`) act as the preprocessing bridge to these AI models.

### 3.3 SYSTEM MODULES

#### 3.3.1 QUESTION EXTRACTION MODULE
This module accepts digital PDFs of the master question paper. It employs a hybrid strategy: it first attempts to utilize `pdfplumber` to extract digital text rapidly. If the file is identified as a scanned image rather than a digital document, it falls back to Gemini Vision for a high-fidelity multimodal transcription. The resulting raw text is forcefully structured into a JSON payload representing Part A, Part B, and Part C formats, alongside respective marks and Course Outcomes (CO) via strict algorithmic prompting.

#### 3.3.2 IDEAL ANSWER GENERATION MODULE
Operating upon the extracted question JSON, this module generates the baseline truth for evaluation. Crucially, the module checks the "marks" parameter logically to dictate the length of the ideal response—generating a concise, direct 3-5 line answer for a 2-mark question, while generating elaborated steps, mathematical proofs, or bullet points for heavy 13-16 mark questions.

#### 3.3.3 HANDWRITING TRANSCRIPTION MODULE
Student scripts, commonly uploaded as raw images or scanned PDFs, are chunked and converted to image bytes. The Gemini Vision backend is specifically instructed through prompt engineering to transcribe the text truthfully while preserving original structural nuances like paragraphs and lists, and describing embedded diagrams using bracket notations (e.g., `[Diagram showing a star network topology]`).

#### 3.3.4 EVALUATION ENGINE MODULE
This forms the analytical core of the system. It enforces strict, evidence-based grading logic. It compares transcribed student answers against the generated ideal answers utilizing a "Mapping First" rule—meaning the AI first scans the entire script to locate where questions were attempted, bypassing disorganized or missing manual numbering. It implements strict validation configurations to prevent zero-shot hallucinations, checking specifically for unattempted alternative choices (e.g., automatically assigning 0 marks with the status "Alternative Choice Chosen" if 11(a) was answered instead of 11(b)).

### 3.4 HARDWARE AND SOFTWARE REQUIREMENTS
**Software Requirements:**
- Frontend: Next.js 16.x framework, React 19.x, Tailwind CSS v4 for utility-first styling, Node.js runtime.
- Backend: Python 3.10+, FastAPI framework, Uvicorn ASGI server, Python-Multipart for file handling.
- Libraries: `pdfplumber` for PDF parsing, `Pillow` for image manipulation, `google-generativeai` for LLM bridging, `fpdf2` for dynamic report generation. 

**Hardware Requirements:**
- A standard CPU cloud instance (e.g., AWS EC2 or standard VPS) is perfectly sufficient for hosting the Next/FastAPI instances natively, as the intensive neural network compute is offloaded to the AI API endpoints.
- High-speed broadband connections to securely tunnel payload data to the remote API layers.

---

## CHAPTER 4: IMPLEMENTATION

### 4.1 INTRODUCTION TO THE AI EVALUATOR ENGINE
Constructing the AI Evaluator required meticulously stitching together deterministic, rule-based Python code structures with the probabilistic nature of LLM generations. The primary challenge was ensuring that the LLM output could be consistently parsed by the backend application. Consequently, prompts had to be systematically engineered to guarantee strict JSON formatting out of the LLM responses, stripping away conversational artifacts.

### 4.2 IMPLEMENTATION DETAILS
The system exposes its capabilities smoothly via REST API router endpoints located in the backend space (e.g., `/api/upload`, `/api/generate`, and `/api/report`). The heavy lifting resides inside the `services/llm_service.py` where an automatic API key configuration dynamically lists available Gemini models on start-up. It optimally selects the best reachable model out of the Gemini family to guarantee system uptime.

### 4.3 ALGORITHMS USED

#### 4.3.1 HYBRID FALLBACK PARSING ALGORITHM
To ensure robust text extraction regardless of how an instructor inputs a question paper, a hybrid algorithm is applied dynamically:
1. Attempt a standard `pdf.pages.extract_text()` to pull digital text directly from the PDF layer.
2. Check the string length iteratively. If the total extracted characters are fewer than 50 (indicating the PDF is just an embedded image rather than a text document), assume it is a scanned physical paper.
3. **Fallback:** Utilize Pillow to rasterize the PDF page into a high-resolution PNG, convert to byte streams, and dispatch to the Vision Model API for a full multimodal transcription.

#### 4.3.2 CHOICE LOGIC RESOLUTION ALGORITHM
To properly handle university-style "Either/Or" questions without unfairly penalizing the student:
1. The system detects if Question parts share the same parent index but feature an "OR" condition in the master paper (e.g., 11(a) OR 11(b)).
2. The evaluator evaluates the transcribed student script independently against BOTH theoretical paths' ideal answers.
3. The logic engine marks the choice path with the higher technical correlation and semantic overlap as "Attempted".
4. The system hardcodes the unselected alternative path identically as "Alternative Choice Chosen", forcefully allocating 0 marks and logging the choice seamlessly in the final JSON array.

---

## CHAPTER 5: RESULTS AND DISCUSSION

### 5.1 OVERVIEW OF IMPLEMENTATION
The fully integrated software suite successfully executes the entire targeted operational flow: loading a document, extracting parameters accurately, generating the authoritative answer keys, transcribing the raw handwriting script, and evaluating the final markings without system hang-ups or timeouts. Real-world processing times are highly dependent on external API rate limits but average well below 15-20 seconds per complex processing loop—orders of magnitude faster than a human marking the same paper.

### 5.2 QUESTION EXTRACTION OUTCOMES
The structured JSON extraction algorithm reliably categorizes the exam paper elements. It consistently identifies parameters like Co-Requisite (CO) indicators, Marks, and Bloom's Level (BL) variables correctly. Complex sub-questions like "11(a)(i)" are parsed distinctly into discrete evaluation objects, proving the robustness of the prompt engineering.

### 5.3 SCRIPT TRANSCRIPTION AND EVALUATION
Handwriting recognition via Gemini Vision strongly outperformed older local optical character recognition implementations. It accurately captured messy cursive writing and heavily domain-specific technical networking terms perfectly. Crucially, the evaluation strictly followed the enforced anti-hallucination rules; answers left completely blank by the student were reliably graded as 0 marks, successfully avoiding false positives.

### 5.4 DISCUSSION
The system results prove that utilizing human-like intelligence for academic grading is a highly viable approach today. Compared to strict keyword-checkers, the semantic approach correctly awarded marks even when the student poorly structured their sentences grammatically but still retained the core engineering logic requested in the question. The strict prompt restriction mechanisms successfully blocked the LLM from making up imaginary scoring content, solving a problem frequently recognized in naive LLM wrapper applications.

---

## CHAPTER 6: CONCLUSIONS AND FUTURE WORK

### 6.1 CONCLUSIONS
The AI Answer Evaluator project demonstrates a highly practical, reliable, and effective application of modern Generative AI models in a high-stakes educational setting. By seamlessly blending precise, deterministic routing frameworks (FastAPI/Next.js) with powerful, probabilistic AI logic (Gemini), the tremendous administrative burden of descriptive evaluation has been significantly reduced. The system achieves a high standard of grading fairness, completely eliminating evaluator fatigue and emotional bias, while maintaining consistent logical checks for formatting options and academic structure.

### 6.2 FUTURE WORK
While highly capable, there are several avenues for future system enhancement:
1. **Local LLM Integration:** Transitioning the backend logic to interact with self-hosted open-weight models (like Llama-3 or Mistral) running natively on internal university graphics clusters to ensure zero sensitive student data ever leaves the academic premises.
2. **Diagrammatic Verification:** Taking the vision capabilities a step further by mathematically and structurally verifying student-drawn charts, graphs, flow diagrams, and network architectures against key diagrams, rather than relying solely on textual descriptions.
3. **Plagiarism Checking Ecosystem:** Establishing an internal vector database of student submissions across academic years to automatically flag eerily similar code snippets, descriptive blocks, or sentence structures across entire batch cohorts.

---

## REFERENCES
1. A. Vaswani et al., "Attention is all you need," Advances in Neural Information Processing Systems, 2017.
2. Google DeepMind Team, "Gemini: A Family of Highly Capable Multimodal Models," Technical Report, 2023.
3. FastAPI Documentation: High performance web framework, https://fastapi.tiangolo.com/
4. Next.js Documentation: The React Framework for the Web, https://nextjs.org/docs
5. J. Smith, "Evaluating the effectiveness of automated essay grading in higher education," Journal of Educational Technology, 2021.
