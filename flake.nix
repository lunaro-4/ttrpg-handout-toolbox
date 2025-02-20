{
  description = "A flake to work on python project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-24.11";
  };

  outputs = { self, nixpkgs }: 

  let

    system = "x86_64-linux";
	pkgs = import nixpkgs {
	inherit system;
	};
	
	in
	{
		devShells.${system}.default = pkgs.mkShell {
			
			packages = [(pkgs.python3.withPackages(pypkgs: with pypkgs;[

			html2image
			beautifulsoup4
			pillow
			icecream
			requests
			types-beautifulsoup4
			types-requests
			]))

			];
		
		
			buildInputs = with pkgs; [
				pyright
				# wkhtmltopdf
				# libstdcxx5
				chromium
				vscode-langservers-extracted
				mypy
				ruff


			];
# 			multiPkgs = with pkgs; [
# # libstdcxx5
# 				gcc
# 					libgcc
# 					extra-cmake-modules
# 					stdenv.cc.cc.lib
# 			];
			# LIBRARY_PATH= "/usr/lib:/usr/lib64/:$LIBRARY_PATH";
			# LD_LIBRARY_PATH= "${pkgs.gcc.cc.lib}/lib:$LD_LIBRARY_PATH";
			# shellHook = ''
			# # source .venv/bin/activate
			# #zsh
			# '';
  };
};
}
