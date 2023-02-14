python3 extract-regex.py -f script.sql -r "from\s+(\w+\.\w+)\s+" -o output.txt
python3 extract-regex.py -f script.sql -r "join\s+(\w+\.\w+)\s+" -o output.txt
python3 extract-regex.py -f script.sql -r "into\s+(\w+\.\w+)\s+" -o output.txt
python3 extract-regex.py -f script.sql -r "create\s+table\s+(\w+\.\w+)" -o output.txt
python3 extract-regex.py -f script.sql -r "truncate\s+table\s+(\w+\.\w+)" -o output.txt
python3 extract-regex.py -f script.sql -r "delete\s+table\s+(\w+\.\w+)" -o output.txt
python3 extract-regex.py -f script.sql -r "drop\s+table\s+if\s+exists\s+(\w+\.\w+)" -o output.txt
python3 extract-regex.py -f script.sql -r "truncate\s+table\s+if\s+exists\s+(\w+\.\w+)" -o output.txt
python3 extract-regex.py -f script.sql -r "delete\s+table\s+if\s+exists\s+(\w+\.\w+)" -o output.txt

