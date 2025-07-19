# MINORS Assessment Tool 📊

A comprehensive Streamlit web application for conducting **Methodological Index for Non-Randomized Studies (MINORS)** assessments, designed for systematic reviews and meta-analyses.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

## 🎯 About

The MINORS Assessment Tool is a digital implementation of the validated **Methodological Index for Non-Randomized Studies** developed by Slim et al. (2003). This tool enables researchers to systematically evaluate the methodological quality of non-randomized studies in their systematic reviews and meta-analyses.

### 🔬 Developer Information

**Muhammad Nabeel Saddique**
- Fourth-year MBBS student at King Edward Medical University, Lahore, Pakistan
- Founder of **Nibras Research Academy**
- Passionate about research methodology and evidence synthesis
- Expert in systematic review tools: Rayyan, Zotero, EndNote, WebPlotDigitizer, Meta-Converter, RevMan, MetaXL, Jamovi, CMA, OpenMeta, and R Studio

## ✨ Features

### 📋 Comprehensive Assessment
- **All 12 MINORS criteria** with detailed descriptions
- **Automatic scoring** (0-2 points per criterion)
- **Study type differentiation** (Comparative vs Non-comparative)
- **Real-time quality rating** (High/Moderate/Low quality)

### 💾 Data Management
- **Study database** with complete information storage
- **Professional export** to Excel and CSV formats
- **Citation-ready format** (e.g., "Saddique et al., 2025")
- **Batch assessment** capabilities

### 📊 Analytics Dashboard
- **Assessment statistics** and quality distribution
- **Individual study details** with score breakdowns
- **Reviewer tracking** and assessment dates
- **Study comparison** features

### 🎨 User Experience
- **Intuitive interface** designed for researchers
- **Responsive design** for desktop and mobile
- **Professional styling** suitable for academic use
- **Error handling** and data validation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/minors-assessment-tool.git
cd minors-assessment-tool
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

4. **Open your browser** and navigate to `http://localhost:8501`

### Docker Installation

```bash
# Build the image
docker build -t minors-tool .

# Run the container
docker run -p 8501:8501 minors-tool
```

## 📖 Usage Guide

### 1. New Assessment
- Enter study information (title, author, journal, year, type)
- Complete the MINORS assessment for all applicable criteria
- Review and save the assessment

### 2. View Studies
- Browse all completed assessments
- View detailed scores and quality ratings
- Compare studies side-by-side

### 3. Export Data
- Download assessments in Excel or CSV format
- Generate publication-ready tables
- Export statistics and summaries

## 🧮 MINORS Criteria

### Items 1-8: All Studies
1. **Clearly stated aim** - Precise and relevant research question
2. **Consecutive patients** - All eligible patients included
3. **Prospective data collection** - Pre-established protocol
4. **Appropriate endpoints** - Outcomes match study aims
5. **Unbiased assessment** - Blinded evaluation when possible
6. **Appropriate follow-up** - Sufficient duration for outcomes
7. **Loss to follow-up <5%** - Minimal patient attrition
8. **Sample size calculation** - Power analysis and statistical planning

### Items 9-12: Comparative Studies Only
9. **Adequate control group** - Gold standard comparison
10. **Contemporary groups** - Same time period management
11. **Baseline equivalence** - Matched groups
12. **Adequate statistics** - Appropriate analytical methods

## 📚 Scientific Background

### Citation
```
Slim K, Nini E, Forestier D, Kwiatkowski F, Panis Y, Chipponi J. 
Methodological index for non-randomized studies (MINORS): development 
and validation of a new instrument. ANZ J Surg. 2003;73:712-716.
```

### Validation
- **Inter-reviewer agreement:** κ > 0.4 (satisfactory)
- **Test-retest reliability:** High correlation after 2 months
- **Internal consistency:** Cronbach's α = 0.73 (good)
- **External validity:** Validated against randomized controlled trials

## 🏥 Use Cases

### Academic Research
- **Systematic reviews** and meta-analyses
- **Quality assessment** for evidence synthesis
- **Manuscript preparation** and peer review
- **Research methodology** training

### Clinical Applications
- **Evidence-based medicine** practice
- **Clinical guideline** development
- **Quality improvement** initiatives
- **Research proposal** evaluation

## 🤝 Contributing

We welcome contributions to improve the MINORS Assessment Tool! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone the repo
git clone https://github.com/yourusername/minors-assessment-tool.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run the app
streamlit run app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Slim K et al.** for developing and validating the original MINORS instrument
- **Nibras Research Academy** for supporting research methodology education

## 📞 Contact

**Muhammad Nabeel Saddique**
- 🎓 King Edward Medical University, Lahore, Pakistan
- 🏢 Nibras Research Academy
- 📧 nabeelsaddique@kemu.edu.pk


## 🌟 Support

If you find this tool helpful for your research, please consider:
- ⭐ **Starring** this repository
- 🔄 **Sharing** with fellow researchers
- 🐛 **Reporting** issues and suggesting improvements
- 🤝 **Contributing** to the project

---

**Made with ❤️ for the research community by Nibras Research Academy**