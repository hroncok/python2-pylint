%{!?_python_sitelib: %define _python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pylint
Version:        0.22.0
Release:        3%{?dist}
Summary:        Analyzes Python code looking for bugs and signs of poor quality

Group:          Development/Debuggers
License:        GPLv2+
URL:            http://www.logilab.org/projects/pylint
Source0:        ftp://ftp.logilab.org/pub/pylint/pylint-%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  python-devel python-setuptools
Requires:       python-logilab-astng >= 0.21.0


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
for FILE in README doc/*.txt; do
    iconv -f iso-8859-15 -t utf-8 $FILE > $FILE.utf8
    mv -f $FILE.utf8 $FILE
done


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc/*.txt README ChangeLog examples elisp COPYING
%{_python_sitelib}/pylint*
%{_bindir}/*
%{_mandir}/man?/*
%exclude %{_python_sitelib}/pylint/gui.py*
%exclude %{_bindir}/pylint-gui

%files gui
%defattr(-,root,root,-)
%doc COPYING
%{_python_sitelib}/pylint/gui.py*
%{_bindir}/pylint-gui


%changelog
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Brian C. Lane <bcl@redhat.com> - 0.22.0-2
- Add version to requirement for python-logilab-astng so that updates will
  work correctly.

* Mon Nov 29 2010 Brian C. Lane <bcl@redhat.com> - 0.22.0-1
- Upstream 0.22.0

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 08 2010 Brian C. Lane <bcl@redhat.com> - 0.21.1-1
- Upstream 0.21.1
- Removed patch for 500272, fixed upstream - http://www.logilab.org/ticket/22962

* Mon Apr 05 2010 Brian C. Lane <bcl@redhat.com> - 0.20.0-2
- Added patch for bug 500272 (exception with --disable-msg-cat)

* Fri Mar 26 2010 Brian C.Lane <bcl@redhat.com> - 0.20.0-1
- Upstream 0.20.0
- Added python-setuptools to BuildRequires

* Sun Aug 30 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.18.1-1
- Upstream 0.18.1 (bugfixes and small enhancements)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.18.0-1
- Upstream 0.18.0 (bugfixes and minor feature updates)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.16.0-1
- Upstream 0.16.0

* Tue Dec 30 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.15.2-1
- Upstream 0.15.2

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.14.0-2
- Rebuild for Python 2.6

* Thu Jan 17 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.14.0-1
- Upstream 0.14.0
- Package the .egg-info files.

* Mon Dec 24 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.2-1
- Upstream 0.13.2
- Adjust license to a more precise version
- Fix docs to be valid utf-8

* Sun Apr 01 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.1-1
- Upstream 0.13.1

* Sun Dec 17 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.12.2-1
- Upstream 0.12.2
- Add COPYING to -gui

* Tue Sep 26 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.12.1-1
- Upstream 0.12.1
- Require the renamed python-logilab-astng

* Mon May 01 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.11.0-0
- Version 0.11.0

* Sun Mar 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.10.0-1
- Version 0.10.0

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
