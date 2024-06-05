#! /usr/bin/env python
import pylint

pylint.run_pylint(argv=["apiAlerts.py"])

# To see Pylint score, simply run $python3 test.py
# If pylint not found, run $pip install pylint