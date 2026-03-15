# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 13:38:11 2024

@author: cortespea
"""
import biosteam as bst
from thermosteam.constants import R
from math import exp

__all__ = (
    'create_system_lactic_acid_purification',
)

def create_system_lactic_acid_purification(alg='sequential modular'):
    bst.settings.set_thermo(['Water', 'LacticAcid', 'MethylLactate', 'Methanol', 'SuccinicAcid'], cache=True)
    
    class Esterification(bst.KineticReaction):
        catalyst_fraction = 0.5 
        
        def volume(self, stream): # kg of catalyst
            rho_cat = 770 # kg / m3
            liquid_volume = self.liquid_volume
            catalyst_volume = self.catalyst_fraction * liquid_volume
            catalyst_mass = catalyst_volume * rho_cat
            return catalyst_mass
        
        def rate(self, stream):
            T = stream.T
            kf = 6.52e3 * exp(-4.8e4 / (R * T))
            kr = 2.72e3 * exp(-4.8e4 / (R * T))
            LaEt, La, H2O, EtOH, _ = stream.mol / stream.F_mol
            return 3600 * (kf * La * EtOH - kr * LaEt * H2O) # kmol / kg-catalyst / hr
    
    
    with bst.System(algorithm=alg) as sys:
        feed = bst.Stream(
            'feed',
            LacticAcid=4.174,
            Water=5.460,
            SuccinicAcid=0.531,
            MethylLactate=1e-6,
            total_flow=10.165,
            P=0.106 * 101325,
            T=72.5 + 273.15
        )
        feed.T = feed.bubble_point_at_P(P=0.2 * 101325).T
        makeup_methanol = bst.Stream('makeup_methanol', Methanol=0.035, P=2 * 101325, phase='g')
        makeup_methanol.T = makeup_methanol.dew_point_at_P(P=0.2 * 101325).T
        recycle_methanol = bst.Stream('recycle_methanol')
        esterification = bst.MESHDistillation(
            'esterification',
            ins=(feed, makeup_methanol, recycle_methanol), 
            outs=('esterification_distillate', 'bottoms'),
            N_stages=21,
            feed_stages=(1, 19),
            stage_specifications={
                0: ('Reflux', 1), # Unknown (update later)
                20: ('Flow', 0.0334), # Fraction of feed.
            },
            full_condenser=True,
            stage_reactions={
                i: Esterification('LacticAcid + Methanol -> Water + MethylLactate', reactant='LacticAcid')
                for i in range(1, 19)
            },
            maxiter=50,
            LHK=('Methanol', 'MethylLactate'),
            P=0.2 * 101325,
            use_cache=True
        )
        @esterification.add_specification(run=True)
        def adjust_flow():
            target = 0.2 + 16.495
            makeup_methanol.imol['Methanol'] = max(target - recycle_methanol.imol['Methanol'], 0)
        
        # catalyst_fraction = 0
        # dc = 1e-6
        # while catalyst_fraction < 0.5:
        #     dc *= 1.5
        #     if dc > 5e-3: dc = 1e-3
        #     if dc < 1e-4: dc = 1e-4
        #     catalyst_fraction += dc
        #     if catalyst_fraction > 0.5:
        #         catalyst_fraction = 0.5
        #     print('----')
        #     print(catalyst_fraction)
        #     print('----')
        #     Esterification.catalyst_fraction = catalyst_fraction
        #     esterification.simulate()
        #     for i in esterification.stages: print(i.Hnet) 
        #     esterification.show()
        
        # esterification.simulate()
        # for i in esterification.stages: print(i.Hnet) 
        # esterification.stage_reactions={
        #         i: Esterification('LacticAcid + Butanol -> Water + ButylLactate', reactant='LacticAcid')
        #         for i in range(1, 17)
        #     }
        # esterification.LHK=('Butanol', 'ButylLactate')
        # breakpoint()
        # esterification.simulate()
        hydrolysis = bst.MESHDistillation(
            'hydrolysis',
            ins=(esterification-0, water),
            outs=('hydrolysis_distillate', 'lactic_acid'),
            N_stages=89,
            feed_stages=(27, 50, 0),
            stage_specifications={
                0: ('Boilup', 0),
                52: ('Boilup', 1),
            },
            liquid_side_draws={
                0: 1.0,
            },
            stage_reactions={
                i: Esterification('LacticAcid + Butanol -> Water + ButylLactate', reactant='LacticAcid')
                for i in range(1, 52) # It will run in reverse
            },
            P=101325,
            LHK=('Butanol', 'LacticAcid'),
        )
        
        # @esterification.add_specification(run=True)
        # def adjust_flow():
        #     target = 5.85
        #     makeup_butanol.imol['Butanol'] = max(target - recycle_butanol.imol['Butanol'], 0)
        
        # Decanter
        butanol_rich_azeotrope = bst.Stream('butanol_rich_azeotrope')
        hydrolysis_settler = bst.StageEquilibrium(
            'settler',
            ins=(hydrolysis-2, water_distiller-0, butanol_rich_azeotrope), 
            outs=('butanol_rich_extract', hydrolysis_reflux),
            phases=('L', 'l'),
            top_chemical='Butanol',
            T=310,
        )
        
        # Butanol purification
        butanol_distiller = bst.BinaryDistillation(
            ins=(hydrolysis_settler-0),
            outs=(butanol_rich_azeotrope, recycle_butanol),
            x_bot=0.0001, y_top=0.6, k=1.2, Rmin=0.01,
            LHK=('Water', 'Butanol'),
        )
        
    return sys

if __name__ == '__main__':
    sys = create_system_lactic_acid_purification()
    sys.flatten()
    sys.diagram()
    sys.simulate()