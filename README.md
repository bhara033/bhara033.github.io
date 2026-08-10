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

# **Phase 3 – Portfolio UI Refinement, Social Icons, Blog, Gallery, and Multilingual Routing**

## Objective

Phase 3 focused on refining the visual consistency of the portfolio and adding functional content features after the main Hugo sections had been standardized.

The major goals were:

* Make Experience and Accomplishments visually consistent with Education by using card-based layouts instead of list-style layouts.
* Preserve the original Hugo Profile theme styling while modifying the section HTML.
* Fix minor social-media icon and light/dark-mode display issues.
* Improve link styling consistency across sections.
* Build a functioning image gallery with descriptions.
* Add a functioning blog section.
* Configure multilingual content and custom language paths.
* Resolve Hugo URL/path issues caused by multilingual routing and relative versus absolute URLs.
* Improve responsive behavior and verify changes through browser developer tools and repeated local testing.

---

## Step 1 – Convert Experience and Accomplishments to Card-Based Layouts

Education was used as the visual reference because it already had the desired card-based presentation.

Experience and Accomplishments were adjusted so that their content could be displayed using a similar Bootstrap card structure rather than relying on the original list-oriented presentation.

### Experience

The Experience section was rebuilt around the same general visual model as Education while preserving Experience-specific features such as:

* Company grouping
* Multiple positions within one company
* Job metadata
* Links and icons
* Existing Hugo Profile data structure

During testing, an important layout issue was identified: the Experience card appeared wider than the Education and Accomplishments cards even when similar Bootstrap column widths were being used.

The cause was structural rather than simply a `col-md-*` setting. The Experience partial did not contain the same container hierarchy used by the other sections.

The fix was to restore the appropriate container structure instead of changing the global CSS.

### Accomplishments

The Accomplishments section was also aligned with the Education-style card presentation.

The goal was not to make every section identical, but to establish a common visual language:

```text
Education       → Card
Experience      → Card
Accomplishments → Card
```

Section-specific content and functionality were retained.

---

## Step 2 – Preserve the Existing `index.css` Design

A key requirement during the Phase 3 changes was to avoid unnecessarily rewriting the existing theme CSS.

The Hugo Profile theme already contained styling in:

```text
assets/css/index.css
```

Important existing styling included CSS variables such as:

```css
--primary-color
--secondary-color
--text-secondary-color
--text-link-color
```

and card styling such as borders, rounded corners, shadows, spacing, and dark-mode backgrounds.

The HTML partials were therefore adjusted to work with the existing stylesheet rather than replacing the visual system with large amounts of new inline CSS.

This helped preserve the original Hugo Profile appearance while allowing the structure of the sections to be customized.

---

## Step 3 – Fix Education Link Styling

The Education section contained a small visual inconsistency in the way the school/resource URL was displayed.

Other portfolio links used a blue, underlined appearance and a darker blue hover state, while the Education link initially behaved differently.

The final styling used the existing visual convention, including:

```css
#education .card .card-body > a h6 {
    display: inline-block;
    color: #007bff !important;
    text-decoration: underline;
}

.dark #education .card .card-body > a h6 {
    color: #007bff !important;
}
```

The hover color observed during browser inspection was:

```text
#0056b3
```

Browser developer tools were used to identify the actual rendered colors and pseudo-element behavior rather than guessing which CSS rule controlled the appearance.

This also revealed that the Education link had an existing `::after` hover rule that affected the underline animation.

---

## Step 4 – Fix Social Media and Dark-Mode Icon Issues

Several minor issues were found with social-media icons when switching between light and dark modes, particularly on mobile.

The debugging process involved inspecting the rendered HTML and the `<body>` class.

Examples observed during testing included:

```html
<body class="light">
```

and temporarily:

```html
<body class="light dark">
```

This helped identify that the problem was related to how the theme's light/dark state was being applied rather than simply being an incorrect image file.

An important lesson from this work was to avoid using CSS such as:

```css
content: url(...);
```

as a general replacement mechanism for image elements.

Instead, the actual HTML/image elements and the theme's light/dark state should be allowed to control which asset is displayed.

The issue was verified on the rendered page rather than relying only on the source template.

---

## Step 5 – Build a Functional Image Gallery

A dedicated Hugo gallery layout was implemented to support image collections.

The gallery uses a structure similar to:

```text
content/
└── gallery/
    └── ...
```

and a gallery layout that renders each image in a Bootstrap card.

The gallery supports:

* Multiple images
* Image viewer/zoom functionality
* Optional image descriptions
* Responsive image sizing
* Dark-mode-compatible description text

The image template was extended so that a description could appear underneath an image:

```html
{{ if .description }}
<div class="gallery-description text-center">
    {{ .description }}
</div>
{{ end }}
```

The associated CSS was kept separate from the HTML:

```css
.viewer-enabled-image {
    cursor: zoom-in;
}

.gallery-description {
    color: inherit;
    padding: 8px 4px;
}
```

Using `color: inherit` allows the description to follow the active light/dark theme.

---

## Step 6 – Correct Gallery Markdown and YAML Structure

While creating gallery entries, a YAML parsing error occurred:

```text
found character that cannot start any token
```

The problem was caused by gallery image data being placed in the wrong part of the Markdown/front-matter structure.

The gallery image definitions must belong to the YAML front matter rather than being treated as ordinary Markdown content.

The general structure is:

```yaml
---
title: "Gallery"
date: 2026-01-01
description: "Gallery description"
layout: gallery

galleryImages:
  - src: "/files/image1.jpg"
    description: "Description of image 1"
  - src: "/files/image2.jpg"
    description: "Description of image 2"

viewer: true
---
```

This reinforced the Phase 1 lesson that Hugo configuration and content are highly dependent on correct YAML structure and indentation.

---

## Step 7 – Add a Functional Blog

A blog section was added to the portfolio so that posts could be created and rendered through Hugo rather than being static HTML.

The blog uses Hugo content organization and a section index page.

The initial blog index Markdown included content similar to:

```markdown
---
title: "Blogs"
---
```

The blog was tested locally through Hugo's development server.

Testing exposed an important distinction between:

* the physical content path,
* the generated Hugo URL,
* the site's `baseURL`,
* multilingual URL prefixes,
* and the URL functions used inside templates.

This became particularly important once multilingual routing was introduced.

---

## Step 8 – Multilingual Configuration and Custom Language Paths

The site was expanded to support multiple languages, including:

```text
en
es
fr
```

Language-specific configuration files were used for translated navigation and content.

The Hugo configuration included multilingual settings such as:

```yaml
defaultContentLanguage: "en"
defaultContentLanguageInSubdir: false
```

The behavior of:

```yaml
defaultContentLanguageInSubdir: true
```

was also investigated because it changes whether the default language receives its own URL prefix.

Custom language paths were explored so that the language URLs could use project-specific names rather than simply:

```text
/es/
/fr/
```

For example:

```text
/curated/
/complete/
```

The important lesson was that Hugo's language configuration, content directories, and generated URLs must be considered together.

---

## Step 9 – Debug Relative and Absolute Hugo URLs

Blog and gallery testing exposed differences between:

```hugo
relURL
```

and:

```hugo
absURL
```

These functions were investigated because the site was being served under different local paths during testing.

The distinction is important:

* `relURL` generates a URL relative to the configured site base URL.
* `absURL` generates a URL using the site's configured base URL.

For assets and navigation, choosing the correct function depends on whether the target should be relative to the current site location or anchored to the configured site base.

Testing URLs directly in the browser was used to determine whether Hugo was generating paths such as:

```text
/curated/
```

or incorrectly producing duplicated or missing path segments.

---

## Step 10 – Responsive Gallery and About-Section Refinement

Responsive behavior was also tested on different mobile devices.

The About section used a two-column `<ul>` grid:

```css
#about ul {
    display: grid;
    grid-template-columns: repeat(2, minmax(140px, 200px));
}
```

Testing showed that long text in the right-most column could cause horizontal overflow on some mobile screen sizes.

The investigation focused on the grid width and the relationship between the `<ul>` container and its `<li>` elements rather than simply adding a horizontal scrollbar.

The goal was to allow the content to fit within the viewport without forcing the user to scroll horizontally.

---

## Step 11 – Browser Developer Tools as a Debugging Method

Phase 3 relied heavily on browser developer tools to identify the actual source of visual problems.

Developer tools were used to inspect:

* Rendered HTML
* `<body>` classes
* Computed CSS
* CSS variables
* Link colors
* Hover colors
* Pseudo-elements
* Bootstrap container and column widths
* Image paths
* Generated URLs

For example, the actual hover blue for links was identified as:

```text
#0056b3
```

rather than relying on assumptions about the theme's CSS.

This proved more reliable than repeatedly changing unrelated CSS rules.

---

## Phase 3 Troubleshooting Lessons

### 1. HTML structure can affect Bootstrap width

A `col-md-9` does not guarantee that two sections will have the same visible width.

The surrounding `.container`, `.row`, and other wrapper elements affect the final layout.

### 2. Preserve existing theme CSS when possible

When a theme already provides a complete visual system, modifying the HTML structure while reusing the existing CSS is safer than recreating the styling from scratch.

### 3. Inspect computed styles instead of guessing

Browser developer tools provide the actual CSS rule, variable, color, or pseudo-element affecting an element.

### 4. Hugo URLs depend on configuration

`baseURL`, language configuration, content paths, and URL helper functions all affect the final generated URL.

### 5. YAML structure remains critical

Gallery data and other Hugo configuration must be placed in the correct YAML structure. A visually correct Markdown file can still fail to build if the YAML hierarchy is invalid.

### 6. Browser caching can hide successful changes

When Hugo's live reload or browser caching appears to leave an old version visible, a hard refresh such as:

```text
Ctrl + Shift + R
```

can confirm whether the new version is actually being served.

---

## Phase 3 Outcome

At the conclusion of Phase 3:

* Experience uses a card-based layout consistent with Education.
* Accomplishments uses a card-based layout consistent with Education.
* Existing Hugo Profile CSS styling was preserved wherever possible.
* Experience card width and container structure were corrected.
* Education link styling was aligned with the rest of the site.
* Social-media/light-dark icon behavior was investigated and corrected.
* A functional image gallery was added.
* Gallery images support descriptions below each image.
* Gallery viewer/zoom behavior was retained.
* A functioning blog section was added.
* Multilingual configuration was expanded to support English, Spanish, and French.
* Custom language URL paths were investigated and configured.
* Hugo `relURL` versus `absURL` behavior was investigated while debugging generated paths.
* Responsive behavior was tested on different screen sizes.
* Browser developer tools became a primary method for diagnosing CSS and layout issues.

Phase 3 transformed the project from a primarily customized portfolio template into a more complete portfolio site with structured content, a blog, a gallery, multilingual support, and a more consistent visual system.

---


---

# Author

Created using:

* Hugo
* Hugo Profile Theme (Creator: Gurusabarish)
* GitHub Actions
* GitHub Pages
