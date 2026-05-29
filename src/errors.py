from datetime import datetime
import logging

def save_error_as_csv(df_errors, error_type, layer):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    path = f"data/errors/{layer}/{timestamp}_{error_type}.csv"
    df_errors.to_csv(path, index = False)
    logging.warning(f"{len(df_errors)} errors of type {error_type} saved on {path}")    
    
def save_error_as_log(match_id: str, status_code: int, reason: str):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    path = f"data/errors/extraction/{timestamp}_extraction_error.log"
    
    with open(path, "a") as f: # "a" : append, errors are additive in the same file
        f.write(f"{timestamp} | match_id: {match_id} | status: {status_code} | reason : {reason}")
        
    logging.error(f"Extraction error in match {match_id} : {status_code} - {reason}")