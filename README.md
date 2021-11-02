# Personal-Website
This is the source code of my personal website. Checkout the live version [here](https://alshishtawy.github.io/).

The website is generated using [pelican](https://blog.getpelican.com/) which is a static site generator.

To keep the git repo small, I didn't check in PDFs. If you want to test and rebuild the website, copy
the 'pdfs' folder form [Google Drive](https://drive.google.com/open?id=0B2Ed_iVCUD4aaEFDQVBDYy1OZ0E) and place
it the 'content' folder.

# Build and Development
Cheat sheet mainly for me to remember!
Note that the instructions are specific to the settings I use in `pelicanconf.py`

## Packages
```bash
# Required to build
pip install pelican
pip install Markdown
pip install typogrify
 
# To run tasks in tasks.py
pip install invoke
 
# Auto reload browser during development
pip install livereload

# Publish on GitHub Pages
pip install ghp-import
```

## Build
```bash
# Build one time
pelican content

# Auto build and refresh browser
invoke livereload
```

## Publish Manually
```bash
pelican content -s publishconf.py
```

## Publish on GitHub Pages
Warning! This will over write the master branch. For this to work, make sure that the source is in a separate branch.

```bash
# Publish
invoke gh-pages
```


