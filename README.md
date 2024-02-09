# Data Systems project - Police Academy - 2023/24 
## Group A2

[Teaser Video](https://www.youtube.com/watch?v=LSAxR6QDHyk) | [Application Demo Video](https://www.youtube.com/watch?v=DxgNtYaCU7Y)

***

### Abstract

This study addresses the global challenge of drug trafficking by harnessing open-source data from Reddit discussions to identify emerging drug trends, employing sentiment analysis and federated learning to enhance privacy and data security. By analyzing drug related comments for sentiment distribution and slang terminology, patterns are uncovered in drug use across various regions. The methodology includes data collection from drug-related subreddits, data cleaning, and processing with a focus on privacy-preserving techniques like federated learning, where a global model is trained across distributed datasets without sharing raw data. The research utilizes RoBERTa-base for sentiment analysis and develops a Streamlit interface for visualizing trends and analysis results. Feedback from user experience validation, including interactions with law enforcement, confirms the interface’s effectiveness. The findings reveal distinct sentiment distributions among different drug trends, highlighting the study’s practical implications for combating the illicit drug trade. This project not only contributes to academic discussions on drug trends but also demonstrates the potential of federated learning in sensitive data analysis, setting a precedent for future research in this area.

***

The finetuned model based on the BERT model, used in the project can be found [here](https://huggingface.co/danielsz96/drugobert)


<!-- ### Git workflow:
- For every time you want to collaborate, you must create a new branch for every feature, and create a Pull Request when it's finished. We can merge them when the given part is finished. It would be best to create a new branch for each and every session you do, and then merge it, so others don't have to search through loads of branches. 
- Commit messages must be meaningful, so that it's instantly clear what does the commit do. (hint: the best commit template is: **"This commit will `< Your Commit Message >`)**
- Merging Pull Requests are the responsibility of collaborators, after thorough review (this will be important when developing the MVP later on).
- As for the commit messages, we should use a base version of `conventinal commit` (https://www.conventionalcommits.org/en/v1.0.0/), meaning a commit should always start with one of the following keywords and a semicolon:
    - `chore:` house keeping stuff, like adding config files, removing unneded files, etc.
    - `feat:` every time you research and upload results, develop something, and add value right to the project work, not just the repo, then you should use this.
    - `fix:` self explanatory, in case we have a bug and the commit is intended to fix that.
    - `refactor:` again, self explanatory, use this when you have refactored a given piece of code or research note, or anything.

### Research workflow:
- in the `bin` folder every one of us has a folder. Here you can gather your findings as you wish, maybe in a txt file, gather papers, articles, code, etc. 
- Periodically, we must talk through our findings, then we should decide on what should go into the common `Research` folder. The `Research` folder should not be modified without , however, your personal folder can contain anything you find interesting.
- **Note that no big files, datasets, etc (larger than a couple of Mb at max, but mostly a file should be in the Kb region) should be uploaded to git. Large files should be collected via links, or uploaded to google docs (etc.) for now if you have no permanent link for them.**

### Docker Environment:
- Every docker environment, for every model we try has a dedicated folder, in which there are the docker files.
- Start the docker environment with the following command:
```
docker compose up <name> -->
<!-- ``` -->


#### Group Members:
```
- Mary Adib
- Ömer Ülgen
- Jonathan Hombroek
- Dániel Szabó
- Ákos Makács
```
