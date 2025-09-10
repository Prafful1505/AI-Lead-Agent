import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# --- CONFIGURATION ---
# Define the scope for Google Sheets and Drive APIs
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# The name of the JSON file with your service account credentials
CREDS_FILE = 'credentials.json'
# The name of the Google Sheet where leads will be stored
SHEET_NAME = 'Leads'

def get_sheet_client():
    """
    Authenticates with the Google Sheets API using service account credentials
    and returns a client object.
    
    Returns:
        gspread.Client or None: An authenticated gspread client object, or None if authentication fails.
    """
    if not os.path.exists(CREDS_FILE):
        print(f"Error: Credentials file not found at '{CREDS_FILE}'")
        print("Please follow the setup instructions in README.md to create and place the credentials file.")
        return None
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Failed to authorize Google Sheets API: {e}")
        return None

def save_lead(data):
    """
    Saves a new lead's data to the specified Google Sheet.
    The function expects data as a list in the order: [Name, Budget, Timeline, Notes].
    
    Args:
        data (list): A list of strings containing the lead's information.
    """
    print(f"Attempting to save lead: {data}")
    client = get_sheet_client()
    if not client:
        print("Could not save lead due to authentication failure.")
        return

    try:
        # Open the spreadsheet
        sheet = client.open(SHEET_NAME).sheet1
        
        # Check for header row and add if it doesn't exist
        header = ["Name", "Budget", "Timeline", "Notes"]
        if not sheet.get_all_values() or sheet.row_values(1) != header:
            sheet.insert_row(header, 1)
            print("Added header row to the sheet.")
            
        # Append the new lead data as a new row
        sheet.append_row(data)
        print("Lead successfully saved to Google Sheets.")
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet named '{SHEET_NAME}' not found.")
        print("Please create the Google Sheet and share it with your service account email.")
    except Exception as e:
        print(f"An error occurred while saving the lead: {e}")


if __name__ == '__main__':
    # Example usage for testing the module directly
    print("Testing Google Sheets Helper...")
    # This will fail if credentials.json is not set up correctly.
    test_data = ["Test User", "$10,000", "Next month", "This is a test entry from the script."]
    save_lead(test_data)
