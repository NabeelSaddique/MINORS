"""
MINORS Assessment Tool
A Streamlit web application for conducting Methodological Index for Non-Randomized Studies assessments

Developer: Muhammad Nabeel Saddique
Institution: King Edward Medical University, Lahore, Pakistan
Organization: Nibras Research Academy

Citation: Slim K, et al. Methodological index for non-randomized studies (MINORS): 
development and validation of a new instrument. ANZ J Surg. 2003;73:712-716.
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="MINORS Assessment Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 0.5rem;
}
.sub-header {
    font-size: 1.2rem;
    color: #666;
    text-align: center;
    margin-bottom: 2rem;
}
.developer-info {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}
.minors-item {
    background-color: #fafafa;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    border-left: 4px solid #1f77b4;
}
.score-summary {
    background-color: #e8f4fd;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
.footer {
    text-align: center;
    color: #666;
    margin-top: 2rem;
    padding: 1rem;
    border-top: 1px solid #eee;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">MINORS Assessment Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Methodological Index for Non-Randomized Studies</div>', unsafe_allow_html=True)

# Developer information
st.markdown("""
<div class="developer-info">
<h4>👨‍⚕️ Developer Information</h4>
<p><strong>Muhammad Nabeel Saddique</strong><br>
Fourth-year MBBS student at King Edward Medical University, Lahore, Pakistan<br>
Founder of Nibras Research Academy<br>
Passionate about research and systematic review methodology</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation and study management
st.sidebar.title("📋 Study Management")

# Initialize session state
if 'studies_data' not in st.session_state:
    st.session_state.studies_data = []

if 'current_study' not in st.session_state:
    st.session_state.current_study = {}

# MINORS criteria definitions
MINORS_CRITERIA = {
    1: {
        "title": "A clearly stated aim",
        "description": "The question addressed should be precise and relevant in the light of available literature",
        "all_studies": True
    },
    2: {
        "title": "Inclusion of consecutive patients", 
        "description": "All patients potentially fit for inclusion have been included during the study period",
        "all_studies": True
    },
    3: {
        "title": "Prospective collection of data",
        "description": "Data were collected according to a protocol established before the beginning of the study",
        "all_studies": True
    },
    4: {
        "title": "Endpoints appropriate to the aim of the study",
        "description": "Unambiguous explanation of criteria used to evaluate the main outcome",
        "all_studies": True
    },
    5: {
        "title": "Unbiased assessment of the study endpoint",
        "description": "Blind evaluation of objective endpoints and double-blind evaluation of subjective endpoints",
        "all_studies": True
    },
    6: {
        "title": "Follow-up period appropriate to the aim of the study",
        "description": "Follow-up should be sufficiently long to allow assessment of main endpoint",
        "all_studies": True
    },
    7: {
        "title": "Loss to follow up less than 5%",
        "description": "All patients should be included in follow-up or loss should not exceed endpoint proportion",
        "all_studies": True
    },
    8: {
        "title": "Prospective calculation of the study size",
        "description": "Sample size calculation with power analysis and confidence intervals",
        "all_studies": True
    },
    9: {
        "title": "An adequate control group",
        "description": "Gold standard intervention recognized as optimal according to available data",
        "all_studies": False
    },
    10: {
        "title": "Contemporary groups",
        "description": "Control and studied groups managed during the same time period",
        "all_studies": False
    },
    11: {
        "title": "Baseline equivalence of groups",
        "description": "Groups should be similar regarding criteria other than studied endpoints",
        "all_studies": False
    },
    12: {
        "title": "Adequate statistical analyses",
        "description": "Statistics in accordance with study type with confidence intervals",
        "all_studies": False
    }
}

# Sidebar options
option = st.sidebar.selectbox(
    "Choose Action:",
    ["New Assessment", "View All Studies", "Export Data", "About MINORS"]
)

def create_download_link(df, filename, file_format="excel"):
    """Create a download link for the dataframe"""
    if file_format == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='MINORS Assessment')
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx">📥 Download Excel File</a>'
    else:  # CSV
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">📥 Download CSV File</a>'
    
    return href

def calculate_quality_rating(percentage):
    """Calculate quality rating based on percentage score"""
    if percentage > 75:
        return "High Quality", "green"
    elif percentage >= 50:
        return "Moderate Quality", "orange"
    else:
        return "Low Quality", "red"

if option == "New Assessment":
    st.header("📝 New MINORS Assessment")
    
    # Study Information Form
    with st.form("study_info"):
        st.subheader("Study Information")
        col1, col2 = st.columns(2)
        
        with col1:
            study_title = st.text_input("Study Title*", placeholder="Enter the study title")
            first_author = st.text_input("First Author*", placeholder="e.g., Saddique")
            journal = st.text_input("Journal", placeholder="e.g., Journal of Medical Research")
            year = st.number_input("Year", min_value=1950, max_value=2030, value=2025)
            
        with col2:
            study_type = st.selectbox("Study Type*", ["Non-comparative", "Comparative"])
            reviewer_name = st.text_input("Reviewer Name", value="Muhammad Nabeel Saddique")
            pmid = st.text_input("PMID (Optional)", placeholder="PubMed ID")
            notes = st.text_area("Additional Notes", placeholder="Any additional comments about the study")
        
        study_info_submitted = st.form_submit_button("Continue to Assessment")
    
    if study_info_submitted and study_title and first_author:
        st.session_state.current_study = {
            "study_title": study_title,
            "first_author": first_author,
            "journal": journal,
            "year": year,
            "study_type": study_type,
            "reviewer_name": reviewer_name,
            "pmid": pmid,
            "notes": notes,
            "assessment_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        # MINORS Assessment Form
        st.header("🔍 MINORS Assessment")
        
        with st.form("minors_assessment"):
            scores = {}
            
            # Items 1-8 (All studies)
            st.subheader("Items 1-8: All Studies")
            for i in range(1, 9):
                criteria = MINORS_CRITERIA[i]
                st.markdown(f'<div class="minors-item">', unsafe_allow_html=True)
                st.markdown(f"**{i}. {criteria['title']}**")
                st.markdown(f"*{criteria['description']}*")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    score_options = ["0 - Not reported", "1 - Reported but inadequate", "2 - Reported and adequate"]
                    scores[i] = st.radio(f"Score for item {i}:", options=[0, 1, 2], 
                                       format_func=lambda x, opts=score_options: opts[x], 
                                       key=f"score_{i}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Items 9-12 (Comparative studies only)
            if study_type == "Comparative":
                st.subheader("Items 9-12: Additional Criteria for Comparative Studies")
                for i in range(9, 13):
                    criteria = MINORS_CRITERIA[i]
                    st.markdown(f'<div class="minors-item">', unsafe_allow_html=True)
                    st.markdown(f"**{i}. {criteria['title']}**")
                    st.markdown(f"*{criteria['description']}*")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        score_options = ["0 - Not reported", "1 - Reported but inadequate", "2 - Reported and adequate"]
                        scores[i] = st.radio(f"Score for item {i}:", options=[0, 1, 2], 
                                           format_func=lambda x, opts=score_options: opts[x], 
                                           key=f"score_{i}")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            assessment_submitted = st.form_submit_button("Complete Assessment")
            
            if assessment_submitted:
                # Calculate total score
                total_score = sum(scores.values())
                max_score = 16 if study_type == "Non-comparative" else 24
                percentage = round((total_score / max_score) * 100, 1)
                
                # Quality assessment
                quality, quality_color = calculate_quality_rating(percentage)
                
                # Display results
                st.markdown(f'<div class="score-summary">', unsafe_allow_html=True)
                st.markdown(f"### 📊 Assessment Results")
                st.markdown(f"**Total Score:** {total_score}/{max_score}")
                st.markdown(f"**Percentage:** {percentage}%")
                st.markdown(f"**Quality Rating:** <span style='color: {quality_color}; font-weight: bold;'>{quality}</span>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Prepare study data
                study_data = st.session_state.current_study.copy()
                study_data.update({
                    "total_score": total_score,
                    "max_score": max_score,
                    "percentage": percentage,
                    "quality_rating": quality
                })
                
                # Add individual scores
                for i in range(1, 13):
                    if i <= 8 or study_type == "Comparative":
                        study_data[f"item_{i}"] = scores.get(i, "N/A")
                    else:
                        study_data[f"item_{i}"] = "N/A"
                
                # Add to session state
                st.session_state.studies_data.append(study_data)
                
                st.success("✅ Assessment completed and saved!")
                st.balloons()

elif option == "View All Studies":
    st.header("📚 All Assessed Studies")
    
    if st.session_state.studies_data:
        # Convert to DataFrame for display
        df_display = pd.DataFrame(st.session_state.studies_data)
        
        # Select columns for display
        display_cols = ["first_author", "year", "study_title", "study_type", "total_score", "max_score", "percentage", "quality_rating"]
        df_show = df_display[display_cols].copy()
        df_show.columns = ["First Author", "Year", "Study Title", "Study Type", "Total Score", "Max Score", "Percentage (%)", "Quality Rating"]
        
        st.dataframe(df_show, use_container_width=True)
        
        # Individual study details
        if len(st.session_state.studies_data) > 0:
            st.subheader("📋 Study Details")
            study_options = [f"{study['first_author']} et al., {study['year']}" for study in st.session_state.studies_data]
            selected_study_idx = st.selectbox("Select study to view details:", range(len(study_options)), format_func=lambda x: study_options[x])
            
            selected_study = st.session_state.studies_data[selected_study_idx]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Title:** {selected_study['study_title']}")
                st.write(f"**Journal:** {selected_study['journal']}")
                st.write(f"**Type:** {selected_study['study_type']}")
                st.write(f"**Reviewer:** {selected_study['reviewer_name']}")
            
            with col2:
                st.write(f"**Assessment Date:** {selected_study['assessment_date']}")
                st.write(f"**Total Score:** {selected_study['total_score']}/{selected_study['max_score']}")
                st.write(f"**Percentage:** {selected_study['percentage']}%")
                st.write(f"**Quality:** {selected_study['quality_rating']}")
            
            # Show individual scores
            st.subheader("Individual Item Scores")
            score_cols = st.columns(4)
            for i in range(1, 13):
                col_idx = (i - 1) % 4
                if f"item_{i}" in selected_study and selected_study[f"item_{i}"] != "N/A":
                    score_cols[col_idx].metric(f"Item {i}", selected_study[f"item_{i}"])
    
    else:
        st.info("No studies assessed yet. Please start with a new assessment.")

elif option == "Export Data":
    st.header("📤 Export Assessment Data")
    
    if st.session_state.studies_data:
        # Create comprehensive DataFrame
        df_export = pd.DataFrame(st.session_state.studies_data)
        
        # Reorder columns for better presentation
        base_cols = ["first_author", "year", "study_title", "journal", "study_type", "reviewer_name", "assessment_date"]
        score_cols = [f"item_{i}" for i in range(1, 13)]
        summary_cols = ["total_score", "max_score", "percentage", "quality_rating", "pmid", "notes"]
        
        # Reorder DataFrame
        all_cols = base_cols + score_cols + summary_cols
        df_export = df_export.reindex(columns=[col for col in all_cols if col in df_export.columns])
        
        # Rename columns for better readability
        column_mapping = {
            "first_author": "First Author",
            "year": "Year",
            "study_title": "Study Title",
            "journal": "Journal",
            "study_type": "Study Type",
            "reviewer_name": "Reviewer",
            "assessment_date": "Assessment Date",
            "total_score": "Total Score",
            "max_score": "Max Score",
            "percentage": "Percentage (%)",
            "quality_rating": "Quality Rating",
            "pmid": "PMID",
            "notes": "Notes"
        }
        
        # Add item column mappings
        for i in range(1, 13):
            column_mapping[f"item_{i}"] = f"Item {i}"
        
        df_export = df_export.rename(columns=column_mapping)
        
        # Display preview
        st.subheader("📊 Data Preview")
        st.dataframe(df_export, use_container_width=True)
        
        # Export options
        st.subheader("💾 Download Options")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Excel Format")
            st.markdown(create_download_link(df_export, "MINORS_Assessment_Results", "excel"), unsafe_allow_html=True)
            
        with col2:
            st.markdown("### CSV Format")
            st.markdown(create_download_link(df_export, "MINORS_Assessment_Results", "csv"), unsafe_allow_html=True)
        
        # Statistics
        st.subheader("📈 Assessment Statistics")
        total_studies = len(st.session_state.studies_data)
        comparative_studies = len([s for s in st.session_state.studies_data if s['study_type'] == 'Comparative'])
        non_comparative_studies = total_studies - comparative_studies
        
        if total_studies > 0:
            avg_score_comp = sum([s['percentage'] for s in st.session_state.studies_data if s['study_type'] == 'Comparative']) / max(comparative_studies, 1)
            avg_score_non_comp = sum([s['percentage'] for s in st.session_state.studies_data if s['study_type'] == 'Non-comparative']) / max(non_comparative_studies, 1)
            overall_avg = (avg_score_comp * comparative_studies + avg_score_non_comp * non_comparative_studies) / total_studies
        else:
            overall_avg = 0
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Studies", total_studies)
        col2.metric("Comparative Studies", comparative_studies)
        col3.metric("Non-comparative Studies", non_comparative_studies)
        col4.metric("Overall Avg Quality", f"{round(overall_avg, 1)}%")
        
    else:
        st.info("No data to export. Please complete some assessments first.")

elif option == "About MINORS":
    st.header("📖 About MINORS")
    
    st.markdown("""
    ### Methodological Index for Non-Randomized Studies (MINORS)
    
    The MINORS instrument is a validated tool designed to assess the methodological quality of non-randomized studies, 
    both comparative and non-comparative. It was developed by Slim et al. and published in the ANZ Journal of Surgery in 2003.
    
    #### 🎯 Purpose
    - Evaluate methodological quality of observational studies
    - Support systematic reviews and meta-analyses
    - Assist in manuscript review and publication decisions
    - Enhance evidence-based medicine practices
    
    #### 📊 Validation
    - **Inter-reviewer agreement:** κ > 0.4 (satisfactory for all items)
    - **Test-retest reliability:** High correlation after 2-month interval
    - **Internal consistency:** Cronbach's α = 0.73 (good)
    - **External validity:** Validated against randomized controlled trials
    
    #### 🔍 Assessment Criteria
    
    **Items 1-8: All Studies**
    1. Clearly stated aim
    2. Inclusion of consecutive patients
    3. Prospective collection of data
    4. Endpoints appropriate to study aim
    5. Unbiased assessment of endpoints
    6. Appropriate follow-up period
    7. Loss to follow-up less than 5%
    8. Prospective calculation of study size
    
    **Items 9-12: Comparative Studies Only**
    9. Adequate control group
    10. Contemporary groups
    11. Baseline equivalence of groups
    12. Adequate statistical analyses
    
    #### 📚 Citation
    ```
    Slim K, Nini E, Forestier D, Kwiatkowski F, Panis Y, Chipponi J. 
    Methodological index for non-randomized studies (MINORS): development 
    and validation of a new instrument. ANZ J Surg. 2003;73:712-716.
    ```
    """)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
<p><strong>MINORS Assessment Tool</strong> | Developed by Muhammad Nabeel Saddique | Nibras Research Academy</p>
<p><em>Citation: Slim K, et al. Methodological index for non-randomized studies (MINORS): development and validation of a new instrument. ANZ J Surg. 2003;73:712-716.</em></p>
<p>King Edward Medical University, Lahore, Pakistan</p>
</div>
""", unsafe_allow_html=True)

# Reset data option (for development/testing)
if st.sidebar.button("🗑️ Clear All Data", type="secondary"):
    if st.sidebar.button("⚠️ Confirm Clear", type="secondary"):
        st.session_state.studies_data = []
        st.session_state.current_study = {}
        st.sidebar.success("All data cleared!")

# Version info
st.sidebar.markdown("---")
st.sidebar.markdown("**Version:** 1.0.0")
st.sidebar.markdown("**Last Updated:** 2025")
