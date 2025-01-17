import openai
from app import app, Message, db
import textwrap

# Set your OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

with app.app_context():
    # Fetch all messages from the database
    messages = Message.query.all()

# Generate a prompt for GPT
prompt = "You are a data analyst processing incoming chat message data from a customer service chat widget on our demonstration e-commerce web store hooked up to ShipStation. What useful business data can you glean from the following messages:\n\n"

for message in messages:
    prompt += f"{message.sender}: {message.content}\n"

prompt += "\nSummary:"

# Connect to ChatGPT and get the response
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=prompt,
    temperature=0.5,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)

# Extract the summary from the response
summary = response.choices[0].text.strip()

# Wrap the summary at 80 characters
wrapped_summary = textwrap.fill(summary, width=80)

# Print the summary
print("Summary of messages:")
print(wrapped_summary)