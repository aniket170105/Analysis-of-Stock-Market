# Financial Analysis Web App

[Website](https://analysis-of-stock-market.streamlit.app/)

Welcome to our Analysis of Stock Market repository! 🎉 This project is a web application that provides financial analysis of stocks using technical, fundamental, and sentiment analysis. The app allows users to enter a company ticker symbol and select the types of analysis they want to perform. The results are then displayed on the web page.

## Features

- **Technical Analysis**:
  - Indicator-based strategy (Win Rate: 54%)
  - ML/DL-based model (with varying accuracy rates)
- **Fundamental Analysis** (Accuracy: 66%)
  - Supports technology sector companies
  - Calculates financial ratios from income statements, balance sheets, and cash flow statements
- **Sentiment Analysis**
  - Scrapes and summarizes financial news articles related to the company
  - Performs sentiment analysis on the summarized content

## 📂 File Structure
- **Data Sector Wise**: It contain's all the data set used in this project. It also contain code used to refine and retrieve data. So you can use it to expand and update the data.
- **Fundamental Analysis**: Contain the trained model for Fundamental of Technology Sector. It also contain code used to train this model.
- **Sentimen Analysis**: Contain how to connect to groq api and retrieve model responses.
- **Technical Analysis**: Contain the trained model for Technical of respective tickers. It also contain various technical indicator based strategies (trend based, volume based and momentum based) to generate buy sell signal. It also contain code used to train this models.
- **Rest of Files**: They are mainly used to run the website.

## ⚙️ Instructions for Running the Code
1. Clone the repository:
```bash
   $ cd your-project
   $ git clone https://github.com/your-repo/financial-analysis-web-app.git
```
2. Install the required Python packages:
```bash
   $ pip install -r requirements.txt
```

## Usage
1. Run the Streamlit app:
```bash
   $ streamlit run app.py
```
2. Enter the company ticker symbol in the provided input field.

3. Select the types of analysis you want to perform (Technical, Fundamental, Sentiment).

4. For Fundamental Analysis, enter the required financial ratios.

5. For Sentiment Analysis, choose whether you want to see the sentiment value or the summary of the article.

6. Click the "Submit" button to see the analysis results.

The web app run a little slow please have patience.

## Note
1. For Technical Analysis, the app currently supports the following tickers: ACN, ADBE, CRM, GOOGL, INTU, META, MSFT, NFLX.

2. For Fundamental Analysis, the app supports the technology sector.

3. For Sentiment Analysis, the app supports all tickers.

Contributing
Fork the project.
Create a new branch 
   ```bash
   $ git checkout -b feature
   ```
Commit your changes
   ```bash
   $ git commit -am 'Add feature'
   ```
Push to the branch 
   ```bash
   $ git push origin feature
   ```

## Acknowledgments
I would like to express our gratitude to the following individuals and resources for their contributions to this project:
- Our Mentor Dr. Vivek Vijay
- Yahoo Finance for providing historical stock data.
- Alpha Vantage for providing financial data and APIs.
- Streamlit for their excellent open-source app framework.
- Python and its vibrant community for the numerous libraries and resources.

## License
This project is licensed under the MIT License.





