with import <nixpkgs> { };
with lib;
let
  pipe = { buildPythonPackage, beartype, fetchFromGitHub, more-itertools
    , poetry-core, pytest, rich }:
    buildPythonPackage rec {
      pname = "pipe";
      version = "1.0.0.0";
      src = ./.;
      format = "pyproject";
      nativeBuildInputs = toList poetry-core;
      propagatedNativeBuildInputs = [
        (beartype.overrideAttrs (old: {
          src = fetchFromGitHub {
            owner = "beartype";
            repo = "beartype";
            rev = "a342229ded98ac10d410ce9101a0941f685704d5";
            sha256 = "sha256-mVSQIw4aZQa807eYAnUIpMrOPiuDLYzspY05pYJaw7s=";
          };
        }))
        more-itertools
        pytest
        rich
      ];
    };
in mkShell { buildInputs = toList (python312Packages.callPackage pipe { }); }
