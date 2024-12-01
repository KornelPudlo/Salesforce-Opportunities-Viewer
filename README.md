# Salesforce Opportunities Viewer App

The **Salesforce Opportunities Viewer App** is an interactive web-based tool designed for sales teams to streamline deal management and enhance decision-making. Built using Streamlit, it connects seamlessly with Salesforce to provide detailed insights into Opportunities, Accounts, Contacts, and related activities.

## Features

### Key Functionalities:
1. **Opportunity Insights**:  
   - View Opportunity details such as name, stage, close date, probability, and amount.  
   - Includes stage-specific next steps and guidance to improve win chances.

2. **Risk Analysis**:  
   - Provides actionable insights based on close date, probability, and deal amount.  
   - Highlights high-value opportunities and overdue deals.

3. **Deal Accelerator**:  
   - Offers tailored guidance based on the current Opportunity stage.  
   - Recommends industry-specific resources to support deal closure.

4. **Activity Tracking**:  
   - Displays the most recent tasks and events related to an Opportunity.  

5. **Account & Contact Details**:  
   - Access Account information like industry, priority, rating, and type.  
   - View primary contact details including name, email, and phone.

6. **Industry Resources**:  
   - Download recommended PDF resources tailored to the Opportunity's industry.

## Installation

### Prerequisites:
- Python 3.8 or higher
- Salesforce API credentials (username, password, security token, and domain)
- Required libraries listed in `requirements.txt`

### Steps:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/KornelPudlo/salesforce-opportunities-viewer.git
   cd salesforce-opportunities-viewer
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Credentials**:
   - Create a `secrets.toml` file in the `.streamlit` folder.
   - Add your Salesforce credentials in the following format:
     ```toml
     [salesforce]
     username = "your_username"
     password = "your_password"
     security_token = "your_security_token"
     domain = "your_domain"
     ```

4. **Run the App**:
   ```bash
   streamlit run app.py
   ```

5. **Access the App**:
   - Open the provided URL (usually `http://localhost:8501`) in your browser.

## Usage

### Navigation:
- **Overview**: Learn about the app's purpose and features.  
- **Opportunities Viewer**: Select an Opportunity to view detailed insights, guidance, and resources.  
- **About the Author**: Connect with the developer and explore their work.

### Features in Detail:
- **Risk Analysis**: Automatically assesses Opportunity risks and provides tailored recommendations.  
- **Deal Accelerator**: Suggests actions and resources based on Opportunity stage and industry.  
- **Interactive Table**: Explore other Opportunities related to the selected Account.  

## Technologies Used

### Frameworks & Libraries:
- **Streamlit**: For building the interactive web application.  
- **Simple-Salesforce**: For connecting and querying Salesforce data.  
- **Pandas**: For handling tabular data.  

### APIs:
- **Salesforce API**: For retrieving Opportunities, Accounts, Contacts, and activities.

## Screenshots

### Dashboard Overview
![Dashboard Overview](https://github.com/user-attachments/assets/a54b02ee-8f46-432f-a775-b75b87309537)
### Deal Accelerator
![Deal Accelerator](https://github.com/user-attachments/assets/059a0fe0-f6ef-429d-ac8b-db0e263b7b4b)

## Contributing

Contributions are welcome!  
If you’d like to contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add new feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-branch
   ```
5. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

**Kornel Pudło**  
- [GitHub](https://github.com/KornelPudlo)  
- [LinkedIn](https://www.linkedin.com/in/kornel-pud%C5%82o-a19921b5)  
- [Medium](https://medium.com/@korn.pudlo)  

