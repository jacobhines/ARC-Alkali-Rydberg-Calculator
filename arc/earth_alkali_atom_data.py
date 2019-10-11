# coding=utf-8
"""
Data sources
-------------

.. [#c1] J. A. Armstrong, J. J. Wynne, and P. Esherick,
        "Bound, odd-parity J = 1 spectra of the alkaline earths: Ca, Sr, and Ba,"
        J. Opt. Soc. Am. 69, 211-230 (1979)


.. [#c2]R.Beigang K.Lücke A.Timmermann P.J.West D.Frölich
        Determination of absolute level energies of 5sns1S0 and 5snd1D2 Rydberg series of Sr
        Opt. Commun. 42, 19 1982.

.. [#c3] J E Sansonetti and G Nave. Wavelengths,
        Transition Probabilities, and Energy Levels for the Spectrum of Neutral Strontium (Sr I).
        Journal of Physical and Chemical Reference Data, 39:033103, 2010.

.. [#c4]Baig M Yaseen M Nadeem A Ali R Bhatti S
        Three-photon excitation of strontium Rydberg levels
        Optics Communications, vol: 156 (4-6) pp: 279-284, 1998

.. [#c5] P Esherick, J J Wynne, and J A Armstrong.
        Spectroscopy of 3P0 states of alkaline earths.
        Optics Letters, 1:19, 1977.

.. [#c6] P Esherick.
        Bound, even-parity J = 0 and J = 2 spectra of Sr.
        PhysicalReview A, 15:1920, 1977.

.. [#c7] R Beigang and D Schmidt.
        Two-Channel MQDT Analysis of Bound 5snd 3D1,3 Rydberg States of Strontium.
        Physica Scripta, 27:172, 1983.

.. [#c8]J R Rubbmark and S A Borgstr¨om.
        Rydberg Series in Strontium Found in Absorption by Selectively Laser-Excited Atoms.
        Physica Scripta, 18:196,1978

.. [#c9] Beigang R, Lucke K, Schmidt D, Timmermann A and West P J ¨
        One-Photon Laser Spectroscopy of Rydberg Series from Metastable Levels in Calcium and Strontium
        Phys. Scr. 26 183, 1982

.. [c10] L. Couturier, I. Nosske, F. Hu, C. Tan, C. Qiao, Y. H. Jiang, P. Chen, and M. Weidemüller.
        Measurement of the strontium triplet Rydberg series by depletion spectroscopy of ultracold atoms
        http://arxiv.org/abs/1810.07611

-[#yb1] Optical-microwave double-resonance spectroscopy of highly excited Rydberg states of ytterbium
        H. Maeda Y. Matsuo M. Takami A. Suzuki
        Physical Review Avol. 45issue 3(1992)pp: 1732-1741Published by American Physical Society

--[#yb2] Three-step laser spectroscopy and multichannel quantum defect analysis of odd-parity Rydberg states of neutral ytterbium
        M Aymar R J Champeau C Delsart O Robaux
        Journal of Physics B: Atomic and Molecular Physicsvol. 17issue 18(1984)pp: 3645-3661

--[#yb3] Laser and microwave spectroscopy of even-parity Rydberg states of neutral ytterbium and multichannel-quantum-defect-theory analysis
        H. Lehec A. Zuliani W. Maineult E. Luc-Koenig P. Pillet P. Cheinet F. Niyaz T. F. Gallagher
        Physical Review A vol. 98 issue 6 (2018) pp: 062506 Published by American Physical Society

--[#ca1] Microwave spectroscopy of calcium Rydberg states
        Thomas R. Gentile Barbara J. Hughey Daniel Kleppner Theodore W. Ducas
        Physical Review Avol. 42issue 1(1990)pp: 440-451Published by American Physical Society

--[#ca2] Determination of Ionization Potential of Calcium by High-Resolution Resonance Ionization Spectroscopy
        Masabumi Miyabe, Christopher Geppert, Masaaki Kato, Masaki Oba, Ikuo Wakaida, Kazuo Watanabe, Klaus D. A. Wendt
        Journal of the Physical Society of Japan, 75, 034302 (2006) 10.1143/JPSJ.75.034302
        
-- [#ca3] Meija, Juris; et al. (2016). "Atomic weights of the elements 2013 (IUPAC Technical Report)". Pure and Applied Chemistry. 88 (3): 265–91. doi:10.1515/pac-2015-0305.

"""
from __future__ import division, print_function, absolute_import

from .earth_alkali_atom_functions import *

from scipy.constants import physical_constants, pi , epsilon_0, hbar
from scipy.constants import Rydberg as C_Rydberg
from scipy.constants import m_e as C_m_e

class StrontiumI(DivalentAtom):
    """Properties of Strontium atoms"""

    ionisationEnergy = 5.69486740  #eV  ref. [#c3]
    ionisationEnergycm = 45932.1982     #45932.2036 #cm-1  ref. [#c3]
    
    #need to reference James millesn thesis!
    modelPotential_coef = {"1S0":[3.762,-6.33,1.07], "3S1":[2.93,-5.28,1.22], "1P1":[3.49,-1.86,1.10],\
                           "3P2":[3.23,-6.20,1.19],"3P1":[3.35,-6.13,1.12], "3P0":[3.45,-6.02,-6.13],\
                           "1D2":[2.78,-9.06,2.31],"3D3":[2.86,-9.71,2.20],"3D2":[3.12,-4.52,1.24],\
                           "3D1":[3.41,-6.02,1.27],"1F3":[9.22,-6.35,1.00],"3F4":[1.18,-9.04,1.06],\
                           "3F3":[1.18,-9.04,1.06],"3F2":[1.18,-9.04,1.06]}
    
    Z = 38
    scaledRydbergConstant = 109736.627# cm-1 *1.e2\
        #*physical_constants["inverse meter-electron volt relationship"][0] # ref. [#c2]

    levelDataFromNIST = ["sr_1S0.csv", "sr_3S1.csv", "sr_1P1.csv", "sr_3P2.csv", \
                         "sr_3P1.csv", "sr_3P0.csv", "sr_1D2.csv", "sr_3D3.csv", \
                         "sr_3D2.csv", "sr_3D1.csv", "sr_1F3.csv", "sr_3F4.csv", \
                         "sr_3F3.csv", "sr_3F2.csv"]  #: Store list of filenames to read in

    NISTdataLevels = {"1S0":65,"3S1":45, "1P1":79,"3P2":55,"3P1":17, "3P0":10,"1D2":65,"3D3":41,"3D2":45,"3D1":46,"1F3":25,"3F4":24,"3F3":24,"3F2":24}
    level_labels = ["1S0","3S1", "1P1","3P2","3P1", "3P0","1D2","3D3","3D2","3D1","1F3","3F4","3F3","3F2"]
    #dataFolder = 'data/sr_data'
    quantumDefectData ='test.csv'#'quantum_defect.csv'
    groundStateN = 5
    extraLevels = {"3D3":4, "3D1":4, "1F3":4, "3F4":4,"3F3":4, "3F2":4,"1D2":4}
    preferQuantumDefects = False
    alphaC = 15

    precalculatedDB = "sr_precalculated.db"

    dipoleMatrixElementFile = "sr_dipole_matrix_elements.npy"
    quadrupoleMatrixElementFile = "sr_quadrupole_matrix_elements.npy"

    literatureDMEfilename = 'strontium_literature_dme.csv'
    
    useLiterature = False 
    elementName = 'Strontium87'
    #LIZZY FIND A CITATION FOR THIS 
    mass = 87.62*physical_constants["atomic mass constant"][0]

    #fitting ranges have been taken from Pauls fits and christophe
    defectFittingRange ={"1S0":[14,34],"3S1":[13,45], "1P1":[14,28],"3P2":[8,18],"3P1":[8,22],\
                         "3P0":[8,15],"1D2":[36,66],"3D3":[20,45],"3D2":[22,37],"3D1":[20,32],\
                         "1F3":[10,25],"3F4":[10,24],"3F3":[10,24],"3F2":[10,24]}


class Calcium(DivalentAtom):
    """Properties of Calcium atoms"""

    ionisationEnergycm =  49305.924#cm-1  ref. [#ca2]
    ionisationEnergy = ionisationEnergycm/8065.544#eV ref.

    #need to reference James millesn thesis!
    modelPotential_coef = {}
    
    Z = 20
    scaledRydbergConstant = 109735.81        #*physical_constants["inverse meter-electron volt relationship"][0] # ref. [#c2]

    levelDataFromNIST = ["","","","","","","",'ca_1F3.csv']  #: Store list of filenames to read in no data

    NISTdataLevels = {"1F3":146}
    
    level_labels = ["1S0","3S1","1P1","3P1","1D2","3D2","3D1","1F3"]

    quantumDefectData ='quantum_defect_ca.csv'
    groundStateN = 4
    extraLevels = {} #unkown if such exist at time of writing
    preferQuantumDefects = False
    #alphaC = 

    precalculatedDB = "ca_precalculated.db"

    dipoleMatrixElementFile = "ca_dipole_matrix_elements.npy"
    quadrupoleMatrixElementFile = "ca_quadrupole_matrix_elements.npy"

    literatureDMEfilename = 'calcium_literature_dme.csv'
    
    useLiterature = False 
    elementName = 'Calcium'

    #LIZZY FIND A CITATION FOR THIS 
    mass = 40.078 *physical_constants["atomic mass constant"][0] # ref. [#ca3]

    #fitting ranges have been taken from Pauls fits and christophe
    defectFittingRange ={"1S0":[14,34],"3S1":[13,45], "1P1":[14,28],"3P2":[8,18],"3P1":[8,22],\
                         "3P0":[8,15],"1D2":[36,66],"3D3":[20,45],"3D2":[22,37],"3D1":[20,32],\
                         "1F3":[10,25],"3F4":[10,24],"3F3":[10,24],"3F2":[10,24]}

class Ytterbium(DivalentAtom):
    """Properties of Ytterbium atoms"""

   
    ionisationEnergycm = 50443.08  #cm-1  ref. [#yb3]
    ionisationEnergy = ionisationEnergycm/8065.544 #eV ref.
    
    
    #need to reference James millesn thesis!
    modelPotential_coef = {}
    
    Z = 70
    scaledRydbergConstant = 109736.627        #*physical_constants["inverse meter-electron volt relationship"][0] # ref. [#c2]

    levelDataFromNIST = ["yb_1S0.csv", "yb_1P1.csv", "yb_1D2.csv", "yb_3D2.csv"]#: Store list of filenames to read in no data

    NISTdataLevels = {"1S0":74, "1P1":48,"1D2":74, "3D2":74}
    
    level_labels = ["1S0", "1P1","1D2","3D2"]

    quantumDefectData ='quantum_defect_yb.csv'
    groundStateN = 6
    extraLevels = {} #unkown if such exist at time of writing
    preferQuantumDefects = False
    #alphaC = 

    precalculatedDB = "yb_precalculated.db"

    dipoleMatrixElementFile = "yb_dipole_matrix_elements.npy"
    quadrupoleMatrixElementFile = "yb_quadrupole_matrix_elements.npy"

    literatureDMEfilename = 'ytterbium_literature_dme.csv'
    
    useLiterature = False 
    elementName = 'ytterbium'

    #LIZZY FIND A CITATION FOR THIS 
    mass =173.045*physical_constants["atomic mass constant"][0] #ref. [#ca3]

    #fitting ranges have been taken from Pauls fits and christophe
    defectFittingRange ={"1S0":[15,43], "1P1":[35,53],"1D2":[28,75],"3D2":[10,52]}





	