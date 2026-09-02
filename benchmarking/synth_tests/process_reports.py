from result_output import output_results
from result_parser import parse_reports

if __name__ == "__main__":
    results = parse_reports()
    output_results(results)
