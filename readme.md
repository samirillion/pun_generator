# Smart Stupid-Namer
(set up for generating silly cocktail names)
## Build Client-side files
```bash
npm run build
```
This'll generate the build files in the <i>dist</i> folder, along with the index.html file, which the Python/Server side will serve up.

Alternatively, if you just want to work on the client side code, you can remove the parts of HomePage.vue that make http calls to the Flask server, and then run `
npm run serve`, and then view the site at `localhost:8080`
## Start the Flask App
Flask requires a number of dependencies to run, I would recommend using virtualenv
```bash
FLASK_APP=server.py FLASK_DEBUG=1 flask run
```
## Visit Website
At `localhost:5000`