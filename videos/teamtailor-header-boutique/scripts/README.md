`index.html` se genera desde `scripts/index.template.html` con el trazado del isotipo T:

    python3 -I -c "import re;t=open('scripts/index.template.html').read();d=re.search(r' d=\"([^\"]+)\"',open('assets/brand/isotipo-t.svg').read()).group(1);open('index.html','w').write(t.replace('__T_PATH__',d))"
