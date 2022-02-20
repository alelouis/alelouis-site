build:
    zola build
serve:
    zola serve --drafts -f
publish:
    rsync -aP public/ alelouis@ovh:/home/alelouis/alelouis.eu
