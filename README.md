<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img alt="Nilupul Nishan, AI Engineer" src="assets/banner-light.svg" width="860">
</picture>

### Hi, I'm Nilupul <img src="assets/emoji/waving-hand.webp" width="30" alt="">

**AI Engineer** building agentic systems, RAG pipelines, and the tools to ship them.<br>
Colombo, Sri Lanka

[![Portfolio](https://img.shields.io/badge/Portfolio-000000?style=flat-square&logo=vercel&logoColor=white)](https://nilupulnishan.vercel.app)
[![LinkedIn][badge-linkedin]](https://www.linkedin.com/in/nilupulnishan/)
[![Email](https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:nilupulofficial2000@gmail.com)
[![HackerRank](https://img.shields.io/badge/HackerRank-00EA64?style=flat-square&logo=hackerrank&logoColor=black)](https://www.hackerrank.com/profile/nilupulnishan201)

</div>

## <img src="assets/emoji/brain.webp" width="28" alt=""> About

- I build LLM applications: agent workflows in LangGraph, retrieval over long technical manuals, and document pipelines that read invoices and receipts.
- I also build tools for AI coding agents. [BAWA](https://github.com/NilupulNishan/bawa) and [BAAP](https://github.com/NilupulNishan/baap) are open plugins that take Claude Code or Codex from an idea to a working web or Android app.
- My roots are in deep learning and computer vision: Siamese networks for face verification, real-time face recognition, and a line-following robot that serves café tables.
- I studied at the University of Sri Jayewardenepura.
- Off the keyboard: fitness and making content.

## <img src="assets/emoji/rocket.webp" width="28" alt=""> Building now

<table>
<tr>
<td width="50%" valign="top">

**[BAWA: Build Any Web App](https://github.com/NilupulNishan/bawa)**

19 agent skills that take a web app from idea to a public URL. Point your agent at an app you like: it screenshots every page, writes user stories, then builds and tests one story per commit.

`React` `TypeScript` `Claude Code` `Codex`

</td>
<td width="50%" valign="top">

**[BAAP: Build Any Android aPp](https://github.com/NilupulNishan/baap)**

24 agent skills that take an Android app from idea to a signed release, with optional skills for enterprise and rugged devices.

`Kotlin` `Jetpack Compose` `Room` `Claude Code` `Codex`

</td>
</tr>
</table>

## <img src="assets/emoji/glowing-star.webp" width="28" alt=""> Selected work

**Agents, RAG and document AI**

| Project | What it does |
| --- | --- |
| [VivoAssist](https://github.com/NilupulNishan/humanized-rag-workflow-langgraph-automobile) | Chat assistant for car owner manuals. A LangGraph agent works out what the driver is asking, keeps session memory, asks for clarification when needed, and answers in plain language.<br><sub>LangGraph · LlamaIndex · Azure OpenAI · ChromaDB · FastAPI</sub> |
| [Manual RAG engine](https://github.com/NilupulNishan/automobile-pdf-rag-llamaindex) | The retrieval layer under VivoAssist. Hierarchical chunking with parent summaries, and every answer links to the exact PDF page it came from.<br><sub>LlamaIndex · Azure OpenAI · ChromaDB · Streamlit</sub> |
| [Invoice review](https://github.com/NilupulNishan/e2e-invoice-review) | Classifies each document as an invoice or a receipt, extracts its fields with Azure Document Intelligence, and suggests a general ledger account.<br><sub>Pydantic AI · Azure Document Intelligence · Azure OpenAI</sub> |
| [Chart agent](https://github.com/NilupulNishan/agentic-chart-generator-langchain) | Reflection pattern: one model writes matplotlib code, a vision model critiques the rendered chart, and the code is rewritten.<br><sub>LangGraph · OpenAI · Anthropic</sub> |

**Machine learning, vision and robotics**

| Project | What it does |
| --- | --- |
| [Log classifier](https://github.com/NilupulNishan/nlp_log_classification) | Sorts system logs in three tiers: regex for known patterns, sentence embeddings with logistic regression, and an LLM for rare cases. Served as an API.<br><sub>Sentence Transformers · scikit-learn · Groq · FastAPI</sub> |
| [Face attendance](https://github.com/NilupulNishan/face-recognition-attendance-dlib-opencv) | Real-time attendance by face, using 128-dimension ResNet embeddings, with a Flask web view and SQLite logs.<br><sub>OpenCV · dlib · Flask · SQLite</sub> |
| [Face verification](https://github.com/NilupulNishan/Face_verification_app) | A Siamese network trained to verify a face against reference photos, wrapped in a webcam desktop app.<br><sub>TensorFlow · OpenCV · Kivy</sub> |
| [Waiter 117](https://github.com/NilupulNishan/Waiter_117-v1) | Line-following robot for a small café. It drives to a table, serves, and returns to the kitchen.<br><sub>C++</sub> |

## <img src="assets/emoji/high-voltage.webp" width="28" alt=""> Toolbox

**AI and LLM**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/toolbox/ai-dark.svg">
  <img src="assets/toolbox/ai-light.svg" alt="LangGraph, LangChain, LlamaIndex, OpenAI, Azure AI, Anthropic, MCP, Hugging Face, Pydantic AI">
</picture>
<br><sub>LangGraph · LangChain · LlamaIndex · OpenAI · Azure AI · Anthropic · MCP · Hugging Face · Pydantic AI</sub>

**Machine learning and vision**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/toolbox/ml-dark.svg">
  <img src="assets/toolbox/ml-light.svg" alt="Python, TensorFlow, scikit-learn, OpenCV, pandas, NumPy, Jupyter">
</picture>
<br><sub>Python · TensorFlow · scikit-learn · OpenCV · pandas · NumPy · Jupyter</sub>

**Backend and data**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/toolbox/backend-dark.svg">
  <img src="assets/toolbox/backend-light.svg" alt="FastAPI, Flask, Streamlit, PostgreSQL, SQLite">
</picture>
<br><sub>FastAPI · Flask · Streamlit · PostgreSQL · SQLite</sub>

**Web**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/toolbox/web-dark.svg">
  <img src="assets/toolbox/web-light.svg" alt="TypeScript, React, Next.js, Vite, Tailwind CSS, Payload CMS, Vercel">
</picture>
<br><sub>TypeScript · React · Next.js · Vite · Tailwind CSS · Payload CMS · Vercel</sub>

**Mobile and embedded**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/toolbox/mobile-dark.svg">
  <img src="assets/toolbox/mobile-light.svg" alt="Kotlin, Jetpack Compose, Android, Java, Firebase, C++">
</picture>
<br><sub>Kotlin · Jetpack Compose · Android · Java · Firebase · C++</sub>

**Tools**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/toolbox/tools-dark.svg">
  <img src="assets/toolbox/tools-light.svg" alt="Git, GitHub, Claude Code">
</picture>
<br><sub>Git · GitHub · Claude Code</sub>

---

<div align="center">
<sub><img src="assets/emoji/handshake.webp" width="20" alt=""> Happy to collaborate on open-source AI projects. Say hi on <a href="https://www.linkedin.com/in/nilupulnishan/">LinkedIn</a> or by <a href="mailto:nilupulofficial2000@gmail.com">email</a>.</sub>
</div>

<!-- LinkedIn's logo is no longer in Simple Icons; embedded from simple-icons 9.21.0 (CC0). -->
[badge-linkedin]: https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=data:image/svg%2Bxml;base64,PHN2ZyBmaWxsPSJ3aGl0ZSIgcm9sZT0iaW1nIiB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI%2BPHRpdGxlPkxpbmtlZEluPC90aXRsZT48cGF0aCBkPSJNMjAuNDQ3IDIwLjQ1MmgtMy41NTR2LTUuNTY5YzAtMS4zMjgtLjAyNy0zLjAzNy0xLjg1Mi0zLjAzNy0xLjg1MyAwLTIuMTM2IDEuNDQ1LTIuMTM2IDIuOTM5djUuNjY3SDkuMzUxVjloMy40MTR2MS41NjFoLjA0NmMuNDc3LS45IDEuNjM3LTEuODUgMy4zNy0xLjg1IDMuNjAxIDAgNC4yNjcgMi4zNyA0LjI2NyA1LjQ1NXY2LjI4NnpNNS4zMzcgNy40MzNjLTEuMTQ0IDAtMi4wNjMtLjkyNi0yLjA2My0yLjA2NSAwLTEuMTM4LjkyLTIuMDYzIDIuMDYzLTIuMDYzIDEuMTQgMCAyLjA2NC45MjUgMi4wNjQgMi4wNjMgMCAxLjEzOS0uOTI1IDIuMDY1LTIuMDY0IDIuMDY1em0xLjc4MiAxMy4wMTlIMy41NTVWOWgzLjU2NHYxMS40NTJ6TTIyLjIyNSAwSDEuNzcxQy43OTIgMCAwIC43NzQgMCAxLjcyOXYyMC41NDJDMCAyMy4yMjcuNzkyIDI0IDEuNzcxIDI0aDIwLjQ1MUMyMy4yIDI0IDI0IDIzLjIyNyAyNCAyMi4yNzFWMS43MjlDMjQgLjc3NCAyMy4yIDAgMjIuMjIyIDBoLjAwM3oiLz48L3N2Zz4%3D
