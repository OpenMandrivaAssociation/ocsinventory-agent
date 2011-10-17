Name:       ocsinventory-agent
Version:    2.0.1
Release:    %mkrel 1
Epoch:      1
Summary:    Unified client for OCS-Inventory
License:    GPLv2+
Group:      System/Servers
URL:        http://www.ocsinventory-ng.org/
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
Suggests:   perl-Net-CUPS
Suggests:   perl-Proc-Daemon
Suggests:   ipmitool
Obsoletes:  ocsng-linux-agent
Obsoletes:  perl-Ocsinventory
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}

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
rm -rf %{buildroot}
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

%clean
rm -rf %{buildroot}

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
#%{_libdir}/debug/usr/sbin/ipdiscover.debug