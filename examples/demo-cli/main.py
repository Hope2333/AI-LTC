#!/usr/bin/env python3
"""Demo CLI tool for AI-LTC lifecycle validation.

Commands:
  greet --name <name>   Greet a user by name
  wordcount <text>      Count words in the given text
"""
import argparse
import sys


def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to AI-LTC demo."


def wordcount(text: str) -> int:
    return len(text.split())


def main():
    parser = argparse.ArgumentParser(description="AI-LTC Demo CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    greet_parser = subparsers.add_parser("greet", help="Greet a user")
    greet_parser.add_argument("--name", required=True, help="Name to greet")

    wc_parser = subparsers.add_parser("wordcount", help="Count words")
    wc_parser.add_argument("text", nargs="+", help="Text to count words in")

    args = parser.parse_args()

    if args.command == "greet":
        print(greet(args.name))
    elif args.command == "wordcount":
        text = " ".join(args.text)
        count = wordcount(text)
        print(f"Word count: {count}")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
