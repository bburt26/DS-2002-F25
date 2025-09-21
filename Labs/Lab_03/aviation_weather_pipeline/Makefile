.PHONY: all fetch analyze clean

all: analyze

fetch:
	@echo "Fetching: obtaining metar data..."
	bash ./fetch_metars.sh
	@echo "Fetch complete: metar data put in raw_metars/"

analyze: fetch
	@echo "Analyzing metar data..."
	bash ./analyze_data.sh
	@echo "Analysis complete: results in weather_report.csv"
	@echo "Pipeline completed"

clean:
	@echo "Cleaning new files..."
	rm -rf raw_metars/ weather_report.csv
	@echo "Cleaning complete: removed raw_metars/ and weather_report.csv"

