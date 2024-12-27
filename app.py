import streamlit as st
import google.generativeai as genai
import pdfplumber

def generative_ai(prompt):
    genai.configure(api_key=st.secrets["Gemini"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f'{prompt}')
    return response.text


def generate_output_cold_email_prompt():
    prompt = f"""

You are an expert in crafting professional cold emails. Write a formal email to inquire about available job opportunities, using the details provided below. The email should be in Indian English and should sound natural and human-written. Use the inputs as follows:

Company Name: {st.session_state.company_name}
Name of the Candidate: {st.session_state.name}
Introduction: {st.session_state.skills}
Desired Job Role: {st.session_state.job_profile}
Ensure the tone is polite, concise, and appropriately formal for a professional context.

    """
    return generative_ai(prompt)


def generate_output_compatibility_score_prompt():
    pass

def generate_skills_gaps_prompt():
    pass

def read_resume(pdf):
    text = ""
    with pdfplumber.open(pdf) as f:
        pages = f.pages
        for p in  pages:
            for c in p.chars:
                text+=c["text"]
    # print(text)
    return text

def main():
    st.title("Cold Mail Crafter")
    if "name" not in st.session_state:
        st.session_state.name = ""
        st.session_state.company_name = ""
        st.session_state.job_profile = ""
        st.session_state.skills = ""
        st.session_state.click = False

    st.session_state.name = st.text_input("Enter your name")
    pdf_resume = st.file_uploader("Upload your resume", type = "pdf")
    if pdf_resume:
        st.session_state.skills = read_resume(pdf_resume)

    st.session_state.company_name = st.text_input("Enter company name")
    st.session_state.job_profile = st.text_area("Enter or paste the job profile (Use Ctrl C and Ctrl V for better results) for which you need to apply", height=168)
    if(st.button("Generate Content")):
        response = generate_output_cold_email_prompt()
        with st.container(border = True):
            st.write(response)
    
main()
    


    