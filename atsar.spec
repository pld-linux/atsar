Summary:	AT Computing System Activity Report - a sar clone for Linux
Summary(pl):	Atsar - odpowiednik uniksowego programu sar dla Linuksa
Name:		atsar
Version:	1.7
Release:	2
License:	GPL
Group:		Daemons
Source0:	ftp://ftp.atcomputing.nl/pub/tools/linux/%{name}_linux-%{version}.tar.gz
# Source0-md5:	2aa73a4a99dd176a02c5336889d8b028
Source1:	%{name}.init
Source2:	%{name}.cron
Patch:		%{name}-runfrompath.patch
URL:		ftp://ftp.atcomputing.nl/pub/tools/linux/
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
wykorzystaniu procesora, dysków, pamiêci (operacyjnej i wymiany),
³±czy szeregowych i sieci (TCP/IP v4 i v6).

%prep
%setup -q -n %{name}_linux-%{version}
%patch -p1

%build
for r in atsar atsadc \*.o ;do
	find -iname $r -exec rm -v {} \;
done
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,/var/log/atsar} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,cron.d}

for s in scripts/atsa1 atsar_linux.conf ;do
	cat $s | sed -e 's|usr/local/bin|%{_bindir}|g' > sed.$$
	mv -f sed.$$ $s
done

install atsar/atsar atsadc/atsadc scripts/atsa1	\
	scripts/atsaftp scripts/atsahttp $RPM_BUILD_ROOT%{_bindir}
install man/* $RPM_BUILD_ROOT%{_mandir}/man1

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/atsar
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.d/atsar
install atsar_linux.conf $RPM_BUILD_ROOT%{_sysconfdir}/atsar.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/bin/atsa1
/sbin/chkconfig --add atsar
if [ -f /var/lock/subsys/atsar ]; then
	/etc/rc.d/init.d/atsar restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/atsar start\" to start atsar" 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/atsar ]; then
		/etc/rc.d/init.d/atsar stop
	fi
	/sbin/chkconfig --del atsar
fi

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
%attr(754,root,root) %config /etc/rc.d/init.d/atsar
%config(noreplace) %verify(not size mtime md5) /etc/cron.d/atsar
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/atsar.conf
