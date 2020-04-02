let
  pkgs = import <carga-nixpkgs> {};

  django-qr-code = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-qr-code-${version}";
    version = "0.3.3";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/1d/26/f7505b4accaacb00b33716163f488bed9b5a83eacaa4f92cb3e56e359ffc/django-qr-code-0.3.3.tar.gz";
      sha512 = "1b4yygj1pvdnw9sml7k6nvz2y04b5dir5bi596lab5qipg7d5v655p7fgc21rvzwi0prhzznl93hllija5bxwzy5jpf062q9ishy9sf";
    };
    propagatedBuildInputs = [ qrcode pillow ];
    buildInputs = [ django_1_11 ];
    doCheck = false;  	
  };

  django-crispy-forms = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-crispy-forms-${version}";
    version = "1.7.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/fb/70/99ad5d04120859368de27dcc306a387bd4d8263d82a6e6a7174c2df247d0/django-crispy-forms-1.7.0.tar.gz";
      sha512 = "09fm54h13xwdlhz0rl3a50jj84bifxcx38bf26cad43dx7l4pc1dnl4v9kfmxylkk04yzr1q4gpx8aqn1cyb0js9a26jm409i1dcj07";
    };
    buildInputs = [ django_1_11 ];
    doCheck = false;  	
  };

  django-constance = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-constance-${version}";
    version = "2.1.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/a5/e1/9a2442f108a1a9f01aeef49b62cf62473d8f03b6b8536866e0c7f7868728/django-constance-2.1.0.tar.gz";
      sha512 = "15n1m7q4mmbvmd645hn59qsa4is62pdzkn0myc1nxnr6j5vbgp28di180cqbxbk2nmfyjk9ks255znca2bb8v42y87q3yjmw6rlzdd6";
    };
    buildInputs = [ django_1_11 ];
    doCheck = false;  	
  };

  python-crontab = with pkgs.python3Packages; buildPythonPackage rec {
    name = "python-crontab-${version}";
    version = "2.1.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/43/bd/3bfb19dd7c01d1a68894512be8e9a3f5924c6e5f9f2e931ef68270bfa81b/python-crontab-2.1.1.tar.gz";
      sha512 = "3wwj9f7d73ia1s6i4znkarvgr6mxp04y0sald9vj2ndcf3q54fnzm12a9kqgm97a6d5nj6dq70r6i8zljfmdv4d22f39n13ddy00fyk";
    };
    propagatedBuildInputs = [ dateutil ];
    doCheck = false;
  };

  django-kronos = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-kronos-${version}";
    version = "1.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/4e/90/15b99070666da99c3904c0ad7b66b263a7fd678cf0c2764810435ab18ed6/django-kronos-1.0.tar.gz";
      sha512 = "31x1ymxpbrxk6q6aa4zf5gnq1m7zakh6gxf1h7jhqcdkqd9iyxzb1gkfn1rw6xf9jk6lb90q84xq3f9a5j0rk1pchwxa92mnvq56ivm";
    };
    buildInputs = [ django_1_11 ];
    propagatedBuildInputs = [ python-crontab ];
    doCheck = false;
  };

  django-markdown2 = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-markdown2-${version}";
    version = "0.3.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/de/98/1c0c18dda0993af0bde44914aa00e025126fba54f1dd72fd4cb84043b4a8/django-markdown2-0.3.0.tar.gz";
      sha512 = "1fsg4wi059515qca28bww9s4jvddpyr2c92h2cnaq7sy1snpm7za7lbazg7826a16vwky9rf9ysyidw9m5nhjqr6dnbbpfr0ncrlvcd";
    };
    propagatedBuildInputs = [ markdown2 ];
    doCheck = false;
  };

  django-easy-select2 = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-easy-select2-${version}";
    version = "1.3.4";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/23/e5/8cd4a721bcb7a205dd0eab09305bd3ad39d4dca33d1cb7498f876c15fa58/django-easy-select2-1.3.4.tar.gz";
      sha512 = "2023sq3jp6jwyyqprgry1bwb9ybkdnlgbw1awpp7a5n06w816qlznh0xc2qf79l409sl5ga0mdh75b1dngkr4nmzx9xc1kvc60nb218";
    };
    doCheck = false;
  };

  xlsxwriter = with pkgs.python3Packages; buildPythonPackage rec {
    name = "xlsxwriter-${version}";
    version = "0.8.8";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/2a/de/4ee20ac103417662865e0e3acde859b002c13f52af0d50a2664d3eca5897/XlsxWriter-0.8.9.tar.gz";
      sha512 = "3qr0pvxf8w7q2pjqy96mh4hg0y9j5p1wbbx1cs2pdgixgnyg5xnb5zxz79aa38x2a1lwr8hzsb7zhbgxpac85s7nww5ifgnqnhsdz85";
    };
    doCheck = false;
  };

  lepl = with pkgs.python3Packages; buildPythonPackage rec {
    name = "lepl-${version}";
    version = "5.1.3";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/source/L/LEPL/LEPL-5.1.3.tar.gz";
      sha512 = "1myk8h3br5rxzgsyvqvrx61myfanj7cwdiixmmpjk5gbi38klpqzdzhnq6qmx70xfx34cilgv2vf7xkq6z4yxjv06sbr11c32938ysf";
    };
    doCheck = false;
  };

  raven = with pkgs.python3Packages; buildPythonPackage rec {
    name = "raven-${version}";
    version = "5.26.0";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/5f/55/1367ac2941dbc33a3c92a96ea56be3b25a7a4cde8f8060df91654528e602/raven-5.26.0.tar.gz";
      sha512 = "1pnlxbidyp4xy1c3svd281577l49hbf7ybfr2gb867k76hdpcy9kv28829dg6a1vi4nkd15vhdhhyq62wn9klkhk7sxnr2qfxkm98v8";
    };
    doCheck = false;
  };

  petl = with pkgs.python3Packages; buildPythonPackage rec {
    name = "petl-${version}";
    version = "1.1.1";
    src = pkgs.fetchFromGitHub {
    	owner = "alimanfoo";
	repo = "petl";
	rev = "fa8aabe78696957744300fd333e4e7bc48e20893";
	sha512 = "3jdr7kfq14mybn7q0aj5ijv5m3px5467bpnvz4hb5mhc0cyli0wx4rc3v3wq8njb9csnsc637hy1xwn7wj4la0789mdcskiddldb53c";
    };

    doCheck = false;
  };

  django-extensions = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-extensions-${version}";
    version = "1.7.4";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/1a/1a/ec5bb3673ac4945a4c7dd7973ca4b60b4ecdc962df67799666168e1567c5/django-extensions-1.7.4.tar.gz";
      sha512 = "1vywll8dl6a7v382nd27rm89x7yf47aa8hpp5w70j0awvb830brzcc8mh8z30lsm5sjvw06f8wx6lgq8zxyr3s5c7pjw6iy6jkfzmyh";
    };
    propagatedBuildInputs = [ six ];
    doCheck = false;
  };

  django-imagekit = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-imagekit-${version}";
    version = "3.3";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/4d/31/a5c11fbdc4b28932ba838f135671d468e4ea227d84ba2e70b01b0aacd9f4/django-imagekit-3.3.tar.gz";
      sha512 = "1gvkkj58gmsdwxhc1v43d4ablij2zl2frxpgaqwhn7x9f25dlgg3r4nf529parac3gh72gyvzw58yw5lcdxzv2snzaa455kfrja1jdf";
    };
    propagatedBuildInputs = [ django_appconf pillow pilkit ];
    doCheck = false;
  };

  django-widget-tweaks = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-widget-tweaks-${version}";
    version = "1.4.1";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/f9/bb/ba988f76bdb0e2760fb6667305565df6ae0697efee3df54cac829a66d248/django-widget-tweaks-1.4.1.tar.gz";
      sha512 = "12sdyzgjsc8c61hzmwrgz1rkjwk2pdkj3b586fv4hx75g1858fsr86vbkkgr19b3370qsdv7f9jw94bkm19idk0wl3mwda4zgc8m7k9";
    };
    doCheck = false;
  };

  django-localflavor = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-localflavor-${version}";
    version = "1.2";
    src = pkgs.fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-localflavor/django-localflavor-1.2.tar.gz";
      sha512 = "0s30216piy1nxrarqfrws64wrxq7ki35q38fcrm6jcrykn3hkclacjdn3mccjikn3dchwzwqdyay8i1bfsli06qlm4vq3b6lbz3yxy2";
    };
    doCheck = false;
  };

  django-simple-history = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-simple-history-${version}";
    version = "1.8.0";
    src = pkgs.fetchurl {
    	url = "https://pypi.python.org/packages/b4/56/25e1505fd0215ad3f365456f2fef12badc70c18d2eb756b2a7776d8264ab/django-simple-history-1.9.0.tar.gz";
	sha512 = "1kn406cl6xii8hch8xqp5301n118bqfq8d94jmp9mk0hvmzr7kvwg60g9c6qzh2wik8wsz2bb4a9rjz530i38xrnw6ig0cd3c6mpbs9";
    };
    doCheck = false;
  };

  model_mommy = with pkgs.python3Packages; buildPythonPackage rec {
    name = "model_mommy-${version}";
    version = "1.2.6";
    src = pkgs.fetchurl {
    	url = "https://pypi.python.org/packages/source/m/model_mommy/model_mommy-1.2.6.tar.gz";
	sha512 = "2qhjjq889a36x3nb582hv85xdy3w31f1f3a17zd6pcd4jb0qxsq64cpj0aqfw88289lr8mjhsm64in2lllqsfyqbnna68nx8rxyz94n";
    };
    buildInputs = [ django_1_11 ];
    propagatedBuildInputs = [ six ];
    doCheck = false;
  };

  django-wkhtmltopdf = with pkgs.python3Packages; buildPythonPackage rec {
    name = "django-wkhtmltopdf-${version}";
    version = "3.1.0";
    src = pkgs.fetchurl {
    	url = "https://pypi.python.org/packages/04/a7/2dbf0233a234d343cf6e37a7ef5e2757203315a4ddbf9ef06f3616bdca08/django-wkhtmltopdf-3.1.0.tar.gz";
	sha512 = "1v40qwsk5vp7i2mzir5w30fy79wpyglz024v0z8yanksbxkgi53lfgyh874lrqdgj2xjq70ahihn45xq38q93ssi07rcqp12qsclknd";
    };
    propagatedBuildInputs = [ pkgs.wkhtmltopdf ];
    doCheck = false;
  };

in
{ stdenv ? pkgs.stdenv }:

pkgs.python3Packages.buildPythonApplication {
  name = "carga";
  namePrefix = "";
  version = "0.0.1";
  src = if pkgs.lib.inNixShell then null else ./.;
  strictDeps = false;
  buildInputs = with pkgs; [ gettext ];
  propagatedBuildInputs = with pkgs;
   [
    python3
    python3Packages.django_1_11
    python3Packages.psycopg2
    python3Packages.pytz
    python3Packages.python_magic
    python3Packages.waitress
    python3Packages.requests
    python3Packages.redis
    python3Packages.unidecode
    django-qr-code
    django-crispy-forms
    django-constance
    django-kronos
    django-easy-select2
    django-imagekit
    django-wkhtmltopdf
    django-localflavor
    django-widget-tweaks
    django-simple-history
    django-extensions
    django-markdown2
    raven
    model_mommy
    petl
    python3Packages.openpyxl
    lepl
    xlsxwriter
    postgresql ];

  shellHook = ''
    touch .make.nix-shell.$PPID
    make db_start
    trap 'make db_stop && rm .make.nix-shell.$PPID' EXIT
  '';
  doCheck = false;
  LANG = "en_US.UTF-8";
  LOCALE_ARCHIVE = "${pkgs.glibcLocales}/lib/locale/locale-archive";
  LC_ALL = "en_US.UTF-8";
}
