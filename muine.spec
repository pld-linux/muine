#
%define		min_ver	0.6.0
%define		snap	20040126
#
Summary:	Music player for GNOME
Summary(pl):	Odtwarzacz muzyczny dla GNOME
Name:		muine
Version:	0.2.1
Release:	0.%{snap}.2
License:	GPL
Group:		X11/Applications/Multimedia
#Source0:	http://people.nl.linux.org/~jorn/Muine/%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}-%{snap}.tar.bz2
# Source0-md5:	1d2ad1a113c78782e5f25a115370212c
URL:		http://people.nl.linux.org/~jorn/Muine/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gdbm-devel
BuildRequires:	gnome-common
BuildRequires:	gnome-vfs2-devel >= 2.4.0
BuildRequires:	gstreamer-devel >= %{min_ver}
BuildRequires:	gstreamer-GConf-devel >= %{min_ver}
BuildRequires:	gstreamer-plugins-devel >= %{min_ver}
BuildRequires:	gtk+2-devel >= 2.0.4
BuildRequires:	gtk-sharp-devel >= 0.15
BuildRequires:	intltool >= 0.21
BuildRequires:	libid3tag-devel
BuildRequires:	libogg-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	mono-devel >= 0.29
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires(post):	GConf2 >= 2.3.0
Requires(post):	scrollkeeper
Requires:	gstreamer-audio-effects >= %{min_ver}
Requires:	gstreamer-audio-formats >= %{min_ver}
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= %{min_ver}
Requires:	gtk-sharp >= 0.15
Requires:	mono >= 0.29
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

%build
cp %{_datadir}/automake/mkinstalldirs .
glib-gettextize --copy --force
intltoolize --copy --force
%{__libtoolize}
%{__aclocal} -I %{_aclocaldir}/gnome2-macros -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-static
		
%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

rm -f $RPM_BUILD_ROOT%{_libdir}/muine/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install
/usr/bin/scrollkeeper-update
echo
echo "Remember to install appropriate gstreamer plugins for files"
echo "you want to play:"
echo "- gstreamer-mad (for mp3s)"
echo "- gstreamer-vorbis (for Ogg Vorbis)"
echo

%postun -p /usr/bin/scrollkeeper-update

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README TODO
%{_sysconfdir}/gconf/schemas/*
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/muine
%attr(755,root,root) %{_libdir}/muine/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
