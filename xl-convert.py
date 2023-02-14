import argparse
import re


def main():

    parser = argparse.ArgumentParser(
                    prog = 'xl-convert',
                    description = 'Convert XL Script',
                    epilog = 'Devoteam')

    parser.add_argument('-q', '--query', help='The query file', required=True)  
    parser.add_argument('-r', '--regex', help='The regex definition file', required=True)  
    parser.add_argument('-o', '--output', help='The output file', required=True)  
    args = parser.parse_args()

    print("Converting...")
    convert(args.query, args.regex, args.output)


def convert(file, regexfile, output):

    if (file == None):
        print("Please provide query filename.")
        exit()
    if (regexfile == None):
        print("Please provide regex filename.")
        exit()

    contents = None
    regex_definitions = None
    with open(file) as f:
        contents = f.read()
        f.close()

    with open(regexfile) as f:
        regex_definitions = f.read()
        f.close()

    regex_definitions = regex_definitions.split("\n")
    for line in regex_definitions:
        if(len(line.strip()) > 0): 
            l = line.split("===")
            title = l[0].strip()
            regex_search = l[1].strip()
            regex_replace = l[2].strip()

            first_char = line[0]

            if(first_char != "#"):
                print(title + "...")
                if("lowercase" in regex_replace.lower() or "uppercase" in regex_replace.lower() ):
                    matches = re.findall(regex_search, contents, re.IGNORECASE)
                    #print(matches)
                    for match in matches:
                        if("lowercase" in regex_replace.lower()):
                            for keyword in match:
                                contents = contents.replace(keyword, keyword.lower())
                        else:
                            contents = contents.replace(match, match.upper()) 
                else:
                    #print("Processing regex")
                    
                    #print("----- " + regex_search + "->" + regex_replace)
                    #print(regex_replace)
                    
                    #print(ms)
                    regex_replace = regex_replace.replace("$", "\\\\\\\\\\\\\\")
                    
                    contents = re.sub(regex_search, regex_replace, contents) 
                    contents = contents.replace("\\\\\\", "")    

                    
                    fucks = []
                    ms = re.findall(regex_search, contents, re.IGNORECASE)
                    for m in ms:
                        if(type(m) == str):
                            #print(m)
                            if(m not in fucks):
                                #print("=========word: " + m)
                                contents = contents.replace(m, regex_replace) 
                                fucks.append(m)
                    

    f = open(output, "w")
    f.write(contents)
    f.close()

    print("\nConverting finished. The converted result is saved to '" + output + "'")


if __name__ == "__main__":
    main()



