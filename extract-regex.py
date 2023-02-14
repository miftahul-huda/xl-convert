import argparse
import re


def main():

    parser = argparse.ArgumentParser(
                    prog = 'extract-regex.py',
                    description = 'Extract Regex',
                    epilog = 'Devoteam')

    parser.add_argument('-f', '--file', help='The file to search', required=True)  
    parser.add_argument('-r', '--regex', help='The regex expression', required=True)  
    parser.add_argument('-o', '--output', help='The output file', required=True)  
    parser.add_argument('-u', '--unique', help='Should the result unique?', required=False)  

    args = parser.parse_args()

    print("Searching...")
    if(args.unique == None):
        args.unique = False
    else:
        args.unique =  True

    extract(args.file, args.regex, args.output, args.unique)


def extract(file, regex, output, unique=False):

    result = ""
    if (file == None):
        print("Please provide filename.")
        exit()
   

    contents = None
    regex_definitions = None
    with open(file) as f:
        contents = f.read()
        f.close()

    existing= []
    matches = re.findall(regex, contents, re.IGNORECASE)
    for match in matches:
        if(type(match) == str):
            if((unique and match not in existing) or (unique == False)):
                print(match)
                result += match + "\r\n"
                existing.append(match)


    f = open(output, "w")
    f.write(result)
    f.close()

    print("\nExtracting finished. The extracted result is saved to '" + output + "'")


if __name__ == "__main__":
    main()



