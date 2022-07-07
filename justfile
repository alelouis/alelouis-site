build:
    zola build
serve:
    zola serve --drafts -f
publish: build
    rsync -aP public/ alelouis@ovh:/home/alelouis/alelouis.eu
figures module='':
    python -m code.generate_figures {{module}}
