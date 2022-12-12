from choices import *
from functions import *

# Library to fetch data
import wikipedia
# Library to summarize data
import sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
# Library to present the data
import pyttsx3


def main(append=False):
    # Initialize checker boolean
    no_topic = True

    # Have the user pick a valid topic
    topic = findTopic()
    while no_topic:
        # If the user picked a topic (and didn't choose "[None]"):
        if topic != "[None]":
            # Set the checker boolean to False (to exit the while loop)
            no_topic = False
        # Otherwise (if the user didn't pick a topic):
        else:
            # Guide the user to find another topic
            topic = findTopic()

    # Output ASCII art of the topic title
    asciiText(topic + " :")

    # Get the data about the chosen topic
    data = getData(topic)
    # Format the data to be easily readable
    list_data = scrubData(data)
    # Print the formatted data
    printData(list_data)

    # Have the AI speak the research results
    speak(data['title'], summarize(data['summary']))

    # Prompt the user to save the collected data
    print("Save research data to file?")
    choice_bool = choiceYesNo()

    # If the user chose to save it:
    if choice_bool:
        # Save the data
        saveData(list_data, append)
    # Otherwise:
    else:
        # Output an affirmation
        print("\nOkay.")

    # Prompt the user to research another topic
    print("\nResearch something else?")
    choice_bool = choiceYesNo()

    # If the user chose to research again:
    if choice_bool:
        # Output line break
        print()
        # Re-run the main method to start the process over again
        main(True)
    # Otherwise:
    else:
        # Output the user a farewell
        print("\nGoodbye.")


def researchSuggestions(researchTopic):
    options = wikipedia.search(researchTopic)
    options.append("[None]")
    print("Research one of these?")

    counter = 1
    for i in options:
        print(str(counter) + ":", i)
        counter += 1

    return options


def findTopic():
    topic = input("What would you like to research? ")

    suggestion = wikipedia.suggest(topic)

    if suggestion is not None:
        print("Research \"" + suggestion + "\"?")
        choice_bool = choiceYesNo()

        if choice_bool:
            topic = suggestion
        elif not choice_bool:
            options = researchSuggestions(topic)

            topic = options[choiceNum(len(options)) - 1]
    else:
        options = researchSuggestions(topic)

        topic = options[choiceNum(len(options)) - 1]

    return topic


def getData(researchTopic):
    data = {
        'title': wikipedia.page(researchTopic).title,
        'url': wikipedia.page(researchTopic).url,
        'content': wikipedia.page(researchTopic).content,
        'summary': wikipedia.page(researchTopic).summary,
        'categories': wikipedia.page(researchTopic).categories,
        'links': wikipedia.page(researchTopic).links,
        'images': wikipedia.page(researchTopic).images,
        'references': wikipedia.page(researchTopic).references
    }

    return data


def scrubData(data):
    list_data = [data['title'], "\n",
                 data['url'], "\n",
                 "\n" * 2 + "#" * 120, "\n",
                 "#" * 55 + " Summary " + "#" * 56, "\n",
                 "#" * 120 + "\n", "\n",
                 ]

    char_count = 0
    sentence = ""

    for char in data['summary']:
        char_count += 1
        sentence = sentence + char

        if char_count >= 120 and char in ('.', '!', '?', ',', ' '):
            char_count = 0
            list_data.append(sentence + "\n")
            sentence = ""

    list_data.append("\n" * 2 + "#" * 120 + "\n")
    list_data.append("#" * 54 + " References " + "#" * 54 + "\n")
    list_data.append("#" * 120 + "\n" + "\n")

    for ref in data['references']:
        list_data.append(ref + "\n")

    list_data.append("\n" * 2 + "#" * 120 + "\n")
    list_data.append("#" * 50 + " Compressed Summary " + "#" * 50 + "\n")
    list_data.append("#" * 120 + "\n" * 2)

    for sentence in summarize(data['summary']):
        list_data.append(str(sentence))
        list_data.append("\n")

    list_data.append("\n" * 2)

    return list_data


def printData(data_list):
    for line in data_list:
        print(line, end='')


def saveData(data_list, append=False):
    if append:
        file = open("Research.txt", "a")
        file.writelines("\n\n\n\n\n\n\n\n\n\n")
    else:
        file = open("Research.txt", "w")

    file.writelines(data_list)

    file.close()


def summarize(fullSummary):
    summary = ""

    for sentence in fullSummary:
        summary += sentence

    parser = PlaintextParser.from_string(summary, Tokenizer("english"))

    # Use the LexRank summarizer - one algorithm to summarize the data
    summarizer = LexRankSummarizer()

    # How many sentences to return for the summary?
    num_of_sentences_in_summary = 4

    # Let the magic happen - SUMMARIZE!
    compressed_summary = summarizer(parser.document, num_of_sentences_in_summary)

    return compressed_summary


def speak(title, summary):
    zira_voice_id = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

    # Initialize the speech converter
    converter = pyttsx3.init()
    # Set the rate of speech (100 = 100% normal speed)
    converter.setProperty('rate', 150)
    # Set the speech volume (values of 0-1)
    converter.setProperty('volume', 0.7)
    # Set the speech voice
    converter.setProperty('voice', zira_voice_id)

    # What does the AI say?
    converter.say("Research on " + title + " successful...")
    converter.say("Initializing summarized results.....")

    for sentence in summary:
        converter.say(sentence)

    # Speak the programmed text
    converter.runAndWait()

    # See available voices
    # voices = converter.getProperty('voices')
    # for voice in voices:
    #     print("VOICE ID: %s" % voice.id)


if __name__ == "__main__":
    main()
