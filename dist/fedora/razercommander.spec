%global appid org.gabmus.razercommander

Name:    razerCommander
Version: 1.2.0
Release: 1%{dist}
Summary: Razer device manager for Linux
License: GPLv3+
URL:     https://github.com/GabMus/razerCommander
Source0: %{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires: python3-devel >= 3.4
BuildRequires: meson >= 0.40.0
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: libappstream-glib
# BuildRequires: gettext
Requires: python3-gobject
Requires: gtk3 >= 3.14
# Requires: libsoup

%description
Razer device manager for Linux

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
#%find_lang trg

%check
/usr/bin/appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

# -f trg.lang
%files
%license COPYING
%doc README.md
%{_bindir}/razercommander
%dir %{python3_sitelib}/razercommander
%{python3_sitelib}/razercommander/
%{_datadir}/razercommander/%{appid}.gresource
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/dbus-1/services/%{appid}.service
%{_datadir}/appdata/%{appid}.appdata.xml
%{_datadir}/glib-2.0/schemas/%{appid}.gschema.xml
%{_datadir}/icons/hicolor/**/apps/%{appid}*.svg
