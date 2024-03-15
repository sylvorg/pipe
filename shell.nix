with import <nixpkgs> { };
with lib;
let
  pipe =
    { buildPythonPackage, beartype, more-itertools, poetry-core, pytest, rich }:
    buildPythonPackage rec {
      pname = "pipe";
      version = "1.0.0.0";
      src = ./.;
      format = "pyproject";
      nativeBuildInputs = toList poetry-core;
      propagatedNativeBuildInputs = [ beartype more-itertools pytest rich ];
    };
in mkShell { buildInputs = toList (python311Packages.callPackage pipe { }); }
