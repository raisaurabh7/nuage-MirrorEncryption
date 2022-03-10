import main


def test_mirror_encryption():
    obj = main.MirrorEncryption()
    test1 = obj.get_mirror("ABC")
    test2 = obj.get_mirror("abc")
    test3 = obj.get_mirror("ABC1234XYZ")
    test4 = obj.get_mirror("gygyuGyYfyy435##453gfc")
    test5 = obj.get_mirror("^%^%4%$554644354753443#$%#$%%&")
    assert test1 == "ZYX"
    assert test2 == "zyx"
    assert test3 == "ZYX1234CBA"
    assert test4 == "tbtbfTbBubb435##453tux"
    assert test5 == "^%^%4%$554644354753443#$%#$%%&"


