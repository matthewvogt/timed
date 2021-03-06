QT -= gui
QT += dbus network

TEMPLATE = app

equals(QT_MAJOR_VERSION, 4): TARGET = timed
equals(QT_MAJOR_VERSION, 5): TARGET = timed-qt5

VERSION = $$(TIMED_VERSION)

INCLUDEPATH += ../h

QMAKE_LIBDIR_FLAGS += -L../lib -L../voland
equals(QT_MAJOR_VERSION, 4): LIBS += -ltimed -ltimed-voland
equals(QT_MAJOR_VERSION, 5): LIBS += -ltimed-qt5 -ltimed-voland-qt5

IODATA_TYPES = queue.type config.type settings.type customization.type tzdata.type

CONFIG(dsme_dbus_if) {
    SOURCES += dsme-mode.cpp
    HEADERS += dsme-mode.h interfaces.h
    DEFINES += HAVE_DSME
}

HEADERS += peer.h \
    settings.h \
    csd.h \
    adaptor.h \
    timed.h \
    state.h \
    cluster.h \
    machine.h \
    singleshot.h \
    pinguin.h \
    unix-signal.h \
    onitz.h \
    networktime.h \
    networktimewatcher.h \
    networkoperator.h \
    networkregistrationwatcher.h \
    networktimeinfo.h \
    ofonomodemmanager.h \
    modemwatcher.h \
    ofonoconstants.h

SOURCES += peer.cpp \
    tzdata.cpp \
    cellular.cpp \
    csd.cpp \
    cluster.cpp \
    machine.cpp \
    state.cpp \
    main.cpp \
    timed.cpp \
    timeutil.cpp \
    event.cpp \
    misc.cpp \
    settings.cpp \
    pinguin.cpp \
    unix-signal.cpp \
    onitz.cpp \
    networktime.cpp \
    networktimewatcher.cpp \
    networkoperator.cpp \
    networkregistrationwatcher.cpp \
    networktimeinfo.cpp \
    ofonomodemmanager.cpp \
    modemwatcher.cpp \
    ofonoconstants.cpp

SOURCES += credentials.cpp aegis.cpp
HEADERS += credentials.h

SOURCES += olson.cpp tz.cpp
HEADERS += tz.h

SOURCES += backup.cpp
HEADERS += backup.h

SOURCES += notification.cpp
HEADERS += notification.h

CONFIG += link_pkgconfig
PKGCONFIG += libpcrecpp
equals(QT_MAJOR_VERSION, 4) {
    CONFIG += iodata
    PKGCONFIG += contextprovider-1.0
}
equals(QT_MAJOR_VERSION, 5) {
    CONFIG += iodata-qt5
}


CONFIG(dsme_dbus_if) {
    PKGCONFIG += dsme_dbus_if
}

target.path = $$(DESTDIR)/usr/bin

xml.files  = com.nokia.time.context
xml.path = $$(DESTDIR)/usr/share/contextkit/providers

# typeinfo.files = queue.type config.type settings.type customization.type tzdata.type timed-cust-rc.type
# typeinfo.path = $$(DESTDIR)/usr/share/timed/typeinfo

backupconf.files = timedbackup.conf
backupconf.path = $$(DESTDIR)/usr/share/backup-framework/applications

backupscripts.files = timed-backup-script.sh timed-restore-script.sh
backupscripts.path = $$(DESTDIR)/usr/share/backup-framework/scripts

cud.files = timed-clear-device.sh
cud.path = $$(DESTDIR)/etc/osso-cud-scripts

rfs.files = timed-restore-original-settings.sh
rfs.path = $$(DESTDIR)/etc/osso-rfs-scripts

aegishelper.files = timed-aegis-session-helper
aegishelper.path  = $$(DESTDIR)/usr/bin

aegisfs.files = timed.aegisfs.conf
aegisfs.path  = $$(DESTDIR)/etc/aegisfs.d

equals(QT_MAJOR_VERSION, 4) {
    timedrc.files = timed.rc
    dbusconf.files = timed.conf
    systemd.files = timed.service
}
equals(QT_MAJOR_VERSION, 5) {
    timedrc.files = timed.rc
    dbusconf.files = timed-qt5.conf
    systemd.files = timed-qt5.service
}
timedrc.path  = $$(DESTDIR)/etc
dbusconf.path  = $$(DESTDIR)/etc/dbus-1/system.d
systemd.path = $$(DESTDIR)/lib/systemd/system

INSTALLS += target xml backupconf backupscripts cud rfs aegishelper aegisfs timedrc dbusconf systemd

CONFIG(MEEGO) \
{
  message("MEEGO flag is set")
  DEFINES += __MEEGO__
} \
else \
{
  message("MEEGO flag is not set, assuming HARMATTAN")
  CONFIG  += cellular-qt
  LIBS    += -lcreds
  DEFINES += __HARMATTAN__
  QMAKE_CXXFLAGS  += -Wall -Wno-psabi
}

QMAKE_CXXFLAGS  += -Wall
