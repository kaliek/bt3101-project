# Web Crawler Module

This module handles the automation of data extraction. It requires the following 3 tokens, all in string format:

1. university_name
2. department_name
3. faculty_list_url

The extracted data will be stored in MongoDB hosted in Theodore's server for now.

# Logic, simple pseudo-code

1. Input university name, department name, faculty list url
2. download faculty list page, analyse html content and extract tabular data, stored in lists
3. determine the type(attribute) and sequence of list
4. extract the prof name list, store the other associated data for verification
4. Based on (university name, department name, professor name), construct keyword for LinkedIn crawl

The output of the module should have in total, three different states:

1. the data is complete (required fields all filled), verified both on web and LinkedIn
2. the data is incomplete, no obvious conflict in data integrity
3. there are conflicts in data, in which cases both will be stored

STATE 2 and 3 will be passed into the second part of this project and being examined by the user,
which is not the concern of this module.

A pseudo-code of the execution logic is shown below.

```
if professo_data in LinkedIn:
    if the data is complete:
        verified with data get from web
        
        if verified:
            end with STATE 1
        else:
            end with STATE 3
    else:
        verified with data get from web, form a more complete data
        
        if no obvious error:
            end with STATE 2
        else:
            end with STATE 3
```

# Sample Excel file from Cindy

A summary on the list of universities and their department is shown below.

Ideally, a url of the faculty list should be able to locate based on the keyword (department name, university name).

__Geography__:

University College London

University of Colorado – Boulder

University of Manchester

University of Toronto (St George)

Queen Mary London

University of Cambridge

University of British Columbia

University of Oxford

__Biomedical Engineer__:

Columbia University

Northwestern University

Rice University

University of California--Los Angeles (Samueli)

University of Michigan

University of Toronto

Johns Hopkins University

Georgia Institute of Technology

University of California-San Diego

Duke University

Massachusetts Institute of Technology

Stanford University

__Biochemistry__:

University of Chicago

The University of Hong Kong

New York University (NYU)

Monash University

University of California, San Francisco

University of College London

University of Illinois at Urbana-Champaign

McGill University




