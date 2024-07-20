from scripts.database.log_error import log_error

def findSet(sets, magic):
    try:
        for data in sets:
            if str(data["stats"]["magic"]) == str(magic):
                return data
    except KeyError as e:
        errMsg = f"Task: (Find Set)  KeyError: {e} - Error accessing 'stats' or 'magic' key in set data"
        print(errMsg)
        log_error(errMsg)
    except Exception as e:
        errMsg = f"Task: (Find Set)  Unexpected error: {e} occurred while finding set for magic {magic}"
        print(errMsg)
        log_error(errMsg)

    return None