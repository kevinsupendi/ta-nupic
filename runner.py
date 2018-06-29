# ----------------------------------------------------------------------
# Copyright (C) 2014-2015, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
import pandas
from detectors.base import detectDataSet
from detectors.numenta.numenta_detector import NumentaDetector


class Runner(object):
  """
  Class to run an endpoint (detect, optimize, or score) on the NAB
  benchmark using the specified set of profiles, thresholds, and/or detectors.
  """

  def __init__(self,
               dataDir,
               resultsDir):
    """
    @param dataDir        (string)  Directory where all the raw datasets exist.

    @param resultsDir     (string)  Directory where the detector anomaly scores
                                    will be scored.
    """
    self.dataDir = dataDir
    self.resultsDir = resultsDir

    self.probationaryPercent = 0.15
    self.windowSize = 0.10

  def readFile(self, filePath):
    return pandas.read_csv(filePath, header=0, parse_dates=[0])


  def detect(self):
    """Generate results file given a dictionary of detector classes

    Function that takes a set of detectors and a corpus of data and creates a
    set of files storing the alerts and anomaly scores given by the detectors

    @param detectors     (dict)         Dictionary with key value pairs of a
                                        detector name and its corresponding
                                        class constructor.
    """
    print "\nRunning detection step"

    dataSet = self.readFile("data/ec2_cpu_utilization.csv")
    relativePath = "data/ec2_cpu_utilization.csv"
    args = (
      NumentaDetector(
        dataSet=dataSet,
        probationaryPercent=self.probationaryPercent),
      "numenta",
      self.resultsDir,
      relativePath
    )

    detectDataSet(args)
