#!"C:\perl\bin\perl.exe"
use strict;
use warnings;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI;
use Data::Dumper;
use Number::Fraction ':constants';
use JSON;
use Prima qw(Application);
$\ = "\n";
print "Content-Type: text/json\n\n";


my $req = new CGI;

my $initialPoints = $req->param('points');
my $iterations = $req->param('iterations');
my @points = split(' ',$initialPoints);

sub generateFirstIteration {
	my (@points) = @_;
	my $points_count = ($#points+1)/2;
	my @vpoints;
	for (my $i = 0; $i < $points_count ; $i++) {
		my $i2 = ($i+1)%$points_count;
		my $i3 = ($i+2)%$points_count;
		push (@vpoints, "1/4v".$i."+3/4v".$i2."");
		push (@vpoints, "3/4v".$i2."+1/4v".$i3."");
	}

	return @vpoints;
}

sub calcPlusString {
	my ($str) = @_;
	my @vnumbers = split('\+', $str);
	my %numbers;
	my ($key, $value, $return);
	foreach my $vnumber (@vnumbers) {
		$vnumber =~ m/(\d+\/\d+)(v\d+)/;
		if (defined $numbers{$2}){
			$numbers{$2} = Number::Fraction->new($1)+Number::Fraction->new($numbers{$2});
		}else{
			$numbers{$2} = $1;
		}
	}
	while (($key, $value) = each (%numbers)) {
	  $return .= "$value$key+";
	}
	$return =~ s/\+$//;
	return $return;
}

sub generateNextIteration {
	my (@vpoints) = @_;
	my @next_points;
	for (my $i = 0; $i < $#vpoints+1; $i++) {
		my $i2 = ($i+1)%($#vpoints+1);
		my $i3 = ($i+2)%($#vpoints+1);
		
		my $vpoint1 = $vpoints[$i];
		my $vpoint2 = $vpoints[$i2];
		my $vpoint3 = $vpoints[$i3];
		$vpoint1 =~ s/(\d+\/\d+)/Number::Fraction->new($1)*Number::Fraction->new(1,4)/eg; 
		$vpoint2 =~ s/(\d+\/\d+)/Number::Fraction->new($1)*Number::Fraction->new(3,4)/eg;
		$vpoint3 =~ s/(\d+\/\d+)/Number::Fraction->new($1)*Number::Fraction->new(1,4)/eg;
		push (@next_points, calcPlusString($vpoint1.'+'.$vpoint2));
		push (@next_points, calcPlusString($vpoint2."+".$vpoint3));
		# push (@next_points, "(1/4".$vpoints[$i]."+3/4".$vpoints[$i2].")");
		# push (@next_points, "(3/4".$vpoints[$i2]."+1/4".$vpoints[$i3].")");
	}
	return @next_points;
}

sub chaikinsString {
	my ($iterations, @points) = @_;
	my @vpoints;
	if ($iterations==0) {
		return @points;
	} else {
		@vpoints = generateFirstIteration(@points);
		for (my $i = 1; $i < $iterations; $i++) {
			@vpoints = generateNextIteration(@vpoints);
		}
		return @vpoints;
	}
}

sub generatePointsString{
	return map {"P($_) "} @_;
}

sub calcRealPoints {
	my ($points, $vpoints) = @_;

	my @real_points;
	foreach my $vpoint (@$vpoints) {
		
		my @abstract_points = split('\+', $vpoint);

		my %point;
		$point{'x'} = 0;
		$point{'y'} = 0;
		foreach my $abs_point (@abstract_points) {
			$abs_point =~ m/(\d+\/\d+)v(\d+)/;
			
			$point{'x'} += Number::Fraction->new($1)*$$points[$2*2];
			$point{'y'} += Number::Fraction->new($1)*$$points[$2*2+1];
		}
		push (@real_points, $point{'x'}->to_num().' ');
		push (@real_points, $point{'y'}->to_num().' ');
	}
	push (@real_points, $real_points[0]);
	push (@real_points, $real_points[1]);
	return @real_points;

}

my @vpoints = chaikinsString($iterations, @points);


my @real_points = calcRealPoints(\@points, \@vpoints);

#print Dumper(@real_points);

#### MAKE THE IMAGE
my $image = Prima::Image-> new(
   width => 500,
   height => 500,
);

# draw 
$image-> begin_paint; 
$image-> color( cl::White);
for (my $j = 0; $j<= $#real_points; $j+=2){
	if ($real_points[$j+3]){
		$image->line( int $real_points[$j], int $real_points[$j+1], int $real_points[$j+2], int $real_points[$j+3] );
	}
}
$image-> end_paint; 

# file operations
$image-> save('../test.jpg') or die "Error saving:$@\n";
my $rand=int(rand(100));
my @dummy=generatePointsString(@vpoints);
my %result = ('image' => "test.jpg?$rand", 'string' => "@dummy");
print encode_json \%result;
#print ( @real_points );