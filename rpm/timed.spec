# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.26
# 

Name:       timed

# >> macros
# << macros

Summary:    Time daemon
Version:    2.59
Release:    1
Group:      System/System Control
License:    LGPLv2
URL:        https://github.com/nemomobile/timed
Source0:    %{name}-%{version}.tar.bz2
Source100:  timed.yaml
Requires:   tzdata
Requires:   tzdata-timed
Requires:   systemd
Requires(preun): systemd
Requires(post): /sbin/ldconfig
Requires(post): systemd
Requires(postun): /sbin/ldconfig
Requires(postun): systemd
BuildRequires:  pkgconfig(contextprovider-1.0)
BuildRequires:  pkgconfig(libpcrecpp)
BuildRequires:  pkgconfig(QtCore) >= 4.7
BuildRequires:  pkgconfig(dsme_dbus_if)
BuildRequires:  libiodata-devel >= 0.19
BuildRequires:  libxslt

%description
The time daemon (%{name}) managing system time, time zone and settings,
executing actions at given time and managing the event queue.


%package tests
Summary:    Test cases for %{name}
Group:      Development/System
Requires:   %{name} = %{version}-%{release}
Requires:   testrunner-lite

%description tests
Simple automated test cases, to be executed in cita.

%package tools
Summary:    Command line tools for communication with the time daemon
Group:      Development/Tools
Requires:   %{name} = %{version}-%{release}

%description tools
Command line timed tools: 'simple-client' - a command line
simple client for time daemon; 'fake-dialog-ui' - a command
line voland implementation; 'ticker' - a command line clock
and signal notification; timedclient - add, modify, remove,
and query alarms.


%package devel
Summary:    Development package for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   pkgconfig(QtCore) >= 4.6

%description devel
Header files and shared lib symlink for %{name}.

%prep
%setup -q -n %{name}-%{version}

# >> setup
# << setup

%build
# >> build pre
export TIMED_VERSION=%{version}
mkdir -p src/h/timed
ln -sf ../../lib/qmacro.h src/h/timed
# << build pre

%qmake  \
    -recursive "CONFIG += MEEGO dsme_dbus_if"

make %{?jobs:-j%jobs}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%qmake_install

# >> install post
#install -m 644 -D src/doc/timed.8 %{buildroot}/%{_mandir}/man8/timed.8
#install -m 644 -D src/doc/libtimed.3 %{buildroot}/%{_mandir}/man3/libtimed.3
#install -m 644 src/doc/libtimed-voland.3 %{buildroot}/%{_mandir}/man3/libtimed-voland.3

install -d %{buildroot}/%{_localstatedir}/cache/%{name}/aegis/

# The file %{buildroot}/lib/systemd/system/%{name}.service is installed by make install
install -d %{buildroot}/lib/systemd/system/multi-user.target.wants/
ln -s ../%{name}.service %{buildroot}/lib/systemd/system/multi-user.target.wants/%{name}.service

# Missing executable flags.
chmod 755 %{buildroot}%{_datadir}/backup-framework/scripts/timed-restore-script.sh
# << install post

%preun
if [ "$1" -eq 0 ]; then
systemctl stop %{name}.service
fi

%post
/sbin/ldconfig
systemctl daemon-reload
systemctl reload-or-try-restart %{name}.service

%postun
/sbin/ldconfig
systemctl daemon-reload

%files
%defattr(-,root,root,-)
# >> files
%doc COPYING debian/changelog debian/copyright
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/aegisfs.d/timed.aegisfs.conf
%config(noreplace) %{_sysconfdir}/timed.rc
%{_sysconfdir}/osso-cud-scripts/timed-clear-device.sh
%{_sysconfdir}/osso-rfs-scripts/timed-restore-original-settings.sh
%{_bindir}/%{name}
%{_bindir}/timed-aegis-session-helper
%{_libdir}/libtimed.so.*
%{_libdir}/libtimed-voland.so.*
%{_datadir}/backup-framework/applications/timedbackup.conf
%{_datadir}/backup-framework/scripts/timed-backup-script.sh
%{_datadir}/backup-framework/scripts/timed-restore-script.sh
%{_datadir}/contextkit/providers/com.nokia.time.context
# %{_mandir}/man3/libtimed.3.gz
# %{_mandir}/man3/libtimed-voland.3.gz
# %{_mandir}/man8/timed.8.gz
%{_localstatedir}/cache/timed/
/lib/systemd/system/%{name}.service
/lib/systemd/system/multi-user.target.wants/%{name}.service
# << files

%files tests
%defattr(-,root,root,-)
# >> files tests
%doc COPYING
/opt/tests/%{name}-tests
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.fakeofono.conf
# << files tests

%files tools
%defattr(-,root,root,-)
# >> files tools
%doc COPYING
%{_bindir}/timedclient
# << files tools

%files devel
%defattr(-,root,root,-)
# >> files devel
%doc COPYING
%{_includedir}/%{name}/*
%{_includedir}/timed-voland/*
%{_libdir}/libtimed.so
%{_libdir}/libtimed-voland.so
%{_libdir}/pkgconfig/timed.pc
%{_libdir}/pkgconfig/timed-voland.pc
%{_datadir}/qt4/mkspecs/features/timed.prf
%{_datadir}/qt4/mkspecs/features/timed-voland.prf
# << files devel
