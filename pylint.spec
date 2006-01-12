%{!?_python_sitelib: %define _python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pylint
Version:        0.9.0
Release:        1%{?dist}
Summary:        Analyzes Python code looking for bugs and signs of poor quality

Group:          Development/Debuggers
License:        GPL
URL:            http://www.logilab.org/projects/pylint
Source0:        ftp://ftp.logilab.org/pub/pylint/pylint-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
Requires:       python-abi = %(%{__python} -c "import sys; print sys.version[:3]")
Requires:       python-logilab-common, python-astng

%description
Pylint is a python tool that checks if a module satisfy a coding standard. 
Pylint can be seen as another PyChecker since nearly all tests you can do 
with PyChecker can also be done with Pylint. But Pylint offers some more 
features, like checking line-code's length, checking if variable names are 
well-formed according to your coding standard, or checking if declared 
interfaces are truly implemented, and much more. The big advantage with 
Pylint is that it is highly configurable, customizable, and you can easily 
write a small plugin to add a personal feature.


%package gui
Summary:        Graphical Interface tool for Pylint
Group:          Development/Debuggers
Requires:       %{name} = %{version}-%{release}
Requires:       tkinter

%description gui
This package provides a gui tool for pylint written in tkinter.


%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_python_sitelib}/pylint/test
mkdir -pm 755 $RPM_BUILD_ROOT%{_mandir}/man1
install -pm 644 man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/*.txt README ChangeLog TODO examples elisp COPYING
%dir %{_python_sitelib}/pylint
%dir %{_python_sitelib}/pylint/checkers
%dir %{_python_sitelib}/pylint/reporters
%{_python_sitelib}/pylint/*.py
%{_python_sitelib}/pylint/*.pyc
%ghost %{_python_sitelib}/pylint/*.pyo
%{_python_sitelib}/pylint/*/*.py
%{_python_sitelib}/pylint/*/*.pyc
%ghost %{_python_sitelib}/pylint/*/*.pyo
%{_bindir}/pylint
%{_bindir}/symilar
%{_mandir}/man?/*
%exclude %{_python_sitelib}/pylint/gui.py*


%files gui
%defattr(-,root,root,-)
%{_python_sitelib}/pylint/gui.py
%{_python_sitelib}/pylint/gui.pyc
%ghost %{_python_sitelib}/pylint/gui.pyo
%{_bindir}/pylint-gui


%changelog
* Thu Jan 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.9.0-1
- Version 0.9.0
- Add COPYING to docs

* Sun Nov 13 2005 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.8.1-1
- Version 0.8.1
- Add dependency on python-astng
- Drop artificial version requirement on python-logilab-common

* Mon Jun 13 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.7.0-1
- Version 0.7.0
- No longer in the logilab subdir
- Disttagging

* Mon May 09 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-4
- Install the pylint.1 manfile.
- Add examples and elisp dirs to docs.

* Thu May 05 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-3
- Only doc the .txt files.
- Don't buildrequire python-logilab-common
- Fix paths.

* Tue Apr 26 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-2
- Ghost .pyo files.
- Remove the test dir, as it doesn't do anything.
- Separate the gui package, which depends on tkinter.
- Don't own site-packages/logilab, which is owned by
  python-logilab-common.

* Fri Apr 22 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-1
- Initial packaging.