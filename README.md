# Personal Portfolio Website Using Hugo, GitHub Actions, and GitHub Pages

A step-by-step guide for creating a professional portfolio website using the **Hugo Profile theme**, **GitHub Actions**, and **GitHub Pages** without installing Hugo, Go, or additional build tools locally.

This approach uses GitHub's cloud-based CI/CD environment to build and deploy the website automatically.

---

# Overview

This project creates a static portfolio website using:

* **Hugo** — Static site generator
* **Hugo Profile Theme** — Portfolio website template
* **GitHub Actions** — Automated build and deployment workflow
* **GitHub Pages** — Website hosting
* **Git** — Version control

The local computer only requires:

* Git
* A text editor
* Optional: Python or R for project development

No local installation of:

* Hugo
* Go
* Node.js

is required.

---

# Website Deployment Workflow

The deployment pipeline follows this process:

```
Local Computer
      |
      | git push
      ↓
GitHub Repository
      |
      | GitHub Actions
      |
      |-- Install Hugo
      |-- Build website
      |-- Generate static files
      |
      ↓
GitHub Pages
      |
      ↓
yourusername.github.io
```

Every time changes are pushed to the `main` branch:

1. GitHub Actions starts automatically
2. Hugo is installed in the GitHub runner environment
3. The website is built
4. The generated files are deployed to GitHub Pages

---

# Step 1 — Create GitHub Repository

Create a repository:

```
yourusername.github.io
```

Example:

```
bhara033.github.io
```

Clone the repository:

```bash
git clone https://github.com/yourusername/yourusername.github.io.git

cd yourusername.github.io
```

---

# Step 2 — Create Hugo Project Structure

Because Hugo is not installed locally, create the project structure manually.

Final repository structure:

```
.github/
└── workflows/
    └── hugo.yml

content/

static/

themes/
└── hugo-profile/

config.yaml

README.md
```

---

# Step 3 — Add Hugo Profile Theme

Download the Hugo Profile theme:

https://github.com/gurusabarish/hugo-profile

Copy the theme folder:

```
hugo-profile
```

into:

```
themes/hugo-profile
```

The final structure should contain:

```
themes/
└── hugo-profile/
    ├── layouts/
    ├── assets/
    ├── static/
    └── theme.toml
```

---

# Step 4 — Configure Hugo Website

Create:

```
hugo.yaml
```

(or `config.yaml`)

Example:

```yaml
baseURL: "https://yourusername.github.io/"
languageCode: "en-us"
title: "Your Name"

theme: "hugo-profile"

params:

  title: "Your Name"

  description: >
    Data Scientist | Researcher | Analyst

  hero:
    enable: true
    intro: "Hi, I'm"
    title: "Your Name"

  about:
    enable: true

  skills:
    enable: true

  experience:
    enable: true

  projects:
    enable: true

  contact:
    enable: true
```

---

# Step 5 — Add GitHub Actions Workflow

Create:

```
.github/workflows/hugo.yml
```

GitHub Actions configuration:

```yaml
name: Deploy Hugo site

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

jobs:

  build:

    runs-on: ubuntu-latest

    steps:

    - name: Checkout
      uses: actions/checkout@v4
      with:
        submodules: recursive

    - name: Setup Hugo
      uses: peaceiris/actions-hugo@v3
      with:
        hugo-version: latest

    - name: Build
      run: hugo --minify

    - name: Upload artifact
      uses: actions/upload-pages-artifact@v3
      with:
        path: ./public


  deploy:

    environment:
      name: github-pages

    runs-on: ubuntu-latest

    needs: build

    steps:

    - name: Deploy
      uses: actions/deploy-pages@v4
```

---

# Step 6 — Enable GitHub Pages

Navigate:

```
Repository
→ Settings
→ Pages
```

Change source to:

```
GitHub Actions
```

Do not select:

```
Deploy from branch
```

---

# Step 7 — Deploy Website

Commit and push:

```bash
git add .

git commit -m "Website deployment v1"

git push origin main
```

Check:

```
Repository
→ Actions
```

A successful workflow should show:

```
✓ Build
✓ Deploy
```

Website:

```
https://yourusername.github.io
```

---

# YAML Configuration Lessons Learned

The majority of build issues were related to YAML structure.

## 1. YAML dictionaries vs lists

A dictionary:

```yaml
person:
  name: "John"
  role: "Developer"
```

A list:

```yaml
skills:
  - Python
  - R
  - SQL
```

A list of dictionaries:

```yaml
experience:
  items:
    - company: "Organization"
      role: "Researcher"
```

---

# 2. Do not mix dictionaries and lists

Incorrect:

```yaml
Courses:
  enable: true
  - title: "Course"
```

Why?

`Courses` becomes a dictionary because of:

```yaml
enable: true
```

Then YAML encounters:

```yaml
- title:
```

which is a list.

A key cannot be both.

Correct:

```yaml
Courses:
  enable: true
  items:
    - title: "Course"
```

---

# 3. Use "|" for multiline text

Long descriptions should not use quotes:

Incorrect:

```yaml
content: "Line 1
Line 2
Line 3"
```

Correct:

```yaml
content: |
  Line 1
  Line 2
  Line 3
```

For multiline content where the ending newline should be removed:

```yaml
content: |-
  Line 1
  Line 2
```

---

# 4. Indentation matters

YAML uses indentation to define relationships.

Correct:

```yaml
experience:
  items:
    - company: "Organization"
      jobs:
        - name: "Research Intern"
```

Incorrect:

```yaml
experience:
 items:
 - company: "Organization"
```

Use spaces consistently.

Recommended:

```
2 spaces per indentation level
```

---

# Troubleshooting Build Issues

## Issue 1 — Hugo failed to load configuration

Error:

```
failed to load config
value is not allowed in this context
```

Cause:

A YAML list item was placed inside a dictionary.

Example:

```yaml
Courses:
  enable: true
  - title: "Course"
```

Solution:

Add a list container:

```yaml
Courses:
  enable: true
  items:
    - title: "Course"
```

---

## Issue 2 — Multiline content caused YAML errors

Error occurred when descriptions contained multiple bullet points.

Cause:

Using double quotes around multiline text.

Solution:

Replace:

```yaml
content: "bullet 1
bullet 2"
```

with:

```yaml
content: |
  bullet 1
  bullet 2
```

---

## Issue 3 — Hugo build failed repeatedly

Approach used:

1. Read the line number from GitHub Actions error
2. Inspect surrounding YAML lines
3. Identify dictionary/list mismatch
4. Correct indentation
5. Commit changes
6. Allow GitHub Actions to rebuild

---

# Build History

Major implementation milestones:

```
Initial commit
    ↓
Website deployment v1
    ↓
Converted multiline descriptions to YAML block format
    ↓
Corrected indentation
    ↓
Converted Courses, Education, Organizations,
Honors/Awards, and Volunteering sections
into proper YAML lists
    ↓
Successful Hugo build and deployment
```

---

# Future Enhancements

Potential improvements:

* Add project pages
* Add downloadable resume PDF
* Add GitHub project cards
* Add Tableau dashboards
* Add Google Scholar integration
* Add custom domain
* Add analytics tracking
* Add automated project updates

---

# Lessons Learned

Building a portfolio website with Hugo and GitHub Actions provides:

* Reproducible deployment
* No local build dependencies
* Version-controlled website updates
* Automated publishing workflow

The most important technical lesson:

> Hugo configuration is only as reliable as the YAML structure behind it. Understanding YAML dictionaries, lists, indentation, and multiline strings is essential for maintaining a static website configuration.

---

# Author

Created using:

* Hugo
* Hugo Profile Theme (Creator: Gurusabarish)
* GitHub Actions
* GitHub Pages
