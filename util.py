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
import math
import os
import pandas
import json



def getProbationPeriod(probationPercent, fileLength):
  """Return the probationary period index."""
  return min(
    math.floor(probationPercent * fileLength),
    probationPercent * 5000)


def writeJSON(filePath, data):
  """Dumps data to a nicely formatted json at filePath."""
  with open(filePath, "w") as outFile:
    outFile.write(json.dumps(data,
                             sort_keys=True,
                             indent=4,
                             separators=(',', ': ')))


def convertAnomalyScoresToDetections(anomalyScores, threshold):
  """
  Convert anomaly scores (values between 0 and 1) to detections (binary
  values) given a threshold.
  """
  length = len(anomalyScores)
  detections = pandas.Series([0]*length)

  alerts = anomalyScores[anomalyScores >= threshold].index

  detections[alerts] = 1

  return detections


def relativeFilePaths(directory):
  """Given directory, get path of all files within relative to the directory.

  @param directory  (string)      Absolute directory name.

  @return           (iterable)    All filepaths within directory, relative to
                                  that directory.
  """
  for dirpath,_,filenames in os.walk(directory):
    filenames = [f for f in filenames if not f[0] == "."]
    for f in filenames:
      yield os.path.join(dirpath, f)


def absoluteFilePaths(directory):
  """Given directory, gets the absolute path of all files within.

  @param  directory   (string)    Directory name.

  @return             (iterable)  All absolute filepaths within directory.
  """
  for dirpath,_,filenames in os.walk(directory):
    filenames = [f for f in filenames if not f[0] == "."]
    for f in filenames:
      yield os.path.abspath(os.path.join(dirpath, f))


def makeDirsExist(dirname):
  """Makes sure a given directory exists. If not, it creates it.
  @param dirname  (string)  Absolute directory name.
  """

  if not os.path.exists(dirname):
    # This is being run in parallel so watch out for race condition.
    try:
      os.makedirs(dirname)
    except OSError:
      pass


def createPath(path):
  """Makes sure a given path exists. If not, it creates it.

  @param path   (string) Absolute path name.
  """
  dirname = os.path.dirname(path)
  makeDirsExist(dirname)
