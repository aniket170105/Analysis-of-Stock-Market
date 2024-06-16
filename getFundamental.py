### Order --->>> reportedEPS	Current Ratio	Quick Ratio	Debt to Equity	Debt to Asset	
# Gross Margin	Profit Margin	Operating Margin	Interest Coverage	Return On StockHolder	Free Cash Flow Conversion

import joblib
import numpy as np

def appFundamental(list_of_ratios, sector):
    loaded_pipeline = joblib.load(f'Fundamental Analysis/{sector}FundamentalModel.pkl')
    temp = [list_of_ratios] ###Because model expect a 2D array
    predictions = loaded_pipeline.predict(temp)
    return predictions

print(appFundamental([1.4600,0.988012,0.843312,4.673462,0.823741,0.456823,0.305076,0.316398,27.944112,0.369388,0.656100],'technologySector'))

