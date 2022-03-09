# doskey jarvis=python "C:\pyscripts\jarvis.py" $*

import win32clipboard
import argparse
import os
import json
import requests
from tabulate import tabulate
from datetime import date

# create card
def create_trello_card(card_name):
    create_card_end_point = 'https://api.trello.com/1/cards'
    jsonObj = {
                "key":'TRELLO_API_KEY',
                "token":'TRELLO_TOKEN', 
                "idList":'TRELLO_ID_LIST',
                "name":card_name,
                "desc":""}

    requests.post(create_card_end_point, json=jsonObj)
    print('Card created.')

def clean_chars(tx):
    '''
    Clear all turkish characters in given text
    '''
    i = 0
    # Char Sets
    old_char = ['İ','ı','Ö','ö','Ü','ü','Ğ','ğ','Ş','ş','Ç','ç']
    new_char = ['i','i','o','o','u','u','g','g','s','s','c','c']

    for i in range(0,len(old_char)):
        tx = tx.replace(old_char[i],new_char[i])
        i += 1
        
    return tx.lower()

def get_clipboard(text = ''):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()

def create_json(list):
    '''
    Create JSON file with given list.
    if the file is exist, file will be removed
    '''
    if os.path.exists(jsonlocation):
        os.remove(jsonlocation)

    with open(jsonlocation, 'w', encoding='utf-8') as f:
        json.dump(list, f, ensure_ascii=False, indent=4)

def read_json():
    '''
    Read JSON file and then return it.
    if JSON File is not exist, the file will be created with first record.
    First record is used for header
    '''
    if not os.path.exists(jsonlocation):
        # Create new list with first row which is used for header.
        new_list = [{"PROJECT": "PROJECT", "USERNAME": "USERNAME", "PASSWORD": "PASSWORD"}]
        create_json(new_list)
        
    with open(jsonlocation, 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def main():
    # Parser
    parser = argparse.ArgumentParser(description='Emre Akayoglu (2022) ---> e-mail me :) emre.akayoglu@mechsoft.com.tr')
    parser.add_argument('-l','--list', action = 'store_true', help = 'Use -l if you want to view all the records present in the vault\n') 

    parser.add_argument('-f','--find', type=str, help = 'Use -f if you want to find specified project name present in the vault')
    parser.add_argument('-s','--show', action = 'store_true', help = '** Using with find argument. ** Use -s if you want to show specified project records present in the vault.')
    parser.add_argument('-u','--copyusername', action = 'store_true', help = '** Using with find argument. ** Use -u if you want to copy specified project usename to clipboard present in the vault.')
    parser.add_argument('--delete', type=str, help = 'Use --delete if you want to delete specified project name present in the vault')
    parser.add_argument('-tr','--trello', type=str, help = 'Use -t if you want to create a card specified')

    subparser = parser.add_subparsers(dest='command')
    rnew = subparser.add_parser('new')
    rupdate = subparser.add_parser('update')
    rtodo = subparser.add_parser('todo')

    rnew.add_argument('-pr','--project', type=str, required=True, help = 'This is the project name to be written into the vault.json')
    rnew.add_argument('-un','--username', type=str, required=True, help = 'This is the username to be written into the vault.json')
    rnew.add_argument('-pw','--password', type=str, required=True, help = 'This is the password to be written into the vault.json')

    rupdate.add_argument('-pr','--project', type=str, required=True, help = 'This is the project name to be written into the vault.json')
    rupdate.add_argument('-un','--username', type=str, default = '', help = 'This is the username to be written into the vault.json')
    rupdate.add_argument('-pw','--password', type=str, required=True, help = 'This is the password to be written into the vault.json')

    rtodo.add_argument('-d','--do', type = str, help = 'This is the to-do item to be written into the list')
    rtodo.add_argument('-n','--name', type = str, default = list_name, help = 'Name of the do-to list. Default name is todo_list_YYMMDD')
    rtodo.add_argument('-l','--listitems', action = 'store_true', help = 'Use -l if you want to view all the to-do items present in the list') 

    args = parser.parse_args()

    records = read_json()

    if args.list:
        print('\n\tAll records in the vault\n')
        print(tabulate(records,tablefmt="grid",headers="firstrow"))
    
    if args.find:
        project_found = False
        project_name = clean_chars(args.find)
        for r in records:
            if r['PROJECT'] == project_name:
                project_found = True
                break
        
        if not project_found:
            print(f'\n\tProject {project_name} is not found :/')
        else:
            if args.show:
                print("\nPROJECT\t\tUSERNAME\tPASSWORD")
                print("---------\t---------\t---------")
                print('{}\t\t{}\t{}'.format(r['PROJECT'], r['USERNAME'], r['PASSWORD']))
            elif args.copyusername:
                get_clipboard(r['USERNAME'])
                print("\n> ----- The username is copied to clipboard! ----- <")
            else:
                get_clipboard(r['PASSWORD'])
                print("\n> ----- The password is copied to clipboard! ----- <")
    
    if args.delete:
        project_found = False
        bdelete = clean_chars(args.delete)
        for r in records:
            if r['PROJECT'] == bdelete:
                rindex = records.index(r)
                project_found = True
                break
        
        if project_found:
            records.pop(rindex)
            create_json(records)
        else:
            print(f'\n\tProject {bdelete} is not found :/')

    if args.trello:
        create_trello_card(args.trello)

    if args.command == 'new':
        project_found = False
        nproject = clean_chars(args.project)
        for r in records:
            if r['PROJECT'] == nproject:
                project_found = True
                break

        if project_found:
            print(f'\n\tProject {nproject} is already inside :) Hu huuu')
        else:
            ndic = {'PROJECT':nproject,'USERNAME':args.username,'PASSWORD':args.password}
            records.append(ndic)
            create_json(records)

    elif args.command == 'update':
        project_found = False
        for r in records:
            if r['PROJECT'] == args.project:
                r['PASSWORD'] = args.password
                if not args.username == '':
                    r['USERNAME'] = args.username
                project_found = True

        if project_found:
            create_json(records)
        else:
            print(f'\n\tProject {bdelete} is not found :/')
    
    elif args.command == 'todo':
        list_txt_file = os.path.join(desktop_path, args.name + '.txt')
        if args.listitems:
            with open(list_txt_file, "r") as myfile:
                items = myfile.read()
                print(items)

        if args.do:
            if not os.path.exists(list_txt_file):
                with open(list_txt_file, "w") as myfile:
                    myfile.write(f"[] {dt} ---> {args.do}")
            else:
                with open(list_txt_file, "a") as myfile:
                    myfile.write(f"\n[] {dt} ---> {args.do}")

if __name__ == '__main__':
    dt = date.today().strftime("%y%m%d")
    list_name = f'daily_notes_{dt}'
    desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Daily_Notes')
    jsonlocation = os.path.realpath(os.path.join(os.path.dirname(__file__),'vault.json'))

    main()
