# _templates Folder

This folder contains Jinja2 templates for customizing the HTML output of your Sphinx documentation.

## Current Files

- **footer.html** - Custom footer template
- **sidebar.html** - Custom sidebar template with quick links

## How Templates Work

Sphinx uses Jinja2 templates to generate HTML. You can override default templates by placing them in this folder with the same name.

## Common Templates to Override

- `layout.html` - Main page layout
- `footer.html` - Footer section
- `sidebartoc.html` - Table of contents sidebar
- `sidebar.html` - Sidebar customization
- `page.html` - Individual page template
- `searchbox.html` - Search box

## Template Syntax

Templates use Jinja2 syntax:

```html
{% extends "layout.html" %}
{% block footer %}
    Your custom footer content
{% endblock %}
```

## Available Variables

Common variables available in templates:

- `project` - Project name
- `release` - Version number
- `copyright` - Copyright string
- `pathto()` - Function to generate paths
- `theme` - Current theme name

## Finding Templates to Override

1. Check your theme's documentation
2. Look in theme's source code (usually in Python site-packages)
3. Use Sphinx's template debugging: `make html SPHINXOPTS="-D sphinx_debug=1"`

## Best Practices

- Extend existing templates rather than copying everything
- Test changes after each modification
- Keep templates simple and maintainable
- Use theme variables when possible

## Example: Custom Footer

```html
{# _templates/footer.html #}
<div class="custom-footer">
    <p>&copy; {{ copyright }}</p>
    <p>Version {{ release }}</p>
</div>
```

See `STATIC_TEMPLATES_GUIDE.md` in the docs folder for more detailed information.

