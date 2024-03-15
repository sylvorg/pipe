with import <nixpkgs> { };
let
  pipe =
    { buildPythonPackage, beartype, more-itertools, poetry-core, pytest, rich }:
    buildPythonPackage rec {
      pname = "pipe";
      version = "1.0.0.0";
      src = ./.;
      format = "pyproject";
      nativeBuildInputs = [ poetry-core ];
      propagatedNativeBuildInputs = [ beartype more-itertools pytest rich ];
    };
in mkShell {
  buildInputs = [ (python311Packages.callPackage pipe { }) fish ];
  shellHook = "exec fish";
}
