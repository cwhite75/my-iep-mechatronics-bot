python
import streamlit as st
import openai
import requests
from datetime import datetime

st.set_page_config(page_title="My IEP & Mechatronics Helper", page_icon="🤖")

try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.error("Please add your OpenAI API key in Streamlit secrets!")
    st.stop()

st.title("🤖 My Smart IEP & Mechatronics AI Helper")
st.write("Ask me anything! I can provide current information and create presentations.")

def get_ai_response(question):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a helpful assistant specializing in:
                1. IEP (Individualized Education Program) support - goals, accommodations, meetings
                2. Mechatronics education - courses, projects, careers, current technology
                3. Special education strategies
                Always provide helpful, encouraging, and accurate information."""},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return get_offline_response(question)

def get_offline_response(question):
    question_lower = question.lower()
    if "iep" in question_lower or "goal" in question_lower:
        return "IEP goals should be SMART: Specific, Measurable, Achievable, Relevant, Time-bound!"
    elif "mechatronics" in question_lower:
        return "Mechatronics combines mechanical engineering, electronics, computer science, and control engineering!"
    elif "accommodation" in question_lower:
        return "Common accommodations: extended time, quiet workspace, assistive technology, frequent breaks."
    elif "project" in question_lower:
        return "Great projects: Arduino robots, automated systems, sensor networks, smart home devices!"
    else:
        return "I can help with IEP planning, mechatronics education, accommodations, and project ideas!"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your AI helper for IEP and mechatronics. What can I help you with?"}
    ]

if "students" not in st.session_state:
    st.session_state.students = {}

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.header("🛠️ Quick Tools")
    
    if st.button("📝 IEP Goal Template"):
        template = """**IEP Goal Template:**
        
**Student:** [Name]  
**Subject:** [Area]  
**Goal:** By [date], [student] will [skill] with [accuracy] as measured by [method].
**Objectives:**
1. [First milestone]
2. [Second milestone]
3. [Third milestone]"""
        st.markdown(template)
    
    if st.button("🤖 Career Paths"):
        careers = """**Mechatronics Careers:**
        
🔧 **Automation Engineer**
🤖 **Robotics Technician** 
🏭 **Manufacturing Engineer**
🚗 **Automotive Engineer**
🏠 **IoT Developer**
⚡ **Control Systems Engineer**"""
        st.markdown(careers)
    
    if st.button("📊 Create PowerPoint"):
        if st.session_state.messages:
            recent_context = ""
            for msg in st.session_state.messages[-4:]:
                recent_context += f"{msg['role']}: {msg['content']}\n"
            
            ppt_prompt = f"""Create a PowerPoint outline based on our conversation:
            Context: {recent_context}
            
            Include:
            - Title slide
            - 5-7 main slides  
            - Conclusion
            Format with clear titles and bullet points."""
            
            with st.spinner("Creating outline..."):
                outline = get_ai_response(ppt_prompt)
                st.markdown("### 📊 PowerPoint Outline:")
                st.markdown(outline)
                st.info("Copy this outline to slidesai.io or gamma.app to create your presentation!")
        else:
            st.warning("Have a conversation first!")
    
    st.header("👥 Student Tracker")
    with st.expander("Add Student"):
        name = st.text_input("Name")
        goals = st.text_area("IEP Goals")
        progress = st.slider("Progress (1-10)", 1, 10, 5)
        notes = st.text_area("Notes")
        
        if st.button("Save Student"):
            st.session_state.students[name] = {
                "goals": goals, "progress": progress, 
                "notes": notes, "date": datetime.now().strftime("%Y-%m-%d")
            }
            st.success(f"Saved {name}!")
    
    if st.session_state.students:
        for name, data in st.session_state.students.items():
            with st.expander(f"{name} - {data['progress']}/10"):
                st.write(f"**Goals:** {data['goals']}")
                st.write(f"**Notes:** {data['notes']}")
    
    if st.button("🧠 Generate Quiz"):
        quiz = get_ai_response("Create a 5-question mechatronics quiz with multiple choice answers")
        st.markdown("### Quiz:")
        st.markdown(quiz)
    
    st.info("💡 Ask specific questions for better help!")
