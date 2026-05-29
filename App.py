import streamlit as st
import PyPDF2
from groq import Groq

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}

h1 {
    color: #1f2937;
    text-align: center;
}

.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    border: none;
}

.stButton > button:hover {
    background-color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)


st.title("📄 AI Resume Analyzer for Freshers")
st.markdown("### Developed by Taneti Ritesh")

st.caption(
    "Upload your resume and get AI-powered ATS analysis, missing skills detection, and improvement suggestions."
)

st.markdown("---")


st.sidebar.title("👨‍💻 About Developer")

st.sidebar.info("""
Name: Taneti Ritesh

Skills:
Python, SQL, Power BI, Data Analytics

Project:
AI Resume Analyzer
""")


try:
    client = Groq(
        api_key="YOUR API KEY"
    )

except Exception as e:
    st.error(f"❌ API Error: {e}")


def extract_text(pdf_file):

    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    return text


def calculate_ats_score(resume_text, job_role):

    resume_text = resume_text.lower()

    role_skills = {

        "Data Analyst": [
            "python", "sql", "excel", "power bi", "pandas",
            "numpy", "data analysis", "data visualization",
            "dashboard", "statistics"
        ],

        "Data Scientist": [
            "python", "machine learning", "deep learning",
            "tensorflow", "pytorch", "sql",
            "pandas", "numpy", "statistics", "data science"
        ],

        "Python Developer": [
            "python", "django", "flask", "fastapi",
            "sql", "api", "git", "github",
            "oop", "data structures"
        ],

        "Software Engineer": [
            "java", "python", "sql", "git", "github",
            "object oriented", "api", "leetcode",
            "problem solving", "data structures"
        ],


        "QA Tester": [
            "testing", "manual testing", "automation",
            "selenium", "jira", "bug tracking",
            "test cases", "api testing", "sql", "agile"
        ],

        "Business Analyst": [
            "excel", "sql", "power bi",
            "tableau", "requirements gathering",
            "stakeholder management", "documentation",
            "data analysis", "reporting", "communication"
        ]
    }

    skills = role_skills.get(job_role, [])

    score = 0
    found_skills = []
    missing_skills = []

    for skill in skills:

        if skill.lower() in resume_text:
            score += 10
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    score = min(score, 100)

    return score, found_skills, missing_skills


def analyze_resume(resume_text, job_role):

    try:

        prompt = f"""
Rate this resume for a Fresher {job_role} role.

Return EXACTLY in this format:

ATS Score: <number>/100

Strengths:
- ...

Missing Skills:
- ...

Recommendations:
- ...

Interview Tips:
- ...

Hiring Readiness: <number>/10

Resume:
{resume_text}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=1200
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"❌ Error Generating AI Suggestions: {e}"


job_role = st.selectbox(
    "🎯 Select Target Role",
    [
        "Data Analyst",
        "Data Scientist",
        "Python Developer",
        "Software Engineer",
        "QA Tester",
        "Business Analyst"
    ]
)


uploaded_file = st.file_uploader(
    "📂 Upload Your Resume PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success("✅ Resume Uploaded Successfully")

    resume_text = extract_text(uploaded_file)

    if st.button("🚀 Analyze Resume"):

        with st.spinner("Analyzing Resume..."):

            score, found_skills, missing_skills = calculate_ats_score(
            resume_text,
            job_role
            )

            st.subheader("📊 ATS Score")
            st.progress(score)
            st.markdown(f"## ATS Score: {score}/100")
            
            # Skills Found

            st.subheader("✅ Skills Found")

            if found_skills:
                for skill in found_skills:
                    st.write(f"• {skill}")
            else:
                st.warning("No matching skills found")

            # Missing Skills

            st.subheader("❌ Missing Skills")

            if missing_skills:
                for skill in missing_skills:
                    st.write(f"• {skill}")
            else:
                st.success("No missing skills detected")

            # AI Suggestions

            st.subheader("🤖 AI Resume Suggestions")

            result = analyze_resume(
                resume_text,
                job_role
            )

            st.write(result)


st.markdown("---")

st.markdown(
    """
    <center>
    Developed by <b>Taneti Ritesh</b> | AI Resume Analyzer Project
    </center>
    """,
    unsafe_allow_html=True
)
