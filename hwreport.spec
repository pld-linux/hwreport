Summary:	Collect system informations for the hardware4linux site
Summary(pl.UTF-8):	Zbieranie informacji dla strony hardware4linux
Name:		hwreport
Version:	0.11.0
Release:	2
License:	GPL v2
Group:		Applications/System
Source0:	http://hardware4linux.info/res/%{name}-%{version}.tar.bz2
# Source0-md5:	463109a35076dfe946ab115cd5422e6d
URL:		http://hardware4linux.info/
BuildRequires:	libusb
BuildRequires:	pkgconfig
Requires:	dmidecode
Requires:	pld-release
Requires:	pciutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hwreport uses a script hwreport and scan-printers to find out the
hardware in your PC and confront it with a compatibility list on
<http://hardware4linux.info/>.

It works both ways - you can get information about the drivers and
compatibility of your hardware from the site and submit new entries to
the hardware4linux site.

%description -l pl.UTF-8
Hwreport używa skryptu hwreport i programu scan-printers do
rozpoznawania sprzętu w komputerze i porównywania go z listą
kompatybilności na stronie <http://hardware4linux.info/>.

Działa to w obie strony - można pobierać informacje na temat
sterowników i kompatybilności sprzętu ze strony lub wysyłać nowe wpisy
na stronę hardware4linux.

%prep
%setup -q
cat > Makefile <<'EOF'
TARGET = scan-printers reportusb
INSTALL = %{_bindir}/install -c
BINARIES = hwreport osinfo
sbindir = %{_sbindir}
all: Makefile $(TARGET)
scan-printers: scan-printers.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

reportusb: reportusb.c
	$(CC) $(CFLAGS) `pkg-config --cflags libusb-1.0` $(LDFLAGS) `pkg-config --libs libusb-1.0` -o $@ $^

clean:
	rm -f $(OBJECTS) $(TARGET)

install:
	$(INSTALL) $(TARGET) $(DESTDIR)/$(sbindir)
	$(INSTALL) $(BINARIES) $(DESTDIR)/$(sbindir)
EOF

%build
%{__make} \
	CC="%{__cc}" \
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
