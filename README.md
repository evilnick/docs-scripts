# docs-scripts
various scripts for doing things with markdown etc

## discfetch.py

Fairly simple tool, will fetch the markdown content of a given discourse URL. if run with the '--follow' option, it will also follow any links to other discourse topics and fetch those too. The saved files have the URL encoded in the top as an HTML comment. 
Note: This uses the raw access and doesn't need an API key or special permissions.

