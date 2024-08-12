#!/usr/bin/env python3

import json
import sys

results = []

# input is in the format:
# .github/CODE_OF_CONDUCT.md:73:0: error: Wrong amount of left-padding spaces(want multiple of 4)
# <file>:<line>:<column>: <severity>: <message>

for line in sys.stdin:
  line = line.strip()
  if not line:
      continue

  parts = line.split(":", 4)
  if len(parts) != 5:
      continue

  file, line, column, severity, message = parts
  line = int(line)
  column = int(column)
  message = message.strip()

  ruleId = "editorconfig-checker"

  # Switch for message beginning
  if message.startswith("Wrong amount of left-padding spaces"):
    ruleId = "left-padding"
  elif message.startswith("Wrong indentation type"):
    ruleId = "indentation-type"
  elif message.startswith("Trailing whitespace"):
    ruleId = "trailing-whitespace"
  elif message.startswith("Not all lines have the correct end of line character"):
    ruleId = "end-of-line"
  elif message.startswith("Wrong line endings or no final newline"):
    ruleId = "line-endings"
  elif message.startswith("No final newline expected"):
    ruleId = "final-newline"

  results.append({
      "ruleId": ruleId,
      "level": severity.lower().strip(),
      "message": {"text": message},
      "locations": [
          {
              "physicalLocation": {
                  "artifactLocation": {
                      "uri": file,
                  },
                  "region": {
                      "startLine": line,
                      "startColumn": column,
                  },
              },
          },
      ],
  })

sarif = {
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [{"results": results}],
}

print(json.dumps(sarif, indent=2))
