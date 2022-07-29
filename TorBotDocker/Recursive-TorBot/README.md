## TorBot Recursive Crawler


### Setup

- Clone the repository
```
git clone https://github.com/ranjanikrishnan/Recursive-TorBot.git
```
- Build the docker image
```
cd Recursive-TorBot
docker build -t torbot .
```
- Run and enter bash into the container
```
docker run -ti torbot
```
- Run setup script(faced errors while adding these commands to Dockerfile, hence a separate script)
```
sh install-script.sh
```
- To run the tool
```
python3 torBot.py -h
python3 torBot.py -u <url-link> -s -r 10
```


### Extended Features

The features provided by the original TorBoT tool can be found [here](TorBoT/README.md).
The tool has been extended to provide the following features:

1. Recursive crawling from the website - Crawls the given onion link, and the user specified number of links from the seed link (Default value of 10).
  - ` python3 torBot.py -u <url-link> -r <number-of-links-to-be-crawled>`
2. Segregates clearnet and onion links and saves them in separate json files.
  - ` python3 torBot.py -u <url-link> -s`
3. Printing the list of links to the screen is made optional. The following command can be used to show the output on the screen.
  - `python3 torBot.py -u <url-link> -p`
