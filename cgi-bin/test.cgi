#!"C:\perl\bin\perl.exe"
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI;
use Data::Dumper;
use Number::Fraction ':constants';
use strict;
use warnings;
$\ = "\n";
print "Content-Type: text/html\n\n";
my $str = '(1/4v0+3/4v1+5/8v4)';
my $f1 = '1/4';
$str =~ s/(\d+?\/\d+?)/Number::Fraction->new($1)*$f1/eg;
print $str;

# my $f1 = '1/2';
# print $f1*2;