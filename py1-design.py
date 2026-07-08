import sys
import json

def get_unique_emails(email_list):
    # Convert emails to lowercase for comparison but store original cases
    lower_to_original = {email.lower(): email for email in email_list}
    
    unique_emails = sorted(lower_to_original.values(), key=lambda e: e.lower())  # Sort case-insensitively
    gmail_emails = [email for email in unique_emails if email.lower().endswith('@gmail.com')]
    other_emails = [email for email in unique_emails if not email.lower().endswith('@gmail.com')]
    
    prioritized_emails = gmail_emails + other_emails
    return prioritized_emails[:10]  # Return no more than 10 emails

def main():
    if len(sys.argv) < 2:
        print("Usage: python py.py email1,email2,email3,... OR email1 email2 email3 ...")
        return
    
    # Join all arguments (to handle space-separated inputs), then split using both commas and spaces
    emails = " ".join(sys.argv[1:]).replace(",", " ").split()
    
    # Convert to JSON and print
    print(json.dumps({"emails": get_unique_emails(emails)}, indent=4))

if __name__ == "__main__":
    main()
