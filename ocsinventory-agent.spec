Name:       ocsinventory-agent
Version:    2.0.3
Release:    3
Epoch:      1
Summary:    Unified client for OCS-Inventory
License:    GPLv2+
Group:      System/Servers
URL:        https://www.ocsinventory-ng.org/
Source0:    http://launchpad.net/ocsinventory-unix-agent/stable/ocsinventory-unix-agent-1.1.2/+download/Ocsinventory-Unix-Agent-%{version}.tar.gz
Patch0:     Ocsinventory-Agent-1.1.2-fix-syslog-usage.patch
Patch1:     Ocsinventory-Agent-1.1.2-fix-dmidecode-version-test.patch
Patch2:     Ocsinventory-Agent-1.1.2-fix-xen-dom0-identification.patch
Patch3:     Ocsinventory-Agent-1.1.2-add-bios-informations-for-xen-pv-hosts.patch
Requires:   net-tools
Requires:   pciutils
Requires:   nmap
Requires:   monitor-edid
Requires:   dmidecode >= 2.6
Requires:   perl-Net-IP
BuildRequires:   perl-devel
Suggests:   perl-Net-CUPS
Suggests:   perl-Proc-Daemon
Suggests:   ipmitool
Obsoletes:  ocsng-linux-agent
Obsoletes:  perl-Ocsinventory

%description
Linux agent for ocs-inventory. Dialog between client computers and management
server is based on actual standards, HTTP protocol and XML data formatting.

%prep
%setup -q -n Ocsinventory-Unix-Agent-%{version}
#%patch0 -p 1
#%patch1 -p 1
#%patch2 -p 1
#%patch3 -p 1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make

%install
rm -f run-postinst
%makeinstall_std

install -d %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/* %{buildroot}%{_sbindir}/

install -d -m 755 %{buildroot}%{_sysconfdir}/ocsinventory
cat > %{buildroot}%{_sysconfdir}/ocsinventory/ocsinventory-agent.cfg<<EOF
basevardir = %{_localstatedir}/lib/ocsinventory-agent
logger  = File
logfile = %{_localstatedir}/log/ocsinventory-agent/ocsinventory-agent.log
EOF

install -d -m 755 %{buildroot}%{_sysconfdir}/cron.daily
cat > %{buildroot}%{_sysconfdir}/cron.daily/ocsinventory-agent<<EOF
#!/bin/sh
%{_sbindir}/ocsinventory-agent --lazy > /dev/null 2>&1
EOF
chmod +x %{buildroot}%{_sysconfdir}/cron.daily/ocsinventory-agent

install -d %{buildroot}%{_sysconfdir}/logrotate.d
cat > %{buildroot}%{_sysconfdir}/logrotate.d/ocsinventory-agent<<EOF
/var/log/ocsinventory-agent/*.log {
    missingok
}
EOF

install -d %{buildroot}%{_localstatedir}/lib/ocsinventory-agent
install -d %{buildroot}%{_localstatedir}/log/ocsinventory-agent

# cleanup
rm -f %{buildroot}%{perl_vendorlib}/Ocsinventory/postinst.pl

%files
%defattr(-,root, root)
%doc AUTHORS Changes LICENSE README THANKS
%{_sbindir}/%{name}
%{_sbindir}/ipdiscover
%{_mandir}/man1/%{name}.*
%{_mandir}/man3/Ocsinventory::Agent::XML::Inventory.3pm*
%{_mandir}/man3/Ocsinventory::Agent::Common.3pm*
%{perl_vendorlib}/Ocsinventory
%config(noreplace) %{_sysconfdir}/cron.daily/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/ocsinventory
%{_localstatedir}/log/%{name}
%{_localstatedir}/lib/%{name}


%changelog
* Wed Nov 30 2011 Sergey Zhemoitel <serg@mandriva.org> 1:2.0.3-1mdv2012.0
+ Revision: 735763
- add new release 2.0.3

* Wed Nov 16 2011 Sergey Zhemoitel <serg@mandriva.org> 1:2.0.2-1
+ Revision: 730816
- new release 2.0.2

* Mon Oct 17 2011 Andrey Bondrov <abondrov@mandriva.org> 1:2.0.1-1
+ Revision: 704969
- Not a noarch package anymore

  + Sergey Zhemoitel <serg@mandriva.org>
    - new version 2.0.1

* Fri Feb 04 2011 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.1.2.1-2
+ Revision: 635830
- fix cron task (bug #61969)

* Sat Nov 27 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.1.2.1-1mdv2011.0
+ Revision: 601954
- new version

* Mon Jun 14 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.1.2-4mdv2011.0
+ Revision: 548020
- drop useless explicit dependencies
- cleanup space and tabs mixture

* Mon Jun 14 2010 Anne Nicolas <ennael@mandriva.org> 1:1.1.2-4mdv2010.1
+ Revision: 547999
- Fix requires and suggests (#59459)

* Sat May 29 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.1.2-3mdv2010.1
+ Revision: 546575
- patch1: fix dmidecode version test
- patch2: fix xen dom0 identification
- patch3: add bios information for xen PV hosts
- suggests optional perl modules and tools (fix #59459)

* Thu Apr 29 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.1.2-2mdv2010.1
+ Revision: 540800
- patch0: fix syslog usage
- new version
- fix cron task

* Mon Nov 30 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.02-2mdv2010.1
+ Revision: 471940
- ensure cron script is executable

* Sat Jun 06 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.02-1mdv2010.0
+ Revision: 383255
- new version
- merge perl package, no need for a distinct one
- use herein document whenever possible
- switch to a daily cron job, as per default installation

* Sun May 10 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.0.1-1mdv2010.0
+ Revision: 373950
- new version
- drop patches, not needed anymore

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 0.0.9.2-2mdv2009.0
+ Revision: 268323
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Thu May 15 2008 Oden Eriksson <oeriksson@mandriva.com> 0.0.9.2-1mdv2009.0
+ Revision: 207628
- remove versioned deps

* Wed May 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.0.9.2-0.1mdv2009.0
+ Revision: 207254
- import ocsinventory-agent

