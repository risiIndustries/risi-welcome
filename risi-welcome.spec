Name:           risi-welcome
Version:        0.1
Release:        13%{?dist}
Summary:        risiOS's Welcome app.

License:        GPL v3
URL:            https://github.com/risiOS/risi-welcome
Source0:        https://github.com/risiOS/risi-welcome/archive/refs/heads/main.tar.gz

BuildArch:	noarch

BuildRequires:  python
Requires:       python
Requires:	python3-gobject, python3-yaml
Requires:	risi-script, risi-script-gtk

%description
This welcome program will help guide you through the
available resources for risiOS as well as help you setup 
your computer to your likings.

%prep
%autosetup -n %{name}-main

%build
%install

mkdir -p %{buildroot}%{_bindir}
cp -a usr/share %{buildroot}%{_datadir}

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart/

cp io.risi.Welcome.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/io.risi.Welcome.svg
cp usr/share/applications/io.risi.Welcome.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/
install -m 755 __main__.py %{buildroot}%{_bindir}/risi-welcome

%files
# %license add-license-file-here
# %doc add-docs-here
%{_datadir}/risiWelcome
%{_datadir}/glib-2.0/schemas/io.risi.Welcome.gschema.xml
%{_datadir}/applications/io.risi.Welcome.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.risi.Welcome.svg
%{_bindir}/%{name}
%{_sysconfdir}/xdg/autostart/io.risi.Welcome.desktop

%changelog
* Tue Mar 1 2022 PizzaLovingNerd
- First spec file

