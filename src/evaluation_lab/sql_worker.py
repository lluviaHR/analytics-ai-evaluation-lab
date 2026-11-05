"""Subprocess entry point for controlled DuckDB execution."""

import json
import sys

from evaluation_lab.sql_evidence import _worker


class JsonOutput:
    def put(self, result):
        sys.stdout.write(json.dumps(result) + "\n")
        sys.stdout.flush()


def main():
    request = json.load(sys.stdin)
    _worker(
        request["csv_path"],
        request["sql"],
        JsonOutput(),
        request["max_rows"],
    )


if __name__ == "__main__":
    main()
