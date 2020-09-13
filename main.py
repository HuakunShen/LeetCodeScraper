import argparse
import src.scrape_extra_info as spider


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Scrape Extra Info")
    parser.add_argument('-m', '--multiprocess', action='store_true',
                        help='Use Multiprocessing (utilize as much cores as possible)')
    parser.add_argument('-y', '--yield_', action='store_true',
                        help='Use Yield when Sending requests')
    args = parser.parse_args()
    spider.main(yield_=args.yield_, multiprocess=args.multiprocess)
