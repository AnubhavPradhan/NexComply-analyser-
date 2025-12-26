"""
NexComply Analyzer - Streamlit Dashboard

Enterprise-grade GRC automation platform with comprehensive UI.

Note: Install the package in development mode with `pip install -e .` 
      before running this application.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from io import BytesIO

try:
    from src.models.compliance_analyzer import RAGComplianceAnalyzer
    from src.models.risk_assessor import AdvancedRiskAssessor, RiskFactor
    from src.data.framework_loader import FrameworkLoader
    from src.data.policy_processor import PolicyProcessor
    from src.utils.reporting import ReportGenerator
    from src.config.settings import get_settings
except ImportError:
    st.error("""
    ⚠️ Import Error: Cannot find the NexComply modules.
    
    Please install the package in development mode:
    ```
    pip install -e .
    ```
    
    Or run from the project root directory.
    """)
    st.stop()

# Page configuration
st.set_page_config(
    page_title="NexComply Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
    }
    div[data-testid="stSidebarNav"] {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None
if 'risk_assessor' not in st.session_state:
    st.session_state.risk_assessor = None
if 'framework_loader' not in st.session_state:
    st.session_state.framework_loader = None
if 'policy_processor' not in st.session_state:
    st.session_state.policy_processor = None
if 'report_generator' not in st.session_state:
    st.session_state.report_generator = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'risk_results' not in st.session_state:
    st.session_state.risk_results = None


def initialize_components():
    """Initialize application components."""
    settings = get_settings()
    
    if st.session_state.framework_loader is None:
        st.session_state.framework_loader = FrameworkLoader()
    
    if st.session_state.policy_processor is None:
        st.session_state.policy_processor = PolicyProcessor()
    
    if st.session_state.report_generator is None:
        st.session_state.report_generator = ReportGenerator()
    
    if st.session_state.risk_assessor is None:
        st.session_state.risk_assessor = AdvancedRiskAssessor()


def render_sidebar():
    """Render sidebar with navigation and quick stats."""
    with st.sidebar:
        st.markdown('<h1 style="color: #1f77b4;">🛡️ NexComply</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### Quick Stats")
        
        if st.session_state.analysis_results:
            gaps = st.session_state.analysis_results
            st.metric("Total Gaps", len(gaps))
            critical = sum(1 for g in gaps if g.get('severity') == 'Critical')
            st.metric("Critical Gaps", critical)
        else:
            st.info("Run analysis to see stats")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        **NexComply Analyzer** is an enterprise-grade GRC automation platform 
        with RAG capabilities for compliance analysis and risk assessment.
        """)
        
        st.markdown("---")
        st.markdown("**Version:** 1.0.0")
        st.markdown("**Last Updated:** Dec 2024")


def page_dashboard():
    """Main dashboard page with KPIs and visualizations."""
    st.markdown('<div class="main-header">📊 Dashboard</div>', unsafe_allow_html=True)
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Overall Compliance",
            value="78%",
            delta="5%"
        )
    
    with col2:
        st.metric(
            label="Critical Gaps",
            value="12",
            delta="-3"
        )
    
    with col3:
        st.metric(
            label="Risk Score",
            value="15.2",
            delta="-2.1"
        )
    
    with col4:
        st.metric(
            label="Open Items",
            value="45",
            delta="8"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Compliance by Framework")
        
        # Sample data
        framework_data = pd.DataFrame({
            'Framework': ['ISO27001', 'NIST-CSF', 'SOC2', 'GDPR', 'HIPAA'],
            'Compliance': [85, 72, 90, 68, 75]
        })
        
        fig = px.bar(
            framework_data,
            x='Framework',
            y='Compliance',
            color='Compliance',
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Risk Distribution")
        
        # Sample data
        risk_data = pd.DataFrame({
            'Risk Level': ['Critical', 'High', 'Medium', 'Low'],
            'Count': [5, 12, 23, 15]
        })
        
        fig = px.pie(
            risk_data,
            values='Count',
            names='Risk Level',
            color='Risk Level',
            color_discrete_map={
                'Critical': '#d62728',
                'High': '#ff7f0e',
                'Medium': '#ffbb00',
                'Low': '#2ca02c'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Timeline
    st.subheader("Compliance Trend")
    
    # Sample timeline data
    dates = pd.date_range(start='2024-01-01', end='2024-12-01', freq='M')
    timeline_data = pd.DataFrame({
        'Date': dates,
        'Compliance': [65, 68, 70, 73, 75, 76, 77, 78, 78, 79, 79, 78],
        'Target': [70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timeline_data['Date'],
        y=timeline_data['Compliance'],
        name='Actual',
        mode='lines+markers',
        line=dict(color='#1f77b4', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=timeline_data['Date'],
        y=timeline_data['Target'],
        name='Target',
        mode='lines',
        line=dict(color='#2ca02c', width=2, dash='dash')
    ))
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Compliance %",
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)


def page_compliance_analysis():
    """Compliance analysis page."""
    st.markdown('<div class="main-header">🔍 Compliance Analysis</div>', unsafe_allow_html=True)
    
    initialize_components()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Policy Document")
        
        uploaded_file = st.file_uploader(
            "Choose a policy document",
            type=['pdf', 'docx', 'txt'],
            help="Upload your organization's policy document"
        )
        
        framework = st.selectbox(
            "Select Target Framework",
            options=st.session_state.framework_loader.get_available_frameworks(),
            help="Choose the compliance framework to analyze against"
        )
        
        top_k = st.slider(
            "Number of controls to analyze",
            min_value=3,
            max_value=20,
            value=5
        )
        
        if st.button("🚀 Analyze Compliance", type="primary"):
            if not uploaded_file:
                st.error("Please upload a policy document")
            else:
                with st.spinner("Analyzing compliance gaps..."):
                    try:
                        # Initialize analyzer if needed
                        if st.session_state.analyzer is None:
                            settings = get_settings()
                            st.session_state.analyzer = RAGComplianceAnalyzer(
                                embedding_model_name=settings.embedding_model,
                                vector_db_path=settings.vector_db_path
                            )
                        
                        # Extract text from document
                        policy_text = st.session_state.policy_processor.load_from_uploaded_file(uploaded_file)
                        
                        if not policy_text:
                            st.error("Could not extract text from document")
                        else:
                            # Load and index framework
                            controls = st.session_state.framework_loader.load_framework(framework)
                            st.session_state.analyzer.index_framework(framework, controls)
                            
                            # Analyze gaps
                            gaps = st.session_state.analyzer.analyze_compliance_gap(
                                framework=framework,
                                policy_document=policy_text,
                                top_k=top_k
                            )
                            
                            st.session_state.analysis_results = gaps
                            st.success(f"✅ Analysis complete! Found {len(gaps)} gaps.")
                    
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
    
    with col2:
        st.subheader("Analysis Parameters")
        st.info("""
        **How it works:**
        1. Upload your policy document
        2. Select the target compliance framework
        3. Click 'Analyze Compliance' to start
        4. Review identified gaps and recommendations
        """)
    
    # Display results
    if st.session_state.analysis_results:
        st.markdown("---")
        st.subheader("📋 Analysis Results")
        
        gaps = st.session_state.analysis_results
        
        # Summary stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Gaps", len(gaps))
        with col2:
            critical = sum(1 for g in gaps if g.get('severity') == 'Critical')
            st.metric("Critical", critical)
        with col3:
            high = sum(1 for g in gaps if g.get('severity') == 'High')
            st.metric("High", high)
        with col4:
            medium = sum(1 for g in gaps if g.get('severity') == 'Medium')
            st.metric("Medium", medium)
        
        # Filters
        st.markdown("### Filter Results")
        severity_filter = st.multiselect(
            "Filter by Severity",
            options=['Critical', 'High', 'Medium', 'Low'],
            default=['Critical', 'High', 'Medium', 'Low']
        )
        
        filtered_gaps = [g for g in gaps if g.get('severity') in severity_filter]
        
        # Display gaps
        for i, gap in enumerate(filtered_gaps, 1):
            with st.expander(f"Gap {i}: {gap.get('control_id', 'N/A')} - {gap.get('severity', 'Unknown')}"):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"**Control ID:** {gap.get('control_id', 'N/A')}")
                    st.markdown(f"**Severity:** {gap.get('severity', 'Unknown')}")
                    st.markdown(f"**Confidence:** {gap.get('confidence', 0):.1%}")
                
                with col2:
                    st.markdown(f"**Framework:** {gap.get('framework', 'N/A')}")
                
                st.markdown("**Requirement:**")
                st.text(gap.get('requirement', 'N/A'))
                
                st.markdown("**Current State:**")
                st.text(gap.get('current_state', 'N/A'))
                
                st.markdown("**Recommendations:**")
                for rec in gap.get('recommendations', []):
                    st.markdown(f"- {rec}")
        
        # Export options
        st.markdown("---")
        st.subheader("📥 Export Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV Export
            if st.button("Export to CSV"):
                df = st.session_state.report_generator.generate_compliance_report(
                    gaps, framework
                )
                csv_data = st.session_state.report_generator.export_to_csv(df)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"compliance_gaps_{framework}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            # Excel Export
            if st.button("Export to Excel"):
                df = st.session_state.report_generator.generate_compliance_report(
                    gaps, framework
                )
                excel_data = st.session_state.report_generator.export_to_excel(df)
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=f"compliance_gaps_{framework}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )


def page_risk_assessment():
    """Risk assessment page."""
    st.markdown('<div class="main-header">⚠️ Risk Assessment</div>', unsafe_allow_html=True)
    
    initialize_components()
    
    st.subheader("Define Risk Factors")
    
    # Risk configuration
    risk_id = st.text_input("Risk ID", value="RISK-001", help="Unique identifier for this risk")
    risk_description = st.text_area("Risk Description", help="Describe the risk being assessed")
    
    st.markdown("---")
    st.markdown("### Risk Factors")
    
    # Dynamic risk factors
    num_factors = st.number_input("Number of risk factors", min_value=1, max_value=10, value=2)
    
    risk_factors = []
    
    for i in range(num_factors):
        with st.expander(f"Risk Factor {i+1}", expanded=(i==0)):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(f"Factor Name", key=f"name_{i}", value=f"Factor {i+1}")
                category = st.selectbox(
                    "Category",
                    options=["Technical", "Operational", "Strategic", "Compliance", "Financial"],
                    key=f"category_{i}"
                )
                likelihood = st.slider("Likelihood (1-5)", 1, 5, 3, key=f"likelihood_{i}")
            
            with col2:
                impact = st.slider("Impact (1-5)", 1, 5, 3, key=f"impact_{i}")
                control_eff = st.slider("Control Effectiveness (%)", 0, 100, 50, key=f"control_{i}")
                current_controls = st.text_area(
                    "Current Controls",
                    key=f"controls_{i}",
                    value="Existing control measures"
                )
            
            risk_factors.append(RiskFactor(
                name=name,
                category=category,
                likelihood=likelihood,
                impact=impact,
                current_controls=current_controls,
                control_effectiveness=control_eff
            ))
    
    if st.button("🎯 Assess Risk", type="primary"):
        if not risk_description:
            st.error("Please provide a risk description")
        else:
            with st.spinner("Assessing risk..."):
                try:
                    assessment = st.session_state.risk_assessor.assess_risk(
                        risk_factors=risk_factors,
                        risk_id=risk_id,
                        description=risk_description
                    )
                    
                    st.session_state.risk_results = assessment
                    st.success("✅ Risk assessment complete!")
                
                except Exception as e:
                    st.error(f"Error during assessment: {str(e)}")
    
    # Display results
    if st.session_state.risk_results:
        st.markdown("---")
        st.subheader("📊 Assessment Results")
        
        assessment = st.session_state.risk_results
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Risk ID", assessment.risk_id)
        with col2:
            st.metric("Category", assessment.category)
        with col3:
            st.metric("Inherent Risk", f"{assessment.inherent_risk_score:.1f}")
        with col4:
            risk_color = {
                "Critical": "🔴",
                "High": "🟠",
                "Medium": "🟡",
                "Low": "🟢",
                "Minimal": "⚪"
            }.get(assessment.risk_level, "⚪")
            st.metric("Risk Level", f"{risk_color} {assessment.risk_level}")
        
        st.markdown("### Risk Reduction")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                "Residual Risk",
                f"{assessment.residual_risk_score:.1f}",
                delta=f"-{assessment.inherent_risk_score - assessment.residual_risk_score:.1f}"
            )
        
        with col2:
            reduction_pct = ((assessment.inherent_risk_score - assessment.residual_risk_score) / 
                            assessment.inherent_risk_score * 100)
            st.metric("Risk Reduction", f"{reduction_pct:.1f}%")
        
        st.markdown("### Recommendations")
        for i, rec in enumerate(assessment.recommendations, 1):
            st.markdown(f"{i}. {rec}")


def page_framework_explorer():
    """Framework explorer page."""
    st.markdown('<div class="main-header">📚 Framework Explorer</div>', unsafe_allow_html=True)
    
    initialize_components()
    
    # Framework selection
    frameworks = st.session_state.framework_loader.get_available_frameworks()
    
    selected_framework = st.selectbox("Select Framework", options=frameworks)
    
    if selected_framework:
        # Load controls
        controls = st.session_state.framework_loader.load_framework(selected_framework)
        
        st.markdown(f"### {selected_framework} Framework")
        st.info(f"Total Controls: {len(controls)}")
        
        # Search
        search_query = st.text_input("🔍 Search controls", placeholder="Enter keywords...")
        
        # Filter controls
        if search_query:
            filtered_controls = [
                c for c in controls
                if search_query.lower() in c.get('title', '').lower() or
                   search_query.lower() in c.get('description', '').lower() or
                   search_query.lower() in c.get('control_id', '').lower()
            ]
        else:
            filtered_controls = controls
        
        st.markdown(f"**Showing {len(filtered_controls)} of {len(controls)} controls**")
        
        # Display controls in a table
        if filtered_controls:
            df = pd.DataFrame(filtered_controls)
            
            # Select columns to display
            display_cols = ['control_id', 'title', 'category', 'criticality', 'status']
            available_cols = [col for col in display_cols if col in df.columns]
            
            if available_cols:
                st.dataframe(
                    df[available_cols],
                    use_container_width=True,
                    hide_index=True
                )
            
            # Detailed view
            st.markdown("---")
            st.markdown("### Control Details")
            
            control_ids = [c.get('control_id', f"Control {i}") for i, c in enumerate(filtered_controls)]
            selected_control_id = st.selectbox("Select control to view details", options=control_ids)
            
            if selected_control_id:
                selected_control = next(
                    (c for c in filtered_controls if c.get('control_id') == selected_control_id),
                    None
                )
                
                if selected_control:
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown(f"**Control ID:** {selected_control.get('control_id', 'N/A')}")
                        st.markdown(f"**Title:** {selected_control.get('title', 'N/A')}")
                        st.markdown(f"**Category:** {selected_control.get('category', 'N/A')}")
                    
                    with col2:
                        st.markdown(f"**Criticality:** {selected_control.get('criticality', 'N/A')}")
                        st.markdown(f"**Status:** {selected_control.get('status', 'N/A')}")
                    
                    st.markdown("**Description:**")
                    st.write(selected_control.get('description', 'No description available'))


def page_reports():
    """Reports generation page."""
    st.markdown('<div class="main-header">📄 Reports</div>', unsafe_allow_html=True)
    
    st.subheader("Generate Reports")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        report_type = st.selectbox(
            "Report Type",
            options=[
                "Executive Summary",
                "Detailed Compliance Report",
                "Risk Register",
                "Gap Analysis Report",
                "Audit Trail"
            ]
        )
        
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now())
        )
        
        export_format = st.selectbox(
            "Export Format",
            options=["PDF", "Excel", "Word"]
        )
    
    with col2:
        st.info("""
        **Report Types:**
        - **Executive Summary**: High-level overview
        - **Detailed Compliance**: Full compliance analysis
        - **Risk Register**: Complete risk inventory
        - **Gap Analysis**: Detailed gap assessment
        - **Audit Trail**: Activity logs and changes
        """)
    
    if st.button("📊 Generate Report", type="primary"):
        with st.spinner("Generating report..."):
            st.success(f"✅ {report_type} generated successfully!")
            st.info(f"Report will be available in {export_format} format")
            
            # Placeholder for actual report generation
            st.download_button(
                label=f"Download {export_format}",
                data="Sample report data",
                file_name=f"report_{datetime.now().strftime('%Y%m%d')}.{export_format.lower()}",
                mime="application/octet-stream"
            )


def page_settings():
    """Settings page."""
    st.markdown('<div class="main-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["General", "Models", "Integrations"])
    
    with tabs[0]:
        st.subheader("General Settings")
        
        org_name = st.text_input("Organization Name", value="My Organization")
        org_email = st.text_input("Contact Email", value="contact@organization.com")
        
        st.markdown("### Thresholds")
        gap_threshold = st.slider("Gap Severity Threshold", 0.0, 1.0, 0.7)
        confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.6)
        
        if st.button("💾 Save General Settings"):
            st.success("Settings saved successfully!")
    
    with tabs[1]:
        st.subheader("Model Configuration")
        
        embedding_model = st.text_input(
            "Embedding Model",
            value="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        llm_model = st.text_input(
            "LLM Model",
            value="gpt-3.5-turbo"
        )
        
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Your OpenAI API key"
        )
        
        if st.button("💾 Save Model Settings"):
            st.success("Model settings saved successfully!")
    
    with tabs[2]:
        st.subheader("Integration Settings")
        
        st.markdown("### Ticketing Systems")
        col1, col2 = st.columns(2)
        
        with col1:
            jira_enabled = st.checkbox("Enable Jira Integration")
            if jira_enabled:
                st.text_input("Jira URL")
                st.text_input("Jira API Token", type="password")
        
        with col2:
            servicenow_enabled = st.checkbox("Enable ServiceNow Integration")
            if servicenow_enabled:
                st.text_input("ServiceNow Instance")
                st.text_input("ServiceNow API Key", type="password")
        
        st.markdown("### Notifications")
        col1, col2 = st.columns(2)
        
        with col1:
            slack_enabled = st.checkbox("Enable Slack Notifications")
            if slack_enabled:
                st.text_input("Slack Webhook URL")
        
        with col2:
            teams_enabled = st.checkbox("Enable Microsoft Teams")
            if teams_enabled:
                st.text_input("Teams Webhook URL")
        
        if st.button("💾 Save Integration Settings"):
            st.success("Integration settings saved successfully!")


def main():
    """Main application entry point."""
    render_sidebar()
    
    # Page navigation
    page = st.sidebar.radio(
        "Navigation",
        options=[
            "Dashboard",
            "Compliance Analysis",
            "Risk Assessment",
            "Framework Explorer",
            "Reports",
            "Settings"
        ],
        label_visibility="collapsed"
    )
    
    # Route to appropriate page
    if page == "Dashboard":
        page_dashboard()
    elif page == "Compliance Analysis":
        page_compliance_analysis()
    elif page == "Risk Assessment":
        page_risk_assessment()
    elif page == "Framework Explorer":
        page_framework_explorer()
    elif page == "Reports":
        page_reports()
    elif page == "Settings":
        page_settings()


if __name__ == "__main__":
    main()
