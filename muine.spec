#
# Conditional build
%bcond_with	gstreamer	# build with gstreamer instead xine-lib
#
%define		min_ver	0.8.0
#
Summary:	Music player for GNOME
Summary(pl):	Odtwarzacz muzyczny dla GNOME
Name:		muine
Version:	0.6.0
Release:	0.1
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	http://muine.gooeylinux.org/%{name}-%{version}.tar.gz
# Source0-md5:	cb1bef87070dfbddc6c824404d48c985
Patch0:		%{name}-locale-names.patch
URL:		http://muine.gooeylinux.org/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flac-devel
BuildRequires:	gdbm-devel
BuildRequires:	gnome-common
BuildRequires:	gnome-vfs2-devel >= 2.4.0
%if %{with gstreamer}
BuildRequires:	gstreamer-devel >= %{min_ver}
BuildRequires:	gstreamer-GConf-devel >= %{min_ver}
BuildRequires:	gstreamer-plugins-devel >= %{min_ver}
%endif
BuildRequires:	gtk+2-devel >= 2.0.4
BuildRequires:	dotnet-gtk-devel >= 0.91.1
BuildRequires:	intltool >= 0.21
BuildRequires:	libid3tag-devel >= 0.15
BuildRequires:	libogg-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	mono-devel >= 0.91
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
%{!?with_gstreamer:BuildRequires:	xine-lib-devel >= 1.0.0}
Requires(post):	GConf2 >= 2.3.0
Requires(post):	scrollkeeper
%if %{with gstreamer}
Requires:	gstreamer-audio-effects >= %{min_ver}
Requires:	gstreamer-audio-formats >= %{min_ver}
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= %{min_ver}
# videobalance plugin is required!
Requires:	gstreamer-video-effects >= %{min_ver}
%endif
Requires:	dotnet-gtk >= 0.91.1
Requires:	mono >= 0.91
%{!?with_gstreamer:Requires:	xine-plugin-audio}
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

mv po/{no,nb}.po

%build
cp /usr/share/automake/mkinstalldirs .
glib-gettextize --copy --force
intltoolize --copy --force
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	%{?with_gstreamer:--enable-gstreamer=yes} \
	--disable-static
		
%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%find_lang %{name} --with-gnome --all-name

rm -f $RPM_BUILD_ROOT%{_libdir}/muine/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install
/usr/bin/scrollkeeper-update
%if %{with gstreamer}
echo
echo "Remember to install appropriate gstreamer plugins for files"
echo "you want to play:"
echo "- gstreamer-flac (for FLAC)"
echo "- gstreamer-mad (for mp3s)"
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

%postun -p /usr/bin/scrollkeeper-update

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/muine
%attr(755,root,root) %{_libdir}/muine/*
%{_datadir}/application-registry/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
