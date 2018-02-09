%global with_python3 1

Name:           pylint
Version:        1.7.4
Release:        3%{?dist}
Summary:        Analyzes Python code looking for bugs and signs of poor quality
Group:          Development/Debuggers
License:        GPLv2+
URL:            http://www.pylint.org/
Source0:        https://github.com/PyCQA/pylint/archive/pylint-%{version}.tar.gz

# Fix for rhbz#1483869
Patch0:         0001-Remove-module-that-wasn-t-actually-moved.-Close-1565.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python2-configparser
BuildRequires:  python2-mccabe
BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python-astroid >= 1.4.5
# For tests
BuildRequires:  python2-isort
BuildRequires:  python2-backports-functools_lru_cache
BuildRequires:  python2-pytest-runner
# Python 3 is default for Fedora 26+
%if 0%{?fedora} >= 26 || 0%{?rhel} > 7
Requires:       python%{python3_pkgversion}-%{name} = %{version}-%{release}
%else
Requires:       python2-%{name} = %{version}-%{release}
%endif
Obsoletes:      pylint-gui < 1.7

%description
Pylint is a Python source code analyzer which looks for programming
errors, helps enforcing a coding standard and sniffs for some code
smells (as defined in Martin Fowler's Refactoring book).
Pylint can be seen as another PyChecker since nearly all tests you
can do with PyChecker can also be done with Pylint. However, Pylint
offers some more features, like checking length of lines of code,
checking if variable names are well-formed according to your coding
standard, or checking if declared interfaces are truly implemented,
and much more.
Additionally, it is possible to write plugins to add your own checks.


%package -n python2-pylint
Summary:        Analyzes Python code looking for bugs and signs of poor quality
Group:          Development/Debuggers
Requires:       python-astroid >= 1.4.5
Requires:       python-setuptools
Requires:       python-six
Requires:       python2-mccabe
Requires:       python2-isort
Requires:       python2-backports-functools_lru_cache
Requires:       python2-configparser
Requires:       python2-pytest-runner
Obsoletes:      python2-pylint-gui < 1.7

%description -n python2-pylint
Pylint is a Python source code analyzer which looks for programming
errors, helps enforcing a coding standard and sniffs for some code
smells (as defined in Martin Fowler's Refactoring book).
Pylint can be seen as another PyChecker since nearly all tests you
can do with PyChecker can also be done with Pylint. However, Pylint
offers some more features, like checking length of lines of code,
checking if variable names are well-formed according to your coding
standard, or checking if declared interfaces are truly implemented,
and much more.
Additionally, it is possible to write plugins to add your own checks.


%if 0%{?with_python3}
%package -n python%{python3_pkgversion}-pylint
Summary:        Analyzes Python code looking for bugs and signs of poor quality
Group:          Development/Debuggers
BuildRequires:  python%{python3_pkgversion}-devel python%{python3_pkgversion}-setuptools python%{python3_pkgversion}-tools
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  python%{python3_pkgversion}-astroid >= 1.4.5
# For tests
BuildRequires:  python%{python3_pkgversion}-isort
BuildRequires:  python%{python3_pkgversion}-mccabe
BuildRequires:  python%{python3_pkgversion}-pytest-runner
Requires:       python%{python3_pkgversion}-astroid >= 1.4.5
Requires:       python%{python3_pkgversion}-setuptools
Requires:       python%{python3_pkgversion}-six
Requires:       python%{python3_pkgversion}-mccabe
Requires:       python%{python3_pkgversion}-isort
Requires:       python%{python3_pkgversion}-pytest-runner
Obsoletes:      python%{python3_pkgversion}-pylint-gui < 1.7

%description -n python%{python3_pkgversion}-pylint
Pylint is a Python source code analyzer which looks for programming
errors, helps enforcing a coding standard and sniffs for some code
smells (as defined in Martin Fowler's Refactoring book).
Pylint can be seen as another PyChecker since nearly all tests you
can do with PyChecker can also be done with Pylint. However, Pylint
offers some more features, like checking length of lines of code,
checking if variable names are well-formed according to your coding
standard, or checking if declared interfaces are truly implemented,
and much more.
Additionally, it is possible to write plugins to add your own checks.
%endif # with_python3

%prep
%setup -q -n pylint-pylint-%{version}
%patch0 -p1

%build
%py2_build

%if 0%{?with_python3}
%py3_build
%endif # with_python3

%install
%if 0%{?with_python3}
%py3_install
rm -rf %{buildroot}%{python3_sitelib}/pylint/test
mkdir -pm 755 %{buildroot}%{_mandir}/man1
install -pm 644 man/*.1 %{buildroot}%{_mandir}/man1/
# Add -%{python3_version} to the binaries and manpages
for NAME in epylint pylint pyreverse symilar; do
    mv %{buildroot}%{_bindir}/{$NAME,${NAME}-%{python3_version}}
    ln -s ${NAME}-%{python3_version} %{buildroot}%{_bindir}/${NAME}-3
    mv %{buildroot}%{_mandir}/man1/{${NAME}.1,${NAME}-%{python3_version}.1}
    ln -s ${NAME}-%{python3_version}.1 %{buildroot}%{_mandir}/man1/${NAME}-3.1
done
%endif # with_python3

%py2_install
rm -rf %{buildroot}%{python2_sitelib}/pylint/test
mkdir -pm 755 %{buildroot}%{_mandir}/man1
install -pm 644 man/*.1 %{buildroot}%{_mandir}/man1/
# Add -%{python2_version} to the binaries and manpages
for NAME in epylint pylint pyreverse symilar; do
    mv %{buildroot}%{_bindir}/{$NAME,${NAME}-%{python2_version}}
    ln -s ${NAME}-%{python2_version} %{buildroot}%{_bindir}/${NAME}-2
    mv %{buildroot}%{_mandir}/man1/{${NAME}.1,${NAME}-%{python2_version}.1}
    ln -s ${NAME}-%{python2_version}.1 %{buildroot}%{_mandir}/man1/${NAME}-2.1
done

for NAME in epylint pylint pyreverse symilar; do
%if 0%{?fedora} >= 26 || 0%{?rhel} > 7
    ln -s ${NAME}-%{python3_version} %{buildroot}%{_bindir}/${NAME}
    ln -s ${NAME}-%{python3_version}.1 %{buildroot}%{_mandir}/man1/${NAME}.1
%else
    ln -s ${NAME}-%{python2_version} %{buildroot}%{_bindir}/${NAME}
    ln -s ${NAME}-%{python2_version}.1 %{buildroot}%{_mandir}/man1/${NAME}.1
%endif
done
# remove pylint-gui manpage, as we have no pylint-gui anymore (removed upstream)
rm -f %{buildroot}%{_mandir}/man1/pylint-gui*

%check
export PYTHONPATH=%{buildroot}%{python2_sitelib}
bin/pylint -rn --rcfile=pylintrc --load-plugins=pylint.extensions.docparams, pylint.extensions.mccabe pylint || :
%{__python2} -Wi -m unittest discover -s pylint/test || :
%if 0%{?with_python3}
export PYTHONPATH=%{buildroot}%{python3_sitelib}
%{__python3} bin/pylint -rn --rcfile=pylintrc --load-plugins=pylint.extensions.docparams, pylint.extensions.mccabe pylint || :
%{__python3} -Wi -m unittest discover -s pylint/test || :
%endif

%files
%doc README.rst ChangeLog examples elisp
%license COPYING
%{_bindir}/epylint
%{_bindir}/pylint
%{_bindir}/pyreverse
%{_bindir}/symilar
%{_mandir}/man1/epylint.1*
%{_mandir}/man1/pylint.1*
%{_mandir}/man1/pyreverse.1*
%{_mandir}/man1/symilar.1*


%files -n python2-pylint
%doc README.rst ChangeLog examples elisp
%license COPYING
%{_bindir}/*-2
%{_bindir}/*-%{python2_version}
%{_mandir}/man1/*-2.1*
%{_mandir}/man1/*-%{python2_version}.1*
%{python2_sitelib}/pylint*


%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-pylint
%doc README.rst ChangeLog examples elisp
%license COPYING
%{python3_sitelib}/pylint*
%{_bindir}/*-3
%{_bindir}/*-%{python3_version}
%{_mandir}/man1/*-3.1*
%{_mandir}/man1/*-%{python3_version}.1*
%endif # with_python3

%changelog
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Karsten Hopp <karsten@redhat.com> - 1.7.4-2
- update requirements

* Tue Oct 10 2017 Christian Dersch <lupinix@mailbox.org> - 1.7.4-1
- new version
- added BR: python2-configparser, python(2,3)-mccabe for proper test execution

* Thu Aug 31 2017 Brian C. Lane <bcl@redhat.com> - 1.7.2-2
- Remove module that wasn't actually moved. (#1483869)

* Wed Aug 02 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.7.2-1
- 1.7.2.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun May 14 2017 Christian Dersch <lupinix@mailbox.org> - 1.7.1-1
- new version
- we need pytest-runner now
- pylint-gui has been removed upstream

* Wed Apr 5 2017 Orion Poplawski <orion@cora.nwra.com> - 1.6.5-4
- Provide python major version links (bug #1439070)

* Tue Mar 28 2017 Orion Poplawski <orion@cora.nwra.com> - 1.6.5-3
- Split python2 modules into sub-packages
- Make python3 the default for scripts on Fedora 26+

* Mon Mar 13 2017 Orion Poplawski <orion@cora.nwra.com> - 1.6.5-2
- Enable python3 build for EPEL
- Include python3-pylint-gui __pycache__ files in gui package (bug #1422609)
- Cleanup spec
- Run tests, but they currently fail

* Wed Feb 22 2017 Christian Dersch <lupinix@mailbox.org> - 1.6.5-1
- new version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.6.4-2
- Rebuild for Python 3.6

* Mon Oct 03 2016 Jon Ciesla <limburgher@gmail.com> - 1.6.4-1
- Upstream v1.6.4

* Fri Jul 29 2016 Jon Ciesla <limburgher@gmail.com> - 1.5.6-1
- Upstream v1.5.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 07 2016 Brian C. Lane <bcl@redhat.com> 1.5.5-1
- Upstream v1.5.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Brian C. Lane <bcl@redhat.com> 1.5.4-1
- Upstream v1.5.4

* Mon Jan 04 2016 Brian C. Lane <bcl@redhat.com> 1.5.2-1
- Upstream v1.5.2

* Thu Dec 10 2015 Brian C. Lane <bcl@redhat.com> 1.5.1-1
- Upstream v1.5.1
- Remove %check section, it does not work due to unpackaged requirements.
- Update description from the package's __pkginfo__.py file.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Mathieu Bridon <bochecha@daitauha.fr> - 1.4.3-2
- Drop python3 requirements from the python2 package.
- Add missing requirement on six.

* Tue Apr 28 2015 Brian C. Lane <bcl@redhat.com> 1.4.3-1
- Upstream v1.4.3

* Fri Jan 30 2015 Brian C. Lane <bcl@redhat.com> 1.4.1-3
- Exclude the python3-* files from the python2 package

* Thu Jan 29 2015 Brian C. Lane <bcl@redhat.com> 1.4.1-2
- Add python-six requirement

* Wed Jan 28 2015 Brian C. Lane <bcl@redhat.com> 1.4.1-1
- Upstream v1.4.1

* Mon Oct 27 2014 Brian C. Lane <bcl@redhat.com> 1.3.1-2
- python3-pylint-gui needs python3-tkinter

* Fri Oct 03 2014 Brian C. Lane <bcl@redhat.com> 1.3.1-1
- Upstream v1.3.1
  Dropped patches included in upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Brian C. Lane <bcl@redhat.com> 1.2-6
- Add python3-astroid and python3-setuptools as Requires (#1103479)

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri May 09 2014 Brian C. Lane <bcl@redhat.com> 1.2-4
- Fix a potential AttributeError when checking for `reversed` arguments.
  https://bitbucket.org/logilab/pylint/commits/93babaf6bffc59a49c75319d9850086b4935edbc

* Thu May 08 2014 Brian C. Lane <bcl@redhat.com> 1.2-3
- fix explicit check of python script
  https://bitbucket.org/logilab/pylint/issue/219/

* Thu Apr 24 2014 Brian C. Lane <bcl@redhat.com> 1.2-2
- Patch to Fix --init-hook typo (dshea)
  https://bitbucket.org/logilab/pylint/issue/211/init-hook-no-longer-works

* Tue Apr 22 2014 Brian C. Lane <bcl@redhat.com> 1.2-1
- Upstream v1.2

* Thu Feb 27 2014 Brian C. Lane <bcl@redhat.com> 1.1.0-1
- Upstream v1.1.0
  Drop patch included in upstream

* Thu Oct 24 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-3
- Switching on python3 support

* Tue Sep 03 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-2
- Add upstream patch for epylint input validation (#981859)

* Tue Aug 13 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-1
- Upstream 1.0.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Brian C. Lane <bcl@redhat.com> 0.26.0-1
- Upstream 0.26.0
- Add python3-pylint and python3-pylint-gui subpackages. Not ready to turn it
  on yet due to this upstream bug: http://www.logilab.org/ticket/110213

* Fri Aug 03 2012 Brian C. Lane <bcl@redhat.com> 0.25.2-1
- Upstream 0.25.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Brian C. Lane <bcl@redhat.com> 0.25.1-1
- Upstream 0.25.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Brian C. Lane <bcl@redhat.com> - 0.25.0-1
- Upstream 0.25.0

* Fri Jul 29 2011 Brian C. Lane <bcl@redhat.com> - 0.24.0-1
- Upstream 0.24.0

* Mon Mar 28 2011 Brian C. Lane <bcl@redhat.com> - 0.23-0.1
- Upstream 0.23.0
- Add unit tests to spec

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
