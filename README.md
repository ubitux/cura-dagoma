Mainlining CuraByDagoma to the Cura Project
===========================================

- **Dagoma**: https://dagoma.fr/
- **Cura**:   https://github.com/Ultimaker/Cura (and other related repositories)

Dagoma Github repository
------------------------

https://github.com/dagomafr/Cura_by_dagoma is outdated:

- **latest commit**: `7e6d558` on Nov 26, 2014
- **forked from**: https://github.com/daid/LegacyCura/
- **fork point found at**: `b0802486 Version 14.07.1-RC1` (no tag or release)

CuraByDagoma website releases
-----------------------------

- **website**: https://dist.dagoma.fr/betagoma
- **product**: `CuraByDagoma`
- **os**: `Windows` (no `Linux` available)
- **build date**: `2016/11/29-14h58` (`1480427910`), last and only
- **download URL**: `https://dist.dagoma.fr/get/zip/CuraByDagoma/<build-date>/<hash>`

Files:

- `CuraByDagoma_D200_New_1480427910_10253135e366b7d3aa85469384fba301.zip` (en)
- `CuraByDagoma_D200_New_1480427910_aa387aa8e9c16d8e25f8663ec5fb2058.zip` (fr)
- `CuraByDagoma_D200_Old_1480427910_ca922ef7c327ebe478c93cb04ca66d99.zip`
- `CuraByDagoma_E200_1480427910_476b6c21e6aefb2c66077fd6168d88d6.zip` (fr)
- `CuraByDagoma_E200_1480427910_d0965d25707767ef87c626dfbaaab4c9.zip` (en)

Observations
------------

- `D200_Old`: unaltered original Discovery
- `D200_New`: Discovery modified
- `E200`:     DiscoEasy

```
    [~/.wine/drive_c/Program Files (x86)]☭ find -iname 'Disco*.stl' -exec md5sum {} \;
    3791c5530b68f6418b061f7261fc5b35  ./CuraByDagoma_E200_1480427910_476b6c21e6aefb2c66077fd6168d88d6/resources/meshes/Discovery_platform.stl
    3791c5530b68f6418b061f7261fc5b35  ./CuraByDagoma_E200_1480427910_d0965d25707767ef87c626dfbaaab4c9/resources/meshes/Discovery_platform.stl
    3791c5530b68f6418b061f7261fc5b35  ./CuraByDagoma_D200_New_1480427910_10253135e366b7d3aa85469384fba301/resources/meshes/Discovery_platform.stl
    0317ada639e281a784b74e9eeaace200  ./CuraByDagoma_D200_Old_1480427910_ca922ef7c327ebe478c93cb04ca66d99/resources/meshes/Discovery_platform.stl
    3791c5530b68f6418b061f7261fc5b35  ./CuraByDagoma_D200_New_1480427910_aa387aa8e9c16d8e25f8663ec5fb2058/resources/meshes/Discovery_platform.stl
```

```
    [~/.wine/drive_c/Program Files (x86)]☭ find -iname 'xml_config.xml' -exec md5sum {} \;
    8407bf33c391eb83bfd000758001ca51  ./CuraByDagoma_E200_1480427910_476b6c21e6aefb2c66077fd6168d88d6/resources/XML/xml_config.xml
    3b71e9cc9681c40e82408172d4ab7b91  ./CuraByDagoma_E200_1480427910_d0965d25707767ef87c626dfbaaab4c9/resources/XML/xml_config.xml
    3b71e9cc9681c40e82408172d4ab7b91  ./CuraByDagoma_D200_New_1480427910_10253135e366b7d3aa85469384fba301/resources/XML/xml_config.xml
    fefb7c7772f0901681c03815a40879e1  ./CuraByDagoma_D200_Old_1480427910_ca922ef7c327ebe478c93cb04ca66d99/resources/XML/xml_config.xml
    8407bf33c391eb83bfd000758001ca51  ./CuraByDagoma_D200_New_1480427910_aa387aa8e9c16d8e25f8663ec5fb2058/resources/XML/xml_config.xml
```

`D200_New` are actually the same as `E200`: DiscoEasy is a modified Discovery (same XML config + same `.stl` model)

Usage
-----

```
    % make O=out
```

Generated files can be found in the `out` directory

Progress
--------

- materials extracted and upstreamed: https://github.com/Ultimaker/fdm_materials/pull/5

Dependencies
------------

- `make`
- `python3`
- `admesh`
