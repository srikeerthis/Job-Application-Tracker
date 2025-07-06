from gmail_client import get_gmail_service, fetch_emails
from database import save_application
from parser import parse_mail

def main():
    service = get_gmail_service()
    if service:
        print("Gmail service created successfully.")
        emails = fetch_emails(service=service, return_full_message=True)
        if emails:
            for email in emails:
                parsed_data = parse_mail(email)
                if parsed_data:
                    save_application(parsed_data)
                else:
                    print("No relevant data found in the email.")
        print("Email fetching completed.")
    else:
        print("Failed to create Gmail service.")

if __name__ == "__main__":
    main()
    print("Job application tracker completed successfully.")