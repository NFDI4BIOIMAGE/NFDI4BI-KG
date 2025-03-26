---
name: NFDI4BIOIMAGE Participant
about: Add someone to NFDI4BIOIMAGE Participants on Wikidata
title: Add [your name] to wikidata NFDI4BIOIMAGE participants
labels: ''
assignees: ''

---

# Tasks
## Check if there's already a wikidata Item for You
On the [wikidata homepage](https://www.wikidata.org), search for your "Firstname Lastname". If you get any hits, check if one actually corresponds to You. Tick the appropriate box:
- [ ] 1: I'm already an Item on wikidata
- [ ] 2: I'm not on wikidata or there's someone else with the same name

If you ticked box 2, create a new Item, if you ticked box 2, you can continue with "Add statements" below.

## Add your self to wikidata
Open the [New Item form](https://www.wikidata.org/wiki/Special:NewItem) on wikidata.

### Mandatory
- [ ] Select language (the language in which you will enter your name and description)
- [ ] Label: Your name (Firstname Lastname)
### Optional
- [ ] Description: E.g. your occupation
- [ ] Aliases: Other names you are known by, nicknames, artist names, ...

Don't forget to click "Create" to finalize your new Item.

You will then be redirected to your new Item's page. The URL pattern is https://www.wikidata.org/wiki/QXXXXXXXXX . The
Q-number is your unique wikidata ID.

## Statements
All other data about yourself is entered as statements (property-value pairs). To create
a new statement, click the "+ add statement" link at the end of the Statements section on
your Item page. 

### Become a human
This statement is to ensure you are represented as an instance of the type "Human". Start creating a new
statement. Then
- [ ] In the "Property" field, enter "P31" and select the only item "instance of (P31)" from the selection menu.
- [ ] In the value field, enter "Q5" and select "human (Q5)" from the menu.
Finalize by clicking "✓ publish"

### Participate in NFDI4BIOIMAGE
This statement connects You as a participant in NFDI4BIOIMAGE (Q113500855).
In addition, you will annotate this statement with the date when you entered NFDI4BIOIMAGE.

Add a new statement and
- [ ] Enter "P1344" in the "Property" field and select "participant in".
- [ ] In the value field, enter Q113500855 and select NFDI4BIOIMAGE (Q113500855).
- [ ] Click (+ add qualifier) and select "start time" for the Property. Enter the appropriate date as YYYY-MM-DD.
Optional: Add more qualifiers as you see fit.

Finalize by clicking "✓ publish"
### Nice to have: Your ORCID
Add new statement and
- [ ] Property: P496, Value: Your ORCID

Done!

