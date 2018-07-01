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

import abc

class AnomalyDetector(object):
  """
  Base class for all anomaly detectors. When inheriting from this class please
  take note of which methods MUST be overridden, as documented below.
  """
  __metaclass__ = abc.ABCMeta

  def __init__(self):
    self.inputMin = 0
    self.inputMax = 0.1


  def initialize(self):
    """Do anything to initialize your detector in before calling run.

    Pooling across cores forces a pickling operation when moving objects from
    the main core to the pool and this may not always be possible. This function
    allows you to create objects within the pool itself to avoid this issue.
    """
    pass


  @abc.abstractmethod
  def handleRecord(self, inputData):
    """
    Returns a list [anomalyScore, *]. It is required that the first
    element of the list is the anomalyScore. The other elements may
    be anything, but should correspond to the names returned by
    getAdditionalHeaders().

    This method MUST be overridden by subclasses
    """
    raise NotImplementedError


  def run(self, dataRow):
    """
    Main function that is called to collect anomaly scores for a given file.
    """
    inputData = dataRow

    detectorValues = self.handleRecord(inputData)
    return detectorValues


def detectDataSet(args):
  """
  Function called in each detector process that run the detector that it is
  given.

  @param args   (tuple)   Arguments to run a detector on a file and then
  """
  (detectorInstance, dataRow) = args
  return detectorInstance.run(dataRow)