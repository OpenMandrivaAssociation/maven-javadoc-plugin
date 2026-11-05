Name:           maven-javadoc-plugin
Version:        3.12.0
Release:        1
Summary:        Maven Javadoc Plugin
License:        ASL 2.0
URL:            https://maven.apache.org/plugins/maven-javadoc-plugin
BuildArch:      noarch
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption:	-Dmaven.javadoc.skip=true

Source0:        https://github.com/apache/maven-javadoc-plugin/archive/refs/tags/maven-javadoc-plugin-%{version}.tar.gz

BuildRequires:  maven-plugins-pom

%description
The Maven Javadoc Plugin is a plugin that uses the javadoc tool for
generating javadocs for the specified project.
 
%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n maven-javadoc-plugin-maven-javadoc-plugin-%{version}

%files -f .mfiles
%doc LICENSE README.md

%files javadoc
%doc LICENSE README.md 
