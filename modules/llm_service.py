"""
LLM Service wrapping Google Gemini API with fallback for offline/demo use.
"""
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL
from prompts.analysis_prompts import build_resume_feedback_prompt, build_interview_prep_prompt

class LLMService:
    def __init__(self):
        self.api_available = False
        if GEMINI_API_KEY:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel(GEMINI_MODEL)
                self.api_available = True
            except Exception:
                self.api_available = False

    def generate_feedback(self, resume_text: str, job_desc: str, matched: list, missing: list) -> str:
        prompt = build_resume_feedback_prompt(resume_text, job_desc, matched, missing)
        if self.api_available:
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"[API Error: {str(e)}]\n\n" + self._fallback_feedback(matched, missing)
        return self._fallback_feedback(matched, missing)

    def generate_interview_questions(self, job_desc: str, matched: list, missing: list) -> str:
        prompt = build_interview_prep_prompt(job_desc, matched, missing)
        if self.api_available:
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"[API Error: {str(e)}]\n\n" + self._fallback_interview(matched)
        return self._fallback_interview(matched)

    def _fallback_feedback(self, matched: list, missing: list) -> str:
        return f"""### Executive Alignment Summary
The candidate demonstrates foundational knowledge in {', '.join(matched[:4]) if matched else 'core domains'}. To increase competitiveness, align project outcomes with measurable business and technical metrics.

### High-Impact Resume Enhancements
- **Quantify Impact:** Add performance figures (e.g., latency reduction, user count, test coverage) to project descriptions.
- **Surface Key Competencies:** Move relevant skills to the upper third of your resume so ATS parsers index them immediately.
- **Bridge Gap Areas:** Detail any hands-on exposure to {', '.join(missing[:3]) if missing else 'emerging frameworks'} through lab coursework or repositories.

### Targeted Learning Roadmap
- **Week 1-2:** Build a prototype using {missing[0] if missing else 'cloud containerization'}.
- **Week 3-4:** Deploy with CI/CD and document architecture patterns.
"""

    def _fallback_interview(self, matched: list) -> str:
        s1 = matched[0] if matched else "Data Structures"
        s2 = matched[1] if len(matched) > 1 else "REST APIs"
        return f"""### Recommended Interview Questions
1. **Technical:** How do you handle concurrency, caching, and state management when building applications in {s1}?
   *Tip: Highlight real-world trade-offs between memory overhead and latency.*
2. **Architecture:** Describe the lifecycle of a request in your recent project and how you secured your endpoints using {s2}.
   *Tip: Walk through authentication, validation, and error boundaries step-by-step.*
3. **Problem Solving:** Walk through a scenario where your application experienced unexpected crashes under load. How did you profile and resolve the bottleneck?
   *Tip: Emphasize logging, telemetry, and methodical debugging.*
4. **Behavioral:** Describe a recent situation where you had to learn an unfamiliar library under tight academic deadlines.
   *Tip: Focus on your documentation review habits and rapid prototyping methodology.*
"""
