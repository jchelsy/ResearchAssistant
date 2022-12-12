__all__ = ['userChoiceString', 'userChoiceChar',
           'userChoiceInt', 'choiceYesNo', 'choiceNum']


# Method to output a question & get user input
def userChoiceString(txt):
    # Output the question & return user input
    return input(txt + ": ")


# Method to output "Choice: " get user input
def userChoiceChar():
    # Output "Choice: " & return user input
    return input("Choice: ")


# Method to get user input (no output)
def userChoiceInt():
    # Return user input
    return input(">>> ")


# Method to get a Yes/No answer from the user
def choiceYesNo():
    # Keep repeating the code block until a proper
    # answer is given (Y/N).
    # Upon returning True/False, the loop breaks.
    while True:
        # Output "(Y\N): " & set var
        # 'choice' to the user input
        choice = userChoiceString("(Y/N)")

        # If user chose 'Y'/'y':
        if choice.lower() == "y":
            # return True
            return True
        # If user chose 'N'/'n':
        elif choice.lower() == "n":
            # return False
            return False
        # Otherwise:
        else:
            # Output error message to the user
            print("Please choose only Yes or No.")

            # No return or break here, so the loop
            # repeats for a proper Y/N answer.


def choiceNum(numOfChoices):
    # Keep repeating the code block until a proper
    # answer is given (a valid integer).
    # Upon returning a value, the loop breaks.
    while True:
        # Set var 'choice' to user input
        choice = userChoiceInt()

        # If user chose a valid integer:
        if 1 <= int(choice) <= numOfChoices:
            # Return the chosen number (string)
            return int(choice)
        # Otherwise (if a non-valid integer was given):
        else:
            # Output error message to the user
            print("Please choose only a number between 1 and " + str(numOfChoices) + ".")

            # No return or break here, so the loop
            # repeats for a valid response.
