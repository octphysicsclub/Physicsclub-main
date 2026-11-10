# STEM October Physics Club Website

## Project layout

- `index.html` is the home page.
- `pages/` contains the site sections. IPhR pages are grouped under `pages/iphr/`.
- `articles/` contains the magazine articles; YPWC winning articles are grouped under `articles/ypwc/`.
- `content/articles/` stores editable Markdown article sources.
- `content/source-manuscripts/` keeps the original submitted Word and PDF files.
- `assets/articles/` stores article covers and figures; other image groups live in `assets/magazine/`, `assets/publications/`, and `assets/brand/`.
- `assets/vendor/gsap/` contains the local GSAP libraries used by the site.
- `tools/` contains the reusable YPWC article builder.
- `docs/` contains design notes.

## Clean URLs

`vercel.json` enables Vercel clean URLs and maps short routes such as `/about`, `/magazine`, `/publications`, and `/iphr` to their organized static pages. Article pages are served at their paths under `/articles/`. Existing `.html` links redirect to their new paths.

## Local preview

Internal navigation links point directly to the HTML files, so a regular static server can preview the site without applying Vercel routing. From the project folder, run `py -m http.server 5500` and open `http://localhost:5500`. Vercel redirects those file paths to the clean public routes when deployed.
