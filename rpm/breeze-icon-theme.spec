## allow building with an older extra-cmake-modules
%global kf5_version 5.33.0

%global framework breeze-icons

Name:    breeze-icon-theme
Summary: Breeze icon theme
Version: 5.104.0
Release: 1%{?dist}

# http://techbase.kde.org/Policies/Licensing_Policy
License: LGPLv3+
URL:     https://api.kde.org/frameworks-api/frameworks-apidocs/frameworks/breeze-icons/html/
Source0: %{name}-%{version}.tar.bz2

## upstream patches (lookaside cache)

## upstreamable patches

# must come *after* patches or %%autosetup sometimes doesn't work right -- rex
BuildArch: noarch

BuildRequires: opt-extra-cmake-modules
BuildRequires: opt-kf5-rpm-macros
BuildRequires: opt-qt5-qtbase-devel

# icon optimizations
BuildRequires: util-linux
# for generate-24px-versions.py
BuildRequires: python3-lxml

# upstream name
Provides:       breeze-icons = %{version}-%{release}
Provides:       kf5-breeze-icons = %{version}-%{release}

%description
%{summary}.

%package rcc
Summary: breeze Qt resource files
Requires: %{name} = %{version}-%{release}
%description rcc
%{summary}.



%prep
%autosetup -n %{name}-%{version}/upstream -p1

%if 0%{?kf5_version:1}
sed -i -e "s|%{version}|%{kf5_version}|g" CMakeLists.txt
%endif


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

mkdir -p build
pushd build

%_opt_cmake_kf5 ../ \
		-DCMAKE_INSTALL_PREFIX:PATH=/usr
%make_build

popd

%install
pushd build
make DESTDIR=%{buildroot} install
popd

## icon optimizations
du -s .
hardlink -c -v %{buildroot}%{_datadir}/icons/
du -s .

%files
%license COPYING-ICONS
%doc README.md
%ghost %{_datadir}/icons/breeze/icon-theme.cache
%ghost %{_datadir}/icons/breeze-dark/icon-theme.cache
%{_datadir}/icons/breeze/
%{_datadir}/icons/breeze-dark/
%exclude %{_datadir}/icons/breeze/breeze-icons.rcc
%exclude %{_datadir}/icons/breeze-dark/breeze-icons-dark.rcc

%files rcc
%{_datadir}/icons/breeze/breeze-icons.rcc
%{_datadir}/icons/breeze-dark/breeze-icons-dark.rcc
