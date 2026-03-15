# -*- coding: utf-8 -*-
"""
Created on Fri Jul  4 08:32:10 2025

@author: yoelr
"""
import biosteam as bst

__all__ = (
    'create_stripper_system', 
    'create_flash_system',
    'create_shortcut_column_system',
    'create_heat_exchanger_system',
)

def create_stripper_system(alg):
    bst.settings.set_thermo(['AceticAcid', 'Water', 'MTBE'], cache=True)
    feed = bst.Stream('feed', Water=75, AceticAcid=5, MTBE=20, T=320)
    steam = bst.Stream('steam', Water=100, phase='g', T=390)
    stripper = bst.Stripper('D1',
        N_stages=5, ins=[feed, steam], 
        outs=['vapor', 'liquid'],
        solute="AceticAcid", 
    )
    return bst.System.from_units(units=[stripper], algorithm=alg)
    
def create_flash_system(alg):
    bst.settings.set_thermo(
        ['Water', 'Ethanol'], cache=True
    )
    with bst.System(algorithm=alg) as system:
        bst.StageEquilibrium(
            ins=bst.Stream('feed', Water=1, Ethanol=1), 
            outs=['vapor', 'liquid'],
            phases=('g', 'l')
        )
    return system

def create_shortcut_column_system(alg):
    bst.settings.set_thermo(['Butane', 'Hexane'], cache=True)
    feed = bst.Stream('feed', Butane=75, Hexane=50, T=320)
    column = bst.ShortcutColumn('D1',
        ins=[feed], 
        outs=['vapor', 'liquid'],
        LHK=('Butane', 'Hexane'),
        y_top=0.99, x_bot=0.01, k=2,
        is_divided=True,
    )
    return bst.System.from_units(units=[column], algorithm=alg)

def create_heat_exchanger_system(alg):
    bst.settings.set_thermo(['Butane', 'Hexane', 'Water'], cache=True)
    feed = bst.Stream('feed', Butane=75, Hexane=50, T=330)
    utility = bst.Stream('feed', Water=75, T=310)
    HX = bst.StageEquilibrium(
        'heat_exchanger',
        ins=[feed, utility], 
        phases=('g', 'l'),
        B=0,
    )
    return bst.System.from_units(units=[HX], algorithm=alg)


