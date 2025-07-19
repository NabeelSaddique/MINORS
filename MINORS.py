"""
MINORS Assessment Tool - Enhanced Version
A modern Streamlit web application for conducting MINORS assessments

Developer: Muhammad Nabeel Saddique
Institution: King Edward Medical University, Lahore, Pakistan
Organization: Nibras Research Academy
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime
import base64

# Page configuration
st.set_page_config(
    page_title="MINORS Assessment Tool",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
/* Main styling */
.main-header {
    background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
    color: white;
    padding: 2rem;
    border-radius: 1rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.main-title {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.main-subtitle {
    font-size: 1.2rem;
    opacity: 0.9;
}

/* Developer info card */
.dev-card {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border: 1px solid #cbd5e1;
    border-radius: 1rem;
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* Assessment items */
.assessment-item {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 0.75rem;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
}

.assessment-item:hover {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-color: #3b82f6;
}

/* Score summary */
.score-card {
    background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    border: 1px solid #10b981;
    border-radius: 1rem;
    padding: 2rem;
    margin: 2rem 0;
    text-align: center;
}

/* Instructions panel */
.instruction-panel {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    padding: 1rem;
    margin-bottom: 1rem;
    font-size: 0.9rem;
}

/* Sidebar enhancements */
.sidebar-metric {
    background: white;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
    border-left: 4px solid #3b82f6;
}

/* Status indicators */
.status-success {
    color: #10b981;
    font-weight: bold;
}

.status-warning {
    color: #f59e0b;
    font-weight: bold;
}

.status-error {
    color: #ef4444;
    font-weight: bold;
}

/* Form improvements */
.stSelectbox > div > div {
    border-radius: 0.5rem;
}

.stTextInput > div > div {
    border-radius: 0.5rem;
}

/* Progress indicator */
.progress-bar {
    background: #e5e7eb;
    border-radius: 1rem;
    height: 0.5rem;
    margin: 1rem 0;
}

.progress-fill {
    background: linear-gradient(90deg, #3b82f6, #10b981);
    height: 100%;
    border-radius: 1rem;
    transition: width 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

# Enhanced MINORS criteria with detailed instructions
MINORS_CRITERIA = {
    1: {
        "title": "A clearly stated aim",
        "description": "The question addressed should be precise and relevant in the light of available literature",
        "instruction": """
        **What to look for:**
        • Clear research question or hypothesis
        • Specific objectives stated
        • Relevance to existing literature mentioned
        
        **Score 2:** Clear, precise aim with specific research question
        **Score 1:** Aim stated but vague or incomplete
        **Score 0:** No clear aim or research question stated
        """,
        "all_studies": True
    },
    2: {
        "title": "Inclusion of consecutive patients",
        "description": "All patients potentially fit for inclusion have been included during the study period",
        "instruction": """
        **What to look for:**
        • Clear inclusion/exclusion criteria
        • Statement about consecutive enrollment
        • Explanation of any excluded patients
        
        **Score 2:** Consecutive patients clearly stated with reasons for exclusions
        **Score 1:** Some mention of patient selection but incomplete
        **Score 0:** No information about patient selection process
        """,
        "all_studies": True
    },
    3: {
        "title": "Prospective collection of data",
        "description": "Data were collected according to a protocol established before the beginning of the study",
        "instruction": """
        **What to look for:**
        • Mention of prospective data collection
        • Pre-established protocol or methodology
        • Timeline of data collection
        
        **Score 2:** Clearly prospective with pre-established protocol
        **Score 1:** Some prospective elements but incomplete
        **Score 0:** Retrospective or no mention of data collection timing
        """,
        "all_studies": True
    },
    4: {
        "title": "Endpoints appropriate to the aim of the study",
        "description": "Unambiguous explanation of criteria used to evaluate the main outcome",
        "instruction": """
        **What to look for:**
        • Primary and secondary outcomes clearly defined
        • Outcome measures appropriate to research question
        • Intention-to-treat analysis mentioned
        
        **Score 2:** Well-defined endpoints matching study aims
        **Score 1:** Endpoints defined but some ambiguity
        **Score 0:** Poorly defined or inappropriate endpoints
        """,
        "all_studies": True
    },
    5: {
        "title": "Unbiased assessment of the study endpoint",
        "description": "Blind evaluation of objective endpoints and double-blind evaluation of subjective endpoints",
        "instruction": """
        **What to look for:**
        • Blinding of outcome assessors
        • Objective vs subjective outcome measures
        • Methods to minimize bias
        
        **Score 2:** Appropriate blinding for outcome type
        **Score 1:** Some bias control but incomplete
        **Score 0:** No mention of bias control in assessment
        """,
        "all_studies": True
    },
    6: {
        "title": "Follow-up period appropriate to the aim of the study",
        "description": "Follow-up should be sufficiently long to allow assessment of main endpoint",
        "instruction": """
        **What to look for:**
        • Duration of follow-up specified
        • Appropriateness for detecting outcomes
        • Justification for follow-up period
        
        **Score 2:** Follow-up duration appropriate and justified
        **Score 1:** Follow-up mentioned but may be inadequate
        **Score 0:** No follow-up information or clearly inadequate
        """,
        "all_studies": True
    },
    7: {
        "title": "Loss to follow up less than 5%",
        "description": "All patients should be included in follow-up or loss should not exceed endpoint proportion",
        "instruction": """
        **What to look for:**
        • Percentage of patients lost to follow-up
        • Reasons for loss to follow-up
        • Impact on study validity
        
        **Score 2:** <5% loss to follow-up or acceptable given endpoint rate
        **Score 1:** 5-10% loss with some explanation
        **Score 0:** >10% loss or no information provided
        """,
        "all_studies": True
    },
    8: {
        "title": "Prospective calculation of the study size",
        "description": "Sample size calculation with power analysis and confidence intervals",
        "instruction": """
        **What to look for:**
        • Sample size calculation provided
        • Power analysis (usually 80% power)
        • Alpha level specified (usually 0.05)
        • Effect size assumptions
        
        **Score 2:** Complete sample size calculation with power analysis
        **Score 1:** Some sample size consideration but incomplete
        **Score 0:** No sample size calculation mentioned
        """,
        "all_studies": True
    },
    9: {
        "title": "An adequate control group",
        "description": "Gold standard intervention recognized as optimal according to available data",
        "instruction": """
        **What to look for:**
        • Control group represents current standard of care
        • Control intervention well-described
        • Justification for control choice
        
        **Score 2:** Gold standard control group well-justified
        **Score 1:** Adequate control but some limitations
        **Score 0:** Poor control group or inadequately described
        """,
        "all_studies": False
    },
    10: {
        "title": "Contemporary groups",
        "description": "Control and studied groups managed during the same time period",
        "instruction": """
        **What to look for:**
        • Both groups treated in same time period
        • No historical controls
        • Similar treatment conditions
        
        **Score 2:** Clearly contemporary groups
        **Score 1:** Mostly contemporary with minor time differences
        **Score 0:** Historical controls or significant time differences
        """,
        "all_studies": False
    },
    11: {
        "title": "Baseline equivalence of groups",
        "description": "Groups should be similar regarding criteria other than studied endpoints",
        "instruction": """
        **What to look for:**
        • Baseline characteristics compared
        • Statistical testing of baseline differences
        • Important confounders addressed
        
        **Score 2:** Groups well-matched with statistical comparison
        **Score 1:** Some baseline comparison but incomplete
        **Score 0:** No baseline comparison or significant differences
        """,
        "all_studies": False
    },
    12: {
        "title": "Adequate statistical analyses",
        "description": "Statistics in accordance with study type with confidence intervals",
        "instruction": """
        **What to look for:**
        • Appropriate statistical tests for data type
        • Confidence intervals provided
        • Multiple comparisons addressed
        • Statistical software mentioned
        
        **Score 2:** Appropriate statistics with confidence intervals
        **Score 1:** Adequate statistics but some limitations
        **Score 0:** Inappropriate or inadequate statistical analysis
        """,
        "all_studies": False
    }
}

# Initialize session state
if 'studies_data' not in st.session_state:
    st.session_state.studies_data = []
if 'current_study' not in st.session_state:
    st.session_state.current_study = {}
if 'current_scores' not in st.session_state:
    st.session_state.current_scores = {}
if 'assessment_started' not in st.session_state:
    st.session_state.assessment_started = False

# Header
st.markdown("""
<div class="main-header">
    <div class="main-title">🔬 MINORS Assessment Tool</div>
    <div class="main-subtitle">Methodological Index for Non-Randomized Studies</div>
</div>
""", unsafe_allow_html=True)

# Enhanced sidebar
with st.sidebar:
    st.title("📊 Dashboard")
    
    # Study statistics
    total_studies = len(st.session_state.studies_data)
    st.markdown(f"""
    <div class="sidebar-metric">
        <h4>📈 Statistics</h4>
        <p><strong>Total Studies:</strong> {total_studies}</p>
        <p><strong>High Quality:</strong> {len([s for s in st.session_state.studies_data if s.get('percentage', 0) > 75])}</p>
        <p><strong>Moderate Quality:</strong> {len([s for s in st.session_state.studies_data if 50 <= s.get('percentage', 0) <= 75])}</p>
        <p><strong>Low Quality:</strong> {len([s for s in st.session_state.studies_data if s.get('percentage', 0) < 50])}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    st.markdown("### 🧭 Navigation")
    page = st.radio(
        "Choose Action:",
        ["🆕 New Assessment", "📚 View Studies", "📤 Export Data", "ℹ️ About MINORS"],
        key="navigation"
    )
    
    # Assessment progress
    if st.session_state.assessment_started:
        st.markdown("### 📋 Current Assessment")
        if st.session_state.current_study:
            st.write(f"**Study:** {st.session_state.current_study.get('study_title', 'Untitled')[:30]}...")
            st.write(f"**Author:** {st.session_state.current_study.get('first_author', 'Unknown')}")
            
            # Progress calculation
            total_items = 8 if st.session_state.current_study.get('study_type') == 'Non-comparative' else 12
            completed_items = len(st.session_state.current_scores)
            progress = (completed_items / total_items) * 100
            
            st.markdown(f"""
            <div style="margin: 1rem 0;">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {progress}%"></div>
                </div>
                <small>{completed_items}/{total_items} items completed</small>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("🗑️ Clear Current Assessment", type="secondary"):
        st.session_state.current_study = {}
        st.session_state.current_scores = {}
        st.session_state.assessment_started = False
        st.success("Assessment cleared!")
        st.rerun()
    
    if st.button("💾 Save & New", type="primary"):
        if st.session_state.current_study and len(st.session_state.current_scores) > 0:
            # Save current assessment
            save_current_assessment()
            # Clear for new assessment
            st.session_state.current_study = {}
            st.session_state.current_scores = {}
            st.session_state.assessment_started = False
            st.success("Assessment saved! Ready for new assessment.")
            st.rerun()

# Developer info
st.markdown("""
<div class="dev-card">
    <h4>👨‍⚕️ Developer Information</h4>
    <p><strong>Muhammad Nabeel Saddique</strong> • Fourth-year MBBS student at King Edward Medical University, Lahore, Pakistan</p>
    <p><strong>Nibras Research Academy</strong> • Mentoring young researchers in systematic review and meta-analysis</p>
</div>
""", unsafe_allow_html=True)

# Helper functions
@st.cache_data
def get_quality_rating(percentage):
    """Calculate quality rating based on percentage score"""
    if percentage > 75:
        return "High Quality", "#10b981", "🟢"
    elif percentage >= 50:
        return "Moderate Quality", "#f59e0b", "🟡"
    else:
        return "Low Quality", "#ef4444", "🔴"

def save_current_assessment():
    """Save the current assessment to studies data"""
    if not st.session_state.current_study or not st.session_state.current_scores:
        return False
    
    # Calculate scores
    total_score = sum(st.session_state.current_scores.values())
    study_type = st.session_state.current_study.get('study_type', 'Non-comparative')
    max_score = 16 if study_type == "Non-comparative" else 24
    percentage = round((total_score / max_score) * 100, 1)
    quality, color, icon = get_quality_rating(percentage)
    
    # Prepare study data
    study_data = st.session_state.current_study.copy()
    study_data.update({
        "total_score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "quality_rating": quality,
        "assessment_date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    
    # Add individual scores
    for i in range(1, 13):
        study_data[f"item_{i}"] = st.session_state.current_scores.get(i, "N/A")
    
    # Add to studies data
    st.session_state.studies_data.append(study_data)
    return True

def create_download_link(df, filename, file_format="excel"):
    """Create download link for dataframe"""
    if file_format == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='MINORS Assessment')
        output.seek(0)
        b64 = base64.b64encode(output.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx" style="display: inline-block; padding: 0.5rem 1rem; background: #3b82f6; color: white; text-decoration: none; border-radius: 0.5rem;">📥 Download Excel</a>'
    else:
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv" style="display: inline-block; padding: 0.5rem 1rem; background: #10b981; color: white; text-decoration: none; border-radius: 0.5rem;">📥 Download CSV</a>'
    
    return href

# Main content based on selected page
if page == "🆕 New Assessment":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 New MINORS Assessment")
        
        # Study information form
        if not st.session_state.assessment_started:
            with st.form("study_info_form", clear_on_submit=False):
                st.subheader("📋 Study Information")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    study_title = st.text_input("Study Title*", placeholder="Enter the complete study title")
                    first_author = st.text_input("First Author*", placeholder="e.g., Saddique")
                    journal = st.text_input("Journal", placeholder="e.g., Journal of Medical Research")
                    
                with col_b:
                    year = st.number_input("Publication Year", min_value=1950, max_value=2030, value=2025)
                    study_type = st.selectbox("Study Type*", ["Non-comparative", "Comparative"])
                    reviewer_name = st.text_input("Reviewer Name", value="Muhammad Nabeel Saddique")
                
                pmid = st.text_input("PMID (Optional)", placeholder="PubMed ID if available")
                notes = st.text_area("Additional Notes", placeholder="Any relevant comments about the study")
                
                if st.form_submit_button("🚀 Start Assessment", type="primary"):
                    if study_title and first_author:
                        st.session_state.current_study = {
                            "study_title": study_title,
                            "first_author": first_author,
                            "journal": journal,
                            "year": year,
                            "study_type": study_type,
                            "reviewer_name": reviewer_name,
                            "pmid": pmid,
                            "notes": notes
                        }
                        st.session_state.assessment_started = True
                        st.session_state.current_scores = {}
                        st.success("✅ Study information saved! Proceed with MINORS assessment.")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in required fields: Study Title and First Author")
        
        # MINORS assessment form
        elif st.session_state.assessment_started:
            st.subheader(f"🔍 MINORS Assessment: {st.session_state.current_study['study_title'][:50]}...")
            
            study_type = st.session_state.current_study.get('study_type', 'Non-comparative')
            max_items = 8 if study_type == "Non-comparative" else 12
            
            # Assessment items
            for i in range(1, max_items + 1):
                if i == 9 and study_type == "Non-comparative":
                    break
                    
                criteria = MINORS_CRITERIA[i]
                
                st.markdown(f"""
                <div class="assessment-item">
                    <h4>{i}. {criteria['title']}</h4>
                    <p style="color: #6b7280; margin-bottom: 1rem;">{criteria['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col_score, col_inst = st.columns([1, 1])
                
                with col_score:
                    score_options = [
                        "0 - Not reported",
                        "1 - Reported but inadequate", 
                        "2 - Reported and adequate"
                    ]
                    
                    current_score = st.session_state.current_scores.get(i, 0)
                    score = st.radio(
                        f"Score for Item {i}:",
                        options=[0, 1, 2],
                        format_func=lambda x: score_options[x],
                        key=f"score_{i}",
                        index=current_score
                    )
                    
                    # Update scores in real-time
                    st.session_state.current_scores[i] = score
                
                with col_inst:
                    with st.expander("📖 Detailed Instructions"):
                        st.markdown(criteria['instruction'])
                
                st.markdown("---")
            
            # Real-time score display
            if st.session_state.current_scores:
                total_score = sum(st.session_state.current_scores.values())
                max_score = 16 if study_type == "Non-comparative" else 24
                percentage = round((total_score / max_score) * 100, 1)
                quality, color, icon = get_quality_rating(percentage)
                
                st.markdown(f"""
                <div class="score-card">
                    <h3>📊 Current Assessment Score</h3>
                    <h2 style="color: {color};">{icon} {total_score}/{max_score} ({percentage}%)</h2>
                    <h4 style="color: {color};">{quality}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col_save, col_reset = st.columns(2)
                with col_save:
                    if st.button("💾 Save Assessment", type="primary"):
                        if save_current_assessment():
                            st.success("✅ Assessment saved successfully!")
                            st.session_state.current_study = {}
                            st.session_state.current_scores = {}
                            st.session_state.assessment_started = False
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Error saving assessment")
                
                with col_reset:
                    if st.button("🔄 Reset Scores", type="secondary"):
                        st.session_state.current_scores = {}
                        st.rerun()
    
    with col2:
        st.markdown("### 📚 MINORS Quick Reference")
        
        with st.expander("🎯 Quality Thresholds"):
            st.markdown("""
            - **High Quality:** >75% (>12/16 or >18/24)
            - **Moderate Quality:** 50-75% (8-12/16 or 12-18/24)
            - **Low Quality:** <50% (<8/16 or <12/24)
            """)
        
        with st.expander("📊 Scoring Guidelines"):
            st.markdown("""
            **Score 2:** Reported and adequate
            - All required information present
            - Methodology clearly described
            - Meets scientific standards
            
            **Score 1:** Reported but inadequate
            - Some information present
            - Incomplete or unclear methodology
            - Partially meets standards
            
            **Score 0:** Not reported
            - Information not provided
            - Cannot assess quality
            - Does not meet standards
            """)

elif page == "📚 View Studies":
    st.header("📚 Assessed Studies Database")
    
    if st.session_state.studies_data:
        # Create DataFrame
        df = pd.DataFrame(st.session_state.studies_data)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Studies", len(df))
        with col2:
            high_quality = len(df[df['percentage'] > 75])
            st.metric("High Quality", high_quality)
        with col3:
            moderate_quality = len(df[(df['percentage'] >= 50) & (df['percentage'] <= 75)])
            st.metric("Moderate Quality", moderate_quality)
        with col4:
            avg_quality = round(df['percentage'].mean(), 1)
            st.metric("Average Quality", f"{avg_quality}%")
        
        # Studies table
        display_df = df[['first_author', 'year', 'study_title', 'study_type', 'total_score', 'max_score', 'percentage', 'quality_rating']].copy()
        display_df.columns = ['Author', 'Year', 'Title', 'Type', 'Score', 'Max', 'Percentage', 'Quality']
        
        st.dataframe(display_df, use_container_width=True)
        
        # Study details
        if len(df) > 0:
            st.subheader("📋 Study Details")
            study_options = [f"{row['first_author']} et al., {row['year']}" for _, row in df.iterrows()]
            selected_idx = st.selectbox("Select study:", range(len(study_options)), format_func=lambda x: study_options[x])
            
            selected_study = df.iloc[selected_idx]
            
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
                quality, color, icon = get_quality_rating(selected_study['percentage'])
                st.markdown(f"**Quality:** <span style='color: {color}'>{icon} {quality}</span>", unsafe_allow_html=True)
            
            # Individual scores
            st.subheader("Individual Item Scores")
            score_cols = st.columns(6)
            for i in range(1, 13):
                col_idx = (i - 1) % 6
                if f"item_{i}" in selected_study and selected_study[f"item_{i}"] != "N/A":
                    score_cols[col_idx].metric(f"Item {i}", f"{selected_study[f'item_{i}']}/2")
    else:
        st.info("No studies assessed yet. Start with a new assessment!")

elif page == "📤 Export Data":
    st.header("📤 Export Assessment Data")
    
    if st.session_state.studies_data:
        df = pd.DataFrame(st.session_state.studies_data)
        
        # Reorder and rename columns
        base_cols = ["first_author", "year", "study_title", "journal", "study_type", "reviewer_name", "assessment_date"]
        score_cols = [f"item_{i}" for i in range(1, 13)]
        summary_cols = ["total_score", "max_score", "percentage", "quality_rating", "pmid", "notes"]
        
        export_df = df.reindex(columns=base_cols + score_cols + summary_cols)
        
        # Rename columns
        column_mapping = {
            "first_author": "First Author", "year": "Year", "study_title": "Study Title",
            "journal": "Journal", "study_type": "Study Type", "reviewer_name": "Reviewer",
            "assessment_date": "Assessment Date", "total_score": "Total Score",
            "max_score": "Max Score", "percentage": "Percentage (%)",
            "quality_rating": "Quality Rating", "pmid": "PMID", "notes": "Notes"
        }
        
        for i in range(1, 13):
            column_mapping[f"item_{i}"] = f"Item {i}"
        
        export_df = export_df.rename(columns=column_mapping)
        
        # Display preview
        st.subheader("📊 Data Preview")
        st.dataframe(export_df, use_container_width=True)
        
        # Download options
        st.subheader("💾 Download Options")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(create_download_link(export_df, "MINORS_Assessment_Results", "excel"), unsafe_allow_html=True)
        with col2:
            st.markdown(create_download_link(export_df, "MINORS_Assessment_Results", "csv"), unsafe_allow_html=True)
        
    else:
        st.info("No data to export. Complete some assessments first!")

else:  # About MINORS
    st.header("ℹ️ About MINORS")
    
    tab1, tab2, tab3 = st.tabs(["📖 Overview", "🔍 Criteria", "📚 Citation"])
    
    with tab1:
        st.markdown("""
        ### Methodological Index for Non-Randomized Studies (MINORS)
        
        The MINORS instrument is a validated tool designed to assess the methodological quality of non-randomized studies.
        
        #### 🎯 Purpose
        - Evaluate methodological quality of observational studies
        - Support systematic reviews and meta-analyses
        - Assist in manuscript review decisions
        - Enhance evidence-based medicine practices
        
        #### 📊 Validation Results
        - **Inter-reviewer agreement:** κ > 0.4 (satisfactory)
        - **Test-retest reliability:** High correlation after 2 months
        - **Internal consistency:** Cronbach's α = 0.73 (good)
        - **External validity:** Validated against RCTs
        """)
    
    with tab2:
        st.markdown("### 🔍 MINORS Assessment Criteria")
        
        st.markdown("#### Items 1-8: All Studies")
        for i in range(1, 9):
            with st.expander(f"{i}. {MINORS_CRITERIA[i]['title']}"):
                st.markdown(MINORS_CRITERIA[i]['instruction'])
        
        st.markdown("#### Items 9-12: Comparative Studies Only")
        for i in range(9, 13):
            with st.expander(f"{i}. {MINORS_CRITERIA[i]['title']}"):
                st.markdown(MINORS_CRITERIA[i]['instruction'])
    
    with tab3:
        st.markdown("""
        ### 📚 Citation Information
        
        **Original MINORS Paper:**
        ```
        Slim K, Nini E, Forestier D, Kwiatkowski F, Panis Y, Chipponi J. 
        Methodological index for non-randomized studies (MINORS): development 
        and validation of a new instrument. ANZ J Surg. 2003;73:712-716.
        ```
        
        **This Tool:**
        ```
        Saddique, M. N. (2025). MINORS Assessment Tool: A Streamlit web application 
        for conducting Methodological Index for Non-Randomized Studies assessments. 
        Version 2.0. Nibras Research Academy.
        ```
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 2rem;">
    <p><strong>MINORS Assessment Tool v2.0</strong> | Developed by Muhammad Nabeel Saddique | Nibras Research Academy</p>
    <p>King Edward Medical University, Lahore, Pakistan | <em>Enhancing research methodology worldwide</em></p>
</div>
""", unsafe_allow_html=True)
