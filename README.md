<h1>Jarvis the Helper</h1>

This is a simple helper application that I have built in Python, which can also be called from the command-line by making an alias for it.

<h2>Listing all the records ("-l" or "--list" argument)</h2>
Listing (printing) down all the to-do list items of the to-do list on the command-line

```
python jarvis.py -l
```

<h2>Find record in the vault ("-f" or "--find" argument)</h2> 
Copy specified project's password to clipboard

```
python jarvis.py -f "Sample"
```

<h3>Find record in the vault ("-s" or "--show" argument)</h3> 
Show the specified project's record

```
python jarvis.py -f "Sample" -s
```

<h3>Find record in the vault ("-u" or "--copyusername" argument)</h3> 
Copy specified project's username to clipboard

```
python jarvis.py -f "Sample" -u
```

<h2>Delete record in the vault ("--delete" argument)</h2> 
Delete specified project into the vault

```
python jarvis.py --delete "Sample"
```

<h2>Create a card into Trello ("-tr" or "--trello" argument)</h2> 
Create a card into specified list on trello

```
python jarvis.py -tr "Sample Card"
```

<h2>New record into vault</h2> 
Create a record into the vault

```
python jarvis.py new -pr "PROJECT_NAME" -un "USER_NAME" -pw "PASSWORD"
```

<h2>Update record into vault</h2> 
Update a record into the vault. Username is optional

```
python jarvis.py update -pr "PROJECT_NAME" -pw "PASSWORD" -un "USER_NAME"
```

<h2>Adding a to-do list item ("-d" or "--do" argument)</h2>
Add a new todo list item or note to the default text file at the default location (Desktop/Daily_Notes)

```
python jarvis.py todo -d "Hello World"
```

<h3>Specifying the name of to-do list ("-n" or "--name" argument)</h3>
Add a new todo list item or note to the specified file (minutes_of_meeting.txt for this example) at the default location (Desktop/Daily_Notes)

```
python jarvis.py todo -d "Hello World" -n "minutes_of_meeting"
```

<h2>Listing all the to-do list items ("-l" or "--listitems" argument)</h2>
Listing (printing) down all the to-do list items of the to-do list on the command-line</h2>

```
python jarvis.py todo -l
```
