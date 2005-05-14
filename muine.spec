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
BuildRequires:	mono-csharp >= 0.96
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
# videobalance plugin is required!
Requires:	gstreamer-video-effects >= %{min_ver}
%endif
Requires:	dotnet-gtk-sharp >= 1.9.3
Requires:	mono >= 1.1
%{!?with_gstreamer:Requires:	xine-plugin-audio}
ExcludeArch:	alpha amd64
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

rm -f $RPM_BUILD_ROOT%{_libdir}/muine/*.la

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no
%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install muine.schemas
%scrollkeeper_update_post
%if %{with gstreamer}
echo
echo "Remember to install appropriate gstreamer plugins for files"
echo "you want to play:"
echo "- gstreamer-flac (for FLAC)"
echo "- gstreamer-mad (for MP3s)"
echo "- gstreamer-vorbis (for Ogg Vorbis)"
echo
%else
echo
echo "Remember to install appropriate xine-decode plugins for files"
echo "you want to play:"
echo "- xine-decode-flac (for FLAC)"
echo "- xine-decode-ogg (for Ogg Vorbis)"
echo
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
%attr(755,root,root) %{_libdir}/muine/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
/usr/lib/dbus-1.0/services/*
/usr/lib/mono/gac/*
%{_pkgconfigdir}/*.pc
