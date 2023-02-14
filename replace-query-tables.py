import argparse
import re


def main():

    parser = argparse.ArgumentParser(
                    prog = 'replace-query-tables.py',
                    description = 'Replace tables in query with its full format',
                    epilog = 'Devoteam')

    parser.add_argument('-q', '--query', help='The query file', required=True)  
    parser.add_argument('-s', '--source', help='The source table names file', required=True)  
    parser.add_argument('-o', '--output', help='The output file', required=True)  
    args = parser.parse_args()

    print("Replacing...")
    replaceTables(args.query, args.source, args.output)

def replaceTables(queryfile, sourcefile, outputfile):
    query_contents = None
    source_contents = None
    output_content = None 
    source_tables = []

    with open(queryfile) as f:
        query_contents = f.read()
        f.close()

    with open(sourcefile) as f:
        source_contents = f.read()
        f.close()
        source_tables = source_contents.split("\n")

    
    print("================ REPLACE 'FROM' TABLES...=====================\n")
    [query_contents, replaced_tables] = replace_all_tables(query_contents, source_tables, "from\s+(\w+\.\w+)", [])
    
    print("================ REPLACE 'JOIN' TABLES...=====================\n")
    [query_contents, replaced_tables] = replace_all_tables(query_contents, source_tables, "join\s+(\w+\.\w+)", replaced_tables)
    
    print("================ REPLACE 'INTO' TABLES...=====================\n")
    [query_contents, replaced_tables] = replace_all_tables(query_contents, source_tables, "into\s+(\w+\.\w+)", replaced_tables)
    
    print("================ REPLACE 'CREATE' TABLES...=====================\n")
    [query_contents, replaced_tables] = replace_all_tables(query_contents, source_tables, "create\s+table\s+(\w+\.\w+)", replaced_tables)
    
    print("================ REPLACE 'DROP' TABLES...=====================\n")
    [query_contents, replaced_tables] = replace_all_tables(query_contents, source_tables, "drop\s+table\s+if\s+exists\s+(\w+\.\w+)", replaced_tables)
    
    print("================ REPLACE 'TRUNCATE' TABLES...=====================\n")
    [query_contents, replaced_tables] = replace_all_tables(query_contents, source_tables, "truncate\s+table\s+if\s+exists\s+(\w+\.\w+)", replaced_tables)
    
    print("================ REPLACE 'DELETE' TABLES...=====================\n")
    [query_contents, replaced_tables] = replace_all_tables(query_contents, source_tables, "delete\s+table\s+if\s+exists\s+(\w+\.\w+)", replaced_tables)

    print("Cleaning...")
    query_contents = clean(query_contents)

    f = open(outputfile, "w")
    f.write(query_contents)
    f.close()


def replace_all_tables(query_contents, source_tables, regex, replaced_tables):
    from_tables = re.findall(regex, query_contents, re.IGNORECASE)
    for table in from_tables:
        if(table not in replaced_tables and "not_found" not in table):
            print("Search for {} ...".format(table))
            found_table = search_table_from_source(source_tables, table)
            if(found_table is None):
                found_table =  "not_found." + table
            
            print("Replacing '{}' with '{}'.\n".format(table, found_table))
            query_contents = query_contents.replace(table, found_table)
            
            replaced_tables.append(table)
            replaced_tables.append(found_table)
    
    return [query_contents, replaced_tables]

def clean(query_contents):
    pattern = "[A-Za-z-0-9_]+\.[A-Za-z-0-9_]+\."
    matches = re.findall(pattern, query_contents, re.IGNORECASE)
    for match in matches:
        if(type(match) is str):
            m = match.split(".")
            if(m[0] == m[1]):
                to_replace  = m[0] + "." + m[0];
                replaced_by = m[0]
                print("Replacing {} with {}...".format(to_replace, replaced_by))
                query_contents = query_contents.replace(to_replace, replaced_by)
    
    return query_contents

def search_table_from_source(source_tables, table):
    for source_table in source_tables:
        if(table in source_table):
            return source_table
    
    return None


if __name__ == "__main__":
    main()