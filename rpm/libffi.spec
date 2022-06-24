Name:       libffi
Summary:    A portable foreign function interface library
Version:    3.2.1
Release:    1
Group:      System/Libraries
License:    BSD
URL:        https://github.com/sailfishos/libffi
Source0:    %{name}-%{version}.tar.gz
Patch0:     includedir.patch
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: texinfo
BuildRequires: automake
BuildRequires: libtool

# See install section for more info
Provides: libffi.so.5

%description
Compilers for high level languages generate code that follow certain
conventions.  These conventions are necessary, in part, for separate
compilation to work.  One such convention is the "calling convention".
The calling convention is a set of assumptions made by the compiler
about where function arguments will be found on entry to a function.  A
calling convention also specifies where the return value for a function
is found.  

Some programs may not know at the time of compilation what arguments
are to be passed to a function.  For instance, an interpreter may be
told at run-time about the number and types of arguments used to call a
given function.  `Libffi' can be used in such programs to provide a
bridge from the interpreter program to compiled code.

The `libffi' library provides a portable, high level programming
interface to various calling conventions.  This allows a programmer to
call any function specified by a call interface description at run time.

FFI stands for Foreign Function Interface.  A foreign function
interface is the popular name for the interface that allows code
written in one language to call code written in another language.  The
`libffi' library really only provides the lowest, machine dependent
layer of a fully featured foreign function interface.  A layer must
exist above `libffi' that handles type conversions for values passed
between the two languages.


%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}/%{name}

# includedir.patch
%patch0 -p1

%build
%reconfigure --disable-static \
    --includedir=%{_includedir}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# Have both .so.5 and .so.6 as those are binary compatible, this prevents
# the build breaking when we do the update.
ln -sf libffi.so.6 %{buildroot}%{_libdir}/libffi.so.5

%post -p /sbin/ldconfig

%posttrans
# This is here because for some reason when updating from libffi 3.0.x to 3.2.1
# the symbolic link that is part of the package install section disappears.
# It seems that rpm does not detect that the link target has changed and removes the
# new link as part of the old package as both are libffi.so.5 files, eventhough one
# points to libffi.so.5.0.10 and other to libffi.so.6.
if [ ! -e %{_libdir}/libffi.so.5 ]; then
  ln -sf libffi.so.6 %{_libdir}/libffi.so.5 || :
fi

%postun -p /sbin/ldconfig

%post devel
%install_info --info-dir=%_infodir %{_infodir}/libffi.info.gz || :

%postun devel
if [ $1 = 0 ] ;then
%install_info_delete --info-dir=%{_infodir} %{_infodir}/libffi.info.gz || :
fi

%files
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/*.so.*

%files devel
%doc LICENSE README
%defattr(-,root,root,-)
%{_prefix}/include/ffi.h
%{_prefix}/include/ffitarget.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%doc %{_mandir}/man3/*.gz
%{_infodir}/libffi.info.gz
