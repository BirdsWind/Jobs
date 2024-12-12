

import re
from striprtf.striprtf import rtf_to_text
import matplotlib.pyplot as plt

# Install frameworks above if not already installed, for example
# pip install striprtf

# Function to read and parse the RTF file
def read_rtf_file(file_path):
    with open(file_path, "r") as file:
        rtf_content = file.read()
        # Convert RTF to plain text
        plain_text = rtf_to_text(rtf_content)
    return plain_text

# Function to count word frequencies
def count_word_frequencies(text, words):
    # Normalize text and split into words, it removes special characters 
    # \w matches any alphanumeric character(letter, digits, and underscore)
    # \s matches any whitespace character, spaces, tabs, newlines 
    normalized_text = re.sub(r"[^\w\s#.]", "", text.lower())
    # re.sub make this string "Hello world! C#" become "hello world c", replace all characters in text that are not alphanumeric or whitespace with an empty string
    # ^ negation, anything that is NOT alphanumeric or whitespace 
    #keep the # and .
    word_list = normalized_text.split()
    
    # Count frequencies
    # Return a dictionary 
    word_count = {}
    for word in words:
        # check if the word is a substring of the noamlized_text, adds all the 1.... that finds the match
        count = 0
        for w in word_list:
           if word.lower() in w.lower():
               count += 1
        word_count[word] = count
    return word_count

# Main script
if __name__ == "__main__":
    # Define your array of words, in my case, I feed in some of the most common phrases in IT
    words_to_count = [
    # General IT and Software Development
    "Cloud", "moln","Analyst", "Analytics",

    # Software and Web Development
    "Backend",

    # Data and Artificial Intelligence
    "Data", "ML",
    "Machine Learning", "AI", "Big Data", "Hadoop",

    # Infrastructure, Networking, and Security
    "DevOps", "cybersäkerhet",
    "Cyber", "Security", "SOC",
    "Network", "Nätverk", "Infrastructure",

    # Specialized Roles
    "QA", "Tester", "Testare", "Test",

    # Trendy or Emerging Roles
    "Site Reliability Engineer", "Blockchain", "VR", "IoT", "SRE",
    
    # Languages
    "Java", "python", "React",
    
    # platforms
    "Azure", ".Net", "C#", "Dotnet"
]


    # Path to your RTF file, I stored it as a textfile, tried to scrape it, well, dynamic content and javascript does not allow me to get the real data
    # If you can refine this, I am happy to see the code
    rtf_file_path = "WORDS.rtf"

    # Read the RTF file
    plain_text = read_rtf_file(rtf_file_path)

    # Count word frequencies
    frequencies = count_word_frequencies(plain_text, words_to_count)
    
    # Merge some specific keys, some words are in English, some in Swedish, they mean the same thing, I would like to merge them
    
    merged_data = {}
    merge_rules = {"moln/Cloud": ["moln", "Cloud"], 
                   "Analyst/Analytics": ["Analyst", "Analytics"],
                   "ML/Machine Learning": ["ML", "Machine Learning"],
                   "cybersäkerhet/Cyber": ["cybersäkerhet", "Cyber"],
                   "Network/Nätverk": ["Network", "Nätverk"],
                   "QA/Tester/Testare/Test":["QA", "Tester", "Testare", "Test"],
                   ".Net/Dotnet": [".Net", "Dotnet"]
                   }
    
    for new_key, old_keys in merge_rules.items(): 
        merged_value = sum(frequencies.get(key,0) for key in old_keys)
        merged_data[new_key] = merged_value

    for key, value in frequencies.items():
        if not any(key in group for group in merge_rules.values()):
            merged_data[key] = value
            
            
      # Sort the frequencies in ascending order
    sorted_frequencies = dict(sorted(merged_data.items(), key=lambda item:item[1]))

    # Print the results, just for development
    print("Word Frequencies:")
    for word, count in sorted_frequencies.items():
        print(f"{word}: {count}")
        
        
    # Visualise the results, where are the IT jobs?
    
jobs, counts = zip(*sorted_frequencies.items())
print(f'list of jobs {list(jobs)}')
# Plot the bar chart
plt.figure(figsize=(12, 10))
bars = plt.barh(jobs, counts, color="skyblue")
plt.xlabel("Job Count", fontsize = 10)
plt.ylabel("Job Name", fontsize = 10)
plt.title("Where are the IT jobs today?")
plt.xticks(fontsize = 8)
plt.yticks(fontsize = 8)

for bar in bars:
    plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}', va = 'center', ha = 'left')
plt.tight_layout()
plt.show()

# Good luck with finding jobs! I know it is not easy, don't give up and you are good enough! 