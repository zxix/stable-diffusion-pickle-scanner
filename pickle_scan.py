# copyright zxix 2022
# https://creativecommons.org/licenses/by-nc-sa/4.0/
import torch
import pickle_inspector
import sys
from pathlib import Path

debug = len(sys.argv) == 3

dir = sys.argv[1]
print("checking dir: " + dir)

BASE_DIR = Path(dir)
EXTENSIONS = {'.pt', '.bin', '.ckpt'}
BAD_CALLS = {'os', 'shutil', 'sys', 'requests', 'net'}
BAD_SIGNAL = {'rm ', 'cat ', 'nc ', '/bin/sh '}

for path in BASE_DIR.glob(r'**/*'):
  if path.suffix in EXTENSIONS:
    print("")
    print("..." + path.as_posix())
    result = torch.load(path.as_posix(), pickle_module=pickle_inspector.pickle)
    result_total = 0
    result_other = 0
    result_calls = {}
    result_signals = {}
    result_output = ""

    for call in BAD_CALLS:
      result_calls[call] = 0

    for signal in BAD_SIGNAL:
      result_signals[signal] = 0

    for c in result.calls:
      for call in BAD_CALLS:
        if (c.find(call + ".") == 0):
          result_calls[call] += 1
          result_total += 1
          result_output += "\n--- found lib call (" + call + ") ---\n"
          result_output += c
          result_output += "\n---------------\n"
          break
      for signal in BAD_SIGNAL:
        if (c.find(signal) > -1):
          result_signals[signal] += 1
          result_total += 1
          result_output += "\n--- found malicious signal (" + signal + ") ---\n"
          result_output += c
          result_output += "\n---------------\n"
          break

      if (
        c.find("numpy.") != 0 and 
        c.find("_codecs.") != 0 and 
        c.find("collections.") != 0 and 
        c.find("torch.") != 0):
        result_total += 1
        result_other += 1
        result_output += "\n--- found non-standard lib call ---\n"
        result_output += c
        result_output += "\n---------------\n"

    if (result_total > 0):
      for call in BAD_CALLS:
        print("library call (" + call + ".): " + str(result_calls[call]))
      for signal in BAD_SIGNAL:
        print("malicious signal (" + signal + "): " + str(result_signals[signal]))
      print("non-standard calls: " + str(result_other))
      print("total: " + str(result_total))
      print("")
      print("SCAN FAILED")

      if (debug):
        print(result_output)
    else:
      print("SCAN PASSED!")
