# TODO:
# - aac support (faad2)
#
# Conditional build
%bcond_with	gstreamer	# build with gstreamer instead xine-lib 
#
%define		min_ver	0.8.0
#
Summary:	Music player for GNOME
Summary(pl):	Odtwarzacz muzyczny dla GNOME
Name:		muine
Version:	0.8.3
Release:	0.3
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://muine.gooeylinux.org/%{name}-%{version}.tar.gz
# Source0-md5:	4e21eeb8e809bebf1e13540e44a6259d
Patch0:		%{name}-desktop.patch
URL:		http://muine.gooeylinux.org/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flac-devel
BuildRequires:	gdbm-devel
BuildRequires:	gnome-common >= 2.8.0
BuildRequires:	gnome-vfs2-devel >= 2.4.0
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= %{min_ver}
BuildRequires:	gstreamer-GConf-devel >= %{min_ver}
BuildRequires:	gstreamer-plugins-devel >= %{min_ver}
%endif
BuildRequires:	gtk+2-devel >= 1:2.0.4
BuildRequires:	dotnet-gtk-sharp-gnome-devel >= 1.9.3
BuildRequires:	intltool >= 0.21
BuildRequires:	libid3tag-devel >= 0.15
BuildRequires:	libogg-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	mono-csharp >= 1.1.6
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
BuildRequires:	libgnome-devel
%{!?with_gstreamer:BuildRequires:	xine-lib-devel >= 1.0.0}
Requires(post,preun):	GConf2 >= 2.3.0
Requires(post,postun):	scrollkeeper
%if %{with gstreamer}
Requires:	gstreamer-audio-effects >= %{min_ver}
Requires:	gstreamer-audio-formats >= %{min_ver}
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= %{min_ver}
%endif
Requires:	dotnet-dbus-sharp
Requires:	dotnet-gtk-sharp-gnome >= 1.9.3
Requires:	mono >= 1.1.6
%{!?with_gstreamer:Requires:	xine-plugin-audio}
# TODO: recheck alpha
ExcludeArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Muine is a music player using some new UI ideas. The idea is that it
will be much easier and comfortable to use than the iTunes model,
which is used by both Rhythmbox and Jamboree.

%description -l pl
Muine jest odtwarzaczem muzycznym u¿ywaj±cym nowego typu UI
(interfejsu u¿ytkownika). Za³o¿eniem programu jest bycie o wiele
³atwiejszym i bardziej komfortowym  w u¿yciu ni¿ programy oparte
na wzorze iTunes jak Rhythmbox i Jamboree.

%package plugin-dashboard
Summary:        Dashboard plugin for Muine
Summary(pl):    Wtyczka dashboard dla Muine
Group:          X11/Applications
Requires:       %{name} = %{version}-%{release}
Requires:       dashboard

%description plugin-dashboard
Simple dashboard plugin for Muine.

%description -l pl plugin-dashboard
Prosta wtyczka dashboard dla Muine.

%package plugin-trayicon
Summary:        Trayicon plugin for Muine
Summary(pl):    Wtyczka obszaru powiadamiania dla Muine
Group:          X11/Applications
Requires:       %{name} = %{version}-%{release}

%description plugin-trayicon
Trayicon plugin for Muine.

%description -l pl plugin-trayicon
Wtyczka obszaru powiadamiania dla Muine.

%prep
%setup -q
%patch0 -p1

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
install -d $RPM_BUILD_ROOT%{_libdir}/muine/plugins

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

install plugins/*.{dll,png,xml} \
	$RPM_BUILD_ROOT%{_libdir}/muine/plugins

rm -f $RPM_BUILD_ROOT%{_libdir}/muine/*.la

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no
%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install muine.schemas
%scrollkeeper_update_post
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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/muine
%attr(755,root,root) %{_libdir}/muine/libmuine.so.*.*.*
%attr(755,root,root) %{_libdir}/muine/muine.*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
/usr/lib/dbus-1.0/services/*
/usr/lib/mono/gac/*
%{_pkgconfigdir}/*.pc

%files plugin-dashboard
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/muine/plugins/DashboardPlugin.dll

%files plugin-trayicon
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/muine/plugins/TrayIcon.dll
%{_libdir}/muine/plugins/TrayIcon.xml
%{_libdir}/muine/plugins/muine-tray-*.png
