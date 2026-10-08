# static site generator

### 8 october 2026

> building my own static site generator

this is a small static site generator that turns markdown content and static
assets into a website. it started as a boot.dev exercise and became another
place for me to understand how the pieces of a web project fit together.

## explore

- [static site generator](#static-site-generator)
  - [what it does](#what-it-does)
  - [live url](#live-url)
  - [setup](#setup)
  - [usage](#usage)
  - [test](#test)
  - [stack](#stack)
  - [find me](#find-me)

## what it does

the generator currently:

- walks through the `content/` directory recursively
- turns markdown files into html pages
- copies images and css from `static/`
- rewrites root-relative links for local and github pages builds
- writes the finished site to `docs/`

## live url

the site is live here: [static site generator](https://tgr-wjya.github.io/static-site-generator/)

## setup

this project uses Python 3.13+ and `uv`.

```bash
uv sync
```

## usage

generate the site for local development:

```bash
python3 src/main.py
```

serve the generated site at `http://localhost:8888`:

```bash
./main.sh
```

build the site with its github pages base path:

```bash
./build.sh
```

the base path can also be passed directly:

```bash
python3 src/main.py "/static-site-generator/"
```

## test

run the test suite with:

```bash
python3 -m unittest discover -s src
```

## stack

python + unittest + github pages

## find me

i'm active in boot.dev, you should check me out.

[portfolio website](https://tgr-wjya.up.railway.app/) · [email](mailto:tgrwjya6371+contact@gmail.com) · [linkedin](https://www.linkedin.com/in/tgr-wjya/) · [boot.dev](https://www.boot.dev/u/handmadeinvite39)

---

made with ◉‿◉
