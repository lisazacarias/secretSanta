# secretSanta

Takes a table where each row has a name, email, and message

Sends out emails with randomized assignments

Flow is:
  - Generate a list of names from the input
  - Shuffle them
  - Assign name i+1 to name i, looping around for the last one
