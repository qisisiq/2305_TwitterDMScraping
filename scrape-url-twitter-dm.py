import json
import re
from collections import defaultdict
from datetime import datetime

def extract_links_from_twitter_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # Read the file
        content = f.read()

        # Remove the JavaScript variable assignment
        content = content[content.find('['):content.rfind(']')+1]

        # Load the JSON
        data = json.loads(content)

        # Regex to find URLs
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

        # Dictionary to hold the URLs by month
        urls_by_month = defaultdict(list)

        # Loop through the conversations
        for conversation in data:
            # Loop through the messages in each conversation
            for message in conversation['dmConversation']['messages']:
                # Extract senderId, recipientId, createdAt, and text from messageCreate
                senderId = message['messageCreate']['senderId']
                recipientId = message['messageCreate']['recipientId']
                text = message['messageCreate']['text']
                createdAt = message['messageCreate']['createdAt']

                # Only consider messages sent by you to yourself
                if senderId == recipientId:
                    # Find all URLs in the text
                    urls = re.findall(url_pattern, text)

                    # Parse createdAt into a datetime object
                    timestamp = datetime.strptime(createdAt, "%Y-%m-%dT%H:%M:%S.%fZ")
                    month = timestamp.strftime('%Y-%m')

                    # Add each URL to the list for this month
                    for url in urls:
                        urls_by_month[month].append(url)

    # Write URLs by month to a text file
    with open('output_links.txt', 'w') as output_file:
        for month, urls in urls_by_month.items():
            output_file.write(f'Links from {month}:\n')
            for url in urls:
                output_file.write(f'{url}\n')
            output_file.write('\n')

# Use the function
extract_links_from_twitter_data('direct-messages.js')
