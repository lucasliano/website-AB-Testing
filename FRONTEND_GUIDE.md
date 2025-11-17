# FRONTEND GUIDE
**How to Build Front-End Pages**

This document explains the front-end stack used in this project, the design conventions, and how to build new pages or variants using the existing infrastructure.

---

# 1. Overview of the Front-End Architecture

The site is **server-rendered**, using:

- **Jinja2 templates** for all pages and partials  
- **Tailwind CSS** for styling  
- **Vanilla JavaScript** for light interactivity and analytics tracking  
- **Data attributes** to wire interactive elements and tracking  
- **Variant-specific templates** for A/B testing

There are **no front-end frameworks** (React/Vue/Svelte) and **no bundlers**.  
All HTML is rendered by the backend, and styling is handled through Tailwind’s utility classes.

---

# 2. Template Structure

All templates reside in:

```
app/templates/
```

## 2.1 Base layout

`base.html` defines:

- `<head>` (metadata, CSS)
- The global navbar + footer
- A `{% block content %}` region for page content

Example:

```jinja2
{% extends "base.html" %}

{% block content %}
  <!-- Your content here -->
{% endblock %}
```

## 2.2 Partials

Common reusable blocks live in:

```
app/templates/partials/
```

Examples: header, footer, hero, features.

You include them via:

```jinja2
{% include "partials/hero.html" %}
```

## 2.3 Variants (A/B Testing)

Each section can have multiple variants located in:

```
app/templates/variants/<variant_name>/<template_name>
```

The backend uses:

```jinja2
{% include jinja_load_variant_template("hero.html", current_variant) %}
```

You just create a `hero.html` file under the appropriate variant folder and it will be used automatically.

Example Structure:
```
app/
  templates/
    base.html
    home.html
    product.html
    partials/
      hero.html
      footer.html
    variants/
      A/
        home.html
        partials/
          hero.html
      B/
        home.html
```

---

# 3. Styling with Tailwind CSS

Tailwind is used throughout for spacing, layout, colors, and typography.  
The configuration is in:

```
tailwind.config.cjs
```

Brand colors:

- `text-brand-primary`
- `bg-brand-primary`
- `bg-brand-bg`
- `text-brand-secondary`

### 3.1 Source and build

Source CSS:

```
app/static/css/input.css
```

Build CSS:

```
app/static/css/main.css
```

Build commands:

```bash
npm install
npm run build:css
npm run watch:css
```

### 3.2 Design rules

- Use Tailwind utilities for all spacing:  
  `py-12`, `px-4`, `mt-6`, etc.
- Use `max-w-6xl mx-auto` for content width and horizontal rhythm.
- Typography patterns:
  - Titles: `text-2xl md:text-3xl font-bold`
  - Body: `text-gray-700`
  - Small uppercase: `text-sm text-gray-500 uppercase tracking-wide`

---

# 4. JavaScript & Data Attributes

The site uses **vanilla JS** in:

```
app/static/js/tracking.js
```

It handles:

- **Analytics tracking** via `data-event-name`
- **Tab-like behavior** via `data-app-tab` and `data-app-panel`

### 4.1 Tracking events

To track a UI interaction, add:

```html
<button
  data-event-name="click_buy-now_hero"
>
  Buy now
</button>
```

**Event names follow the structure:**

```
<action>_<target>_<location>
```

Examples:

- `click_buy-now_hero`
- `click_learn-more_pricing-main`
- `select_university_dropdown`

Analytics scripts automatically detect these elements.

---

# 5. How to Build a New Page

Example: creating a `/pricing` page.

## Step 1: create the template

```
app/templates/pricing.html
```

```jinja2
{% extends "base.html" %}

{% block content %}
<section class="bg-white">
  <div class="max-w-6xl mx-auto px-4 py-16">
    <h1 class="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
      Pricing
    </h1>

    <p class="text-gray-700 max-w-2xl mb-10">
      Choose the right configuration for your workflow.
    </p>

    <div class="grid md:grid-cols-3 gap-6">
      <!-- Cards here -->
    </div>
  </div>
</section>
{% endblock %}
```

## Step 2: Add tracking to CTAs

```html
<a
  href="/checkout"
  class="px-5 py-3 bg-brand-primary text-white rounded-lg shadow hover:bg-blue-700"
  data-event-name="click_buy-now_pricing-main"
>
  Buy now
</a>
```

## Step 3: Add variant support (optional)

Create:

```
app/templates/variants/C/hero.html
```

And it will override the default hero for variant C.

---

# 6. How to Build a Section Component

Each content section should be:

- A standalone Jinja partial
- Styled with Tailwind only
- Using consistent spacing (`py-16`, `px-4`)
- Responsive via `md:` classes

Example structure:

```
partials/
  hero.html
  features.html
  footer.html
```

---

# 7. Development Workflow

1. Start backend (FastAPI/Uvicorn)
2. Build or watch Tailwind:
   ```bash
   npm run watch:css
   ```
3. Modify templates
4. Refresh page to see changes

---

# 8. Best Practices

✔ Prefer Tailwind utilities over custom CSS  
✔ Keep pages modular by using partials  
✔ Add tracking (`data-event-name`) to important actions  
✔ Use semantic HTML where possible  
✔ Maintain consistent spacing and layout patterns  
✔ Use variants for A/B testing instead of logic in templates  
✔ Keep JS minimal—stick to attribute-driven interactions  

---

# 9. File Layout Overview

```
app/
  templates/
    base.html
    home.html
    product.html
    partials/
      hero.html
      footer.html
    variants/
      A/
      B/
      C/
  static/
    css/
      input.css
      main.css
    js/
      tracking.js
    images/
    docs/
```

---

# 10. Summary

This front-end stack is intentionally **simple, fast, and designer-friendly**:

- Write HTML in Jinja templates  
- Style everything with Tailwind  
- Use tiny JS helpers for tracking and UI toggles  
- Build variants by duplicating partials  
- Keep everything server-rendered and lightweight  

With this guide, any designer or developer can confidently build pages, components, and A/B variants using the existing infrastructure.
