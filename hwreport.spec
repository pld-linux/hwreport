#
# TODO:
# - checkup, bump to 1.0 and build
#
Summary:	Collect system informations for the hardware4linux site
Summary(pl.UTF-8):	Zbiera informacje dla strony hardware4linux
Name:		hwreport
Version:	0.9
Release:	0.1
License:	GPL v2
Group:		Applications/System
Source0:	http://hardware4linux.info/res/%{name}-%{version}.tar.bz2
# Source0-md5:	47612077f8a00ddb8c9e6c1480c63f63
URL:		http://hardware4linux.info/
Requires:	dmidecode
Requires:	pciutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hwreport uses a script hwreport and scan-printers to find out the
hardware in your PC and confront it with a compatibility list on
http://hardware4linux.info.

It works both ways -- you can get information about the drivers and
compatibility of your hardware from the site and submit new entries to
the hardware4linux site.

%description -l pl.UTF-8
Hwreport używa skryptu hwreport i scan-printers do rozpoznawania
sprzętu w Twoim PC-ie i porównywanie go ze listą kompatybilności na
stronie http://hardware4linux.info.

To działa w obie strony -- możesz pobierać informację na temat
sterowników i kompatybilności Twojego sprzętu ze strony lub wysyłać
nowe wpisy do strony hardware4linux.

%prep
%setup -q
cat > Makefile <<'EOF'
TARGET = scan-printers
INSTALL = %{_bindir}/install -c
OBJECTS = scan-printers.o
BINARIES = osinfo hwreport
sbindir = %{_sbindir}
all: Makefile $(TARGET)
$(TARGET):  $(OBJECTS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $(TARGET) $(OBJECTS)

clean:
	rm -f $(OBJECTS) $(TARGET)

scan-printers.o: scan-printers.c

install:
	$(INSTALL) $(TARGET) $(DESTDIR)/$(sbindir)
	$(INSTALL) $(BINARIES) $(DESTDIR)/$(sbindir)
EOF

%build
%{__make} \
	CC="%{__cc}"
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d  $RPM_BUILD_ROOT%{_sbindir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/*
