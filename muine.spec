#
# Conditional build
%bcond_without	gstreamer	# build with xine-lib instead of gstreamer
#
%define		min_ver	0.10
#
%include	/usr/lib/rpm/macros.mono
Summary:	Music player for GNOME
Summary(pl.UTF-8):	Odtwarzacz muzyczny dla GNOME
Name:		muine
Version:	0.8.8
Release:	1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://www.muine-player.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	0bf318424d35241525df701e107dd6b1
URL:		http://www.muine-player.org/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dotnet-dbus-sharp-devel >= 0.63
BuildRequires:	dotnet-gnome-sharp-devel >= 2.16.0
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.10.0
BuildRequires:	dotnet-ndesk-dbus-glib-sharp-devel
BuildRequires:	faad2-devel
BuildRequires:	flac-devel
BuildRequires:	gdbm-devel
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gnome-vfs2-devel >= 2.16.0
BuildRequires:	gtk+2-devel >= 2:2.10.3
BuildRequires:	intltool >= 0.35
BuildRequires:	libid3tag-devel >= 0.15
BuildRequires:	libogg-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	mono-csharp >= 1.1.6
BuildRequires:	monodoc >= 1.1.9
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(monoautodeps)
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= %{min_ver}
%else
BuildRequires:	xine-lib-devel >= 1.0.0
%endif
Requires(post,preun):	GConf2 >= 2.3.0
Requires(post,preun):	scrollkeeper
%if %{with gstreamer}
Requires:	gstreamer-audio-effects-base >= %{min_ver}
Requires:	gstreamer-audio-formats >= %{min_ver}
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= %{min_ver}
%else
Requires:	xine-plugin-audio
%endif
Obsoletes:	muine-plugin-dashboard
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Muine is a music player using some new UI ideas. The idea is that it
will be much easier and comfortable to use than the iTunes model,
which is used by both Rhythmbox and Jamboree.

%description -l pl.UTF-8
Muine jest odtwarzaczem muzycznym używającym nowego typu UI
(interfejsu użytkownika). Założeniem programu jest bycie o wiele
łatwiejszym i bardziej komfortowym w użyciu niż programy oparte na
wzorze iTunes jak Rhythmbox i Jamboree.

%package plugin-inotify
Summary:	Inotify plugin for Muine
Summary(pl.UTF-8):	Wtyczka Inotify dla Muine
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description plugin-inotify
Inotify plugin for Muine.

%description plugin-inotify -l pl.UTF-8
Wtyczka Inotify dla Muine.

%package plugin-trayicon
Summary:	Trayicon plugin for Muine
Summary(pl.UTF-8):	Wtyczka obszaru powiadamiania dla Muine
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description plugin-trayicon
Trayicon plugin for Muine.

%description plugin-trayicon -l pl.UTF-8
Wtyczka obszaru powiadamiania dla Muine.

%prep
%setup -q

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	%{!?with_gstreamer:--enable-xine=yes} \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/{muine/plugins,monodoc/sources}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

install plugins/*.{dll,png,xml} \
	$RPM_BUILD_ROOT%{_libdir}/muine/plugins

mv $RPM_BUILD_ROOT%{_docdir}/%{name}/* $RPM_BUILD_ROOT%{_libdir}/monodoc/sources

rm -f $RPM_BUILD_ROOT%{_libdir}/muine/*.la

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install muine.schemas
%scrollkeeper_update_post
%update_desktop_database_post
%if %{with gstreamer}
%banner %{name} -e << EOF
Remember to install appropriate GStreamer plugins for files
you want to play:
- gstreamer-flac (for FLAC)
- gstreamer-mad (for MP3s)
- gstreamer-vorbis (for Ogg Vorbis)
EOF
%else
%banner %{name} -e << EOF
Remember to install appropriate xine-decode plugins for files
you want to play:
- xine-decode-flac (for FLAC)
- xine-decode-ogg (for Ogg Vorbis)
EOF
%endif

%preun
%gconf_schema_uninstall muine.schemas

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS PLUGINS README TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/muine
%dir %{_libdir}/muine/plugins
%attr(755,root,root) %{_libdir}/muine/libmuine.*
%attr(755,root,root) %{_libdir}/muine/muine.*
%{_datadir}/dbus-1/services/*
#{_libdir}/mono/gac/*
#{_libdir}/mono/muine
%{_libdir}/muine/muine-dbus.dll
%{_libdir}/muine/muine-plugin.dll
%{_libdir}/monodoc/sources/*
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/16x16/apps/muine.png
%{_iconsdir}/hicolor/22x22/apps/muine.png
%{_iconsdir}/hicolor/24x24/apps/muine.png
%{_iconsdir}/hicolor/32x32/apps/muine.png
%{_iconsdir}/hicolor/scalable/apps/muine.svg
%{_pkgconfigdir}/*
%{_sysconfdir}/gconf/schemas/muine.schemas

%files plugin-inotify
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/muine/libinotifyglue.*
%attr(755,root,root) %{_libdir}/muine/plugins/InotifyPlugin.dll
%{_libdir}/muine/plugins/InotifyPlugin.dll.config

%files plugin-trayicon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/muine/plugins/TrayIcon.dll
%{_libdir}/muine/plugins/TrayIcon.xml
%{_libdir}/muine/plugins/muine-tray-*.png
