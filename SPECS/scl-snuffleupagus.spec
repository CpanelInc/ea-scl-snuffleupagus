%define debug_package %{nil}

# Package namespaces
%global ns_name ea
%global ns_dir /opt/cpanel
%global _scl_prefix %ns_dir

%scl_package %scl

# This makes the ea-php<ver>-build macro stuff work
%scl_package_override

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

Name:    %{?scl_prefix}php-snuffleupagus
Vendor:  cPanel, L.L.C.
Summary: Protective PHP Hardening Extension
Version: 0.5.0
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 4
Release: %{release_prefix}%{?dist}.cpanel
License: PHP
Group:   Development/Languages
URL: https://snuffleupagus.readthedocs.io/
Source: https://github.com/nbs-system/snuffleupagus/archive/v%{version}.tar.gz

BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix}scldevel
BuildRequires: %{?scl_prefix}build
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: autoconf, automake, libtool, pcre-devel
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}

%description
Snuffleupagus is a PHP7+ module designed to drastically raise the cost of attacks against websites. This is achieved by killing entire bug classes and providing a powerful virtual-patching system, allowing the administrator to fix specific vulnerabilities without having to touch the PHP code.

%prep
%setup -n snuffleupagus-%{version}

%build
cd src/
%{_scl_root}/usr/bin/phpize

%configure --with-php-config=%{_bindir}/php-config --enable-snuffleupagus
make %{?_smp_mflags}

%install
cd src/
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
install -d -m 755 $RPM_BUILD_ROOT%{php_extdir}
install -d -m 755 $RPM_BUILD_ROOT%{php_inidir}
install -m 755 modules/snuffleupagus.so $RPM_BUILD_ROOT%{php_extdir}

# by using using config/*.rules if a rule file is added or removed upstream then
# %files will alert us to that fact at build time so we can manage %files properly
install -d -m 755 $RPM_BUILD_ROOT%{php_inidir}/20-snuffleupagus.rules.d
pwd
ls -l ../
ls -l
%{__cp} ../config/*.rules $RPM_BUILD_ROOT%{php_inidir}/20-snuffleupagus.rules.d/

cat > $RPM_BUILD_ROOT%{php_inidir}/20-snuffleupagus.ini <<EOF
; Enable snuffleupagus
extension=snuffleupagus.so
sp.configuration_file=%{php_inidir}/20-snuffleupagus.rules.d/default.rules
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{php_extdir}/snuffleupagus.so

%config(noreplace) %attr(644,root,root) %{php_inidir}/20-snuffleupagus.ini

%dir %{php_inidir}/20-snuffleupagus.rules.d/
%attr(644,root,root) %{php_inidir}/20-snuffleupagus.rules.d/default.rules
%attr(644,root,root) %{php_inidir}/20-snuffleupagus.rules.d/rips.rules
%attr(644,root,root) %{php_inidir}/20-snuffleupagus.rules.d/typo3.rules

%changelog
* Thu Sep 05 2019 Cory McIntire <cory@cpanel.net> - 0.5.0-4
- ZC-5409: Revert previous 0.5.0-3 rollback test

* Thu Sep 05 2019 Cory McIntire <cory@cpanel.net> - 0.5.0-3
- ZC-5409: Rolling “scl-snuffleupagus” back to “63cd813641f9dd7df4ad40df37c66af353df6378”
- Testing EA4-tool rollback procedures

* Wed Aug 28 2019 Daniel Muey <dan@cpanel.net> - 0.5.0-2
- ZC-5444: Add ini that enables the extension

* Wed  Aug 14 2019 Dan Muey <dan@cpanel.net> - 0.5.0-1
- Update to v0.5.0

* Wed  Aug 14 2019 Dan Muey <dan@cpanel.net> - 0.4.1-1
- Update to v0.4.1

* Wed Aug 14 2019 Dan Muey <dan@cpanel.net> - 0.4.0-1
- Initial creation
