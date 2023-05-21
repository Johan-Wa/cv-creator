# CV creator
---
author: Johan David Wallens

email: johandavidgp@gmail.com

---

CV creator is a desktop aplication to create a curriculum vitae.
this is an a personal project that is writo in python language and designed in Qt designer.

### Download
first clone the de repository.

```sh
git clone https://github.com/Johan-Wa/cv-creator
```
to use the program first need the python libraries:

1) Change directory
```sh
cd cv-creator
```
2) Create a virtual environment
```sh
python -m venv venv
```
3) Activate de virtual environment
```sh
source venv/bin/activate
```
or in windows
```bat
 call venv/Scripts/activate.bat
```
4) Install the libreries
```sh
pip install -r requeriments.txt
```
### Use
now we can use the program running 
```sh
python main.py
```
Now we need to create 4 documents that will have our information to generate the pdf CV:

1) A .txt document that have a little description of the profetional profile.
2) A .csv file tha have our education information

| title | state | date | school |
|-------|-------|------|--------|
| biologist, software developer, etc.. | procces, finished | ini_date-finish_date | a random school |

3) A .csv file that have our works information

| job | date | company | description |
|-------|-------|------|--------|
| Data ingenier | ini_date-finish_date | a Data compani | Supports the data centers |

4) A .csv file that have our skills information

| Skill name | Skill description |
|------------|-------------------|
| Python | web and desktop development using python language |

When we open the program we will have an interface like this:
![data](file:///home/dracul/programing/python/documents_create/pdf/CV/src/screenshots/mainpy1.png "data")

complete the data, and then chosse previous files make from our information.
![files](file:///home/dracul/programing/python/documents_create/pdf/CV/src/screenshots/mainpy2.png "files")
for the end we only chosse the two principal colors, the tamplate and the font type.
![config](file:///home/dracul/programing/python/documents_create/pdf/CV/src/screenshots/mainpy3.png "config")
and select if you want add the jobs description or not.