%global bootstrap 0

Name:           maven-javadoc-plugin
Version:        2.7
Release:        6
Summary:        Maven Javadoc Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-javadoc-plugin
# svn export http://svn.apache.org/repos/asf/maven/plugins/tags/maven-javadoc-plugin-2.7
# tar caf maven-javadoc-plugin-2.7.tar.xz maven-javadoc-plugin-2.7/
Source0:        %{name}-%{version}.tar.xz
Patch0:         remove-test-deps.patch
Patch1:         pom.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  maven2
BuildRequires:  maven-clean-plugin
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-plugin-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-shared-plugin-testing-harness
BuildRequires:  maven-shade-plugin
BuildRequires:  plexus-interactivity
BuildRequires:  maven-shared-invoker
%if ! %{bootstrap}
BuildRequires:  maven-javadoc-plugin
%endif        

Requires:       jpackage-utils
Requires:       maven2
Requires:       maven-shared-invoker
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

BuildArch: noarch

Obsoletes: maven2-plugin-javadoc <= 2.0.8
Provides:  maven2-plugin-javadoc = %{version}-%{release}

%description
The Maven Javadoc Plugin is a plugin that uses the javadoc tool for
generating javadocs for the specified project.
 
%if ! %{bootstrap}
%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.
%endif

%prep
%setup -q 
%patch0
# Update source for use with newer doxia
%patch1

sed -i -e "s|org.apache.maven.doxia.module.xhtml.decoration.render|org.apache.maven.doxia.sink.render|g" src/main/java/org/apache/maven/plugin/javadoc/JavadocReport.java

sed -i -e "s|model>|models>|g" pom.xml

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
        install
%if ! %{bootstrap}
mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        -Dmaven.test.skip=true \
       javadoc:javadoc
%endif        

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.apache.maven.plugins maven-javadoc-plugin %{version} JPP maven-javadoc-plugin

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

%if ! %{bootstrap}
# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*
%endif

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%if ! %{bootstrap}
%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
%endif

