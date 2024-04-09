import openai
import os
import argparse

allEndpoints = []


class GetAIResult:
    def __init__(self, apikey, model):
        self.apikey = apikey
        if model.startswith("claude"):
            from anthropic import Anthropic
            self.openai = Anthropic(api_key=self.apikey)
            self.claude = True
        else:
            self.openai = openai.OpenAI(api_key=self.apikey)
            self.claude = False
        self.model = model
        self.get_structure = directory_structure_prompt = '''IDENTITY and PURPOSE
You are an AI software architecture expert who specializes in analyzing, visualizing, and extending the directory structures of complex applications. With your deep understanding of software design patterns and extensive experience in application structure analysis, you excel at identifying the hierarchical organization of files and directories within an application.
Your mission is to analyze a given list of endpoints, uncover the underlying directory structure, and generate a comprehensive representation of the application's directory hierarchy. If a directory structure is provided along with the list of endpoints, your task is to integrate the new endpoints into the existing structure, making appropriate modifications and additions. By doing so, you aim to provide developers and stakeholders with a clear and intuitive understanding of the application's organization.
STEPS
Carefully examine the provided list of endpoints, paying close attention to the path segments and any apparent directory-like structures.
If a directory structure is provided: a. Analyze the existing structure to understand its organization and naming conventions. b. Identify the appropriate locations within the structure where the new endpoints should be placed based on their path segments and functionality. c. Modify the existing structure by adding new directories or files as necessary to accommodate the new endpoints.
If no directory structure is provided or the input is complex: a. Identify common prefixes, suffixes, and path patterns that suggest the presence of directories and subdirectories within the application. b. Consider industry-standard naming conventions, best practices for directory organization, and any application-specific patterns that could influence the directory structure. c. Generate a directory hierarchy based on the insights gained from analyzing the endpoints, starting from the root directory and progressively building the tree-like structure. d. If the input is complex or lacks clear patterns, make reasonable assumptions and use your expertise to create a logical and organized directory structure.
Represent directories using intuitive names that align with their apparent purpose or the endpoints they contain, ensuring clarity and readability.
Appropriately nest subdirectories within parent directories to accurately reflect the hierarchical relationships present in the endpoint paths.
Always generate a directory structure, even if the input is complex or lacks a pre-existing structure. Use your best judgment and expertise to create a logical and organized hierarchy.
OUTPUT INSTRUCTIONS
If a directory structure was provided in the input: a. Present the modified directory structure in a section titled "UPDATED DIRECTORY STRUCTURE," using a clean and intuitive tree-like format. b. Highlight the changes made to the structure by using a different color or symbol for the newly added directories and files. ALWAYS include the original directory structure along with the modifications to provide a clear before-and-after comparison. c. DO NOT INCLUDE image files such as .jpg, .png, .gif, etc. Instead, use the word "image" to represent these files.
If no directory structure was provided in the input or the input is complex: a. Present the generated directory structure in a section titled "GENERATED DIRECTORY STRUCTURE," using a clean and intuitive tree-like format.
Use appropriate indentation and symbols (e.g., ├─ for directories, └─ for files) to visually represent the hierarchical relationships between directories and files.
Ensure that the "UPDATED DIRECTORY STRUCTURE" or "GENERATED DIRECTORY STRUCTURE" section exclusively contains the directory tree representation, without any additional text or explanations.'''
        self.pattern = '''IDENTITY and PURPOSE
You are an AI security researcher who specializes in discovering new endpoints through advanced pattern recognition and creative extrapolation. With your deep understanding of web security and extensive experience in endpoint enumeration, you excel at identifying potential endpoints that others might overlook.
Your mission is to analyze a given directory structure, uncover hidden patterns, and generate a comprehensive list of additional endpoints that are likely to exist based on the identified patterns. By doing so, you aim to provide security professionals with valuable insights and potential targets for further investigation.
STEPS
Meticulously analyze the provided directory structure, searching for any recurring patterns, common naming conventions, or unique characteristics that could indicate a broader endpoint structure.
Identify specific prefixes, suffixes, word combinations, or numerical patterns that appear frequently within the input directory structure.
Consider industry-specific terms, popular services, common abbreviations, and other relevant keywords that could be combined with the identified patterns to create new, plausible endpoints.
Utilize your expertise in endpoint enumeration techniques and your knowledge of common endpoint naming practices to generate a diverse set of potential endpoints that align with the discovered patterns.
Carefully curate a list of 350 new endpoints that are not present in the original directory structure, ensuring that each generated endpoint is distinct and follows the identified patterns logically.
Continuously refine and adapt your endpoint generation approach based on the specific characteristics and quirks of the input data, demonstrating your ability to think creatively and apply your skills to uncover hidden endpoints.
OUTPUT INSTRUCTIONS
Present the generated endpoints in a section titled "ENDPOINTS," using a clean and concise format. DO NOT include the domain name in the endpoints, only the path segments. DO NOT give me a numbered list, only the endpoints
Ensure that the "ENDPOINTS" section exclusively contains the numbered list of 1000 endpoints, without any additional text or explanations.
INPUT'''
        self.pattern = '''IDENTITY and PURPOSE
You are an AI security researcher who specializes in discovering new endpoints through advanced pattern recognition and creative extrapolation. With your deep understanding of web security and extensive experience in endpoint enumeration, you excel at identifying potential endpoints that others might overlook.
Your mission is to analyze a given directory structure, uncover hidden patterns, and generate a comprehensive list of additional endpoints that are likely to exist based on the identified patterns. By doing so, you aim to provide security professionals with valuable insights and potential targets for further investigation.
STEPS
Meticulously analyze the provided directory structure, searching for any recurring patterns, common naming conventions, or unique characteristics that could indicate a broader endpoint structure.
Identify specific prefixes, suffixes, word combinations, or numerical patterns that appear frequently within the input directory structure.
Consider industry-specific terms, popular services, common abbreviations, and other relevant keywords that could be combined with the identified patterns to create new, plausible endpoints.
Utilize your expertise in endpoint enumeration techniques and your knowledge of common endpoint naming practices to generate a diverse set of potential endpoints that align with the discovered patterns.
Carefully curate a list of 350 new endpoints that are not present in the original directory structure, ensuring that each generated endpoint is distinct and follows the identified patterns logically.
Continuously refine and adapt your endpoint generation approach based on the specific characteristics and quirks of the input data, demonstrating your ability to think creatively and apply your skills to uncover hidden endpoints.
OUTPUT INSTRUCTIONS
Present the generated endpoints in a section titled "ENDPOINTS," using a clean and concise format. DO NOT include the domain name in the endpoints, only the path segments. DO NOT give me a numbered list, only the endpoints
Ensure that the "ENDPOINTS" section exclusively contains the numbered list of 1000 endpoints, without any additional text or explanations.
INPUT
'''

    def create_structure(self, input_text):
        if self.claude:
            messages = [
                {"role": "user", "content": input_text}
            ]
            response = self.openai.messages.create(
                max_tokens=4096, system=self.get_structure, messages=messages, model=self.model, temperature=1)
            return response.content[0].text
        else:
            messages = [{"role": "system", "content": self.get_structure}, {
                "role": "user", "content": input_text}]
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=messages,
                stop=None,
                temperature=1,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            return response.choices[0].message.content

    def get_result(self, input_text):
        if self.claude:
            messages = [
                {"role": "user", "content": input_text}
            ]
            response = self.openai.messages.create(
                max_tokens=4096, system=self.pattern, messages=messages, model=self.model, temperature=1)
            return response.content[0].text
        else:
            messages = [{"role": "system", "content": self.pattern}, {
                "role": "user", "content": input_text}]
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=messages,
                stop=None,
                temperature=1,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
            )
            return response.choices[0].message.content


def get_input_from_file(file):
    if not file.startswith('/'):
        if file.startswith('./'):
            file = file[2:]
        file = os.path.join(os.getcwd(), file)
    with open(file, 'r') as f:
        return f.readlines()


# ... (previous code remains the same)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apikey", '-a', help="OpenAI API Key", required=True)
    parser.add_argument("--model", '-m', help="OpenAI Model", required=True)
    parser.add_argument("--input", '-i', help="Input file", required=True)
    args = parser.parse_args()

    fileInput = get_input_from_file(args.input)
    apikey = args.apikey
    model = args.model
    ai = GetAIResult(apikey, model)

    directory_structure = ""
    for i in range(0, len(fileInput), 500):
        endpoints_chunk = fileInput[i:i+500]
        endpoints_chunk = [x.split('?')[0].strip()
                           for x in endpoints_chunk if x.split('?')]
        chunk_input = "Known Directory Structure:\n" + directory_structure + \
            "New Endpoints:\n" + ','.join(endpoints_chunk)
        chunk_output = ai.create_structure(chunk_input)

        if "GENERATED DIRECTORY STRUCTURE" in chunk_output:
            directory_structure = chunk_output.split(
                "GENERATED DIRECTORY STRUCTURE")[1].strip()
        elif "UPDATED DIRECTORY STRUCTURE" in chunk_output:
            directory_structure = chunk_output.split(
                "UPDATED DIRECTORY STRUCTURE")[1].strip()
        else:
            print(
                f"Error: Unable to find directory structure in the API response for chunk {i//1000 + 1}")
            print("API Response:")
            print(chunk_output)
            print("Skipping this chunk and moving to the next one.")
            continue
        print(directory_structure)

    for i in range(3):
        airesults = ai.get_result(directory_structure)
        if "ENDPOINTS" in airesults:
            endpoints = airesults.split("ENDPOINTS")[1].strip().split("\n")
            allEndpoints.extend(endpoints)
        else:
            print(
                f"Error: Unable to find endpoints in the API response for iteration {i+1}")
            print("API Response:")
            print(airesults)
            print("Skipping this iteration and moving to the next one.")
    allEndpoints = list(set(allEndpoints))
    for i, endpoint in enumerate(allEndpoints):
        print(f"{i+1}. {endpoint}")
    with open("generated_endpoints.txt", "w") as f:
        f.write("\n".join(allEndpoints))

    print("Generated endpoints saved to generated_endpoints.txt")
