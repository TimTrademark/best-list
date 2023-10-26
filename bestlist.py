import argparse
from os import path
from typing import Set

import requests

parser = argparse.ArgumentParser(description='Downloads and combines seclist password files')
parser.add_argument('--force', default=False, action='store_true',
                    help='Force overwrite when combined file already exists')

URL = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/'
FILES_TO_COMBINE = ['2020-200_most_used_passwords.txt', '500-worst-passwords.txt', 'Keyboard-Combinations.txt',
                    'Most-Popular-Letter-Passes.txt', 'PHP-Magic-Hashes.txt', 'UserPassCombo-Jay.txt',
                    'bt4-password.txt', 'cirt-default-passwords.txt', 'citrix.txt', 'clarkson-university-82.txt',
                    'common_corporate_passwords.lst', 'darkc0de.txt', 'darkweb2017-top10000.txt', 'days.txt',
                    'der-postillon.txt', 'months.txt', 'mssql-passwords-nansh0u-guardicore.txt', 'openwall.net-all.txt',
                    'probable-v2-top12000.txt', 'seasons.txt', 'unkown-azul.txt', 'twitter-banned.txt',
                    'xato-net-10-million-passwords.txt', 'Common-Credentials/common-passwords-win.txt',
                    'Common-Credentials/100k-most-used-passwords-NCSC.txt',
                    'Default-Credentials/mysql-betterdefaultpasslist.txt',
                    'Default-Credentials/mssql-betterdefaultpasslist.txt',
                    'Default-Credentials/oracle-betterdefaultpasslist.txt',
                    'Default-Credentials/postgres-betterdefaultpasslist.txt',
                    'Default-Credentials/ssh-betterdefaultpasslist.txt',
                    'Default-Credentials/telnet-betterdefaultpasslist.txt']


def main():
    args = parser.parse_args()
    should_force: bool = args.force
    if path.exists('combined.txt') and not should_force:
        raise Exception("combined.txt already exists, consider using --force to overwrite")
    else:
        passwords = combine_files()
        print(f'combined {len(passwords)} passwords!')
        with open('combined.txt', 'w', encoding='utf-8') as f:
            f.writelines(passwords)


def combine_files():
    passwords: Set[str] = set()
    for f in FILES_TO_COMBINE:
        print(f'adding {f}...')
        res = requests.get(f'{URL}{f}')
        lines = res.text.split("\n")
        lines = map(lambda l: l + '\n', lines)
        passwords.update(lines)
    return passwords


if __name__ == '__main__':
    main()
