import argparse
import src.scrape_extra_info as spider
from src import to_table

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Scrape Extra Info")
    parser.add_argument('-m', '--multiprocess', action='store_true',
                        help='Use Multiprocessing (utilize as much cores as possible)')
    parser.add_argument('-y', '--yield_', action='store_true',
                        help='Use Yield when Sending requests')
    parser.add_argument('-t', '--table', action='store_true',
                        help='Generate Table')
    parser.add_argument('-r', '--readme', action='store_true',
                        help='Generate README')
    args = parser.parse_args()
    spider.main(yield_=args.yield_, multiprocess=args.multiprocess)
    if args.table:
        to_table.main()
    if args.readme:
        with open('README.md', 'w') as readme:
            with open('README_HEADER.md', 'r') as readme_header:
                with open('./Data/problems.md', 'r') as problems_table:
                    readme.write(readme_header.read())
                    readme.write(problems_table.read())
