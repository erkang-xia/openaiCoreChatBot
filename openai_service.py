# --------------------------------------------------------------
# Test code 
# --------------------------------------------------------------

from openai import OpenAI
import shelve
from dotenv import load_dotenv
import os
import time
import logging
import json
from llama_service import search_for_long_term_memory
from firbase_service import add_task


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
client = OpenAI(api_key=OPENAI_API_KEY)


# run = client.beta.threads.runs.retrieve(
#   thread_id="thread_mPVccLFbmY28Ct8KVeYkczNg",
#   run_id="run_QuoqZ6kWjiPiCDux2SiLPXOY"
# )
# print(run.status)
# run = client.beta.threads.runs.cancel(
#   thread_id="thread_mPVccLFbmY28Ct8KVeYkczNg",
#   run_id="run_dzhssCFEkfLReuMie03xf51e"
# )
# print(run)

# Use context manager to ensure the shelf file is closed properly
def check_if_thread_exists(wa_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(wa_id, None)


def store_thread(wa_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[wa_id] = thread_id

thread_id = "thread_wV3TzaQKP04fF1qnKWOgHBZf"
wa_id = "OTTKQMDDbbSSVhY4Y0oKcFWa9gI3"
#store_thread(wa_id, thread_id)


def generate_response(message_body, wa_id, name):
    # Check if there is already a thread_id for the wa_id
    thread_id = check_if_thread_exists(wa_id)

    # If a thread doesn't exist, create one and store it
    if thread_id is None:
        logging.info(f"Creating new thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.create()
        store_thread(wa_id, thread.id)
        thread_id = thread.id

    # Otherwise, retrieve the existing thread
    else:
        logging.info(f"Retrieving existing thread for {name} with wa_id {wa_id}")
        thread = client.beta.threads.retrieve(thread_id)

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant_with_help(thread)

    return new_message


def run_assistant_with_help(thread):
    # Retrieve the Assistant
    #
    assistant = client.beta.assistants.retrieve(OPENAI_ASSISTANT_ID)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    
    
    
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        if run.status == "requires_action":
            #get the fuction name and parameter to call function 
            tool_outputs = []
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                output = deliver_func(function_name, arguments)
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": output,
                })

            # Submit function outputs
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    logging.info(f"Generated message: {new_message}")
    return new_message


# Implement the logic to handle different function calls
def deliver_func(function_name, arguments):
    if function_name == "need_llama":
        return search_for_long_term_memory(arguments["message"])
        
    elif function_name == "add_task":
        # TODO implement flask to manage user session 
        return add_task("12344",arguments["task"],arguments["time"],arguments["repeat"])
    
    elif function_name == "add_task":
        # TODO implement flask to manage user session 
        return add_task("12344",arguments["task"],arguments["time"],arguments["repeat"])
        

    else:
        raise ValueError(f"Unknown function: {function_name}")

    return "Function output here"