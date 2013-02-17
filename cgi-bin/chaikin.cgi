#!"C:\perl\bin\perl.exe"
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI;
use Data::Dumper;
use strict;
use warnings;
use Prima qw(Application);
$\ = "\n";

my $req = new CGI;

my $initialPoints = $req->param('points');
my $iterations = $req->param('iterations');

sub chaikin{
	my (@points) = @_;
	my @new_points;
	for (my $i = 0; $i <= $#points; $i+=2){
		if ($points[$i+3]){
			push (@new_points, ($points[$i]*3+$points[$i+2]*1)/4); #x1
			push (@new_points, ($points[$i+1]*3+$points[$i+3]*1)/4); #y1
			push (@new_points, ($points[$i]*1+$points[$i+2]*3)/4); #x2
			push (@new_points, ($points[$i+1]*1+$points[$i+3]*3)/4); #y2
		}
	}
	
	return @new_points;
}

my @points = split(' ',$initialPoints);


for (my $count = 1; $count <= $iterations; $count++) {
	@points = chaikin(@points);
}

#### MAKE THE IMAGE
my $image = Prima::Image-> new(
   width => 500,
   height => 500,
);

# draw 
$image-> begin_paint; 
$image-> color( cl::White);
for (my $j = 0; $j<= $#points; $j+=2){
	if ($points[$j+3]){
		$image->line( int $points[$j], int $points[$j+1], int $points[$j+2], int $points[$j+3] );
	}
}
$image-> end_paint; 

# file operations
$image-> save('../test.jpg') or die "Error saving:$@\n";
my $rand=int(rand(100));
print "Content-Type: text/plain\n\n";
print qq(test.jpg?$rand);