# Tailwind CSS Setup Guide

This guide will walk you through setting up Tailwind CSS v4 in your Django project.

## Prerequisites

- Node.js and npm installed on your system
- Django project already set up

## Installation Steps

### 1. Install Tailwind CSS Dependencies

From the project root directory, run:

```bash
npm install
```

This will install:

- `@tailwindcss/cli` - The Tailwind CSS command-line interface
- `tailwindcss` - The Tailwind CSS framework

### 2. Project Structure

Your Tailwind CSS files should be organized as follows:

```
clinic_project/
└── clinic_project/
    └── static/
        ├── src/
        │   └── styles.css          # Source CSS file with Tailwind imports
        └── dist/
            └── styles.css          # Compiled CSS (generated)
```

### 3. Source CSS File

The source file `clinic_project/clinic_project/static/src/styles.css` should contain:

```css
@import 'tailwindcss';
```

This imports all Tailwind CSS utilities and components.

### 4. Django Settings Configuration

Ensure your `settings.py` has the following configuration:

```python
# Static files configuration
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'clinic_project' / 'static']
```

Also make sure `django.contrib.staticfiles` is in your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... other apps
    'django.contrib.staticfiles',
    # ... your apps
]
```

### 5. Template Configuration

In your Django templates (e.g., `base.html`), make sure to:

1. Load the static template tag at the top:

```django
{% load static %}
```

2. Reference the compiled CSS file:

```django
<link href="{% static 'dist/styles.css' %}" rel="stylesheet" type="text/css" />
```

## Usage

### Development Mode (Watch Mode)

For development, run the watch command to automatically rebuild CSS when you make changes:

```bash
npm run watch:css
```

This will:

- Watch for changes in your source files
- Automatically rebuild `styles.css` when changes are detected
- Keep running until you stop it (Ctrl+C)

**Note:** Keep this terminal running while developing. You only need to run it once per development session.

### Production Build

For a one-time build (useful for production or testing):

```bash
npm run build:css
```

This will compile your CSS once and exit.

## Available npm Scripts

- `npm run build:css` - Build CSS once (no watch)
- `npm run watch:css` - Build CSS and watch for changes

## How It Works

1. **Source File**: `clinic_project/clinic_project/static/src/styles.css`

   - Contains `@import "tailwindcss";`
   - This is where you can add custom CSS if needed

2. **Build Process**: Tailwind CLI processes the source file and:

   - Scans your HTML templates for Tailwind classes
   - Generates only the CSS you actually use
   - Outputs to `clinic_project/clinic_project/static/dist/styles.css`

3. **Django Integration**: Django serves the compiled CSS from the `dist` folder using the `{% static %}` template tag.

## Troubleshooting

### CSS Not Updating

1. Make sure `npm run watch:css` is running
2. Check that the output file `dist/styles.css` exists and is being updated
3. Hard refresh your browser (Ctrl+Shift+R or Cmd+Shift+R)
4. Verify `STATICFILES_DIRS` in `settings.py` points to the correct directory

### Template Errors

If you see "Invalid block tag: 'static'":

- Make sure `{% load static %}` is at the top of your template
- Verify `django.contrib.staticfiles` is in `INSTALLED_APPS`

### File Not Found Errors

- Ensure you're running npm commands from the project root directory
- Check that the paths in `package.json` match your project structure
- Verify the source file exists at `clinic_project/clinic_project/static/src/styles.css`

## Customization

### Adding Custom CSS

You can add custom CSS to your source file:

```css
@import 'tailwindcss';

/* Your custom styles */
.my-custom-class {
  color: #ff0000;
}
```

### Using Tailwind Directives

In Tailwind CSS v4, you primarily use `@import "tailwindcss"`. For custom configurations, you can add:

```css
@import 'tailwindcss';

@theme {
  /* Custom theme configuration */
}
```

## Additional Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS v4 Documentation](https://tailwindcss.com/docs/v4-beta)
- [Django Static Files Documentation](https://docs.djangoproject.com/en/stable/howto/static-files/)
