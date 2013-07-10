# Stack Exchange Cross-Tag Analysis

*Stack Exchange Cross-Tag Analysis* is a small collection of Python scripts to automatically query the most popular tags from all main [Stack Exchange](http://stackexchange.com/) sites, index them, and finally create a CSV file with all cross-tag occurences suitable for import into [Gephi](http://gephi.org/) as well as a JSON file for visualizing the graph with [D3](http://d3js.org/).


## Usage

### Update

```docker-compose run --rm secta /usr/src/app/update.py``` updates the JSON and CSV files in the ```www``` directory.

### Visualize

```docker-compose up -d``` serves the web visualization on port 8000.


## Example Visualizations

### D3

![GephiExample Visualization](https://raw.githubusercontent.com/patrickhoefler/secta/master/examples/secta-d3.png)

### Gephi

![GephiExample Visualization](https://raw.githubusercontent.com/patrickhoefler/secta/master/examples/secta-gephi.png)

This visualization is also available as [PDF](https://raw.githubusercontent.com/patrickhoefler/secta/master/examples/secta-gephi.pdf) and [GEPHI](https://raw.githubusercontent.com/patrickhoefler/secta/master/examples/secta.gephi).


## License

[MIT](LICENSE)
