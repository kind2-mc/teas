#!/bin/bash

log_ext=".log"
errors="0"

for test_file in `find rsc -iname "tests.xml"`
do
  log_file="$test_file$log_ext"
  printf "Running on \033[1m$test_file\033[0m ... "
  python src/__main__.py --max_proc 4 "$test_file" > "$log_file"
  if [ "$?" -eq "0" ]
  then
    echo -e "\033[32msuccess\033[0m."
    echo ""
    rm "$log_file"
  else
    errors=$((errors+1))
    echo -e "\033[31merror\033[0m."
    echo -e "> See log file \033[31m$log_file\033[0m."
    echo ""
  fi
done

if [ "$errors" -gt "0" ]
then
  echo -e "Done, \033[31m$errors errors\033[0m."
  exit 2
else
  echo -e "Done, \033[32mno errors\033[0m."
  exit 0
fi