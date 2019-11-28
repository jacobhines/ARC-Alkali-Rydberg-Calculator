# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import
from .alkali_atom_functions import *

import os
import numpy as np
from math import sqrt

import sqlite3
sqlite3.register_adapter(np.float64, float)
sqlite3.register_adapter(np.float32, float)
sqlite3.register_adapter(np.int64, int)
sqlite3.register_adapter(np.int32, int)


class AlkalineEarthAtom(AlkaliAtom):

    modelPotential_coef = dict()
    """
        Model potential parameters fitted from experimental observations for
        different l (electron angular momentum)
    """

    quantumDefect = [[[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                     [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                     [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]],
                     [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]]
    """ Contains list of modified Rydberg-Ritz coefficients for calculating
        quantum defects for
        [[ :math:`^1S_{0},^1P_{1},^1D_{2},^1F_{3}`],
        [ :math:`^3S_{0},^3P_{0},^3D_{1},^3F_{2}`],
        [ :math:`^3S_{0},^3P_{1},^3D_{2},^3F_{3}`],
        [ :math:`^3S_{1},^3P_{2},^3D_{3},^3F_{4}`]]."""

    def __init__(self, preferQuantumDefects=True, cpp_numerov=True):
        self.cpp_numerov = cpp_numerov
        self.preferQuantumDefects = preferQuantumDefects

        self._databaseInit()

        if self.cpp_numerov:
            from .arc_c_extensions import NumerovWavefunction
            self.NumerovWavefunction = NumerovWavefunction

        # load dipole matrix elements previously calculated
        data = []
        if (self.dipoleMatrixElementFile != ""):
            if preferQuantumDefects is False:
                self.dipoleMatrixElementFile = \
                    "NIST_" + self.dipoleMatrixElementFile

            try:
                data = np.load(os.path.join(self.dataFolder,
                                            self.dipoleMatrixElementFile),
                               encoding='latin1', allow_pickle=True)
            except IOError as e:
                print("Error reading dipoleMatrixElement File "
                      + os.path.join(self.dataFolder,
                                     self.dipoleMatrixElementFile))
                print(e)
        # save to SQLite database
        try:
            self.c.execute('''SELECT COUNT(*) FROM sqlite_master
                            WHERE type='table' AND name='dipoleME';''')
            if (self.c.fetchone()[0] == 0):
                # create table
                self.c.execute('''CREATE TABLE IF NOT EXISTS dipoleME
                 (n1 TINYINT UNSIGNED, l1 TINYINT UNSIGNED,
                 j1 TINYINT UNSIGNED, s1 TINYINT UNSIGNED,
                 n2 TINYINT UNSIGNED, l2 TINYINT UNSIGNED,
                 j2 TINYINT UNSIGNED, s2 TINYINT UNSIGNED,
                 dme DOUBLE,
                 PRIMARY KEY (n1,l1,j1,s1,n2,l2,j2,s2)
                ) ''')
                if (len(data) > 0):
                    self.c.executemany(
                        'INSERT INTO dipoleME VALUES (?,?,?,?,?,?,?,?,?)',
                        data)
                self.conn.commit()
        except sqlite3.Error as e:
            print("Error while loading precalculated values into the database")
            print(e)
            exit()

        # load quadrupole matrix elements previously calculated
        data = []
        if (self.quadrupoleMatrixElementFile != ""):
            if preferQuantumDefects is False:
                self.quadrupoleMatrixElementFile = \
                    "NIST_" + self.quadrupoleMatrixElementFile
            try:
                data = np.load(os.path.join(self.dataFolder,
                                            self.quadrupoleMatrixElementFile),
                               encoding='latin1', allow_pickle=True)

            except IOError as e:
                print("Error reading quadrupoleMatrixElementFile File "
                      + os.path.join(self.dataFolder,
                                     self.quadrupoleMatrixElementFile))
                print(e)
        # save to SQLite database
        try:
            self.c.execute('''SELECT COUNT(*) FROM sqlite_master
                            WHERE type='table' AND name='quadrupoleME';''')
            if (self.c.fetchone()[0] == 0):
                # create table
                self.c.execute('''CREATE TABLE IF NOT EXISTS quadrupoleME
                 (n1 TINYINT UNSIGNED, l1 TINYINT UNSIGNED,
                 j1 TINYINT UNSIGNED, s1 TINYINT UNSIGNED,
                 n2 TINYINT UNSIGNED, l2 TINYINT UNSIGNED,
                 j2 TINYINT UNSIGNED, s2 TINYINT UNSIGNED,
                 qme DOUBLE,
                 PRIMARY KEY (n1,l1,j1,s1,n2,l2,j2,s2)
                ) ''')
                if (len(data) > 0):
                    self.c.executemany(
                        'INSERT INTO quadrupoleME VALUES (?,?,?,?,?,?,?,?,?)',
                        data)
                self.conn.commit()
        except sqlite3.Error as e:
            print("Error while loading precalculated values into the database")
            print(e)
            exit()

        if (self.levelDataFromNIST == ""):
            print("NIST level data file not specified."
                  " Only quantum defects will be used.")
        else:
            levels = self._parseLevelsFromNIST(
                os.path.join(self.dataFolder, self.levelDataFromNIST)
            )
            br = 0
            while br < len(levels):
                self._addEnergy(*levels[br])
                br = br + 1
            try:
                self.conn.commit()
            except sqlite3.Error as e:
                print("Error while loading precalculated values"
                      "into the database")
                print(e)
                exit()

        self._readLiteratureValues()

    def _parseLevelsFromNIST(self, fileData):
        data = np.loadtxt(fileData, delimiter=",",
                          usecols=(0, 1, 3, 2, 4))
        return data

    def _addEnergy(self, n, l, j, s, energy):
        """
            Adds energy level relative to

            NOTE:
            Requres changes to be commited to the sql database afterwards!

            Args:
                n: principal quantum number
                l: orbital angular momentum quantum number
                j: total angular momentum quantum number
                s: spin quantum number
                energy: energy in cm^-1 relative to the ground state
        """
        self.c.execute(
            'INSERT INTO energyLevel VALUES (?,?,?,?,?)',
            (int(n), int(l), int(j), int(s),
             energy * 1.e2
             * physical_constants["inverse meter-electron volt relationship"][0]
             - self.ionisationEnergy)
        )
        self.NISTdataLevels = max(self.NISTdataLevels, int(n))
        # saves energy in eV

    def _databaseInit(self):
        self.conn = sqlite3.connect(os.path.join(self.dataFolder,
                                                 self.precalculatedDB))
        self.c = self.conn.cursor()

        # create space for storing NIST/literature energy levels
        self.c.execute('''SELECT COUNT(*) FROM sqlite_master
                        WHERE type='table' AND name='energyLevel';''')
        if (self.c.fetchone()[0] != 0):
            self.c.execute('''DROP TABLE energyLevel''')
        # create fresh table
        self.c.execute('''CREATE TABLE IF NOT EXISTS energyLevel
             (n TINYINT UNSIGNED, l TINYINT UNSIGNED, j TINYINT UNSIGNED,
             s TINYINT UNSIGNED,
             energy DOUBLE,
             PRIMARY KEY (n, l, j, s)
            ) ''')

        self.conn.commit()

    def _getSavedEnergy(self, n, l, j, s=0):
        self.c.execute('''SELECT energy FROM energyLevel WHERE
            n= ? AND l = ? AND j = ? AND
            s = ? ''', (n, l, j, s))
        energy = self.c.fetchone()
        if (energy):
            return energy[0]
        else:
            return 0      # there is no saved energy level measurement

    def getRadialMatrixElement(self,
                               n1, l1, j1,
                               n2, l2, j2,
                               s1=0.5, s2=0.5,
                               useLiterature=True):
        """
            Radial part of the dipole matrix element

            Calculates :math:`\\int \\mathbf{d}r~R_{n_1,l_1,j_1}(r)\\cdot \
                R_{n_1,l_1,j_1}(r) \\cdot r^3`.

            Args:
                n1 (int): principal quantum number of state 1
                l1 (int): orbital angular momentum of state 1
                j1 (float): total angular momentum of state 1
                n2 (int): principal quantum number of state 2
                l2 (int): orbital angular momentum of state 2
                j2 (float): total angular momentum of state 2
                s1 (float): optional, total spin angular momentum of state 1.
                    By default 0.5 for Alkali atoms.
                s2 (float): optional, total spin angular momentum of state 2.
                    By default 0.5 for Alkali atoms.
            Returns:
                float: dipole matrix element (:math:`a_0 e`).
        """
        dl = abs(l1 - l2)
        dj = abs(j2 - j2)
        if not(dl == 1 and (dj < 1.1)):
            return 0

        if (self.getEnergy(n1, l1, j1) > self.getEnergy(n2, l2, j2)):
            temp = n1
            n1 = n2
            n2 = temp
            temp = l1
            l1 = l2
            l2 = temp
            temp = j1
            j1 = j2
            j2 = temp
            temp = s1
            s1 = s2
            s2 = temp

        n1 = int(n1)
        n2 = int(n2)
        l1 = int(l1)
        l2 = int(l2)

        # HACK: add literature later
        """
        if useLiterature:
            # is there literature value for this DME? If there is,
            # use the best one (smalles error)
            self.c.execute('''SELECT dme FROM literatureDME WHERE
             n1= ? AND l1 = ? AND j1_x2 = ? AND
             n2 = ? AND l2 = ? AND j2_x2 = ?
             ORDER BY errorEstimate ASC''', (n1, l1, j1_x2, n2, l2, j2_x2))
            answer = self.c.fetchone()
            if (answer):
                # we did found literature value
                return answer[0]
        """
        # was this calculated before? If it was, retrieve from memory

        self.c.execute(
            '''SELECT dme FROM dipoleME WHERE
            n1= ? AND l1 = ? AND j1 = ? AND s1 = ? AND
            n2 = ? AND l2 = ? AND j2 = ? AND s2 = ?''',
            (n1, l1, j1, s1, n2, l2, j2, s2)
            )
        dme = self.c.fetchone()
        if (dme):
            return dme[0]

        dipoleElement = self._getRadialDipoleSemiClassical(
            n1, l1, j1, n2, l2, j2, s1=s1, s2=s2
            )

        self.c.execute(
            ''' INSERT INTO dipoleME VALUES (?,?,?,?, ?,?,?,?, ?)''',
            [n1, l1, j1, s1,
             n2, l2, j2, s2,
             dipoleElement])
        self.conn.commit()

        return dipoleElement

    def _readLiteratureValues(self):
        # clear previously saved results, since literature file
        # might have been updated in the meantime
        self.c.execute('''DROP TABLE IF EXISTS literatureDME''')
        self.c.execute('''SELECT COUNT(*) FROM sqlite_master
                        WHERE type='table' AND name='literatureDME';''')
        if (self.c.fetchone()[0] == 0):
            # create table
            self.c.execute('''CREATE TABLE IF NOT EXISTS literatureDME
             (n1 TINYINT UNSIGNED, l1 TINYINT UNSIGNED, j1 TINYINT UNSIGNED,
             s1 TINYINT UNSIGNED,
             n2 TINYINT UNSIGNED, l2 TINYINT UNSIGNED, j2 TINYINT UNSIGNED,
             s2 TINYINT UNSIGNED,
             dme DOUBLE,
             typeOfSource TINYINT,
             errorEstimate DOUBLE,
             comment TINYTEXT,
             ref TINYTEXT,
             refdoi TINYTEXT
            );''')
            self.c.execute('''CREATE INDEX compositeIndex
            ON literatureDME (n1,l1,j1,s1,n2,l2,j2,s2); ''')
        self.conn.commit()

        if (self.literatureDMEfilename == ""):
            return 0  # no file specified for literature values

        try:
            fn = open(os.path.join(self.dataFolder,
                                   self.literatureDMEfilename), 'r')
            data = csv.reader(fn, delimiter=";", quotechar='"')

            literatureDME = []

            # i=0 is header
            i = 0
            for row in data:
                if i != 0:
                    n1 = int(row[0])
                    l1 = int(row[1])
                    j1 = int(row[2])
                    s1 = int(row[3])

                    n2 = int(row[4])
                    l2 = int(row[5])
                    j2 = int(row[6])
                    s2 = int(row[7])
                    if (
                        self.getEnergy(n1, l1, j1) > self.getEnergy(n2, l2, j2)
                            ):
                        temp = n1
                        n1 = n2
                        n2 = temp
                        temp = l1
                        l1 = l2
                        l2 = temp
                        temp = j1
                        j1 = j2
                        j2 = temp
                        temp = s1
                        s1 = s2
                        s2 = temp

                    # convered from reduced DME in J basis (symmetric notation)
                    # to radial part of dme as it is saved for calculated
                    # values

                    # To-DO : see in what notation are Strontium literature elements saved
                    print("To-do (_readLiteratureValues): see in what notation are Sr literature saved (angular part)")
                    dme = float(row[8]) / (
                        (-1)**(int(l1 + 0.5 + j2 + 1.))
                        * sqrt((2. * j1 + 1.) * (2. * j2 + 1.))
                        * Wigner6j(j1, 1., j2, l2, 0.5, l1)
                        * (-1)**l1 * sqrt((2.0 * l1 + 1.0) * (2.0 * l2 + 1.0))
                        * Wigner3j(l1, 1, l2, 0, 0, 0))

                    comment = row[9]
                    typeOfSource = int(row[10])  # 0 = experiment; 1 = theory
                    errorEstimate = float(row[11])
                    ref = row[12]
                    refdoi = row[13]

                    literatureDME.append([n1, l1, j1, s1,
                                          n2, l2, j2, s2, dme,
                                          typeOfSource, errorEstimate,
                                          comment, ref,
                                          refdoi])
                i += 1
            fn.close()

            try:
                if i > 0:
                    self.c.executemany('''INSERT INTO literatureDME
                                        VALUES (?,?,?,?, ?,?,?,?
                                                ?,?,?,?,?,?)''',
                                       literatureDME)
                    self.conn.commit()

            except sqlite3.Error as e:
                print("Error while loading precalculated values "
                      "into the database")
                print(e)
                print(literatureDME)
                exit()

        except IOError as e:
            print("Error reading literature values File "
                  + self.literatureDMEfilename)
            print(e)

    def getLiteratureDME(self,
                         n1, l1, j1, s1,
                         n2, l2, j2, s2):
        """
            Returns literature information on requested transition.

            Args:
                n1,l1,j1, s1: one of the states we are coupling
                n2,l2,j2, s2: the other state to which we are coupling

            Returns:
                bool, float, [int,float,string,string,string]:

                    hasLiteratureValue?, dme, referenceInformation

                    **If Boolean value is True**, a literature value for
                    dipole matrix element was found and reduced DME in J basis
                    is returned as the number. The third returned argument
                    (array) contains additional information about the
                    literature value in the following order [ typeOfSource,
                    errorEstimate , comment , reference, reference DOI]
                    upon success to find a literature value for dipole matrix
                    element:
                        * typeOfSource=1 if the value is theoretical
                         calculation; otherwise, if it is experimentally \
                         obtained value typeOfSource=0
                        * comment details where within the publication the \
                         value can be found
                        * errorEstimate is absolute error estimate
                        * reference is human-readable formatted reference
                        * reference DOI provides link to the publication.

                    **Boolean value is False**, followed by zero and an empty
                    array if no literature value for dipole matrix element is
                    found.

            Note:
                The literature values are stored in /data folder in
                <element name>_literature_dme.csv files as a ; separated
                values. Each row in the file consists of one literature entry,
                that has information in the following order:

                 * n1
                 * l1
                 * j1
                 * s1
                 * n2
                 * l2
                 * j2
                 * s2
                 * dipole matrix element reduced l basis (a.u.)
                 * comment (e.g. where in the paper value appears?)
                 * value origin: 1 for theoretical; 0 for experimental values
                 * accuracy
                 * source (human readable formatted citation)
                 * doi number (e.g. 10.1103/RevModPhys.82.2313 )

                If there are several values for a given transition, program
                outputs the value that has smallest error (under column
                accuracy). The list of values can be expanded - every time
                program runs this file is read and the list is parsed again
                for use in calculations.

        """

        if (self.getEnergy(n1, l1, j1) > self.getEnergy(n2, l2, j2)):
            temp = n1
            n1 = n2
            n2 = temp
            temp = l1
            l1 = l2
            l2 = temp
            temp = j1
            j1 = j2
            j2 = temp
            temp = s1
            s1 = s2
            s2 = temp

        # is there literature value for this DME? If there is,
        # use the best one (wit the smallest error)

        self.c.execute('''SELECT dme, typeOfSource,
                     errorEstimate ,
                     comment ,
                     ref,
                     refdoi FROM literatureDME WHERE
                     n1= ? AND l1 = ? AND j1 = ? AND s1 = ? AND
                     n2 = ? AND l2 = ? AND j2 = ? AND s2 = ?
                     ORDER BY errorEstimate ASC''',
                       (n1, l1, j1, s1, n2, l2, j2, s2))
        answer = self.c.fetchone()
        if (answer):
            # we did found literature value
            return True, answer[0], [answer[1], answer[2], answer[3],
                                     answer[4], answer[5]]

        # if we are here, we were unsucessfull in literature search
        # for this value
        return False, 0, []

    def getQuadrupoleMatrixElement(self, n1, l1, j1, n2, l2, j2,
                                   s1=0.5, s2=0.5):
        """
            Radial part of the quadrupole matrix element

            Calculates :math:`\\int \\mathbf{d}r~R_{n_1,l_1,j_1}(r)\\cdot \
            R_{n_1,l_1,j_1}(r) \\cdot r^4`.
            See `Quadrupole calculation example snippet`_  .

            .. _`Quadrupole calculation example snippet`:
                ./Rydberg_atoms_a_primer.html#Quadrupole-matrix-elements

            Args:
                n1 (int): principal quantum number of state 1
                l1 (int): orbital angular momentum of state 1
                j1 (float): total angular momentum of state 1
                n2 (int): principal quantum number of state 2
                l2 (int): orbital angular momentum of state 2
                j2 (float): total angular momentum of state 2

            Returns:
                float: quadrupole matrix element (:math:`a_0^2 e`).
        """

        dl = abs(l1 - l2)
        dj = abs(j1 - j2)
        if not ((dl == 0 or dl == 2 or dl == 1)and (dj < 2.1)):
            return 0

        if (self.getEnergy(n1, l1, j1, s=s1)
                > self.getEnergy(n2, l2, j2, s=s2)):
            temp = n1
            n1 = n2
            n2 = temp
            temp = l1
            l1 = l2
            l2 = temp
            temp = j1
            j1 = j2
            j2 = temp

        n1 = int(n1)
        n2 = int(n2)
        l1 = int(l1)
        l2 = int(l2)

        # was this calculated before? If yes, retrieve from memory.
        self.c.execute('''SELECT qme FROM quadrupoleME WHERE
         n1= ? AND l1 = ? AND j1 = ? AND s1 = ? AND
         n2 = ? AND l2 = ? AND j2 = ? AND s2= ?''',
         (n1, l1, j1, s1, n2, l2, j2, s2))
        qme = self.c.fetchone()
        if (qme):
            return qme[0]

        # if it wasn't, calculate now

        quadrupoleElement = self._getRadialQuadrupoleSemiClassical(
            n1, l1, j1, n2, l2, j2, s1=s1, s2=s2
        )

        self.c.execute(''' INSERT INTO quadrupoleME VALUES (?,?,?,?, ?,?,?,?, ?)''',
                       [n1, l1, j1, s1, n2, l2, j2, s2, quadrupoleElement])
        self.conn.commit()

        return quadrupoleElement

    def radialWavefunction(self, l, s, j, stateEnergy,
                           innerLimit, outerLimit, step):
        raise NotImplementedError("radialWavefunction calculation for alkaline"
                                  " earths has not been implemented yet.")
        return

    def effectiveCharge(self, l, r):
        raise NotImplementedError("effectiveCharge calculation for alkaline"
                                  " earths has not been implemented yet.")
        return

    def corePotential(self, l, r):
        raise NotImplementedError("corePotential calculation for alkaline"
                                  " earths has not been implemented yet.")
        return

    def potential(self, l, s, j, r):
        raise NotImplementedError("potential calculation for alkaline"
                                  " earths has not been implemented yet.")
        return
