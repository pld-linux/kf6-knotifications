#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.18
%define		qtver		5.15.2
%define		kfname		knotifications

Summary:	Desktop notifications
Name:		kf6-%{kfname}
Version:	6.18.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	6db938bbcf34ebc7614383396d9622ef
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6TextToSpeech-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kconfig-devel >= %{version}
BuildRequires:	kf6-kcoreaddons-devel >= %{version}
BuildRequires:	kf6-kwindowsystem-devel >= %{version}
BuildRequires:	libcanberra-devel
# TODO
#BuildRequires:	libdbusmenu-qt6-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6TextToSpeech >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	kf6-dirs
Requires:	kf6-kconfig >= %{version}
Requires:	kf6-kcoreaddons >= %{version}
Requires:	kf6-kwindowsystem >= %{version}
#Obsoletes:	kf5-%{kfname} < %{version}
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KNotification is used to notify the user of an event. It covers
feedback and persistent events.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6DBus-devel >= %{qtver}
Requires:	Qt6Widgets-devel >= %{qtver}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DBUILD_PYTHON_BINDINGS=OFF \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6_qt.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6Notifications.so.6
%attr(755,root,root) %{_libdir}/libKF6Notifications.so.*.*
%dir %{_libdir}/qt6/qml/org/kde/notification
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/notification/libknotificationqmlplugin.so
%{_libdir}/qt6/qml/org/kde/notification/qmldir
%{_libdir}/qt6/qml/org/kde/notification/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/notification/knotificationqmlplugin.qmltypes
%{_datadir}/qlogging-categories6/knotifications.categories
%{_datadir}/qlogging-categories6/knotifications.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KNotifications
%{_libdir}/cmake/KF6Notifications
%{_libdir}/libKF6Notifications.so
