from scripts.database.log_error import log_error

def isTradeExists(trades, trade_id):
    try:
        # Ensure trade_id is treated as a string for comparison
        str_trade_id = str(trade_id)
        
        # Iterate through trades list
        for trade in trades:
            # Check if trade id matches
            if str(trade['id']) == str_trade_id:
                return True
        
        # If no match found, return False
        return False
    
    except Exception as e:
        errMsg = f"Task: (Is Trade Exists)  Error: {e}"
        print(errMsg)
        log_error(errMsg)
        return False