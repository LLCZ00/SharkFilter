#
# Copyright (C) 2023 LLCZ00
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.  
#
"""
Create Wireshark filter based on given IP addresses

TODO:
    - Add support for protocols
"""
import sys
import argparse

_NAME = "sharkfilter.py"
_VERSION = "v1.0.0"
_AUTHOR = "LCZ00"
_DESCRIPTION = f"""{_NAME} {_VERSION}, by {_AUTHOR}
CLI tool for creating Wireshark filters using the given IP addresses.
"""

class SharkParser(argparse.ArgumentParser):
    """Override argparse class for better error handler"""
    def error(self, message="Unknown error", help=False):
        if help:
            self.print_help()
        else:
            print(f"Error. {message}")
            print(f"Try './{self.prog} --help' for more information.")
        sys.exit(1)


def parse_arguments():
    parser = SharkParser(
    prog=_NAME,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=_DESCRIPTION,
    epilog=f"Examples:\n\t{_NAME} 192.168.1.27 192.168.1.35 192.168.1.41\n\t{_NAME} --exclude 10.10.10.10 35.160.181.201"
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'{_NAME} {_VERSION}',
        help='Show version number and exit'
    )
    parser.add_argument(
        '-e', '--exclude',
        action='store_true',
        dest='exclude',
        help='Filter will EXCLUDE given IPs (Includes all by default)'
    )
    parser.add_argument(
        'ips',
        nargs='+',
        help="IP addresses to create filter with"
    )

    return parser.parse_args()
    

def exclude_filter(addrs):
    rule_text = "!("
    for addr in addrs:
        rule_text += f"ip.addr == {addr} || "
    if rule_text.endswith(" || "):
        rule_text = rule_text[:-4]
    rule_text += ")"
    return rule_text

def include_filter(addrs):
    rule_text = ""
    addrs_len = len(addrs)
    if addrs_len == 1:
        rule_text = f"ip.addr == {addrs[0]}"
    elif addrs_len == 2:
        rule_text = f"ip.addr == {addrs[0]} && ip.addr == {addrs[1]}"
    else:
        rules = []
        for addr_index, addr in enumerate(addrs):
            tmp_rule = f"ip.addr == {addr} && ("
            for count in range(addrs_len):
                if count != addr_index:
                    tmp_rule += f"ip.addr == {addrs[count]} || "                  
            if tmp_rule.endswith(" || "):
                tmp_rule = tmp_rule[:-4]
            tmp_rule += ")"
            rules.append(tmp_rule)
        for rule in rules:
            rule_text += f"({rule}) || "
        if rule_text.endswith(" || "):
            rule_text = rule_text[:-4]
    return rule_text

def main():
    args = parse_arguments()
    if args.exclude:
        print(exclude_filter(args.ips))
        return 0
    print(include_filter(args.ips))

if __name__ == "__main__":
    sys.exit(main())

