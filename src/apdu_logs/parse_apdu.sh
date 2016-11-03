# give as argument file to be parsed
# cat the output of that file and pipe it to apdu_parser.py

# get file path from argument
file_path=$1
cat $file_path | ./make_apdu_readable.py $file_path