import sys
import argparse
import json
from pprintjson import pprintjson as ppjson
from helpers.defs import get_user
from helpers.defs import get_repos
from helpers.defs import get_events
from helpers.defs import create_html
from helpers.defs import json_merge


def main(user, output):
    user_data = get_user(user)
    repos_data = get_repos(user)
    events_data = get_events(user)
    merged_data = json_merge(
        user_data,
        repos_data,
        events_data
    )
    if output == 'pretty':
        ppjson(merged_data)
    elif output == 'html':
        output = create_html(merged_data)
        print("Created file ./{}".format(output))
    else:
        print(json.dumps(merged_data, sort_keys=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', action='store', help="Github username", required=True) # noqa : 501
    parser.add_argument('-o', '--output', choices=['pretty', 'html'], help="Select output") # noqa: 501
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if args.user:
        main(args.user, args.output)
