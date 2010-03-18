#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
The freqattributes.core test suite.
"""

#from obspy.signal import freqattributes, util
import inspect
import os
import unittest
import numpy as np
import util
import freqattributes
from scipy import signal

# only tests for windowed data are implemented currently

class FreqTraceTestCase(unittest.TestCase):
    """
    Test cases for frequency attributes
    """
    def setUp(self):
        # directory where the test files are located
        path = os.path.dirname(inspect.getsourcefile(self.__class__))
        self.path = os.path.join(path, 'data')
        file = os.path.join(self.path, '3cssan.hy.1.MBGA_Z')
        f = open(file)
        self.res = np.loadtxt(f)
        f.close()
        file = os.path.join(self.path, 'MBGA_Z.ASC')
        f = open(file)
        self.data = np.loadtxt(f)
        f.close()
        #self.path = os.path.dirname(inspect.getsourcefile(self.__class__))
        #self.res = np.loadtxt("3cssan.hy.1.MBGA_Z")
        #data = np.loadtxt("MBGA_Z.ASC")
        self.n = 256
        self.fs = 75
        self.smoothie = 3
        self.fk = [2,1,0,-1,-2]
        self.inc = int(0.05*self.fs)
        self.nc = 12
        self.p = np.floor(3*np.log(self.fs))
        #[0] Time (k*inc)
        #[1] A_norm
        #[2] dA_norm
        #[3] dAsum
        #[4] dA2sum
        #[5] ct
        #[6] dct
        #[7] omega
        #[8] domega
        #[9] sigma
        #[10] dsigma
        #[11] logcep
        #[12] logcep
        #[13] logcep
        #[14] dperiod
        #[15] ddperiod
        #[16] bwith
        #[17] dbwith
        #[18] cfreq
        #[19] dcfreq
        #[20] hob1
        #[21] hob2
        #[22] hob3
        #[23] hob4
        #[24] hob5 
        #[25] hob6
        #[26] hob7
        #[27] hob8
        #[28] phi12
        #[29] dphi12
        #[30] phi13
        #[31] dphi13
        #[32] phi23 
        #[33] dphi23
        #[34] lv_h1 
        #[35] lv_h2 
        #[36] lv_h3
        #[37] dlv_h1 
        #[38] dlv_h2
        #[39] dlv_h3
        #[40] rect
        #[41] drect
        #[42] plan
        #[43] dplan
        self.data_win,self.nwin,self.no_win = util.enframe(self.data,
                    signal.hamming(self.n), self.inc)
        self.data_win_bc,self.nwin_,self.no_win_ = util.enframe(self.data,
                     np.ones(self.n),self.inc)
        #self.data_win = data

    def tearDown(self):
        pass

    def test_cfrequency(self):
        """
        """
        cfreq = freqattributes.cfrequency(self.data_win_bc,
                          self.fs,self.smoothie,self.fk)
        rms = np.sqrt(np.sum((cfreq[0]-self.res[:,18])**2)/
                          np.sum(self.res[:,18]**2))
        self.assertEqual(rms < 1.e-5, True)
        rms = np.sqrt(np.sum((cfreq[1]-self.res[:,19])**2)/
                          np.sum(self.res[:,19]**2))
        self.assertEqual(rms < 1.e-5, True)

    def test_bwith(self):
        """
        """
        bwith = freqattributes.bwith(self.data_win,
                                self.fs,self.smoothie,self.fk)
        rms = np.sqrt(np.sum((bwith[0]-self.res[:,16])**2)/
                                np.sum(self.res[:,16]**2))
        self.assertEqual(rms < 1.e-5, True)
        rms = np.sqrt(np.sum((bwith[1]-self.res[:,17])**2)/
                                np.sum(self.res[:,17]**2))
        self.assertEqual(rms < 1.e-5, True)

    def test_domper(self):
        """
        """
        dperiod = freqattributes.domperiod(self.data_win,
                                  self.fs,self.smoothie,self.fk)
        rms = np.sqrt(np.sum((dperiod[0]-self.res[:,14])**2)/
                                  np.sum(self.res[:,14]**2))
        self.assertEqual(rms < 1.e-5, True)
        rms = np.sqrt(np.sum((dperiod[1]-self.res[:,15])**2)/
                                  np.sum(self.res[:,15]**2))
        self.assertEqual(rms < 1.e-5, True)

    def test_logcep(self):
        """
        """
        cep = freqattributes.logcep(self.data_win,self.fs,self.nc,
                                    self.p,self.n, 'Hamming')
        rms = np.sqrt(np.sum((cep[0]-self.res[:,11])**2)/np.sum(self.res[:,11]**2))
        self.assertEqual(rms < 1.e-5, True)
        rms = np.sqrt(np.sum((cep[1]-self.res[:,12])**2)/np.sum(self.res[:,12]**2))
        self.assertEqual(rms < 1.e-5, True)
        rms = np.sqrt(np.sum((cep[2]-self.res[:,13])**2)/np.sum(self.res[:,13]**2))
        self.assertEqual(rms < 1.e-5, True)


def suite():
    return unittest.makeSuite(FreqTraceTestCase, 'test')

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
    
