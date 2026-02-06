
AI-Based Resume Screening & Ranking System

(Assessment Implementation & Evaluation)

📌 Project Context
# Streamlit interface for assessment-based evaluation of an AI-driven resume scoring system
This project is an academic/technical assessment implementation based on an open-source GitHub repository. The purpose of the assessment was to understand, configure, execute, and evaluate an AI-driven resume screening system rather than develop the solution from scratch.

The work focused on:

Understanding system architecture and data flow
This implementation is adapted and evaluated as part of an academic/technical assessment
 based on an open-source project.
Resolving dependency and environment issues

Running the application locally

Evaluating AI-driven resume scoring logic

Identifying strengths, limitations, and design trade-offs

🎯 Project Overview (Assessment Perspective)

The system is an AI-driven resume filtering and ranking application that evaluates candidates based on job-specific criteria. Instead of rigid keyword-based filtering, it uses semantic analysis, embeddings, and weighted scoring to assess resume relevance more contextually.

From an assessment standpoint, the system demonstrates how modern LLM-based architectures can assist in automating candidate shortlisting while retaining flexibility for recruiters.

🧠 Functional Capabilities Evaluated
1. Resume Understanding

Accepts resumes in PDF format

Extracts and chunks resume text

Generates embeddings using a Gemini-based embedding model

Stores embeddings in a local vector database for retrieval

2. Parameter-Driven Evaluation

Recruiters or administrators define evaluation parameters which are categorized into:

Textual parameters – semantic evaluation using LLMs

Quantitative parameters – numeric scoring logic

Boolean parameters – eligibility-based checks

Each parameter contributes to a final weighted score for each candidate.

3. AI-Assisted Shortlisting

Uses a fine-tuned Google Gemini Pro model

Evaluates resumes against job-specific requirements

Produces consistent, explainable scores rather than binary decisions

🏗️ System Architecture (As Analyzed)
Resume Processing Flow
graph TD
    A[Applicant] -->|Uploads Resume| B[PDF File]
    B -->|Text Extraction| C[SimpleDirectoryReader]
    C -->|Chunking| D[Text Chunking]
    D -->|Generate Embeddings| E[Gemini Embeddings]
    E -->|Store| F[Vector Store]
    F --> G[Retrieval Ready]

Parameter Evaluation Flow
graph TD;
    A[Load Evaluation Parameters] --> B{Parameter Type};
    B -->|Textual| C[LLM-Based Evaluation];
    B -->|Quantitative| D[Formula-Based Scoring];
    B -->|Boolean| E[Condition Check];

    C --> F[Compute Final Score];
    D --> F;
    E --> F;

    F --> DB[(Database)];

🧪 Parameter Classification (Assessment Understanding)

All evaluation parameters are categorized to ensure structured scoring.

1️⃣ Textual Parameters

Used for evaluating descriptive or open-ended information such as:

Project descriptions

Skill proficiency

Work responsibilities

A fine-tuned LLM analyzes contextual relevance and assigns a consistent score.

2️⃣ Quantitative Parameters

Used for measurable criteria such as:

Years of experience

Academic scores (GPA)

Number of projects

Predefined formulas are applied and combined with parameter weights.

3️⃣ Boolean Parameters

Used for yes/no conditions such as:

Required certifications

Mandatory skills

GitHub presence

Candidates receive full or zero points based on eligibility.

⚙️ Configuration Details (Observed Setup)
Document Processing

Format: PDF

Chunk size: 70 tokens

Chunk overlap: 10 tokens

Model Configuration

LLM: Google Gemini Pro

Fine-tuned model ID: tunedModels/v1smarthirr-64usbdiq2vd5

Temperature: 0.2

Max output tokens: 2048

Vector Storage

Index type: VectorStoreIndex

Embedding model: Gemini Embeddings

Storage: Local persistence

📊 Key Observations
Strengths

Semantic evaluation beyond keyword matching

Flexible and customizable scoring parameters

Modular design separating embeddings, retrieval, and scoring

Explainable candidate ranking logic

Limitations

Supports PDF resumes only

Heavy dependency on external LLM APIs

Requires strict version alignment for LLM plugins

Local vector storage may not scale for large datasets

API rate limits can impact batch processing

📚 Assessment Summary

This implementation demonstrates how LLMs, embeddings, and vector databases can be applied to resume screening workflows. As part of the assessment, the system was:

Successfully configured and executed locally

Debugged for dependency and compatibility issues

Evaluated from an architectural and functional perspective

The project serves as a strong reference for understanding AI-assisted candidate evaluation systems, while also highlighting real-world challenges related to scalability, dependency management, and API reliance.