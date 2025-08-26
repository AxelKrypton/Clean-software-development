# Clean software development

Material relative to a 5-days training about good practices in software development offered as [HGS-HIRe](https://hgs-hire.de) power week in a joined effort with the [CRC-TR 211](https://itp.uni-frankfurt.de/~strongmatter/) collaboration.
Refer to the lecture [table of content](#table-of-content) to have an overview of the discussed topics.

#### A thrilling alternation of discussion and practical sessions

The course has been structured in many small lecture-like sessions, each followed by an practical one.
Participants have been split into small groups and have worked together on different tasks, reporting to the whole attendees at the end of each day. 
All material has been here uploaded and slides have been created on purposed for later reading.
There is a natural significant overlap between [the _«Good practices in general programming»_ presentations](https://github.com/AxelKrypton/Clean-code-good-practices) and this material.
The content has been reviewed and improved, though.

## The beamer theme

The beamer theme used for this lecture is the same used [for this Bash lecture](https://github.com/AxelKrypton/Bash-lecture).
If you wish to compile LaTeX source code, the `TeXnicalities` package and the used beamer theme are needed and can be found [here](https://github.com/AxelKrypton/TeXnicalities).
You will need the [Yanone Kaffeesatz font](https://fonts.google.com/specimen/Yanone+Kaffeesatz) available on your machine, too.

There is a _Makefile_ in the ***TeX*** folder and the `lualatex` compiler (and a TeX distribution not older than 2020) is required to compile the documents.
Use e.g. `DAY=1 make slide` from within the ***TeX*** folder to compile Day 1 material.

---

## Table of content

Here you can find the list of the topics discussed in the various days, so that you can directly open the right file if you are looking for a specific argument.
Practical sessions have been omitted (refer to the training schedule in the slides about Day 1 for a detailed overview).

### Day 1

1. Training format
1. The idea of clean code
1. Clean testing (I)
   - Why (automated) testing?
   - Types of tests
   - Testing frameworks

### Day 2

1. Clean code principles (I)
   - Meaningful names
   - Comments and formatting
   - Documentation
   - Functions and classes
   - IOSP
1. Clean testing (II)
   - The curse of the **unit** word
   - White- and black-box testing!?
   - Test the behaviour, not the implementation
1. Clean testing (III)
   - Tests goals – properties – good principles
1. Clean code principles (II)
   - The DRY principle
   - The KISS principle
   - The YAGNI principle
   - Optimisation
   - Boy scout philosophy

### Day 3

1. Git in real life
   - `git tag`
   - Semantic versioning
   - Git-flow
1. Clean testing (IV)
   - Test driven development as discipline
   - Behavior driven development as alternative
1. GitHub features
   - Pull requests
   - Issues
   - Branches
   - Special files
   - Wiki and Webpage
   - Projects
   - Releases
   - Actions and CI

### Day 4

1. Data validation and data cleaning
1. Statistical analysis and plotting

### Day 5

1. Code review
   - On a technical level
   - On a more abstract level
   - Software development in academia
1. Summary and outlook

---

### Preparation workroad

- [ ] Lecture slides
  - [X] Day 1
  - [X] Day 2
  - [X] Day 3
  - [ ] Day 4
  - [X] Day 5

- [ ] Review/improve slides examples
  - [X] Day 1
  - [ ] Day 2
  - [X] Day 3
  - [ ] Day 4
  - [X] Day 5

- [ ] Practical sessions
  - [ ] Try Day 3 TDD tasks
  - [ ] Solve Day 4 tasks
