# _static Folder

This folder contains static files (CSS, JavaScript, images) that are automatically copied to the documentation output.

## Current Files

- **custom.css** - Custom stylesheet for documentation styling
- **custom.js** - Custom JavaScript for enhanced functionality

## Adding Files

1. **CSS Files**: Add `.css` files here and reference them in `conf.py`:
   ```python
   html_css_files = ['custom.css', 'your-file.css']
   ```

2. **JavaScript Files**: Add `.js` files here and reference them in `conf.py`:
   ```python
   html_js_files = ['custom.js', 'your-file.js']
   ```

3. **Images**: Place images here and reference them in RST files:
   ```rst
   .. image:: _static/your-image.png
   ```

4. **Other Static Files**: Any static files (fonts, icons, etc.) can be placed here.

## Usage in Templates

Reference static files in templates using `pathto()`:

```html
<link rel="stylesheet" href="{{ pathto('_static/custom.css', 1) }}" />
<script src="{{ pathto('_static/custom.js', 1) }}"></script>
```

## Notes

- Files are copied to `_build/html/_static/` during build
- Use relative paths when referencing from RST files
- Keep file sizes reasonable for web performance

