# Personal Portfolio Website Using Hugo, GitHub Actions, and GitHub Pages

A step-by-step guide for creating a professional portfolio website using the **Hugo Profile theme**, **GitHub Actions**, and **GitHub Pages** without installing Hugo, Go, or additional build tools locally.

This approach uses GitHub's cloud-based CI/CD environment to build and deploy the website automatically.

---

# **Phase 1 – Portfolio Initialization & Hugo Profile Customization**

## Objective

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

Download the Hugo Profile theme (Creator: Gurusabarish).

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

# **Phase 2 – Refactoring Hugo Profile Templates for Structural Consistency**

## Objective

The original Hugo Profile theme provided separate templates for the **Education**, **Experience**, and **Accomplishments** sections. Although each section served a similar purpose (displaying chronological information in a card-based layout), they were implemented using different HTML structures and styling conventions. This made future customization difficult, as visual changes often had to be implemented independently in multiple templates.

The goal of this phase was to standardize these sections by introducing a consistent HTML structure and centralized CSS styling while preserving each section's unique functionality.

---

## Files Modified

### HTML Templates

```
layouts/partials/sections/
├── education.html
├── experience.html
└── accomplishments.html
```

### Stylesheet

```
assets/css/index.css
```

---

## Step 1 – Analyze Existing Theme Structure

Before making any modifications, the original Hugo Profile templates were compared to understand how each section was rendered.

Observations included:

* Education already used a clean Bootstrap card layout.
* Experience contained additional nesting for multiple positions within a company.
* Accomplishments had been adapted from the Education template but contained structural inconsistencies.
* Similar UI components were implemented differently across templates, making maintenance unnecessarily difficult.

This analysis established Education as the visual reference for the remaining sections.

---

## Step 2 – Standardize HTML Templates

The three section templates were refactored to follow the same overall structure wherever possible.

Key improvements included:

* Consistent Bootstrap card hierarchy.
* Unified spacing and container organization.
* Consistent use of Bootstrap utility classes.
* Removal of unnecessary inline styling.
* Improved readability through cleaner indentation and organization.
* Preservation of section-specific functionality (for example, Experience still supports multiple jobs within a company).

Rather than rewriting functionality, the focus was on making the templates easier to maintain while preserving compatibility with Hugo Profile.

---

## Step 3 – Introduce Dedicated Content Wrappers

Dedicated content wrapper classes were introduced for each section.

```
education-content
experience-content
accomplishments-content
```

These wrapper classes provide a common location for formatting long-form Markdown content while allowing each section to receive custom styling independently if needed.

This approach avoids relying on generic selectors and improves future extensibility.

---

## Step 4 – Consolidate Styling in index.css

Visual styling that had previously been scattered between templates and CSS was centralized.

Changes included:

* Standardized card appearance.
* Unified border styling.
* Consistent border radius.
* Common background colors.
* Standardized spacing and padding.
* Improved typography consistency.
* Shared formatting rules for Markdown-generated content.

Centralizing these rules significantly reduces duplicated styling and makes future visual updates much easier.

---

## Step 5 – Preserve Section-Specific Features

Although the visual design was standardized, each section retained its unique functionality.

### Education

* Tab-based navigation
* Institution information
* GPA display
* Resources section

### Experience

* Company grouping
* Multiple positions within the same employer
* Tooltips
* Featured links and custom icons

### Accomplishments

* Organization listing
* Achievement metadata
* Resource links
* Flexible Markdown descriptions

The objective was consistency—not identical templates.

---

## Step 6 – Navigation and Section Validation

After restructuring the templates, section navigation was verified to ensure:

* Navigation bar links correctly target each section.
* Section anchors function as expected.
* Hugo-generated content renders correctly.
* Bootstrap components continue functioning without modification.

During testing, browser caching and Hugo live reload occasionally delayed visible updates. Performing a manual browser refresh confirmed that the implemented changes had been applied successfully.

---

## Lessons Learned

Several important lessons emerged during this phase:

* HTML structure and CSS should be standardized together rather than independently.
* Bootstrap grid layouts are sensitive to container hierarchy; small structural changes can unintentionally affect responsive behavior.
* Centralizing styling in `index.css` greatly simplifies long-term maintenance.
* Hugo's live-reload server may not immediately reflect template or stylesheet updates, making manual refreshes an important part of the debugging workflow.
* Incremental testing after each modification is more effective than introducing multiple structural changes simultaneously.

---

## Outcome

At the conclusion of Phase 2:

* The Education, Experience, and Accomplishments sections share a consistent visual design.
* Card layouts are standardized across the portfolio.
* Styling has been centralized into reusable CSS.
* HTML templates are cleaner, more maintainable, and easier to extend.
* The project now has a stronger architectural foundation for future customization, including additional sections, theme enhancements, and responsive design improvements.

---

# Author

Created using:

* Hugo
* Hugo Profile Theme (Creator: Gurusabarish)
* GitHub Actions
* GitHub Pages
