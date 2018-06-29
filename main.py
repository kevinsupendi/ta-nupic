from runner import Runner

if __name__ == "__main__":
	runner = Runner(dataDir="data",
					resultsDir="output")
	runner.detect()