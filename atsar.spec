Name:		atsar
Version:	1.6
Release:	1
Source0:	ftp://ftp.atcomputing.nl/pub/tools/linux/%{name}_linux-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.cron
Patch:		%{name}-runfrompath.patch
URL:		ftp://ftp.atcomputing.nl/pub/tools/linux/
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}_linux-%{version}-root-%(id -u -n)
Summary:	AT Computing System Activity Report is a sar clone for Linux
Summary(pl):	Atsar jest odpowiednikiem uniksowego programu sar dla Linuksa
License:	GPL
Group:		System Environment/Daemons

%description
Atsar can be used to measure the load on the most relevant system
resources, such as CPU, disk, memory and network. Long-term analysis
can be done via cron, by maintaining log files with statistical
information. Short-term analysis can be done by starting the command
atsar with an interval and a number of samples. The current version of
atsar gathers statistics about the utilization of CPU's, disks, memory
and swap, serial lines and network (TCP/IP v4 and v6).

%description -l pl
Atsar przydaje siê do pomiarów obci±¿enia najbardziej istotnych
zasobów systemowych, takich jak procesor, dysk, pamiêæ i sieæ. Dziêki
po³±czeniu z cronem mo¿liwe jest otrzymanie logów z informacj±
statystyczn±, przydatnych do d³ugoterminowych analiz. Krótkoterminowe
analizy mog± byæ wykonywane przez bezpo¶rednie uruchomienie programu
atsar z podaniem parametrów takich jak ilo¶æ próbek i odstêp czasowy
miêdzy próbkami. Aktualna wersja programu atsar gromadzi informacje o
wykorzystaniu procesora, dysków, pamieci (operacyjnej i wymiany),
³±czy szeregowych i sieci (TCP/IP v4 i v6).

%prep
%setup -q -n %{name}_linux-%{version}

%patch -p1

%build
%{__make}

%install
cat scripts/atsa1 | sed -e 's|usr/local/bin|%{_bindir}|g' > sed.$$
mv -f sed.$$ scripts/atsa1
cat atsar_linux.conf | sed -e 's|usr/local/bin|%{_bindir}|g' > sed.$$
mv -f sed.$$ atsar_linux.conf
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 atsar/atsar atsadc/atsadc scripts/atsa1	\
scripts/atsaftp scripts/atsahttp $RPM_BUILD_ROOT%{_bindir}/
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -m 0644 man/* $RPM_BUILD_ROOT%{_mandir}/man1/
install -m 0755 -d $RPM_BUILD_ROOT/var/log/atsar
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/atsar
install -d $RPM_BUILD_ROOT/etc/cron.d
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/atsar
install -m 0644 atsar_linux.conf $RPM_BUILD_ROOT%{_sysconfdir}/atsar.conf

%clean
rm -rf    $RPM_BUILD_ROOT

%post
/usr/bin/atsa1
/sbin/chkconfig --add atsar
if [ -f /etc/atsar.conf ]; then
        /etc/rc.d/init.d/atsar restart 1>&2
else
        echo "Type \"/etc/rc.d/init.d/atsar start\" to start atsar" 1>&2
fi

%preun
if [ $1 = 0 ]; then
	/sbin/chkconfig --del atsar
fi

%postun
rm -f /var/lock/subsys/atsar 2> /dev/null

%files
%defattr(644,root,root,755)
%doc README

%attr(755,root,root) %{_bindir}/atsar
%attr(755,root,root) %{_bindir}/atsadc
%attr(755,root,root) %{_bindir}/atsa1
%attr(755,root,root) %{_bindir}/atsaftp
%attr(755,root,root) %{_bindir}/atsahttp
%{_mandir}/man1/atsar.1*
%{_mandir}/man1/atsadc.1*
%dir /var/log/atsar
%attr(755,root,root) %config /etc/rc.d/init.d/atsar
%config /etc/cron.d/atsar
%config %{_sysconfdir}/atsar.conf
