import pytest
from unitee import SI


def test_construct():
    m1 = SI.m2
    m2 = SI('m2')
    m3 = SI('1 m2')
    m4 = 1 * SI('m2')
    
    assert m1 == m2 == m3 == m4
    

def test_parsing():
    assert SI.parse_name('km') == ('k', 'm')
    assert SI.parse_name('C') == ('', 'C')
    assert SI.parse_name('GC') == ('G', 'C')
    assert SI.parse_name('m') == ('', 'm')
    assert SI.parse_name('mm') == ('m', 'm')
    assert SI.parse_name('degC') == ('', 'degC')
    assert SI.parse_name('MdegC') == ('M', 'degC')
    assert SI.parse_name('dm') == ('d', 'm')
    
    with pytest.raises(ValueError):
        SI.parse_name('o')
    
    with pytest.raises(ValueError):
        SI.parse_name('ko')
        
    with pytest.raises(ValueError):
        SI.parse_name('oo')
        
    meter = SI.units['m']()
    milimeter = meter.with_prefix('m')
    
    assert SI.parse_expr('m') == meter.as_quantity()
    assert SI.parse_expr('mm') == milimeter.as_quantity()
    assert SI.parse_expr('m2') == SI.parse_expr('m^2') == meter.as_quantity() ** 2
    assert SI.parse_expr('mm2') == SI.parse_expr('mm^2') == milimeter.as_quantity() ** 2
    assert SI.parse_expr('mm500') == SI.parse_expr('mm^500') == milimeter.as_quantity() ** 500
    
    kg = SI.units['kg']()
    
    assert SI.parse_expr('m.kg') == meter.as_quantity() * kg.as_quantity()
    assert SI.parse_expr('m2.kg') == (meter.as_quantity() ** 2) * kg.as_quantity()
    
    

def test_arithmatic():
    meter = 1 * SI.m
    twometer = 2e9 * SI.nm
    coloumb = 3 * SI.C
    
    assert meter + meter == 2 * SI.m
    assert twometer * twometer == SI('4e18 nm2')
    
    assert meter != twometer
    assert twometer > meter
    assert twometer >= meter
    
    assert not twometer > twometer
    assert twometer >= twometer
    
    assert meter < twometer
    assert meter <= twometer
    
    assert not meter < meter
    assert meter <= meter
    
    with pytest.raises(ValueError):    
        twometer + meter
    
    with pytest.raises(ValueError):
        twometer + coloumb
        
    
def test_conversions():
    F = SI('15 kN')
    assert F.to_base() == SI('15000 kg.m.s-2')
    assert F.no_prefix() == SI('15000 N')
    
    W = F * 10 * SI.m
    
    assert W.to('kJ') == SI('150 kJ')
    
    with pytest.raises(ValueError):
        F.to('J')
        
    v = 15 * SI.m / SI.s
    
    assert v.swap('m', 'km') == SI('0.015 km.s-1')
    assert v.to('m.h-1') == 15 * 3600 * SI('m.h-1')
    
    

    