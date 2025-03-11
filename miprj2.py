# app.py - Complete Agentic RAG Workflow with Groq API
import os
import streamlit as st
from groq import Groq

# Set your Groq API key (get from https://console.groq.com/)
os.environ["GROQ_API_KEY"] = "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"  # Replace with your actual key

# Initialize Groq client
client = Groq()

# Mock vector databases (replace with real implementations)
LEGAL_DB = ["Contract Law Principles", "IP Regulations 2023", "Trademark Act Sections"]
SCIENCE_DB = ["Quantum Computing Reviews", "Medical AI Studies", "Protein Folding Papers"]

class LegalAssistant:
    def rewrite_query(self, query):
        response = client.chat.completions.create(
            model="qwen-2.5-coder-32b",  # Qwen model for coding/legal tasks
            messages=[
                {"role": "system", "content": "You are a legal query rewriter"},
                {"role": "user", "content": f"Rewrite this legal query to be more precise: {query}"}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content
    
    def preliminary_answer(self, query):
        response = client.chat.completions.create(
            model="qwen-2.5-coder-32b",
            messages=[
                {"role": "system", "content": "You are a legal advisor"},
                {"role": "user", "content": f"Provide general legal principles for: {query}"}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content
    
    def retrieve_context(self, query):
        # Simple keyword match for demonstration
        matches = [doc for doc in LEGAL_DB if any(kw in query for kw in doc.split())]
        return " | ".join(matches) if matches else "No direct matches"

class ResearchAssistant:
    def refine_query(self, query):
        response = client.chat.completions.create(
            model="qwen-2.5-coder-32b",
            messages=[
                {"role": "system", "content": "You are a research query specialist"},
                {"role": "user", "content": f"Convert to 3 specific research questions: {query}"}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.split("\n")
    
    def generate_hypothesis(self, query):
        response = client.chat.completions.create(
            model="qwen-2.5-coder-32b",
            messages=[
                {"role": "system", "content": "You are a research hypothesis generator"},
                {"role": "user", "content": f"Create a hypothetical study abstract for: {query}"}
            ],
            max_tokens=400
        )
        return response.choices[0].message.content
    
    def retrieve_papers(self, query):
        # Simple keyword match for demonstration
        matches = [doc for doc in SCIENCE_DB if any(kw in query for kw in doc.split())]
        return matches if matches else ["No direct matches - speculative results"]

# Streamlit App
st.set_page_config(page_title="Agentic RAG Workflows", layout="wide")

def main():
    st.title("AI Assistant for Legal & Scientific Queries")
    agent_type = st.sidebar.selectbox("Select Agent", 
                                     ["Legal Assistant", "Scientific Research Assistant"])
    
    if agent_type == "Legal Assistant":
        legal_agent = LegalAssistant()
        query = st.text_input("Enter Legal Question")
        
        if query:
            st.subheader("Processing Pipeline")
            with st.spinner("Rewriting Query..."):
                rewritten = legal_agent.rewrite_query(query)
                st.info(f"Rewritten Query: {rewritten}")
            
            with st.spinner("Generating Preliminary Answer..."):
                prelim = legal_agent.preliminary_answer(rewritten)
                st.write("Preliminary Answer:", prelim)
            
            with st.spinner("Retrieving Legal Context..."):
                context = legal_agent.retrieve_context(rewritten)
                st.write("Retrieved References:", context)
            
            # Confidence mock-up
            confidence = len(context.split()) / 100  # Dummy calculation
            if confidence < 0.5:
                st.warning("Low confidence - Human expert review recommended")
                st.write("Speculative Response: Consult a legal professional regarding recent case law")

    else:
        research_agent = ResearchAssistant()
        query = st.text_input("Enter Research Question")
        
        if query:
            st.subheader("Research Pipeline")
            with st.spinner("Refining Query..."):
                refined = research_agent.refine_query(query)
                st.write("Refined Queries:", refined)
            
            with st.spinner("Generating Hypothesis..."):
                hypothesis = research_agent.generate_hypothesis(refined[0])
                st.write("Hypothetical Study:", hypothesis)
            
            with st.spinner("Retrieving Papers..."):
                sources = research_agent.retrieve_papers(refined[0])
                st.write("Relevant Sources:", sources)
            
            # Contradiction check mock-up
            if "speculative" in sources[0].lower():
                st.warning("Potential contradictions detected between sources")
                st.write("Recommendation: Manual review of methodology sections")

if __name__ == "__main__":
    main()