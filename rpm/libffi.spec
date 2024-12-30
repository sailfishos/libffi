Name:       libffi
Summary:    A portable foreign function interface library
Version:    3.4.6
Release:    1
License:    BSD
URL:        https://github.com/sailfishos/libffi
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: automake
BuildRequires: libtool
# hack: make sure the old .so is available
BuildRequires: libffi

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
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(postun): /sbin/install-info

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep

%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%reconfigure --disable-static \
    --includedir=%{_includedir} \
    --disable-docs

%make_build

%install
%make_install

# include old version to ensure smooth upgrade. to be removed later.
cp -a /%{_libdir}/libffi.so.6 $RPM_BUILD_ROOT/%{_libdir}
cp -a /%{_libdir}/libffi.so.6.0.4 $RPM_BUILD_ROOT/%{_libdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/*.so.*

%files devel
%{_prefix}/include/ffi.h
%{_prefix}/include/ffitarget.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%doc %{_mandir}/man3/*.gz
