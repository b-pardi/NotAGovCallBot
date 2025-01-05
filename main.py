import argparse

import src.call as call
import src.text as text

def main():
    parser = argparse.ArgumentParser(description="Repeat call govt agency, or send a shit load of texts to an enemy maybe idk i admit to nothing")

    parser.add_argument(
        '-m', '--method',
        type=str,
        choices=['call', 'text'],
        required=True,
        help="Specify to 'call' or 'text'"
    )

    args = parser.parse_args()

    if args.method == 'call':
        call.main()
    if args.method == 'text':
        text.main()

if __name__ == '__main__':
    main()