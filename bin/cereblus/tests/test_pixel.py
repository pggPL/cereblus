from bin.cereblus.stimulation import Stimulation

def test_pixel_1():
    s = Stimulation(2)
    s.loop = True
    p1 = s.get_pixel(0)
    p2 = s.get_pixel(0)

    # adding up to 0/5
    p1.add_phase(0.1, True)
    p1.add_phase(0.2, False)
    p1.add_phase(0.1, True)
    p1.add_phase(0.1, False)

    assert p1.get(0.05)
    assert not p1.get(0.15)
    assert not p1.get(0.25)
    assert p1.get(0.35)
    assert not p1.get(0.45)


    assert p1.get(10000000.05)
    assert not p1.get(1000000.15)
    assert not p1.get(10000000.25)
    assert p1.get(100000.35)
    assert not p1.get(10000000.45)