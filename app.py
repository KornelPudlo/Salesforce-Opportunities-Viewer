import streamlit as st
from simple_salesforce import Salesforce
import pandas as pd
import streamlit.components.v1 as components

# Access credentials from the secrets file
credentials = st.secrets["salesforce"]
USERNAME = credentials["username"]
PASSWORD = credentials["password"]
SECURITY_TOKEN = credentials["security_token"]
DOMAIN = credentials["domain"]

# Connect to Salesforce
try:
    sf = Salesforce(
        username=USERNAME,
        password=PASSWORD,
        security_token=SECURITY_TOKEN,
        domain=DOMAIN
    )
except Exception as e:
    st.sidebar.error(f"Failed to connect to Salesforce: {e}")
    sf = None


# Overview Page
def app_overview():
    st.title("Welcome to the Salesforce Opportunities Viewer App :robot_face:")

    # Explain the app's purpose
    st.markdown("""
    ## Purpose of the App
    The Salesforce Opportunities Viewer App is a powerful tool designed for sales teams to streamline deal management and improve decision-making. 
    It provides seamless access to Salesforce data, offering a detailed overview of opportunities, account details, and related activities.

    This app is perfect for sales professionals who need:
    - A centralized view of Salesforce Opportunities
    - Quick insights into Opportunity details, probability, and close dates
    - Guidance on next steps and risk analysis to improve win rates
    - Access to recommended resources based on the industry

    ## Key Features:
    - **Opportunities Viewer**: Explore detailed information about Salesforce Opportunities, including stage, amount, and close date.
    - **Risk Analysis**: Receive actionable insights based on probability, close date, and other metrics.
    - **Deal Accelerator**: Get stage-specific guidance, next steps, and resource recommendations to maximize deal success.
    - **Recent Activity**: Stay updated with recent tasks and events related to the Opportunity.
    - **Account and Contact Details**: Access essential account attributes, primary contact details, and customer priority.

    ## How to Use the App
    1. **Overview**: This page provides an introduction to the app and its purpose.
    2. **Opportunities Viewer**: Select an Opportunity to view detailed insights, guidance, and resources.
    3. **About the Author**: Learn more about the app developer and find links to connect and provide feedback.

    ## Libraries Used:
    - `Streamlit`: For building the interactive web application.
    - `Pandas`: For handling and displaying Opportunity data.
    - `Simple-Salesforce`: For connecting and querying Salesforce data.
    - `Datetime`: For managing and analyzing dates in Salesforce Opportunities.

    ## APIs Used:
    - **Salesforce API**: For fetching Opportunities, Accounts, Contacts, and related activities.

    ## Why Use This App?
    - Improve decision-making with detailed Opportunity insights
    - Streamline sales processes with actionable recommendations
    - Enhance client interactions with industry-specific resources
    - Boost productivity with a user-friendly, interactive interface

    Let's get started! 🚀
    Dive into the next section by picking a sub-page from the navigation menu on the left.
    """, unsafe_allow_html=True)

    # Embed the GIF using components.html
    components.html(
        """
        <iframe src="https://giphy.com/embed/L3Ki84G9k2lGJEKZL3" width="480" height="269" style="" frameBorder="0" class="giphy-embed" allowFullScreen></iframe><p><a href="https://giphy.com/gifs/peacocktv-brooklyn-99-b99-nine-nine-L3Ki84G9k2lGJEKZL3"></a></p>
        """,
        height=600
    )


# Salesforce App Page
def opportunities_viewer():
    if sf:
        st.title("Salesforce Opportunities Viewer")
        st.subheader("Select an Opportunity to View Details")

        # Query all Opportunities
        query = """
        SELECT Id, Name, CloseDate, StageName, Amount, Segment__c, Region__c, AccountId, Probability
        FROM Opportunity
        LIMIT 50
        """
        try:
            opportunities = sf.query(query).get("records", [])
            if opportunities:
                # Create a dropdown filter for selecting an opportunity
                opportunity_options = {opp['Name']: opp['Id'] for opp in opportunities}
                selected_opportunity_name = st.selectbox(
                    "Select an Opportunity",
                    options=list(opportunity_options.keys())
                )

                # Get the selected opportunity's details
                selected_opportunity_id = opportunity_options[selected_opportunity_name]
                selected_opportunity_data = sf.Opportunity.get(selected_opportunity_id)

                # Extract Opportunity details
                opportunity_name = selected_opportunity_data['Name']
                close_date = selected_opportunity_data['CloseDate']
                stage_name = selected_opportunity_data['StageName']
                amount = selected_opportunity_data['Amount']
                segment = selected_opportunity_data.get('Segment__c', 'N/A')
                region = selected_opportunity_data.get('Region__c', 'N/A')
                account_id = selected_opportunity_data['AccountId']
                probability = selected_opportunity_data.get('Probability', 'N/A')

                # Query Account details
                account_data = sf.Account.get(account_id)
                account_name = account_data['Name']
                account_number = account_data.get('AccountNumber', 'N/A')
                industry = account_data.get('Industry', 'N/A')
                customer_priority = account_data.get('CustomerPriority__c', 'N/A')
                account_type = account_data.get('Type', 'N/A')
                rating = account_data.get('Rating', 'N/A')

                # Query Contact details for the Account
                contacts_query = f"""
                SELECT Id, Name, Email, Phone, Title
                FROM Contact
                WHERE AccountId = '{account_id}'
                """
                contacts = sf.query(contacts_query).get("records", [])

                # Use the first contact as the default for the Deal Accelerator section
                if contacts:
                    contact_name = contacts[0].get('Name', 'N/A')
                    contact_email = contacts[0].get('Email', 'N/A')
                    contact_phone = contacts[0].get('Phone', 'N/A')
                    contact_title = contacts[0].get('Title', 'N/A')
                else:
                    contact_name = "N/A"
                    contact_email = "N/A"
                    contact_phone = "N/A"
                    contact_title = "N/A"

                # Query Other Opportunities for the same Account
                other_opportunities_query = f"""
                SELECT Name, CloseDate, StageName, Amount
                FROM Opportunity
                WHERE AccountId = '{account_id}' AND Id != '{selected_opportunity_id}'
                """
                other_opportunities = sf.query(other_opportunities_query).get("records", [])

                # Layout: Opportunity Details and Account Details in two columns
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Opportunity Details")
                    st.write(f"**Name:** {opportunity_name}")
                    st.write(f"**Close Date:** {close_date}")
                    st.write(f"**Stage:** {stage_name}")
                    st.write(f"**Amount:** ${amount:,}")
                    st.write(f"**Segment:** {segment}")
                    st.write(f"**Region:** {region}")

                with col2:
                    st.subheader("Account Details")
                    st.write(f"**Name:** {account_name}")
                    st.write(f"**Account Number:** {account_number}")
                    st.write(f"**Industry:** {industry}")
                    st.write(f"**Customer Priority:** {customer_priority}")
                    st.write(f"**Type:** {account_type}")
                    st.write(f"**Rating:** {rating}")

                # Layout: Primary Contact Details and Recent Activity in two columns
                col3, col4 = st.columns(2)

                with col3:
                    st.subheader("Primary Contact Details")
                    st.write(f"**Name:** {contact_name}")
                    st.write(f"**Title:** {contact_title}")
                    st.write(f"**Email:** {contact_email}")
                    st.write(f"**Phone:** {contact_phone}")

                with col4:
                    st.subheader("Recent Activity")
                    # Query for the most recent activity (Task or Event) related to the selected opportunity
                    task_query = f"""
                    SELECT Subject, Status, ActivityDate, Description, CreatedDate
                    FROM Task
                    WHERE WhatId = '{selected_opportunity_id}'
                    ORDER BY ActivityDate DESC
                    LIMIT 1
                    """
                    tasks = sf.query(task_query).get("records", [])

                    event_query = f"""
                    SELECT Subject, ActivityDate, Description, CreatedDate
                    FROM Event
                    WHERE WhatId = '{selected_opportunity_id}'
                    ORDER BY ActivityDate DESC
                    LIMIT 1
                    """
                    events = sf.query(event_query).get("records", [])

                    # Combine and sort activities
                    activities = tasks + events
                    activities = sorted(activities, key=lambda x: x.get("ActivityDate", ""), reverse=True)

                    if activities:
                        recent_activity = activities[0]
                        activity_subject = recent_activity.get("Subject", "No Subject")
                        activity_status = recent_activity.get("Status", "N/A")  # Tasks have Status; Events do not
                        activity_date = recent_activity.get("ActivityDate", "No Date")
                        activity_description = recent_activity.get("Description", "No Description")

                        st.write(f"**Subject:** {activity_subject}")
                        st.write(f"**Status:** {activity_status}")  # Will display "N/A" for Events
                        st.write(f"**Date:** {activity_date}")
                        st.write(f"**Description:** {activity_description}")
                    else:
                        st.write("No recent activities found for this opportunity.")

                st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

                # Display Other Opportunities as a dropdown
                with st.expander(f"### Other Opportunities for {account_name}", expanded=False):
                    if other_opportunities:
                        # Extract relevant fields into a DataFrame
                        opportunities_df = pd.DataFrame(other_opportunities)
                        filtered_opportunities = opportunities_df[["Name", "CloseDate", "StageName", "Amount"]]

                        # Add a hardcoded $ sign to the Amount column
                        filtered_opportunities["Amount"] = filtered_opportunities["Amount"].apply(
                            lambda x: f"${x}" if pd.notnull(x) else "N/A"
                        )

                        # Reset the index to remove the index column
                        filtered_opportunities = filtered_opportunities.reset_index(drop=True)

                        # Convert the DataFrame to HTML and hide the index
                        table_html = filtered_opportunities.to_html(index=False)

                        # Use styled HTML to adjust table width and center it
                        st.markdown(
                            f"""
                            <div style="width: 80%; margin: 0 auto; overflow-x: auto; text-align: center;">
                                {table_html}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)

                # Add Deal Accelerator Section
                # Add Deal Accelerator Section
                st.write("### Deal Accelerator")
                st.markdown(
                    f"""
                    For the **{opportunity_name}**, the current win probability is **{probability}%**.
                    To increase the chances of winning the deal, please:
                    - **Contact:** {contact_name} ({contact_title})
                      - **Email:** {contact_email}
                      - **Phone:** {contact_phone}
                    """
                )

                # Add Next Steps based on Stage
                if stage_name == "Closed Won":
                    next_step = "Celebrate the win and ensure smooth implementation or delivery for the client. Gather testimonials or case studies if applicable."
                elif stage_name == "Perception Analysis":
                    next_step = "Engage the client with proof points such as case studies or ROI analyses to build confidence."
                elif stage_name == "Negotiation/Review":
                    next_step = "Focus on addressing any legal or procurement concerns. Align with key decision-makers to finalize terms."
                elif stage_name == "Id. Decision Makers":
                    next_step = "Identify all stakeholders involved in the decision-making process and establish a clear buying timeline."
                elif stage_name == "Qualification":
                    next_step = "Verify the client's budget, timeline, and decision-making process to ensure alignment with your solution."
                elif stage_name == "Value Proposition":
                    next_step = "Highlight your unique selling points and how they directly address the client's specific needs."
                elif stage_name == "Prospecting":
                    next_step = "Research the client's business challenges and identify initial points of contact to establish rapport."
                elif stage_name == "Needs Analysis":
                    next_step = "Conduct detailed discovery sessions to fully understand the client's pain points and tailor your solution."
                elif stage_name == "Proposal/Price Quote":
                    next_step = "Present a well-structured proposal with clear pricing. Emphasize value over cost to address potential objections."
                else:
                    next_step = "Follow up with the client and provide any requested information."

                st.markdown(f"- **Next Step:** {next_step}")

                # Add Risk Analysis
                from datetime import datetime

                # Calculate time remaining until the close date
                time_until_close = (pd.to_datetime(close_date) - pd.Timestamp.now()).days
                is_overdue = pd.to_datetime(close_date) < pd.Timestamp.now()

                # Assess risk based on various metrics
                if probability < 50:
                    risk_message = f"This opportunity has a low win probability. {time_until_close} days remain until the close date. Consider re-engaging the client or revising the proposal."
                    action_suggestion = "Focus on strengthening the value proposition and addressing client objections."
                elif is_overdue:
                    risk_message = "This opportunity is overdue. Follow up with the client immediately."
                    action_suggestion = "Contact the client to understand any blockers and discuss the next steps."
                elif time_until_close <= 7:
                    risk_message = f"This opportunity is nearing its close date with {time_until_close} days remaining. Ensure all client concerns are addressed promptly."
                    action_suggestion = "Schedule a final meeting with the client to confirm alignment."
                elif stage_name in ["Proposal/Price Quote", "Negotiation/Review"] and probability < 70:
                    risk_message = f"This opportunity is in a critical stage with {time_until_close} days remaining and moderate win probability. Review terms and address objections."
                    action_suggestion = "Conduct a detailed review of the proposal or contract terms and ensure client satisfaction."
                else:
                    risk_message = f"This opportunity is on track with {time_until_close} days remaining."
                    action_suggestion = "Maintain consistent communication and monitor progress closely."

                # Additional insights based on metrics
                if amount and amount > 100000:
                    high_value_insight = "This is a high-value opportunity. Consider prioritizing resources to maximize chances of success."
                else:
                    high_value_insight = None

                # Display Risk Analysis
                st.markdown(f"- **Risk Analysis:** {risk_message}")
                st.markdown(f"- **Recommended Action:** {action_suggestion}")

                if high_value_insight:
                    st.markdown(f"- **Additional Insight:** {high_value_insight}")

                # Add Stage-Specific Guidance
                stage_guidance = {
                    "Closed Won": "Focus on delivering exceptional results to ensure client satisfaction and secure potential future business or referrals.",
                    "Perception Analysis": "Provide the client with success stories, testimonials, or ROI analyses to reinforce your value proposition.",
                    "Negotiation/Review": "Address all objections and ensure alignment with decision-makers to finalize the deal terms.",
                    "Id. Decision Makers": "Ensure you have identified and engaged all key stakeholders in the decision-making process.",
                    "Qualification": "Validate the client's budget, timeline, and decision-making authority to move forward effectively.",
                    "Value Proposition": "Clearly articulate how your solution uniquely meets the client's specific needs and challenges.",
                    "Prospecting": "Research the client's business environment and challenges to establish meaningful initial engagement.",
                    "Needs Analysis": "Conduct comprehensive discovery sessions to understand the client's pain points and goals fully.",
                    "Proposal/Price Quote": "Craft a compelling proposal that highlights value over cost and addresses potential objections proactively."
                }
                guidance = stage_guidance.get(stage_name, "Continue to progress the deal.")
                st.markdown(f"- **Guidance for {stage_name} Stage:** {guidance}")

                # Add Recommended Resources based on Industry
                resources = {
                    "Technology": ["./resources/Tech_Whitepaper.pdf"],
                    "Healthcare": ["./resources/Healthcare_Report.pdf", "./resources/Clinical_Case_Study.pdf"],
                    "Financial Services": ["./resources/Financial_Insights.pdf", "./resources/Banking_Case_Study.pdf"],
                    "Electronics": ["./resources/Electronics_Industry.pdf"],
                    "Apparel": ["./resources/THE GLOBAL APPAREL VALUE CHAIN.pdf"],
                    "Construction": ["./resources/Construction Industry.pdf"],
                    "Consulting": ["./resources/Consulting_Strategies.pdf"],
                    "Hospitality": ["./resources/Hospitality_Insights.pdf", "./resources/Hospitality Sectors.pdf"],
                    "Energy": ["./resources/Energy Sector Overview.pdf", "./resources/Renewable_Energy.pdf"],
                    "Transportation": ["./resources/Future of transportation.pdf",
                                       "./resources/Logistics_Overview.pdf"],
                    "Education": ["./resources/Education_Whitepaper.pdf", "./resources/HighEdu_Trends.pdf"],
                    "Biotechnology": ["./resources/Biotech_Trends.pdf", "./resources/Biotech_Report.pdf"],
                    "Entertainment": ["./resources/Entertainment_Economics.pdf", "./resources/Media_Insights.pdf"],
                }

                # Fetch resources for the selected industry
                industry_resources = resources.get(industry, [])
                if industry_resources:
                    st.markdown("**Recommended Resources:**")
                    for resource in industry_resources:
                        with open(resource, "rb") as file:
                            st.download_button(
                                label=f"📄 Download {resource.split('/')[-1]}",
                                data=file,
                                file_name=resource.split("/")[-1],
                                mime="application/pdf",
                            )
                else:
                    st.markdown("- **Recommended Resources:** No resources available for this industry.")

            else:
                st.info("No opportunities found.")
        except Exception as e:
            st.error(f"Error fetching opportunities: {e}")
    else:
        st.info("Unable to connect to Salesforce. Please check your credentials.")


# About the Author Page
def about_the_author():
    st.title("About the Author :male-student:")

    # Use icons as images
    st.markdown("""
    Hi, I'm Kornel Pudło, a Data Engineer  with a passion for building impactful applications and sharing knowledge. 
    The Salesforce Opportunities Viewer App is a powerful tool designed for sales teams to streamline deal management and improve decision-making.
    By integrating directly with Salesforce, the app provides a detailed overview of opportunities, account details, and related activities.
    Feel free to connect and share your feedback with me! 😊

    You can find more about my work at the following links [click the icon]:

    - **Check out the code:**  
      [![GitHub](https://img.icons8.com/ios-glyphs/30/000000/github.png)](https://github.com/KornelPudlo) GitHub  
    
    - **Let’s connect here:**  
      [![LinkedIn](https://img.icons8.com/ios-filled/30/000000/linkedin.png)](https://www.linkedin.com/in/kornel-pud%C5%82o-a19921b5) LinkedIn  
    
    - **Read the full story:**  
      [![Medium](https://img.icons8.com/ios-glyphs/30/000000/medium-monogram.png)](https://medium.com/@korn.pudlo) Medium  
    
    - **Watch the demo:**  
      [![YouTube](https://img.icons8.com/ios-glyphs/30/000000/youtube-play.png)](https://www.youtube.com/watch?v=S13dW3reDVw) YouTube    
    """, unsafe_allow_html=True)


# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Navigate through the app :point_down:",
                        ["Overview:robot_face:", "Opportunities Viewer🔍", "About the Author :male-student:"])

# Page Routing
if page == "Overview:robot_face:":
    app_overview()
elif page == "Opportunities Viewer🔍":
    opportunities_viewer()
elif page == "About the Author :male-student:":
    about_the_author()
