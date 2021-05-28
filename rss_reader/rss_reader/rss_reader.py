"""Main module. Receive input info from console, parse it and print result to stdout."""

import requests
from bs4 import BeautifulSoup
import json
import argparse
import logging
import logging.handlers
import sys
import feedparser
from urllib.error import URLError


def command_arguments_parser(args):
    """Adds positional and optional arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", help="Print version info", version="Version 1.2")
    parser.add_argument("source", type=str, help="RSS URL")
    parser.add_argument("-j", "--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("-l", "--limit", type=int, help="Limit news topics if this parameter provided")
    parser.add_argument("--date", type=str)
    args = parser.parse_args(args)
    return args


def server_answer(source):
    """Getting answer from server"""
    try:
        answer = requests.get(source)
        if answer.status_code == 200:
            return answer
    except Exception:
        print("Xml was failed. Input the correct URL, please")


def parses_data(information, limit):
    """Parses data from the xml"""
    list_of_news = []
    data = {}

    try:
        buitiful_soup = BeautifulSoup(information, "xml")
        data["feed"] = buitiful_soup.find("title").text
        news_for_print = buitiful_soup.findAll("item", limit = limit)
        for alone_news in news_for_print:
            title = alone_news.find("title").text
            pub_date = alone_news.find("pubDate").text
            link = alone_news.find("link").text
            images = []
            images_find = alone_news.findAll("media:content")
            for image in images_find:
                link_of_image = image.get("url")
                images.append(link_of_image)
            news_dictionary = {"title": title, "pubDate": pub_date, "link": link, "images": images}
            list_of_news.append(news_dictionary)
        data["news"] = list_of_news
    except Exception:
        print("Xml was failed")
    return data


def printing_news(data):
    """Print news on console"""
    print("\nfeed:", data["feed"], "\n")
    for part in data["news"]:
        print("title:", part["title"])
        print("pubDate:", part["pubDate"])
        print("link:", part["link"])
        print("images:", len(part["images"]))
        print('\n'.join(part["images"]), "\n")
    print("Amount of news:", len(data["news"]), "\n")


def printing_json(data):
    """Print json news on console"""
    print(json.dumps(data, indent=3))


def configurates_logger(verbose):
    """Selects output data for logs and configures the logger"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
        if verbose
        else [
            logging.FileHandler("logs.log"),
        ],
    )
    logger = logging.getLogger()
    return logger


def open_rss_link(source, verbose):
    """Retrieves and processes URLs, print logs"""
    logger = configurates_logger(verbose)

    try:
        news = feedparser.parse(source)
        if not source:
            raise ValueError
        logger.info(f"Reading link {source}")
    except URLError as e:
        logger.error(f"Error {e} in opening the link {source}")
        return print("Wrong link, try again, please")
    except ValueError as e:
        logger.error(f"Error {e} in opening the link {source}")
        return print("Input link, please")
    return news


def main():
    args = command_arguments_parser(sys.argv[1:])
    answer = server_answer(args.source)
    logger = configurates_logger(args.verbose)

    if args.limit == 0:
        print("Invalid limit. Enter the limit (greater than 0), please")
        sys.exit(0)

    try:
        logging.info("Getting access to the RSS")
        number_of_news = parses_data(answer.text, args.limit)
        if args.limit:
            logging.info(f"Reads amount of news - {args.limit}")
        if args.json:
            logging.info("In json")
            printing_json(number_of_news)
        else:
            printing_news(number_of_news)
    except (AttributeError, ValueError, TypeError, FileNotFoundError):
            sys.exit()

    except (requests.exceptions.ConnectionError, requests.exceptions.InvalidURL):
        print("ConnectionError. Correct the URL, please")

    except requests.exceptions.MissingSchema:
        print("Incorrect URL. This is not the rss feed address.")

    logger.info(f"End of reading")

if __name__ == "__main__":
    main()
