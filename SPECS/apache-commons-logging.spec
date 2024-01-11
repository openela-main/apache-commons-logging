%bcond_with bootstrap

Name:           apache-commons-logging
Version:        1.2
Release:        29%{?dist}
Summary:        Apache Commons Logging
License:        ASL 2.0
URL:            http://commons.apache.org/logging
BuildArch:      noarch

Source0:        http://www.apache.org/dist/commons/logging/source/commons-logging-%{version}-src.tar.gz
Source2:        http://mirrors.ibiblio.org/pub/mirrors/maven2/commons-logging/commons-logging-api/1.1/commons-logging-api-1.1.pom

Patch0:         0001-Generate-different-Bundle-SymbolicName-for-different.patch
Patch1:         0002-Port-to-maven-jar-plugin-3.0.0.patch

BuildRequires:  maven-local
%if %{with bootstrap}
BuildRequires:  javapackages-bootstrap
%else
BuildRequires:  mvn(javax.servlet:servlet-api)
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:  mvn(org.apache.maven.plugins:maven-failsafe-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:  mvn(org.codehaus.mojo:build-helper-maven-plugin)
%endif

%description
The commons-logging package provides a simple, component oriented
interface (org.apache.commons.logging.Log) together with wrappers for
logging systems. The user can choose at runtime which system they want
to use. In addition, a small number of basic implementations are
provided to allow users to use the package standalone.
commons-logging was heavily influenced by Avalon's Logkit and Log4J. The
commons-logging abstraction is meant to minimize the differences between
the two, and to allow a developer to not tie himself to a particular
logging implementation.

%{?javadoc_package}

%prep
%autosetup -p1 -n commons-logging-%{version}-src

%pom_remove_dep -r :avalon-framework
%pom_remove_dep -r :logkit
%pom_remove_dep -r :log4j
rm src/main/java/org/apache/commons/logging/impl/AvalonLogger.java
rm src/main/java/org/apache/commons/logging/impl/Log4JLogger.java
rm src/main/java/org/apache/commons/logging/impl/LogKitLogger.java
rm -r src/test/java/org/apache/commons/logging/{avalon,log4j,logkit}
rm src/test/java/org/apache/commons/logging/pathable/{Parent,Child}FirstTestCase.java


# Avoid hard-coded versions in OSGi metadata
%pom_xpath_set "pom:properties/pom:commons.osgi.import" '*;resolution:=optional'

%pom_remove_plugin :cobertura-maven-plugin
%pom_remove_plugin :maven-scm-publish-plugin

sed -i 's/\r//' RELEASE-NOTES.txt LICENSE.txt NOTICE.txt

# for compatibility reasons
%mvn_file ":commons-logging{*}" "commons-logging@1" "%{name}@1"
%mvn_alias ":commons-logging{*}" "org.apache.commons:commons-logging@1" "apache:commons-logging@1"

# Remove log4j12 tests
rm -rf src/test/java/org/apache/commons/logging/log4j/log4j12

%build
%mvn_build -- -Dmaven.compiler.source=1.6 -Dmaven.compiler.target=1.6 -Dcommons.osgi.symbolicName=org.apache.commons.logging

# The build produces more artifacts from one pom
%mvn_artifact %{SOURCE2} target/commons-logging-%{version}-api.jar
%mvn_artifact commons-logging:commons-logging-adapters:%{version} target/commons-logging-%{version}-adapters.jar

%install
%mvn_install

%files -f .mfiles
%license LICENSE.txt NOTICE.txt
%doc PROPOSAL.html RELEASE-NOTES.txt

%changelog
* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.2-29
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed Jun 09 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-28
- Rebuild to workaround DistroBaker issue

* Tue Jun 08 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-27
- Bootstrap Maven for CentOS Stream 9

* Mon May 17 2021 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-26
- Bootstrap build
- Non-bootstrap build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 10 2020 Mat Booth <mat.booth@redhat.com> - 1.2-24
- Build against log4j 2

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Jiri Vanek <jvanek@redhat.com> - 1.2-22
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jun 04 2020 Fabio Valentini <decathorpe@gmail.com> - 1.2-21
- Override javac source and target versions to fix builds with Java 11.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 09 2019 Fabio Valentini <decathorpe@gmail.com> - 1.2-19
- Disable avalon support by default.

* Tue Nov 05 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-15
- Mass rebuild for javapackages-tools 201902

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 24 2019 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-14
- Mass rebuild for javapackages-tools 201901

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 18 2018 Mat Booth <mat.booth@redhat.com> - 1.2-16
- Fix OSGi metadata

* Mon Dec 17 2018 Mat Booth <mat.booth@redhat.com> - 1.2-15
- Rebuild to regenerate requires, fixes rhbz#1660117

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-12
- Cleanup spec file

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 22 2017 Michael Simacek <msimacek@redhat.com> - 1.2-10
- Avoid %%add_maven_depmap

* Mon Feb 13 2017 Michael Simacek <msimacek@redhat.com> - 1.2-9
- Fix conditional

* Fri Feb 10 2017 Michael Simacek <msimacek@redhat.com> - 1.2-8
- Use log4j12
- Add avalon conditional

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 31 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-6
- Port to maven-jar-plugin 3.0.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar  9 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-3
- Add aliases for apache groupId

* Tue Jul 29 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-2
- Generate different Bundle-SymbolicName for different JARs
- Resolves: rhbz#1123055

* Sun Jul 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-1
- Update to upstream version 1.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Michael Simacek <msimacek@redhat.com> - 1.1.3-12
- Disable tests that use log4j12

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.3-11
- Use Requires: java-headless rebuild (#1067528)

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 1.1.3-10
- Set logkit dependency scope to provided

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 1.1.3-9
- Set avalon dependency scope to provided

* Wed Jan 22 2014 Michal Srb <msrb@redhat.com> - 1.1.3-8
- Run all the tests agains

* Sun Aug 11 2013 Michal Srb <msrb@redhat.com> - 1.1.3-7
- Make this package noarch again (Resolves: rhbz#995756)

* Tue Aug 06 2013 Michal Srb <msrb@redhat.com> - 1.1.3-6
- Temporarily remove test which fails in koji

* Mon Aug 05 2013 Michal Srb <msrb@redhat.com> - 1.1.3-5
- Add missing BR: maven-dependency-plugin, build-helper-maven-plugin

* Mon Aug 05 2013 Michal Srb <msrb@redhat.com> - 1.1.3-4
- Add missing BR: maven-failsafe-plugin

* Mon Aug 05 2013 Michal Srb <msrb@redhat.com> - 1.1.3-3
- Adapt to current guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.3-1
- Update to upstream version 1.1.3
- Remove OSGi Bundle-SymbolicName patch (accepted upstream)

* Tue Apr  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.2-2
- Set OSGi Bundle-SymbolicName to org.apache.commons.logging
- Resolves: rhbz#949842

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.2-1
- Update to upstream version 1.1.2
- Convert POM to POM macros
- Remove OSGi manifest patch; fixed upstream

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.1.1-22
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Nov 22 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1.1-21
- Install NOTICE file
- Resolves: rhbz#879581

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 1 2012 Alexander Kurtakov <akurtako@redhat.com> 1.1.1-19
- Bring back jakarta-commons-logging provides/obsoletes - the comment was misleading.

* Mon Apr 30 2012 Alexander Kurtakov <akurtako@redhat.com> 1.1.1-18
- Fix build with latest libs.
- Adapt to current guidelines.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Apr 21 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-16
- Build with maven 3
- Fix build for avalon-framework

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Alexander Kurtakov <akurtako@redhat.com> 1.1.1-14
- Bring back commons-logging* symlinks.

* Thu Dec 16 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-13
- Replace tomcat6 BR with servlet25 only
- Cleanups according to new packaging guidelines
- Install maven metadata for -api jar
- Versionless jars/javadocs

* Tue Nov  9 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-12
- Add depmaps for api and adapters subpackages
- Use apache-commons-parent BR instead of maven-*
- Replace tomcat5 BR with tomcat6
- Reenable tests

* Thu Jul  8 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-11
- Add license to javadoc subpackage

* Wed Jun 9 2010 Alexander Kurtakov <akurtako@redhat.com> 1.1.1-10
- Add osgi manifest entries.

* Fri May 21 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-9
- Correct depmap filename for backward compatibility

* Mon May 17 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-8
- Fix wrong depmap JPP name to short_name
- Add obsoletes to javadoc subpackage

* Wed May 12 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-7
- Fix symlink problems introduced previously in r5

* Tue May 11 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-6
- Add one more add_to_maven_depmap for backward compatibility

* Mon May 10 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-5
- Fix up add_to_maven_depmap
- Add jpackage-utils Requires for javadoc
- Cleanup install a bit

* Fri May  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-4
- Fix provides

* Thu May  6 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-3
- Revert to using default permissions
- Drop "Package" from summary, improve javadoc summary text

* Thu May  6 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-2
- Fix EOLs on docs
- Create javadoc symlinks during install
- Use version macro in Source0 URL, use _mavenpomdir macro

* Thu May  6 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.1.1-1
- Rename and rebase from jakarta-commons-logging
