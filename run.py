# import logging

# from app import create_app

# #start point
# app = create_app()

# if __name__ == "__main__":
#     logging.info("Flask app started")
#     app.run(host="0.0.0.0", port=8000)



from openai_service import generate_response 
from datetime import date


def userInputRefinement(message):
    res = "Message date:"
    today = date.today()
    res = res + str(today) + " \n " + "Message: " + message
    return res


def main():
    # print("Welcome to the Chatbot! Type 'quit' to exit.")
    # print("Please enter your UID.")
    # isLogin = False
    # #name your own chatbot
    # chat_bot_name = "Chatbot"
    # while not isLogin:
    #     uid = input("Your UID: ").strip()
    #     if uid.lower() == 'quit':
    #         print("Exiting chatbot.")
    #         break

    #     user = get_user_by_uid(uid)
    #     if isinstance(user, str):
    #         print(user)  # Print error message
    #     else:
    #         isLogin = True
    #         print(f"User ID: {user.uid}")
    #         print(f"Email: {user.email}")
    #         print(f"Display Name: {user.display_name}")
    #         print("\n\n\n")
    #         print(f"{chat_bot_name}: Welcome Back {user.display_name if user.display_name != 'None' else ''}")
            
    # while isLogin:
    #     user_input = input("You: ")
    #     if user_input.lower() == 'quit':
    #         print(f"{chat_bot_name}: Goodbye!")
    #         break

        # Example: Call your chatbot's response logic here
    while True:                                                  #delete when done with test
        print("hello")
        user_input = userInputRefinement(input("You: "))                             #delete when done with test
        response = generate_response(user_input,"123","erkang")   #delete when done with test
        print(f"xiaoli: {response}")                            #delete when done with test
        # response = generate_response(user_input,user.uid,"erkang")
        # print(f"{chat_bot_name}: {response}")

if __name__ == "__main__":
    main()
