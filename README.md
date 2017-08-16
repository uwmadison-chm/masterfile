# masterfile

## Tools to organize, access, and catalog the variables of interest in a scientific study

## Draft API usage example

```python
import masterfile
# Load all of the .csv files from /path, and the dictionary files in
# /path/dictionaries. Takes settings info from a 'settings.json' file in
# /path.
# joins the .csv files on 'participant_id', which will be used as the index
# There will be warnings if the data look bad in some way
mf = masterfile.load('/path')
# Get the pandas dataframe associated
df = mf.dataframe  # aliased as mf.df

# All the variable stuff is less important, people can go look in data dicts
# So we'll write that stuff later.
v = mf.lookup('sr_t1_panas_pa')
v.contacts # list_of_names
v.measure.contact  # Someone
v.modality # Component("self-report")
```

## CSV file format

CSV files should be comma-separated (no surprise there) and have DOS line endings (CRLF). They should not have the stupid UTF-8 signature at the start. UTF-8 characters are fine. Missing data is indicated by an empty cell. Quoting should be like Excel does.

Basically, you want Excel-for-Windows-style CSV files with no UTF-8 signature.

## Data checks

Here are some (all?) of the things to do to verify you have semantically reasonable data:

* Variable parts not in dictionaries
* Unused dictionary checks
* Missing participant_id column
* Repeated paticipant_id column
* Blanks in participant_id column
* Duplicate columns
* Column names not matching format

## Credits

Written by Nate Vack <njvack@wisc.edu>

masterfile packages two wonderful tools: [docopt](https://github.com/docopt/docopt) and [schema](https://github.com/halst/schema).

docopt is copyright (c) 2013 Vladimir Keleshev, vladimir@keleshev.com

schema is copyright (c) 2012 Vladimir Keleshev, vladimir@keleshev.com
