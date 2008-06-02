Summary:	Unified client for OCS-Inventory
Name:		ocsinventory-agent
Version:	0.0.9.2
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Servers
URL:		http://www.ocsinventory-ng.org/
Source0:	http://search.cpan.org/CPAN/authors/id/G/GO/GONERI/Ocsinventory-Agent-%{version}.tar.gz
Source1:	ocsinventory-agent.logrotate
Source2:	ocsinventory-agent.cron
Source3:	ocsinventory-agent.sysconfig
Source4:	ocsinventory-agent.cfg
Patch0:		Ocsinventory-Agent-unbundle.diff
Patch1:		ocsinventory-agent-options.patch
BuildRequires:	perl-Compress-Zlib
BuildRequires:	perl(Digest::MD5)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(LWP)
BuildRequires:	perl(Net::IP)
BuildRequires:	perl-URI
BuildRequires:	perl-XML-NamespaceSupport
BuildRequires:	perl(XML::SAX)
BuildRequires:	perl-XML-SAX-Expat
BuildRequires:	perl(XML::Simple)
BuildRequires:	perl-XML-Simple
Requires:	net-tools
Requires:	pciutils
Requires:	nmap
Requires:	monitor-edid
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
ocsinventory-agent creates inventory and sent or write them. This agent is the
successor of the former linux_agent which was release with OCS 1.01 and prior.
It also replaces the Solaris/AIX/BSD unofficial agents.

%package -n	perl-Ocsinventory
Summary:	Unified client for OCS-Inventory
Group:		Development/Perl

%description -n	perl-Ocsinventory
ocsinventory-agent creates inventory and sent or write them. This agent is the
successor of the former linux_agent which was release with OCS 1.01 and prior.
It also replaces the Solaris/AIX/BSD unofficial agents.

This package contains the perl module parts of the ocsinventory-agent.

%prep

%setup -q -n Ocsinventory-Agent-%{version}
%patch0 -p1
%patch1 -p0

cp %{SOURCE1} ocsinventory-agent.logrotate
cp %{SOURCE2} ocsinventory-agent.cron
cp %{SOURCE3} ocsinventory-agent.sysconfig
cp %{SOURCE4} ocsinventory-agent.cfg

# fix path
find -type f | xargs perl -pi -e "s|%{_bindir}|%{_sbindir}|g"

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sysconfdir}/cron.hourly
install -d %{buildroot}%{_sysconfdir}/ocsinventory
install -d %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}/var/log/%{name}

rm -f run-postinst

%makeinstall_std

mv %{buildroot}%{_bindir}/* %{buildroot}%{_sbindir}/

install -m0644 ocsinventory-agent.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -m0755 ocsinventory-agent.cron %{buildroot}%{_sysconfdir}/cron.hourly/%{name}
install -m0644 ocsinventory-agent.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -m0644 ocsinventory-agent.cfg %{buildroot}%{_sysconfdir}/ocsinventory/%{name}.cfg

# cleanup
rm -f %{buildroot}%{perl_vendorlib}/Ocsinventory/postinst.pl

%clean
rm -rf %{buildroot}

%files
%defattr(-,root, root)
%doc AUTHORS Changes LICENSE README THANKS
%{_sysconfdir}/cron.hourly/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%dir %{_sysconfdir}/ocsinventory
%config(noreplace) %{_sysconfdir}/ocsinventory/%{name}.cfg
%{_sbindir}/%{name}
%dir /var/log/%{name}
%dir %{_localstatedir}/lib/%{name}
%{_mandir}/man1/%{name}.*

%files -n perl-Ocsinventory
%defattr(-,root, root)
%{perl_vendorlib}/Ocsinventory
