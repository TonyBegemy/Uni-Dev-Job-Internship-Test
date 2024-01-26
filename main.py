### Importing the neccessary libraries
import warnings
import openai
import os
#from IPython.display import display, HTML
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate
import argparse
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

### Functions

def loadModel():
    """
     This is a function that is responsible for initiating the AzureChatOpenAI
    """
    return AzureChatOpenAI(
    openai_api_version = openai_api_version,
    #azure_deployment = openai_api_deployment ,
    base_url = openai_api_endpoint,
    api_key = openai_api_key,
    openai_api_type = openai_api_type,
    model_version = openai_api_model,
    temperature=0.3 ### higher temperature = more randomness and creativity, From 0 to 1.
    
)
def getPrompt(args):
    """
     This is a function used to generate structured prompts. (prompts used only for generating code from question)
    """
    template = """
    Generate a code given the user's query \
    that is delimited by triple backticks, \
    using the programming language: {programing_language}. \
    User's query: ```{code_question}``` \
    Instructions: {Instructions}
    """
    prompt_template = ChatPromptTemplate.from_template(template) # function user to return the input_variables
    prompt = prompt_template.format_messages(
    programing_language=args.language,
    code_question=args.question,
    Instructions = Instructions)
    return prompt

def argumentParser():
    """
     This is a function uses the command-line parsing module in the Python.
    """
    parser = argparse.ArgumentParser()
    # The two below lines return the Programming language and question written bt command line to the object parser
    parser.add_argument("-language", '-lang', '-l', help="Programming language for code e.g. Python", nargs='*', required=True, type=str) 
    parser.add_argument("-question","-q", help="Enter your Question", nargs='*', required=True, type=str)
    args = parser.parse_args()
    return args

def generateResponse():
    """
     This is a function used to generate response from the prompt.
    """
    model = loadModel()
    arguments = argumentParser()
    prompt = getPrompt(args = arguments)
    response = model(prompt)
    print(response.content)

def main():
    """
     This is a main function responsible for the implementation of the code.
    """
    generateResponse()


if __name__ == "__main__":
    #####################################################
    ### Variables
    openai_api_type = os.getenv("OPENAI_API_TYPE")
    openai_api_base = os.getenv("OPENAI_API_BASE")
    openai_api_version = os.getenv("OPENAI_API_VERSION")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_api_endpoint = os.getenv("OPENAI_API_ENDPOINT")
    openai_api_deployment = os.getenv("OPENAI_API_DEPLOYMENT")
    openai_api_model = os.getenv("OPENAI_API_MODEL")
    Instructions =  '''1. write comments in every section in code to illustrate. \
    2. Write below the code in brief a description for the code. \
    3. try to add an implementation example for the code.
    '''
#############################################################
    ### Main function Implementation
    warnings.filterwarnings("ignore")
    main()

#############################################################
#How To Use :
#Open The Terminal "CTRL + Telda(~)", write 'python <write path>\main.py -lang <Write here Programming language for code e.g. Python> -question <Your question or task needed>
#As an example:
# write 'python main.py -lang Python -question write a code to generate a random number'