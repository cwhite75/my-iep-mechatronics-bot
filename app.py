import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="My IEP & Mechatronics Helper", page_icon="🤖")

st.title("🤖 My Smart IEP & Mechatronics AI Helper")
st.write("Ask me anything! I can help with IEP planning and mechatronics education.")

def get_offline_response(question):
    question_lower = question.lower()
    if "iep" in question_lower or "goal" in question_lower:
        return "IEP goals should be SMART: Specific, Measurable, Achievable, Relevant, Time-bound! For example: 'By December 2025, John will solve 8 out of 10 two-step math problems independently as measured by weekly assessments.'"
    elif "mechatronics" in question_lower:
        return "Mechatronics combines mechanical engineering, electronics, computer science, and control engineering! It's used in robotics, automation, smart devices, and manufacturing systems."
    elif "accommodation" in question_lower:
        return "Common accommodations include: extended time on tests, quiet workspace, assistive technology, frequent breaks, modified assignments, and preferential seating."
    elif "project" in question_lower:
        return "Great mechatronics projects: Arduino-based robots, automated plant watering systems, sensor networks, smart home devices, line-following robots, and automated sorting machines!"
    elif "career" in question_lower:
        return "Mechatronics careers: Automation Engineer, Robotics Technician, Manufacturing Engineer, Automotive Engineer, IoT Developer, Control Systems Engineer, Biomedical Equipment Technician."
    else:
        return "I can help with IEP planning, mechatronics education, accommodations, project ideas, and career guidance! Try asking about specific topics."

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm your AI helper for IEP and mechatronics. What can I help you with today?"}
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
            response = get_offline_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar:
    st.header("🛠️ Quick Tools")
    
    if st.button("📝 IEP Goal Template"):
        template = """**IEP Goal Template:**
        
**Student:** [Name]  
**Subject:** [Area]  
**Goal:** By [date], [student] will [skill] with [accuracy] as measured by [method].

**Example:**
By May 2025, Sarah will solve 8 out of 10 single-digit multiplication problems independently as measured by weekly math assessments.

**Objectives:**
1. [First milestone - 25% progress]
2. [Second milestone - 50% progress]  
3. [Third milestone - 75% progress]
4. [Final goal - 100% progress]"""
        st.markdown(template)
    
    if st.button("🤖 Career Paths"):
        careers = """**Mechatronics Careers:**
        
🔧 **Automation Engineer** - Design automated systems
🤖 **Robotics Technician** - Build and maintain robots
🏭 **Manufacturing Engineer** - Optimize production lines
🚗 **Automotive Engineer** - Design vehicle systems
🏠 **IoT Developer** - Create smart connected devices
⚡ **Control Systems Engineer** - Design control algorithms
🏥 **Biomedical Equipment Tech** - Medical device maintenance"""
        st.markdown(careers)
    
    if st.button("📊 Create PowerPoint Outline"):
        if st.session_state.messages:
            recent_context = ""
            for msg in st.session_state.messages[-4:]:
                if len(recent_context) < 200:  # Keep it manageable
                    recent_context += f"{msg['content'][:50]}... "
            
            outline = f"""### 📊 PowerPoint Outline Based on Our Chat:

**Slide 1: Title**
- Topic: {recent_context[:100]}...

**Slide 2: Introduction** 
- What is the main topic?
- Why is it important?

**Slide 3: Key Points**
- Main concept 1
- Main concept 2  
- Main concept 3

**Slide 4: Examples/Applications**
- Real-world examples
- Practical applications

**Slide 5: Benefits/Advantages**
- Why this matters
- Positive outcomes

**Slide 6: Implementation**
- How to get started
- Next steps

**Slide 7: Conclusion**
- Summary of key points
- Call to action

💡 **Tip:** Copy this to slidesai.io or gamma.app to create your presentation!"""
            st.markdown(outline)
        else:
            st.warning("Have a conversation first, then I can create an outline!")
    
    st.header("👥 Student Tracker")
    with st.expander("Add Student"):
        name = st.text_input("Student Name")
        goals = st.text_area("IEP Goals")
        progress = st.slider("Progress (1-10)", 1, 10, 5)
        notes = st.text_area("Notes")
        
        if st.button("Save Student") and name:
            st.session_state.students[name] = {
                "goals": goals, "progress": progress, 
                "notes": notes, "date": datetime.now().strftime("%Y-%m-%d")
            }
            st.success(f"Saved {name}!")
    
    if st.session_state.students:
        st.write("**Saved Students:**")
        for name, data in st.session_state.students.items():
            with st.expander(f"{name} - Progress: {data['progress']}/10"):
                st.write(f"**Goals:** {data['goals']}")
                st.write(f"**Notes:** {data['notes']}")
                st.write(f"**Last Updated:** {data['date']}")
    
    if st.button("🧠 Generate Sample Quiz"):
        quiz = """### 📝 Mechatronics Quiz

**1. What does mechatronics combine?**
a) Only mechanical and electrical engineering
b) Mechanical, electrical, computer, and control engineering
c) Just robotics and automation
d) Only software and hardware

**2. What does SMART stand for in IEP goals?**
a) Simple, Measurable, Achievable, Relevant, Timely
b) Specific, Measurable, Achievable, Relevant, Time-bound
c) Special, Modern, Advanced, Real, Technical
d) Standard, Modified, Accessible, Regular, Tested

**3. Which is a common mechatronics application?**
a) Automated manufacturing systems
b) Smart home devices  
c) Robotic surgery equipment
d) All of the above

**4. What's an appropriate IEP accommodation?**
a) Doing less work than other students
b) Extended time for tests
c) Never taking tests
d) Sitting anywhere in class

**5. Arduino is commonly used for:**
a) Word processing
b) Creating prototypes and learning electronics
c) Professional video editing
d) Database management

**Answers:** 1-b, 2-b, 3-d, 4-b, 5-b"""
        st.markdown(quiz)
    
    st.info("💡 Try asking about: IEP goals, accommodations, mechatronics projects, or career advice!")
