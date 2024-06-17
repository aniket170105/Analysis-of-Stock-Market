import streamlit as st
import webbrowser
import numpy as np
import getTechnical
import getFundamental
import getSentiment
# {"Bullish" if getFundamental.appFundamental(getting_values) == 1 else "Bearish" if getFundamental.appFundamental(getting_values) == 2 else "Neutral"}
# Functions to simulate processing for each type of analysis
detailofeachmodel = {'ACN': {'ML': 57.0, 'DL': 54.0},
 'ADBE': {'ML': 53.0, 'DL': 54.5},
 'GOOGL': {'ML': 58.0, 'DL': 53.0},
 'INTU': {'ML': 53.0, 'DL': 47.0},
 'META': {'ML': 53.0, 'DL': 48.0},
 'MSFT': {'ML': 59.0, 'DL': 53.0},
 'NFLX': {'ML': 53.0, 'DL': 46.0}}

def technical_analysis(ticker):
    # indicator_based = f'Indicator Based Strategy : {getTechnical.appTechnicalIndicatorBased(ticker_name=ticker)}'
    indi = getTechnical.appTechnicalIndicatorBased(ticker_name=ticker)
    indicator_based = f'Indicator Based Strategy (Win Rate : 54%) : {"Bullish" if indi==2 else "Bearish" if indi ==1 else "Neutral" }'
    indi = getTechnical.appMLbased(ticker_name=ticker)
    if ticker in detailofeachmodel:
        mlmodelbase = f'ML/DL Based Model (Accuracy : {detailofeachmodel.get(ticker, {"ML": "NA"})["ML"]}%) : {"Bullish" if indi==1 else "Bearish"}'
    else :
        mlmodelbase = f'ML/DL Based Model (Accuracy : null%) : {"Bullish" if indi==1 else "Bearish"}'
    # mlmodelbase = f'ML/DL Based Model : {getTechnical.appMLbased(ticker_name=ticker)}'
    return [indicator_based,mlmodelbase]

def fundamental_analysis(values):
    lsit_of_columns = ['reportedEPS','Current Ratio','Quick Ratio','Debt to Equity','Debt to Asset','Gross Margin',
                       'Profit Margin','Operating Margin','Interest Coverage','Return On StockHolder','Free Cash Flow Conversion']
    getting_values = []
    for x in lsit_of_columns:
        getting_values.append(float(values[x]))
    getting_values = np.array(getting_values)
    # st.write(getting_values)
    # getting_values = np.array(lsit_of_columns)
    indi = getFundamental.appFundamental(getting_values)
    result = f'Fundamental (Accuracy : 66%) : {"Bullish" if indi==1 else "Bearish"}'
    return [result]

def sentiment_analysis(sentiment_value, summary_of_article, ticker):
    analysis_value, analysis_text = getSentiment.appSentiment(ticker_name=ticker)
    result = []
    if sentiment_value:
        result.append([f'Sentiment : {"Bullish" if analysis_value>=0.65 else "Bearish" if analysis_value<=0.35 else "Neutral"}'])
    if summary_of_article:
        result.append(analysis_text)
    return result

# Initialize session state
if 'previous_ticker' not in st.session_state:
    st.session_state.previous_ticker = ""
    st.session_state.analysis_options = []
    st.session_state.fundamental_values = {}
    st.session_state.sentiment_value = False
    st.session_state.summary_of_article = False

# Streamlit UI
st.title("Financial Analysis Web App")

# Collapsible section for links
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        pass
    #   st.title("Financial Analysis Web App")  # Replace with your app title
    with col2:
        with st.sidebar:
            if st.button("GitHub"):
                st.markdown('<meta http-equiv="refresh" content="0; url=https://github.com/aniket170105/Analysis-of-Stock-Market" />', unsafe_allow_html=True)
            if st.button("App Report"):
                st.markdown('<meta http-equiv="refresh" content="0; url=https://github.com/aniket170105/Analysis-of-Stock-Market/blob/main/final_report.pdf" />', unsafe_allow_html=True)
    # with col2:
    #     # Option 2: Dedicated Buttons (using sidebar)
    #     with st.sidebar:
    #         st.button("GitHub", key="github_button", on_click=lambda: webbrowser.open("https://github.com/aniket170105/Analysis-of-Stock-Market"))
    #         st.button("App Report", key="report_button", on_click=lambda: webbrowser.open("https://github.com/aniket170105/Analysis-of-Stock-Market/blob/main/final_report.pdf"))

# Company ticker input
ticker = st.text_input("Enter company ticker:")

if ticker != st.session_state.previous_ticker:
    # Reset all inputs and selections
    st.session_state.analysis_options = []
    st.session_state.fundamental_values = {
        "reportedEPS": 0.0, "Current Ratio": 0.0, "Quick Ratio": 0.0, "Debt to Equity": 0.0,
        "Debt to Asset": 0.0, "Gross Margin": 0.0, "Profit Margin": 0.0, "Operating Margin": 0.0,
        "Interest Coverage": 0.0, "Return On StockHolder": 0.0, "Free Cash Flow Conversion": 0.0
    }
    st.session_state.sentiment_value = False
    st.session_state.summary_of_article = False

    # Update the previous ticker
    st.session_state.previous_ticker = ticker

if ticker:
    # User selection for type of analysis
    analysis_options = st.multiselect(
        "Select the type of analysis:",
        ["Technical", "Fundamental", "Sentiment"],
        default=st.session_state.analysis_options
    )
    st.session_state.analysis_options = analysis_options

    # Initialize results dictionary
    results = {}

    # Display additional inputs based on user selection
    if "Technical" in analysis_options:
        supported_ticker = ['ACN','ADBE','CRM','GOOGL','INTU','META','MSFT','NFLX']
        if ticker in supported_ticker:
            results["Technical"] = technical_analysis(ticker=ticker)
        else:
            results["Technical"] = ['We Currently do not support this ticker.']

    if "Fundamental" in analysis_options:
        st.subheader("Enter values for Fundamental Analysis:")
        # for key in st.session_state.fundamental_values.keys():
        #     st.session_state.fundamental_values[key] = st.text_input(key.replace('_', ' '), value=st.session_state.fundamental_values[key])
        for key in st.session_state.fundamental_values.keys():
            st.session_state.fundamental_values[key] = st.number_input(key.replace('_', ' '), value=st.session_state.fundamental_values[key])
        # Check if all values are entered
        if all(st.session_state.fundamental_values.values()):
            results["Fundamental"] = fundamental_analysis(st.session_state.fundamental_values)
        else:
            st.warning("Please enter all values for Fundamental Analysis.")

    if "Sentiment" in analysis_options:
        st.subheader("Select Sentiment Analysis Options:")
        sentiment_value = st.checkbox("Sentiment Value", value=st.session_state.sentiment_value)
        summary_of_article = st.checkbox("Summary of Article", value=st.session_state.summary_of_article)

        st.session_state.sentiment_value = sentiment_value
        st.session_state.summary_of_article = summary_of_article

        if sentiment_value or summary_of_article:
            results["Sentiment"] = sentiment_analysis(sentiment_value, summary_of_article,ticker=ticker)
        else:
            st.warning("Please select at least one option for Sentiment Analysis.")

    # Submit button
    if st.button("Submit"):
        st.subheader("Results")
        st.write(f"Company Ticker: {ticker}")
        for analysis_type, result in results.items():
            if analysis_type == 'Technical':
                # st.write(f"Technical Analysis")
                st.subheader("Technical Analysis")
                for x in result:
                    st.write(x)
            if analysis_type == 'Fundamental':
                st.subheader("Fundamental Analysis")
                for x in result:
                    st.write(x)
            if analysis_type == 'Sentiment':
                # st.write('Sentiment Analysis : ')
                st.subheader("Sentiment Analysis")
                for x in result:
                    for y in x:
                        st.write(y)
            # st.write(f"{analysis_type}: {result}")
else:
    st.warning("Please enter a company ticker.")

disclaimer_text = """
<div class="footer-note" style="font-size: 0.8em;">  Note: We provide financial analysis based on technical, fundamental, and sentiment data. We do not provide investment advice.
  <br>
  For Technical Analysis we Support : ACN,ADBE,CRM,GOOGL,INTU,META,MSFT,NFLX
  <br>
  For Fundamental Analysis we Support : Technology Sector
  <br>
  For Sentiment Analysis we Support All tickers.
</div>
"""

st.markdown(disclaimer_text, unsafe_allow_html=True)

# streamlit run app.py
