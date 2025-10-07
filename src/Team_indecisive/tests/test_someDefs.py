import pytest

from someDefs import *

def test_isSumEven():
    assert isSumEven(0,0,0) == True
    assert isSumEven(1,0,0) == False
    assert isSumEven(0,1,0) == False
    assert isSumEven(0,0,1) == False
    assert isSumEven(3,0,7) == True
    assert isSumEven(0,4,6) == True
    assert isSumEven(6,0,8) == True
    assert isSumEven(12,13,14) == False

def test_isSameParity():
    assert isSameParity(0,0,0) == True
    assert isSameParity(1,0,0) == False
    assert isSameParity(1,3,7) == True
    assert isSameParity(2,8,6) == True
    assert isSameParity(12,13,14) == False
    assert isSameParity(-4,3,7) == False

def test_isSumDivisibleByFour():
    assert isSumDivisibleByFour(0,0,0) == True
    assert isSumDivisibleByFour(0,0,1) == False
    assert isSumDivisibleByFour(0,1,0) == False
    assert isSumDivisibleByFour(1,0,0) == False
    assert isSumDivisibleByFour(1,3,8) == True
    assert isSumDivisibleByFour(1,12,1) == False
    assert isSumDivisibleByFour(1,12,3) == True
    assert isSumDivisibleByFour(-100,100,16) == True

def test_Auswahlregel_Silizium():
    assert Auswahlregel_Silizium(0,0,0) == True
    assert Auswahlregel_Silizium(1,3,8) == False
    assert Auswahlregel_Silizium(4,8,16) == True
    assert Auswahlregel_Silizium(-100,100,16) == True



