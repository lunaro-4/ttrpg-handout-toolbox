{
  description = "A very basic flake";

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
			
		
			buildInputs = with pkgs; [
				python3
				pyright
				# wkhtmltopdf
				# libstdcxx5
				chromium
				vscode-langservers-extracted


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
			shellHook = ''
			source .venv/bin/activate
			#zsh
			'';
  };
};
}
