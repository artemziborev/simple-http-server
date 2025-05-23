#!/bin/bash

# Create results directory if not exists
mkdir -p tests/load_tests/results

# Run wrk load tests
echo "Running load tests..."
wrk -t4 -c100 -d30s http://localhost:8080/ > load_tests/results/index.txt
wrk -t4 -c100 -d30s http://localhost:8080/test.html > load_tests/results/test.txt
wrk -t4 -c100 -d30s http://localhost:8080/subdir/ > load_tests/results/subdir.txt

echo "Load tests completed. Results saved to load_tests/results/"
